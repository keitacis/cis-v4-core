#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from cis_core import (
    DATA_DIR,
    ROOT,
    backup_file,
    clean_jp_symbol,
    normalize_symbol,
    parse_active_value,
    validate_symbol_for_market,
    validate_history_json,
    now_jst,
    read_json_strict,
    timestamp_jst,
    write_json,
    write_report,
)

STEM = "watchlist_update"
WATCH = DATA_DIR / "watchlist_master.csv"
COMP = DATA_DIR / "company_master.csv"
HIST = DATA_DIR / "watchlist_history.json"
REQUIRED_ROOT_DATA = [
    DATA_DIR / "watchlist_master.csv",
    DATA_DIR / "company_master.csv",
    DATA_DIR / "buyzone_master.json",
    DATA_DIR / "tv_snapshot.json",
    DATA_DIR / "cis_settings.json",
    DATA_DIR / "watchlist_history.json",
    DATA_DIR / "master_update_history.json",
]

FIELDS_WATCH = ["symbol", "market", "name", "asset_type", "active", "category", "added_date", "notes"]
FIELDS_COMP = ["symbol", "market", "name", "description", "theme"]
VALID_MARKETS = {"US", "JP"}


def normalize_market_symbol(market: str, symbol: str) -> Tuple[str, str]:
    m = str(market or "").strip().upper()
    try:
        s = validate_symbol_for_market(m, symbol)
    except Exception as e:
        raise ValueError(f"market/symbol形式エラー: {market} {symbol} / {e}") from e
    return m, s


def key_from_values(market: str, symbol: str) -> str:
    m, s = normalize_market_symbol(market, symbol)
    return f"{m}:{s}"


def key(row: Dict[str, str]) -> str:
    return key_from_values(row.get("market", ""), row.get("symbol", ""))


def ensure_root_data_initialized() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED_ROOT_DATA if not p.exists()]
    if missing:
        raise ValueError(
            "CIS v4 root data が未初期化です。先に `CIS v4 Apply Seed` を mode=missing_only で実行し、"
            "その後 `CIS v4 Preflight` を再実行してください。不足: " + ", ".join(missing)
        )


def _require_csv_columns(path: Path, fieldnames: List[str] | None, fields: Iterable[str]) -> None:
    if fieldnames is None:
        raise ValueError(f"CSVヘッダーがありません: {path.relative_to(ROOT)}")
    missing = [f for f in fields if f not in fieldnames]
    if missing:
        raise ValueError(f"CSV必須列不足: {path.relative_to(ROOT)} / {', '.join(missing)}")


def read_csv_strict(path: Path, fields: List[str]) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    seen: Dict[str, int] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        _require_csv_columns(path, reader.fieldnames, fields)
        for row_no, row in enumerate(reader, start=2):
            clean = {k: str(v or "") for k, v in row.items()}
            k = key(clean)
            if k in seen:
                raise ValueError(
                    f"{path.name} に重複銘柄があります: {k} / 既存行{seen[k]} / 重複行{row_no}"
                )
            seen[k] = row_no
            market, symbol = normalize_market_symbol(clean.get("market", ""), clean.get("symbol", ""))
            clean["market"] = market
            clean["symbol"] = symbol
            if "active" in fields:
                try:
                    parse_active_value(clean.get("active"))
                except Exception as e:
                    raise ValueError(f"{path.name} のactive値が不正です: {market}:{symbol} 行{row_no} / {e}") from e
            rows.append(clean)
    return rows


def write_csv(path: Path, fields: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})



def usage_text() -> str:
    return (
        "使える命令: "
        "ADD US CRDO / ADD US CRDO|会社名|説明|テーマ / "
        "UPDATE US CRDO|会社名|説明|テーマ / STOP US CRDO|理由 / RESUME US CRDO|理由"
    )


def validate_watch_company_rows(watch_rows: List[Dict[str, str]], comp_rows: List[Dict[str, str]]) -> None:
    watch_keys = {key(r) for r in watch_rows}
    comp_keys = {key(r) for r in comp_rows}
    missing = sorted(watch_keys - comp_keys)
    if missing:
        raise ValueError("watchlist_master.csv の銘柄が company_master.csv にありません: " + ", ".join(missing[:20]))


