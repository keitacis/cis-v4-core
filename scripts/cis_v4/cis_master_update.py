#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 master update.

Manual workflow input examples:
  TV US AVAV｜Strong Buy｜14｜250.00｜月次更新
  TV US EWY｜not_applicable｜ETFのため対象外
  TV US KITT｜no_coverage｜TradingViewにアナリスト予想なし
  BUYZONE US AVAV｜120｜100｜85｜決算後の基準見直し
  BUYZONE JP 6758｜3500｜3200｜2900｜月次レビュー

Design:
- TradingView is updated manually/monthly, not fetched daily.
- Buy-zone rules are stable and only updated intentionally.
- Every change is backed up, diffed, reported, and appended to history.
"""
from __future__ import annotations

import os
import sys
import re
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cis_core import (
    DATA_DIR,
    BACKUP_DIR,
    backup_file,
    clean_jp_symbol,
    fmt_price,
    fmt_pct,
    load_watchlist,
    normalize_symbol,
    normalize_coverage_status,
    parse_tv_rating,
    validate_symbol_for_market,
    validate_history_json,
    now_jst,
    read_json,
    read_json_strict,
    safe_float,
    safe_int,
    timestamp_jst,
    tv_upside,
    validate_tv_noncovered_blank_fields,
    write_json,
    write_report,
)

STEM = "master_update"
TITLE = "CIS マスター更新"
TV_PATH = DATA_DIR / "tv_snapshot.json"
BZ_PATH = DATA_DIR / "buyzone_master.json"
HISTORY_PATH = DATA_DIR / "master_update_history.json"

VALID_TV_RATINGS = {
    "STRONG BUY": "Strong Buy",
    "BUY": "Buy",
    "NEUTRAL": "Neutral",
    "HOLD": "Neutral",
    "SELL": "Sell",
    "STRONG SELL": "Strong Sell",
    "強い買い": "Strong Buy",
    "買い": "Buy",
    "中立": "Neutral",
    "売り": "Sell",
    "強い売り": "Strong Sell",
}


def normalize_commands(raw: str) -> List[str]:
    text = raw.replace("\r\n", "\n").replace("\r", "\n").strip()
    if "\n" not in text and ";" in text:
        text = text.replace(";", "\n")
    return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]


def normalize_market_symbol(market: str, symbol: str) -> Tuple[str, str]:
    m = str(market or "").strip().upper()
    try:
        s = validate_symbol_for_market(m, symbol)
    except Exception as e:
        raise ValueError(f"market/symbol形式エラー: {market} {symbol} / {e}") from e
    return m, s


def key(market: str, symbol: str) -> str:
    return f"{market}:{symbol}"


def parse_rating(value: Any) -> str:
    # Keep this wrapper for older local call sites, but use the shared CIS core
    # validator so Master Update and daily/weekly reports reject the same values.
    return parse_tv_rating(value)



def parse_coverage_status(value: Any) -> str:
    return normalize_coverage_status(value)


def is_coverage_token(value: Any) -> bool:
    try:
        parse_coverage_status(value)
        return True
    except Exception:
        return False

def require_positive_number(value: Any, label: str) -> float:
    n = safe_float(value)
    if n is None or n <= 0:
        raise ValueError(f"{label} は正の数値が必要です: {value}")
    return n


def require_positive_int(value: Any, label: str) -> int:
    n = safe_int(value)
    if n is None or n <= 0:
        raise ValueError(f"{label} は正の整数が必要です: {value}")
    return n


def parse_line(line: str) -> Dict[str, Any]:
    parts = [p.strip() for p in re.split(r"[｜|]", line)]
    if any(p == "" for p in parts[1:]):
        raise ValueError(f"空の入力列があります。余計な区切り記号を削除してください: {line}")
    head = parts[0].split()
    kind = head[0].upper() if head else ""
    if kind not in {"TV", "BUYZONE"}:
        raise ValueError(f"不明な命令です: {line}")
    if len(head) != 3:
        raise ValueError(f"命令の先頭は KIND MARKET SYMBOL の3語だけにしてください: {line}")
    market, symbol = normalize_market_symbol(head[1], head[2])
    return {"kind": kind, "market": market, "symbol": symbol, "parts": parts, "raw": line}


def load_items(path: Path) -> List[Dict[str, Any]]:
    data = read_json_strict(path, default={"items": []}) or {"items": []}
    rows = data.get("items") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError(f"{path.name} のitemsがlistではありません。")
    return rows


def index_tv(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Validate and index existing TradingView master rows strictly."""
    out: Dict[str, Dict[str, Any]] = {}
    for idx, r in enumerate(rows, start=1):
        if not isinstance(r, dict):
            raise ValueError(f"tv_snapshot.json のitems[{idx}]がobjectではありません。")
        market, symbol = normalize_market_symbol(str(r.get("market") or "US"), str(r.get("symbol") or ""))
        if market != "US":
            raise ValueError(f"tv_snapshot.json にUS以外の行があります: items[{idx}] {market}:{symbol}")
        coverage_status = parse_coverage_status(r.get("coverage_status") or "covered")
        base = dict(r, market="US", symbol=symbol, coverage_status=coverage_status)
        if coverage_status == "covered":
            rating = parse_rating(r.get("rating"))
            analyst_count = require_positive_int(r.get("analyst_count"), f"tv_snapshot.json items[{idx}] アナリスト人数")
            avg_target_price = require_positive_number(r.get("avg_target_price"), f"tv_snapshot.json items[{idx}] 平均目標株価")
            base.update(rating=rating, analyst_count=analyst_count, avg_target_price=avg_target_price)
        else:
            validate_tv_noncovered_blank_fields(r, f"US:{symbol} items[{idx}]")
            base.update(rating=None, analyst_count=None, avg_target_price=None)
        k = key(market, symbol)
        if k in out:
            raise ValueError(f"tv_snapshot.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = base
    return out

def index_bz(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Validate and index existing buy-zone master rows strictly.

    Do not silently skip malformed buy-zone rows.  Buy-zone is a core CIS
    signal, so a broken existing row is an error and nothing is written.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for idx, r in enumerate(rows, start=1):
        if not isinstance(r, dict):
            raise ValueError(f"buyzone_master.json のitems[{idx}]がobjectではありません。")
        market, symbol = normalize_market_symbol(str(r.get("market") or ""), str(r.get("symbol") or ""))
        watch_price = require_positive_number(r.get("watch_price"), f"buyzone_master.json items[{idx}] 打診買い価格")
        main_buy_price = require_positive_number(r.get("main_buy_price"), f"buyzone_master.json items[{idx}] 本命買い価格")
        strong_buy_price = require_positive_number(r.get("strong_buy_price"), f"buyzone_master.json items[{idx}] 強く買いたい価格")
        if not (strong_buy_price <= main_buy_price <= watch_price):
            raise ValueError(f"buyzone_master.json の価格順序が不正です: {market}:{symbol} items[{idx}]")
        updated_at = str(r.get("updated_at") or "").strip()
        if not updated_at:
            raise ValueError(f"buyzone_master.json のupdated_atが未設定です: {market}:{symbol} items[{idx}]")
        reason = str(r.get("reason") or "").strip()
        if not reason:
            raise ValueError(f"buyzone_master.json のreasonが未設定です: {market}:{symbol} items[{idx}]")
        k = key(market, symbol)
        if k in out:
            raise ValueError(f"buyzone_master.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = dict(r, market=market, symbol=symbol, watch_price=watch_price, main_buy_price=main_buy_price, strong_buy_price=strong_buy_price)
    return out


def make_tv_update(cmd: Dict[str, Any]) -> Dict[str, Any]:
    if cmd["market"] != "US":
        raise ValueError(f"TV更新はUSのみ対応です: {cmd['raw']}")
    parts = cmd["parts"]
    if len(parts) < 2:
        raise ValueError(f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason または TV US SYMBOL｜no_coverage/not_applicable｜reason 形式です: {cmd['raw']}")

    first = parts[1]
    explicit_status = is_coverage_token(first)
    coverage_status = parse_coverage_status(first) if explicit_status else "covered"

    if coverage_status == "covered":
        if explicit_status:
            if len(parts) not in {5, 6}:
                raise ValueError(
                    f"covered更新は TV US SYMBOL｜covered｜rating｜analyst_count｜avg_target_price｜reason 形式です。"
                    f"余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[2])
            analyst_count = require_positive_int(parts[3], "アナリスト人数")
            avg_target_price = require_positive_number(parts[4], "平均目標株価")
            reason = parts[5] if len(parts) == 6 else "月次更新"
        else:
            if len(parts) not in {4, 5}:
                raise ValueError(
                    f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason 形式です。"
                    f"余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[1])
            analyst_count = require_positive_int(parts[2], "アナリスト人数")
            avg_target_price = require_positive_number(parts[3], "平均目標株価")
            reason = parts[4] if len(parts) == 5 else "月次更新"
        return {
            "symbol": cmd["symbol"],
            "market": "US",
            "coverage_status": "covered",
            "rating": rating,
            "analyst_count": analyst_count,
            "avg_target_price": avg_target_price,
            "updated_at": timestamp_jst(),
            "source": "TradingView",
            "reason": reason,
        }

    if len(parts) not in {2, 3}:
        raise ValueError(
            f"{coverage_status}更新は TV US SYMBOL｜{coverage_status}｜reason 形式です。"
            f"rating/人数/目標株価など余計な列は入れないでください: {cmd['raw']}"
        )
    reason = parts[2] if len(parts) == 3 else ("TradingViewにアナリスト予想なし" if coverage_status == "no_coverage" else "TradingView対象外")
    return {
        "symbol": cmd["symbol"],
        "market": "US",
        "coverage_status": coverage_status,
        "rating": None,
        "analyst_count": None,
        "avg_target_price": None,
        "updated_at": timestamp_jst(),
        "source": "TradingView",
        "reason": reason,
    }

def make_buyzone_update(cmd: Dict[str, Any]) -> Dict[str, Any]:
    parts = cmd["parts"]
    if len(parts) not in {4, 5}:
        raise ValueError(f"BUYZONE更新は BUYZONE MARKET SYMBOL｜watch｜main｜strong｜reason 形式です。余計な列または不足列があります: {cmd['raw']}")
    watch_price = require_positive_number(parts[1], "打診買い価格")
    main_buy_price = require_positive_number(parts[2], "本命買い価格")
    strong_buy_price = require_positive_number(parts[3], "強く買いたい価格")
    if not (strong_buy_price <= main_buy_price <= watch_price):
        raise ValueError(
            f"買い場価格の大小関係が不正です。必要条件: 強く買いたい <= 本命 <= 打診 / {cmd['raw']}"
        )
    reason = parts[4] if len(parts) == 5 else "月次レビュー"
    return {
        "symbol": cmd["symbol"],
        "market": cmd["market"],
        "watch_price": watch_price,
        "main_buy_price": main_buy_price,
        "strong_buy_price": strong_buy_price,
        "updated_at": timestamp_jst(),
        "reason": reason,
    }


def diff(old: Optional[Dict[str, Any]], new: Dict[str, Any], fields: List[str]) -> List[str]:
    lines = []
    for f in fields:
        old_v = old.get(f) if old else None
        new_v = new.get(f)
        if old_v != new_v:
            lines.append(f"{f}: {old_v if old_v not in [None, ''] else '未設定'} → {new_v}")
    return lines


def load_history_items(path: Path = HISTORY_PATH, label: str = "master_update_history.json") -> List[Dict[str, Any]]:
    """Load history rows strictly and return a copy-safe list of objects."""
    validate_history_json(path, label)
    data = read_json_strict(path, default={"items": []}) or {"items": []}
    rows = data.get("items") if isinstance(data, dict) else data
    if rows in [None, ""]:
        return []
    if not isinstance(rows, list):
        raise ValueError(f"{label} のitemsがlistではありません。")
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{label} のitems[{idx}]がobjectではありません。")
        out.append(dict(row))
    return out


def validate_history_payload(payload: Dict[str, Any], label: str = "master_update_history.json") -> None:
    rows = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError(f"{label} のitemsがlistではありません。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{label} のitems[{idx}]がobjectではありません。")


def write_json_temp(target: Path, payload: Dict[str, Any]) -> Path:
    """Write JSON beside target and return the temporary path for atomic replace."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        finally:
            raise
    return tmp


def validate_staged_master_files(tmp_tv: Path, tmp_bz: Path, tmp_history: Path) -> None:
    """Re-read temporary files and validate them before touching root masters."""
    index_tv(load_items(tmp_tv))
    index_bz(load_items(tmp_bz))
    load_history_items(tmp_history, "master_update_history.json")


def replace_master_files_transactionally(payloads: List[Tuple[Path, Dict[str, Any]]]) -> None:
    """Replace TV, BUYZONE and history together, restoring backups on failure.

    Master Update must never end with only part of the three master files
    reflected.  All new payloads are written to temporary files first, then
    re-read and validated.  If any os.replace fails after one file has already
    been replaced, the previous files are restored from backups.
    """
    tmp_paths: Dict[Path, Path] = {}
    backups: Dict[Path, Optional[Path]] = {}
    replaced: List[Path] = []
    try:
        for path, payload in payloads:
            tmp_paths[path] = write_json_temp(path, payload)

        validate_staged_master_files(tmp_paths[TV_PATH], tmp_paths[BZ_PATH], tmp_paths[HISTORY_PATH])

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        for path, _payload in payloads:
            backups[path] = backup_file(path, "master_update")

        for path, _payload in payloads:
            os.replace(tmp_paths[path], path)
            replaced.append(path)

    except Exception:
        # Best-effort rollback for any file already replaced in this transaction.
        for path in reversed(replaced):
            backup = backups.get(path)
            try:
                if backup and backup.exists():
                    shutil.copy2(backup, path)
                elif path.exists():
                    path.unlink()
            except Exception:
                # Preserve the original exception; report will show the first failure.
                pass
        for tmp in tmp_paths.values():
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
        raise
    else:
        for tmp in tmp_paths.values():
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass


def render_report(changes: List[Dict[str, Any]], errors: List[str], status: Dict[str, Any]) -> str:
    lines = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
    if errors:
        lines += ["## エラー", "", "この更新は反映していません。1件でもエラーがある場合、TV・BUYZONE・履歴は書き換えません。", ""]
        lines += [f"- {e}" for e in errors]
        lines.append("")
    lines += ["## 反映内容", ""]
    if not changes:
        lines.append("変更なし")
        lines.append("")
        return "\n".join(lines)
    for c in changes:
        lines += [f"### {c['kind']} {c['market']} {c['symbol']}", "", f"- 入力：{c['raw']}"]
        if c.get("diffs"):
            lines.append("- 変更点：")
            for d in c["diffs"]:
                lines.append(f"  - {d}")
        else:
            lines.append("- 変更点：なし")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    errors: List[str] = []
    changes: List[Dict[str, Any]] = []
    try:
        commands = os.getenv("COMMANDS", "")
        if not commands.strip() and len(sys.argv) > 1:
            commands = Path(sys.argv[1]).read_text(encoding="utf-8")
        lines = normalize_commands(commands)
        if not lines:
            raise ValueError("COMMANDS が空です。")

        watch_items = load_watchlist(True)
        active_keys = {x.key for x in watch_items}
        active_us_keys = {x.key for x in watch_items if x.market == "US"}

        # Phase 1: validate every command before reading/writing mutable masters.
        # One bad command means nothing is reflected.
        staged_updates: List[Tuple[Dict[str, Any], Dict[str, Any], List[str]]] = []
        validation_errors: List[str] = []
        seen_update_keys = set()
        for line in lines:
            try:
                cmd = parse_line(line)
                k = key(cmd["market"], cmd["symbol"])
                update_key = f"{cmd['kind']}:{k}"
                if update_key in seen_update_keys:
                    raise ValueError(f"同じ入力内で同一銘柄の同一種別更新が重複しています: {update_key}")
                seen_update_keys.add(update_key)
                if cmd["kind"] == "TV" and k not in active_us_keys:
                    raise ValueError(f"TV更新対象がactiveな米国株監視リストにありません: {k} / 先にWatchlist Updateで追加してください。")
                if cmd["kind"] == "BUYZONE" and k not in active_keys:
                    raise ValueError(f"BUYZONE更新対象がactiveな監視リストにありません: {k} / 先にWatchlist Updateで追加してください。")
                if cmd["kind"] == "TV":
                    new = make_tv_update(cmd)
                    fields = ["coverage_status", "rating", "analyst_count", "avg_target_price", "source", "reason"]
                else:
                    new = make_buyzone_update(cmd)
                    fields = ["watch_price", "main_buy_price", "strong_buy_price", "reason"]
                staged_updates.append((cmd, new, fields))
            except Exception as e:
                validation_errors.append(f"{line} → {type(e).__name__}: {e}")
        if validation_errors:
            raise ValueError("更新前検証でエラー: " + " / ".join(validation_errors))
        if not staged_updates:
            raise ValueError("有効な更新命令がありません。")

        # Phase 2: strict master load. Malformed JSON must stop the run and must not be treated as empty.
        tv_by = index_tv(load_items(TV_PATH))
        bz_by = index_bz(load_items(BZ_PATH))
        # History is also strictly loaded before any master file is written.
        hist_items = load_history_items(HISTORY_PATH, "master_update_history.json")

        # Phase 3: calculate diffs using copies, then write only after all checks pass.
        for cmd, new, fields in staged_updates:
            k = key(cmd["market"], cmd["symbol"])
            if cmd["kind"] == "TV":
                old = tv_by.get(k)
                tv_by[k] = new
            else:
                old = bz_by.get(k)
                bz_by[k] = new
            changes.append({
                "kind": cmd["kind"],
                "market": cmd["market"],
                "symbol": cmd["symbol"],
                "raw": cmd["raw"],
                "diffs": diff(old, new, fields),
                "updated_at": timestamp_jst(),
            })

        new_tv_payload = {"items": sorted(tv_by.values(), key=lambda r: r.get("symbol", ""))}
        new_bz_payload = {"items": sorted(bz_by.values(), key=lambda r: (r.get("market", ""), r.get("symbol", "")))}
        new_history_payload = {"items": (hist_items + changes)[-1000:]}
        validate_history_payload(new_history_payload, "master_update_history.json")

        replace_master_files_transactionally([
            (TV_PATH, new_tv_payload),
            (BZ_PATH, new_bz_payload),
            (HISTORY_PATH, new_history_payload),
        ])

        status = {
            "status": "ok",
            "generated_at_jst": timestamp_jst(),
            "changed_count": len(changes),
            "error_count": 0,
        }
        md = render_report(changes, errors, status)
        write_report(STEM, md, {"status": status, "changes": changes}, status)
        return 0

    except Exception as e:
        errors.append(f"{type(e).__name__}: {e}")
        status = {
            "status": "error",
            "generated_at_jst": timestamp_jst(),
            "changed_count": 0,
            "error_count": len(errors),
            "error": errors[-1],
        }
        md = render_report([], errors, status)
        write_report(STEM, md, {"status": status, "changes": [], "errors": errors}, status)
        return 1


if __name__ == "__main__":
    sys.exit(main())
