#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate safe initialization templates for CIS v4 masters.

This script does not update master data. It creates iPhone-readable templates
for the two critical initial data sets:
- data/buyzone_master.json
- data/tv_snapshot.json

It can also detect legacy buy-zone CSV files and convert valid rows into
ready-to-paste CIS v4 Master Update commands.
"""
from __future__ import annotations

import csv
import glob
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cis_core import (
    DATA_DIR,
    OUTPUT_DIR,
    DOCS_LATEST_DIR,
    clean_jp_symbol,
    fmt_price,
    load_buyzone_master,
    load_tv_snapshot,
    load_watchlist,
    normalize_symbol,
    now_jst,
    safe_float,
    timestamp_jst,
    write_report,
    write_text,
    write_error_report,
)

STEM = "master_init_template"
TITLE = "CIS 初期マスター投入テンプレート"


def key(market: str, symbol: str) -> str:
    return f"{market}:{symbol}"


def normalize_market_symbol(market: Any, symbol: Any) -> Tuple[Optional[str], Optional[str]]:
    m = str(market or "").strip().upper()
    s = normalize_symbol(symbol)
    if not m:
        if re.fullmatch(r"\d{4}(\.T)?", s):
            m = "JP"
        else:
            m = "US"
    if m in {"TSE", "TYO"}:
        m = "JP"
    if m == "JP":
        s = clean_jp_symbol(s)
    if m not in {"US", "JP"} or not s:
        return None, None
    return m, s


def validate_buyzone_rule(rule: Optional[Dict[str, Any]]) -> List[str]:
    if not rule:
        return ["未設定"]
    errors: List[str] = []
    watch = safe_float(rule.get("watch_price"))
    main = safe_float(rule.get("main_buy_price"))
    strong = safe_float(rule.get("strong_buy_price"))
    if watch is None or watch <= 0:
        errors.append("打診買い価格不正")
    if main is None or main <= 0:
        errors.append("本命買い価格不正")
    if strong is None or strong <= 0:
        errors.append("強く買いたい価格不正")
    if not errors and not (strong <= main <= watch):
        errors.append("価格順序不正")
    if not str(rule.get("updated_at") or "").strip():
        errors.append("updated_at未設定")
    if not str(rule.get("reason") or "").strip():
        errors.append("reason未設定")
    return errors


def valid_tv(tv: Any) -> bool:
    if not tv:
        return False
    if getattr(tv, "coverage_status", "covered") in {"no_coverage", "not_applicable"}:
        return True
    return bool(tv.rating) and tv.analyst_count is not None and tv.avg_target_price is not None


def first_value(row: Dict[str, Any], names: List[str]) -> Any:
    lower = {str(k).strip().lower(): v for k, v in row.items()}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None


def find_legacy_buyzone_candidates(active_keys: set[str]) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    """Find legacy buy-zone CSV rows and convert to v4 field names.

    Supported columns include the old v1/v2 names:
      ticker/symbol, market, probe_price, core_price, strong_price,
      basis_reason, review_note, name.
    """
    candidates: Dict[str, Dict[str, Any]] = {}
    source_files: List[str] = []
    patterns = [
        str(DATA_DIR / "buy_zone_master*.csv"),
        str(DATA_DIR / "buyzone_master*.csv"),
        str(DATA_DIR / "*buy*zone*.csv"),
    ]
    for pattern in patterns:
        for path_str in glob.glob(pattern):
            path = Path(path_str)
            if path.name == "watchlist_master.csv":
                continue
            if path.name in source_files:
                continue
            try:
                with path.open("r", encoding="utf-8-sig", newline="") as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames:
                        continue
                    fields = {x.strip().lower() for x in reader.fieldnames}
                    if not ({"ticker", "symbol"} & fields) or not ({"probe_price", "watch_price"} & fields):
                        continue
                    source_files.append(path.name)
                    for row in reader:
                        symbol_raw = first_value(row, ["symbol", "ticker"])
                        market_raw = first_value(row, ["market"])
                        market, symbol = normalize_market_symbol(market_raw, symbol_raw)
                        if not market or not symbol:
                            continue
                        k = key(market, symbol)
                        if k not in active_keys:
                            continue
                        watch = safe_float(first_value(row, ["watch_price", "probe_price", "probe"]))
                        main = safe_float(first_value(row, ["main_buy_price", "core_price", "core"]))
                        strong = safe_float(first_value(row, ["strong_buy_price", "strong_price", "strong"]))
                        if watch is None or main is None or strong is None:
                            continue
                        if watch <= 0 or main <= 0 or strong <= 0:
                            continue
                        if not (strong <= main <= watch):
                            continue
                        reason = str(
                            first_value(row, ["basis_reason", "review_note", "reason", "notes"]) or "legacy buy-zone master"
                        ).strip()
                        candidates[k] = {
                            "market": market,
                            "symbol": symbol,
                            "watch_price": watch,
                            "main_buy_price": main,
                            "strong_buy_price": strong,
                            "reason": reason[:120] or "legacy buy-zone master",
                            "source_file": path.name,
                        }
            except Exception:
                continue
    return candidates, source_files


def buyzone_command(market: str, symbol: str, watch: Any, main: Any, strong: Any, reason: str) -> str:
    return f"BUYZONE {market} {symbol}|{watch}|{main}|{strong}|{reason}"


def tv_command(symbol: str) -> str:
    return f"TV US {symbol}|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US {symbol}|no_coverage|TradingViewにアナリスト予想なし  または  TV US {symbol}|not_applicable|ETF等のため対象外"


def chunked(values: List[str], size: int = 15) -> List[List[str]]:
    return [values[i:i + size] for i in range(0, len(values), size)]


def write_chunk_files(base_dir: Path, prefix: str, values: List[str], size: int = 15) -> List[str]:
    """Write short iPhone-friendly command chunks and remove stale chunks."""
    for old in base_dir.glob(f"{prefix}_part_*.txt"):
        try:
            old.unlink()
        except Exception:
            pass
    links: List[str] = []
    for idx, part in enumerate(chunked(values, size), start=1):
        name = f"{prefix}_part_{idx:02d}.txt"
        write_text(base_dir / name, "\n".join(part) + ("\n" if part else ""))
        links.append(name)
    return links


def write_semicolon_chunk_files(base_dir: Path, prefix: str, values: List[str], size: int = 15) -> List[str]:
    """Write iPhone-friendly one-line chunks for GitHub Actions string inputs."""
    for old in base_dir.glob(f"{prefix}_semicolon_part_*.txt"):
        try:
            old.unlink()
        except Exception:
            pass
    links: List[str] = []
    for idx, part in enumerate(chunked(values, size), start=1):
        name = f"{prefix}_semicolon_part_{idx:02d}.txt"
        write_text(base_dir / name, " ; ".join(part) + ("\n" if part else ""))
        links.append(name)
    return links


def main() -> int:
    try:
        items = load_watchlist(True)
        active_keys = {x.key for x in items}
        us_items = [x for x in items if x.market == "US"]
        bz = load_buyzone_master()
        tv = load_tv_snapshot()

        legacy_bz, legacy_files = find_legacy_buyzone_candidates(active_keys)

        missing_bz = []
        invalid_bz = []
        ready_bz_commands = []
        blank_bz_templates = []
        for item in items:
            errors = validate_buyzone_rule(bz.get(item.key))
            if errors:
                row = {"item": item, "errors": errors}
                if bz.get(item.key):
                    invalid_bz.append(row)
                else:
                    missing_bz.append(row)
                cand = legacy_bz.get(item.key)
                if cand:
                    ready_bz_commands.append(buyzone_command(
                        cand["market"], cand["symbol"], cand["watch_price"], cand["main_buy_price"], cand["strong_buy_price"],
                        f"legacy:{cand['source_file']} {cand['reason']}"
                    ))
                else:
                    blank_bz_templates.append(buyzone_command(item.market, item.symbol, "打診", "本命", "強く買いたい", "根拠"))

        missing_tv = []
        for item in us_items:
            if not valid_tv(tv.get(item.key)):
                missing_tv.append(item)

        tv_templates = [tv_command(item.symbol) for item in missing_tv]
        # Safety: only legacy-converted commands are exported as ready-to-paste commands.
        # Placeholder templates are intentionally separated so they cannot be pasted by mistake.
        all_ready_commands = ready_bz_commands

        status_level = "ok" if not missing_bz and not invalid_bz and not missing_tv else "partial"
        status = {
            "status": status_level,
            "generated_at_jst": timestamp_jst(),
            "active_count": len(items),
            "active_us_count": len(us_items),
            "buyzone_missing_count": len(missing_bz),
            "buyzone_invalid_count": len(invalid_bz),
            "buyzone_legacy_ready_count": len(ready_bz_commands),
            "tv_missing_count": len(missing_tv),
            "legacy_files": legacy_files,
        }

        lines: List[str] = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += [
            "## 目的",
            "",
            "このページは、買い場基準とTradingViewスナップショットの初期投入漏れを防ぐための確認用です。",
            "この処理はマスターを更新しません。更新するには、下のコマンドを `CIS v4 Master Update` に貼ります。",
            "",
            "## サマリー",
            "",
            f"- active銘柄：{len(items)}",
            f"- 米国株active銘柄：{len(us_items)}",
            f"- 買い場基準未設定：{len(missing_bz)}",
            f"- 買い場基準不正：{len(invalid_bz)}",
            f"- 旧buy-zone CSVから変換候補あり：{len(ready_bz_commands)}",
            f"- TradingView未設定/要区分入力：{len(missing_tv)}",
            "",
        ]
        lines += [
            "## iPhone用・分割コピー",
            "",
            "長すぎる貼り付け事故を避けるため、10〜15銘柄単位の分割txtを先に出します。iPhoneでは基本こちらを1つずつ開いて使います。",
            "",
        ]
        if ready_bz_commands:
            lines += ["### 旧CSV変換BUYZONE 分割", "", "改行版と1行セミコロン版を両方出します。GitHub Actions入力欄で改行が見づらい場合は1行版を使います。", ""]
            lines += [f"- 改行 part {i+1:02d}: [開く](master_init_ready_part_{i+1:02d}.txt) / 1行版: [開く](master_init_ready_semicolon_part_{i+1:02d}.txt)" for i, _ in enumerate(chunked(ready_bz_commands, 15))] + [""]
        if blank_bz_templates:
            lines += ["### 手入力BUYZONE 分割", "", "価格を入れてから使います。空欄のまま貼らないでください。", ""]
            lines += [f"- 改行 part {i+1:02d}: [開く](master_init_buyzone_blank_part_{i+1:02d}.txt) / 1行版: [開く](master_init_buyzone_blank_semicolon_part_{i+1:02d}.txt)" for i, _ in enumerate(chunked(blank_bz_templates, 15))] + [""]
        if tv_templates:
            lines += ["### TradingView 分割", "", "月1回の確認用です。毎日自動取得するのではなく、ここで更新したスナップショットを各レポートで再利用します。", ""]
            lines += [f"- 改行 part {i+1:02d}: [開く](master_init_tv_blank_part_{i+1:02d}.txt) / 1行版: [開く](master_init_tv_blank_semicolon_part_{i+1:02d}.txt)" for i, _ in enumerate(chunked(tv_templates, 15))] + [""]

        lines += [
            "## PC向け・全件コピー",
            "",
            "PCや長文貼り付けに慣れている場合はこちらを使えます。iPhoneでは分割txtの方が安全です。",
            "",
            "- [旧CSVから変換できたBUYZONEコマンド・全件](master_init_template_ready_commands.txt)",
            "- [手入力が必要なBUYZONEテンプレート・全件](master_init_template_buyzone_blank.txt)",
            "- [TradingView更新テンプレート・全件](master_init_template_tv_blank.txt)",
            "",
        ]

        if legacy_files:
            lines += ["## 検出した旧buy-zone CSV", ""] + [f"- {x}" for x in legacy_files] + [""]

        if invalid_bz:
            lines += ["## 買い場基準が不正な銘柄", ""]
            for r in invalid_bz:
                item = r["item"]
                lines.append(f"- {item.key}｜{item.description or item.name}：{' / '.join(r['errors'])}")
            lines.append("")

        if ready_bz_commands:
            lines += ["## そのまま使える可能性があるBUYZONE更新コマンド", "", "旧buy-zone CSVから変換できた候補です。価格水準を見てから使います。", "", "```text"]
            lines += ready_bz_commands
            lines += ["```", ""]

        if blank_bz_templates:
            lines += ["## 手入力が必要なBUYZONEテンプレート", "", "価格を空欄のまま使ってはいけません。打診・本命・強く買いたい価格を入れてから使います。", "", "```text"]
            lines += blank_bz_templates
            lines += ["```", ""]

        if tv_templates:
            lines += ["## TradingView更新テンプレート", "", "TradingViewにアナリスト予想がある銘柄はレーティング・人数・平均目標株価を入れます。ETFやカバレッジなし銘柄は、未取得ではなく `not_applicable` / `no_coverage` と明示します。", "", "```text"]
            lines += tv_templates
            lines += ["```", ""]

        if not ready_bz_commands and not blank_bz_templates and not tv_templates:
            lines += ["## 結果", "", "買い場基準とTradingViewスナップショットは全active対象で揃っています。", ""]

        ready_text = "\n".join(all_ready_commands) + ("\n" if all_ready_commands else "")
        buyzone_blank_text = "\n".join(blank_bz_templates) + ("\n" if blank_bz_templates else "")
        tv_blank_text = "\n".join(tv_templates) + ("\n" if tv_templates else "")
        combined_template_text = "\n".join(blank_bz_templates + tv_templates) + ("\n" if (blank_bz_templates or tv_templates) else "")
        for base_dir in [OUTPUT_DIR, DOCS_LATEST_DIR]:
            write_text(base_dir / "master_init_template_ready_commands.txt", ready_text)
            write_text(base_dir / "master_init_template_buyzone_blank.txt", buyzone_blank_text)
            write_text(base_dir / "master_init_template_tv_blank.txt", tv_blank_text)
            write_chunk_files(base_dir, "master_init_ready", all_ready_commands, 15)
            write_chunk_files(base_dir, "master_init_buyzone_blank", blank_bz_templates, 15)
            write_chunk_files(base_dir, "master_init_tv_blank", tv_templates, 15)
            write_semicolon_chunk_files(base_dir, "master_init_ready", all_ready_commands, 15)
            write_semicolon_chunk_files(base_dir, "master_init_buyzone_blank", blank_bz_templates, 15)
            write_semicolon_chunk_files(base_dir, "master_init_tv_blank", tv_templates, 15)
            # Backward-compatible combined file. Not used as the main iPhone path.
            write_text(base_dir / "master_init_template_blank_templates.txt", combined_template_text)
        write_report(STEM, "\n".join(lines), {"status": status, "ready_commands": all_ready_commands, "blank_buyzone_templates": blank_bz_templates, "tv_templates": tv_templates}, status)
        return 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