def build_order_preserving_rows(
    original_rows: List[Dict[str, str]],
    rows_by_key: Dict[str, Dict[str, str]],
    added_keys: List[str],
) -> List[Dict[str, str]]:
    """Keep existing CSV order and insert new rows at the end of the same market block.

    Watchlist order is a user-facing priority/category order, not merely a sortable key.
    UPDATE/STOP/RESUME must not reorder the whole file. ADD rows are inserted after
    the last existing row for that market so US additions stay in the US block and JP
    additions stay in the JP block.
    """
    original_keys = [key(r) for r in original_rows]
    original_key_set = set(original_keys)

    pending_by_market: Dict[str, List[str]] = {}
    for k in added_keys:
        if k in original_key_set or k not in rows_by_key:
            continue
        market = rows_by_key[k].get("market", "")
        pending_by_market.setdefault(market, [])
        if k not in pending_by_market[market]:
            pending_by_market[market].append(k)

    last_original_key_by_market: Dict[str, str] = {}
    for r in original_rows:
        k = key(r)
        if k in rows_by_key:
            last_original_key_by_market[rows_by_key[k].get("market", r.get("market", ""))] = k

    ordered: List[Dict[str, str]] = []
    emitted: set[str] = set()
    inserted_markets: set[str] = set()

    for r in original_rows:
        k = key(r)
        if k not in rows_by_key:
            continue
        ordered.append(rows_by_key[k])
        emitted.add(k)
        market = rows_by_key[k].get("market", r.get("market", ""))
        if last_original_key_by_market.get(market) == k and market not in inserted_markets:
            for nk in pending_by_market.get(market, []):
                if nk in rows_by_key and nk not in emitted:
                    ordered.append(rows_by_key[nk])
                    emitted.add(nk)
            inserted_markets.add(market)

    # If a market has no existing block, append its new rows in command order.
    for k in added_keys:
        if k in rows_by_key and k not in emitted:
            ordered.append(rows_by_key[k])
            emitted.add(k)

    # Safety fallback: no row should disappear silently.
    for k, row in rows_by_key.items():
        if k not in emitted:
            ordered.append(row)
            emitted.add(k)

    return ordered


def write_csv_temp(target: Path, fields: List[str], rows: List[Dict[str, str]]) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k, "") for k in fields})
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        finally:
            raise
    return tmp


def write_json_temp(target: Path, payload: Dict[str, Any]) -> Path:
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


def replace_watchlist_files_transactionally(watch_rows: List[Dict[str, str]], comp_rows: List[Dict[str, str]], hist_payload: Dict[str, Any]) -> None:
    """Replace watchlist/company/history together and restore on failure."""
    tmp_paths: Dict[Path, Path] = {}
    backups: Dict[Path, Optional[Path]] = {}
    replaced: List[Path] = []
    try:
        tmp_paths[WATCH] = write_csv_temp(WATCH, FIELDS_WATCH, watch_rows)
        tmp_paths[COMP] = write_csv_temp(COMP, FIELDS_COMP, comp_rows)
        tmp_paths[HIST] = write_json_temp(HIST, hist_payload)

        staged_watch = read_csv_strict(tmp_paths[WATCH], FIELDS_WATCH)
        staged_comp = read_csv_strict(tmp_paths[COMP], FIELDS_COMP)
        validate_watch_company_rows(staged_watch, staged_comp)
        validate_history_json(tmp_paths[HIST], "watchlist_history.json")

        for path in [WATCH, COMP, HIST]:
            backups[path] = backup_file(path, "watchlist_update")
        for path in [WATCH, COMP, HIST]:
            os.replace(tmp_paths[path], path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            backup = backups.get(path)
            try:
                if backup and backup.exists():
                    shutil.copy2(backup, path)
                elif path.exists():
                    path.unlink()
            except Exception:
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

def parse_line(line: str):
    raw = line.strip()
    if not raw or raw.startswith("#"):
        return None
    # ADD US CRDO
    # ADD US CRDO｜Credo Technology｜高速接続チップ｜theme(optional)
    # UPDATE US CRDO｜Credo Technology｜高速接続チップ｜theme(optional)
    parts = [p.strip() for p in re.split(r"[｜|]", raw)]
    if any(p == "" for p in parts[1:]):
        raise ValueError(f"空の入力列があります。余計な区切り記号を削除してください: {raw}")
    head = parts[0].split()
    action = head[0].upper() if head else ""
    if action == "DELETE":
        action = "REMOVE"
    if action not in {"ADD", "UPDATE", "REMOVE", "STOP", "RESUME"}:
        raise ValueError(f"不明な命令: {raw} / {usage_text()}")
    if len(head) != 3:
        raise ValueError(f"命令の先頭は ACTION MARKET SYMBOL の3語だけにしてください: {raw} / {usage_text()}")
    market, symbol = normalize_market_symbol(head[1], head[2])
    if action in {"ADD", "UPDATE"}:
        if len(parts) not in {1, 2, 3, 4}:
            raise ValueError(f"{action}は {action} MARKET SYMBOL または {action} MARKET SYMBOL｜name｜description｜theme 形式です。余計な列があります: {raw}")
        name = parts[1] if len(parts) >= 2 else ""
        desc = parts[2] if len(parts) >= 3 else ""
        theme = parts[3] if len(parts) == 4 else ""
    else:
        if len(parts) not in {1, 2}:
            raise ValueError(f"{action}は {action} MARKET SYMBOL または {action} MARKET SYMBOL｜reason 形式です。余計な列があります: {raw}")
        name = symbol
        desc = parts[1] if len(parts) == 2 else ""
        theme = ""
    return {"action": action, "market": market, "symbol": symbol, "name": name, "description": desc, "theme": theme, "raw": raw}

def normalize_commands(raw_commands: str) -> List[str]:
    normalized = raw_commands.replace("\r\n", "\n").replace("\r", "\n")
    if "\n" not in normalized and ";" in normalized:
        normalized = normalized.replace(";", "\n")
    return [line.strip() for line in normalized.splitlines() if line.strip() and not line.strip().startswith("#")]


def render_error(error: str) -> None:
    status = {"status": "error", "generated_at_jst": timestamp_jst(), "error": error}
    write_report(STEM, f"# CIS 監視リスト更新\n\n## エラー\n\nこの更新は反映していません。\n\n{error}\n", {"status": status}, status)


def main() -> int:
    try:
        commands = os.getenv("COMMANDS", "")
        if not commands.strip() and len(sys.argv) > 1:
            commands = Path(sys.argv[1]).read_text(encoding="utf-8")
        if not commands.strip():
            raise ValueError("COMMANDS が空です。監視リストの追加例は CIS v4 Watchlist Template を実行して確認してください。" + " " + usage_text())

        parsed_commands = []
        seen_keys: Dict[str, str] = {}
        for line in normalize_commands(commands):
            cmd = parse_line(line)
            if not cmd:
                continue
            k = f"{cmd['market']}:{cmd['symbol']}"
            if k in seen_keys:
                raise ValueError(
                    f"同じ入力内で同一銘柄が複数回指定されています: {k} / "
                    f"1回目={seen_keys[k]} / 2回目={cmd['raw']}"
                )
            seen_keys[k] = cmd["raw"]
            parsed_commands.append(cmd)
        if not parsed_commands:
            raise ValueError("有効な更新命令がありません。")

        # Do not allow Watchlist Update before root data initialization.
        # Otherwise a user can accidentally create an incomplete one-symbol master by running ADD first.
        ensure_root_data_initialized()

        # Strictly validate current masters before making backups or writing anything.
        watch = read_csv_strict(WATCH, FIELDS_WATCH)
        comp = read_csv_strict(COMP, FIELDS_COMP)
        validate_history_json(HIST, "watchlist_history.json")
        hist = read_json_strict(HIST, default={"items": []}) or {"items": []}
        hist_items = hist.get("items") if isinstance(hist, dict) else []

        watch_by = {key(r): r for r in watch}
        comp_by = {key(r): r for r in comp}
        original_watch_keys = [key(r) for r in watch]
        original_comp_keys = [key(r) for r in comp]
        added_watch_keys: List[str] = []
        added_comp_keys: List[str] = []
        results = []

        # All changes are calculated in memory first. Files are replaced together after staged validation.

        for cmd in parsed_commands:
            k = f"{cmd['market']}:{cmd['symbol']}"
            if cmd["action"] == "ADD":
                row = watch_by.get(k, {"symbol": cmd["symbol"], "market": cmd["market"]})
                existing_comp = comp_by.get(k, {})
                name = cmd["name"] or row.get("name") or existing_comp.get("name") or cmd["symbol"]
                desc = cmd["description"] if cmd["description"] else (row.get("notes") or existing_comp.get("description") or "")
                theme = cmd["theme"] if cmd["theme"] else (row.get("category") or existing_comp.get("theme") or "")
                is_new_watch = k not in watch_by
                is_new_comp = k not in comp_by
                row.update({
                    "symbol": cmd["symbol"],
                    "market": cmd["market"],
                    "name": name,
                    "asset_type": row.get("asset_type") or "stock",
                    "active": "true",
                    "category": theme,
                    "added_date": row.get("added_date") or now_jst().strftime("%Y-%m-%d"),
                    "notes": desc,
                })
                watch_by[k] = row
                comp_by[k] = {"symbol": cmd["symbol"], "market": cmd["market"], "name": name, "description": desc, "theme": theme}
                if is_new_watch and k not in original_watch_keys and k not in added_watch_keys:
                    added_watch_keys.append(k)
                if is_new_comp and k not in original_comp_keys and k not in added_comp_keys:
                    added_comp_keys.append(k)
            elif cmd["action"] == "UPDATE":
                if k not in watch_by:
                    raise ValueError(f"UPDATE は既存銘柄のみ指定できます。新規追加はADDを使ってください: {cmd['raw']}")
                row = watch_by[k]
                existing_comp = comp_by.get(k, {})
                name = cmd["name"] or row.get("name") or existing_comp.get("name") or cmd["symbol"]
                desc = cmd["description"] if cmd["description"] else (row.get("notes") or existing_comp.get("description") or "")
                theme = cmd["theme"] if cmd["theme"] else (row.get("category") or existing_comp.get("theme") or "")
                row.update({"name": name, "category": theme, "notes": desc})
                watch_by[k] = row
                comp_by[k] = {"symbol": cmd["symbol"], "market": cmd["market"], "name": name, "description": desc, "theme": theme}
            elif cmd["action"] in {"REMOVE", "STOP"}:
                if k not in watch_by:
                    raise ValueError(
                        f"{cmd['action']} は既存銘柄のみ指定できます。新規停止行は作りません: {cmd['raw']}"
                    )
                current_active = parse_active_value(watch_by[k].get("active"))
                if not current_active:
                    raise ValueError(f"{cmd['action']} 対象はすでにinactiveです: {cmd['raw']}")
                watch_by[k]["active"] = "false"
                if cmd.get("description"):
                    watch_by[k]["notes"] = cmd["description"]
            elif cmd["action"] == "RESUME":
                if k not in watch_by:
                    raise ValueError(
                        f"RESUME は既存のinactive銘柄のみ指定できます。新規追加はADDを使ってください: {cmd['raw']}"
                    )
                current_active = parse_active_value(watch_by[k].get("active"))
                if current_active:
                    raise ValueError(f"RESUME 対象はすでにactiveです: {cmd['raw']}")
                watch_by[k]["active"] = "true"
                if cmd.get("description"):
                    watch_by[k]["notes"] = cmd["description"]
            hist_items.append({"timestamp_jst": timestamp_jst(), **cmd})
            results.append(cmd)

        new_watch_rows = build_order_preserving_rows(watch, watch_by, added_watch_keys)
        new_comp_rows = build_order_preserving_rows(comp, comp_by, added_comp_keys)
        new_history_payload = {"items": hist_items[-1000:]}
        replace_watchlist_files_transactionally(new_watch_rows, new_comp_rows, new_history_payload)
        status = {"status": "ok", "generated_at_jst": timestamp_jst(), "changed_count": len(results)}
        md = ["# CIS 監視リスト更新", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", "", "## 反映内容", ""]
        md += [f"- {r['raw']}" for r in results] or ["- 変更なし"]
        md += ["", "## 次に見るもの", "", "- 新規追加銘柄がある場合は、Homeの `初期マスター投入テンプレート` でBUYZONE/TV不足を確認します。", "- 入力例は `監視リスト追加・変更テンプレート` にあります。"]
        write_report(STEM, "\n".join(md), {"status": status, "results": results}, status)
        return 0
    except Exception as e:
        render_error(f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
