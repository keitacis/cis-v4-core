#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 TradingView monthly refresh v3 partial.

Generates candidate commands only. It never writes data/tv_snapshot.json directly.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cis_core import (
    DOCS_LATEST_DIR,
    OUTPUT_DIR,
    fmt_price,
    load_tv_snapshot,
    load_watchlist,
    now_jst,
    safe_float,
    safe_int,
    timestamp_jst,
    write_error_report,
    write_json,
    write_report,
    write_text,
)

STEM = "tv_monthly_refresh"
TITLE = "CIS TradingView 月次確認"
EXCHANGES = ["NASDAQ", "NYSE", "AMEX", "NYSEARCA", "BATS", "OTC"]
COLUMNS = [
    "name", "description", "exchange", "close", "currency",
    "recommendation_mark", "number_of_analysts",
    "price_target_average", "price_target_high", "price_target_low",
    "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold",
    "analyst_rating_sell", "analyst_rating_strong_sell",
]
ETF_NOT_APPLICABLE = {"EWY"}


def post_json(url: str, payload: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 CIS-v4 TradingView monthly refresh",
            "Accept": "application/json,text/plain,*/*",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def get_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 CIS-v4 TradingView monthly refresh",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def rating_from_mark(value: Any) -> Optional[str]:
    n = safe_float(value)
    if n is None:
        return None
    # TradingView recommendation_mark is low = bullish, high = bearish.
    if n <= 1.5:
        return "Strong Buy"
    if n <= 2.5:
        return "Buy"
    if n <= 3.5:
        return "Neutral"
    if n <= 4.5:
        return "Sell"
    return "Strong Sell"


def distribution(row: Dict[str, Any]) -> Dict[str, Optional[int]]:
    out = {
        "strong_buy_count": safe_int(row.get("analyst_rating_strong_buy")),
        "buy_count": safe_int(row.get("analyst_rating_buy")),
        "hold_count": safe_int(row.get("analyst_rating_hold")),
        "sell_count": safe_int(row.get("analyst_rating_sell")),
        "strong_sell_count": safe_int(row.get("analyst_rating_strong_sell")),
    }
    if all(v is None for v in out.values()):
        return out
    return {k: (0 if v is None else int(v)) for k, v in out.items()}


def distribution_total(dist: Dict[str, Optional[int]]) -> Optional[int]:
    if not dist or all(v is None for v in dist.values()):
        return None
    total = sum(int(v or 0) for v in dist.values())
    return total if total > 0 else None


def forecast_count(exchange: str, symbol: str) -> Tuple[Optional[int], List[str], Optional[str]]:
    url = f"https://www.tradingview.com/symbols/{exchange}-{symbol}/forecast/"
    errors: List[str] = []
    try:
        text = get_text(url)
    except Exception as e:
        return None, [f"{type(e).__name__}: {str(e)[:220]}"], None
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else None
    matches: List[int] = []
    patterns = [
        r"Based on\s+([0-9]{1,3})\s+analysts?",
        r"([0-9]{1,3})\s+analysts?\s+offering",
        r"([0-9]{1,3})\s+analysts?\s+have",
        r"([0-9]{1,3})\s+analyst ratings",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.I):
            try:
                n = int(m.group(1))
                if 1 <= n <= 300:
                    matches.append(n)
            except Exception:
                pass
    if not matches:
        return None, errors, title
    # Prefer the smallest positive number; it is usually the target-price analyst count.
    return min(matches), errors, title


def scan_symbol(symbol: str) -> Dict[str, Any]:
    attempts: List[Dict[str, Any]] = []
    best: Optional[Dict[str, Any]] = None
    for ex in EXCHANGES:
        ticker = f"{ex}:{symbol}"
        payload = {"symbols": {"tickers": [ticker], "query": {"types": []}}, "columns": COLUMNS}
        attempt: Dict[str, Any] = {"exchange": ex, "ticker": ticker}
        try:
            res = post_json("https://scanner.tradingview.com/america/scan", payload)
            rows = res.get("data") or []
            attempt["http"] = 200
            attempt["row_count"] = len(rows)
            if rows:
                values = rows[0].get("d") or []
                row = {col: values[i] if i < len(values) else None for i, col in enumerate(COLUMNS)}
                row["exchange"] = row.get("exchange") or ex
                attempt["row"] = row
                rating = rating_from_mark(row.get("recommendation_mark"))
                avg = safe_float(row.get("price_target_average"))
                count = safe_int(row.get("number_of_analysts"))
                dist = distribution(row)
                dist_total = distribution_total(dist)
                score = 0
                if rating:
                    score += 5
                if avg is not None and avg > 0:
                    score += 5
                if count is not None and count > 0:
                    score += 3
                if dist_total is not None:
                    score += 2
                if safe_float(row.get("close")) is not None:
                    score += 1
                attempt["score"] = score
                if best is None or score > int(best.get("score") or 0):
                    best = dict(attempt)
            else:
                attempt["score"] = 0
        except Exception as e:
            attempt["error"] = f"{type(e).__name__}: {str(e)[:220]}"
        attempts.append(attempt)
    if best is None:
        return {"symbol": symbol, "status": "failed", "attempts": attempts, "error": "scanner no usable rows"}
    row = best.get("row") or {}
    ex = str(best.get("exchange") or row.get("exchange") or "").upper()
    rating = rating_from_mark(row.get("recommendation_mark"))
    avg = safe_float(row.get("price_target_average"))
    count = safe_int(row.get("number_of_analysts"))
    dist = distribution(row)
    dist_total = distribution_total(dist)
    count_source = "scanner_number_of_analysts" if count is not None and count > 0 else ""
    forecast_errors: List[str] = []
    forecast_title: Optional[str] = None
    if count is None or count <= 0:
        if dist_total is not None:
            count = dist_total
            count_source = "scanner_distribution_total"
        elif ex:
            fc, errs, title = forecast_count(ex, symbol)
            forecast_errors = errs
            forecast_title = title
            if fc is not None and fc > 0:
                count = fc
                count_source = "forecast_page_text"
    if rating and avg is not None and avg > 0:
        coverage = "covered" if count is not None and count > 0 else "covered_partial"
        return {
            "symbol": symbol,
            "status": "success" if coverage == "covered" else "partial",
            "coverage_status": coverage,
            "rating": rating,
            "analyst_count": count if count is not None and count > 0 else None,
            "avg_target_price": avg,
            "exchange": ex,
            "close": safe_float(row.get("close")),
            "currency": row.get("currency"),
            "source": "TradingView scanner" + (" + TradingView forecast page analyst_count" if count_source == "forecast_page_text" else ""),
            "count_source": count_source or None,
            "distribution": dist,
            "distribution_total": dist_total,
            "forecast_errors": forecast_errors,
            "forecast_title": forecast_title,
            "raw": row,
            "attempts": attempts,
        }
    missing = []
    if not rating:
        missing.append("rating")
    if avg is None or avg <= 0:
        missing.append("avg_target_price")
    return {"symbol": symbol, "status": "failed", "missing": missing, "exchange": ex, "raw": row, "attempts": attempts}


def command_for(new: Dict[str, Any]) -> str:
    sym = new["symbol"]
    status = new["coverage_status"]
    reason = f"TradingView monthly auto-check {now_jst().strftime('%Y/%m')}"
    if status == "covered":
        return f"TV US {sym}|{new['rating']}|{int(new['analyst_count'])}|{float(new['avg_target_price']):.2f}|{reason}"
    if status == "covered_partial":
        ac = "-" if new.get("analyst_count") in [None, ""] else str(int(new["analyst_count"]))
        return f"TV US {sym}|covered_partial|{new['rating']}|{ac}|{float(new['avg_target_price']):.2f}|{reason} partial: analyst_count未取得可"
    if status == "not_applicable":
        return f"TV US {sym}|not_applicable|ETFのためTradingView個別株アナリスト予想対象外"
    raise ValueError(f"unsupported status: {status}")


def differs(old: Any, new: Dict[str, Any]) -> bool:
    if old is None:
        return True
    if getattr(old, "coverage_status", None) != new.get("coverage_status"):
        return True
    if new.get("coverage_status") in {"covered", "covered_partial"}:
        if getattr(old, "rating", None) != new.get("rating"):
            return True
        old_count = getattr(old, "analyst_count", None)
        new_count = new.get("analyst_count")
        if old_count != new_count:
            return True
        old_avg = safe_float(getattr(old, "avg_target_price", None))
        new_avg = safe_float(new.get("avg_target_price"))
        if old_avg is None or new_avg is None or abs(old_avg - new_avg) >= 0.01:
            return True
    return False


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_command_file(name: str, commands: List[str], manifest_files: Dict[str, Any]) -> None:
    text = "\n".join(commands).strip() + ("\n" if commands else "")
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        write_text(base / name, text)
    manifest_files[name] = {"sha256": sha256_text(text), "line_count": len(commands), "bytes_utf8": len(text.encode("utf-8"))}


def main() -> int:
    try:
        items = [x for x in load_watchlist(True) if x.market == "US"]
        old_map = load_tv_snapshot()
        candidates: List[Dict[str, Any]] = []
        failed: List[Dict[str, Any]] = []
        unchanged: List[Dict[str, Any]] = []
        for item in items:
            sym = item.symbol
            if sym in ETF_NOT_APPLICABLE:
                new = {"symbol": sym, "market": "US", "coverage_status": "not_applicable", "rating": None, "analyst_count": None, "avg_target_price": None, "source": "TradingView", "reason": "ETF"}
                old = old_map.get(item.key)
                entry = {"key": item.key, "symbol": sym, "name": item.name, "old": old.__dict__ if old else None, "new": new, "command": command_for(new), "resolution_label": "ETF対象外"}
                if differs(old, new):
                    candidates.append(entry)
                else:
                    unchanged.append(entry)
                continue
            result = scan_symbol(sym)
            if result.get("coverage_status") in {"covered", "covered_partial"}:
                new = {
                    "symbol": sym,
                    "market": "US",
                    "coverage_status": result["coverage_status"],
                    "rating": result["rating"],
                    "analyst_count": result.get("analyst_count"),
                    "avg_target_price": result["avg_target_price"],
                    "source": result.get("source") or "TradingView scanner",
                    "exchange": result.get("exchange"),
                    "raw": result.get("raw"),
                }
                dist = result.get("distribution") or {}
                for k in ["strong_buy_count", "buy_count", "hold_count", "sell_count", "strong_sell_count"]:
                    if dist.get(k) is not None:
                        new[k] = dist.get(k)
                old = old_map.get(item.key)
                entry = {
                    "key": item.key,
                    "symbol": sym,
                    "name": item.name,
                    "old": old.__dict__ if old else None,
                    "new": new,
                    "command": command_for(new),
                    "resolution_label": ("完全取得" if new["coverage_status"] == "covered" else "一部取得：人数未取得でもrating/targetを保存"),
                    "scan": result,
                }
                if differs(old, new):
                    candidates.append(entry)
                else:
                    unchanged.append(entry)
            else:
                failed.append({"key": item.key, "symbol": sym, "name": item.name, "result": result})

        apply_commands = [c["command"] for c in candidates]
        changed_commands = apply_commands[:]
        full_count = sum(1 for c in candidates if c.get("new", {}).get("coverage_status") == "covered")
        partial_count = sum(1 for c in candidates if c.get("new", {}).get("coverage_status") == "covered_partial")
        not_applicable_count = sum(1 for c in candidates if c.get("new", {}).get("coverage_status") == "not_applicable")
        generated = timestamp_jst()
        status_value = "ok" if not failed else "partial"
        manifest_files: Dict[str, Any] = {}
        write_command_file("tv_monthly_refresh_apply_commands.txt", apply_commands, manifest_files)
        write_command_file("tv_monthly_refresh_changed_only_commands.txt", changed_commands, manifest_files)
        one_line = "; ".join(apply_commands)
        write_command_file("tv_monthly_refresh_apply_commands_iphone_1line.txt", [one_line] if one_line else [], manifest_files)
        one_line_changed = "; ".join(changed_commands)
        write_command_file("tv_monthly_refresh_changed_only_commands_iphone_1line.txt", [one_line_changed] if one_line_changed else [], manifest_files)
        manifest = {
            "version": 3,
            "status": status_value,
            "generated_at_jst": generated,
            "apply_command_count": len(apply_commands),
            "changed_command_count": len(changed_commands),
            "summary": {
                "us_watchlist_count": len(items),
                "candidate_change_count": len(candidates),
                "unchanged_count": len(unchanged),
                "failed_count": len(failed),
                "covered_candidate_count": full_count,
                "covered_partial_candidate_count": partial_count,
                "not_applicable_candidate_count": not_applicable_count,
                "success_condition": "coveredはrating+analyst_count+avg_target_price、covered_partialはrating+avg_target_priceで候補化",
            },
            "command_files": manifest_files,
            "primary_files": {"apply_all_success": "tv_monthly_refresh_apply_commands.txt", "changed_only": "tv_monthly_refresh_changed_only_commands.txt"},
        }
        for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
            write_json(base / "tv_monthly_refresh_candidate_manifest.json", manifest)

        status = {
            "status": status_value,
            "generated_at_jst": generated,
            "us_watchlist_count": len(items),
            "fetched_count": len(candidates) + len(unchanged),
            "candidate_change_count": len(candidates),
            "unchanged_count": len(unchanged),
            "failed_count": len(failed),
            "apply_command_count": len(apply_commands),
            "changed_command_count": len(changed_commands),
            "covered_candidate_count": full_count,
            "covered_partial_candidate_count": partial_count,
            "not_applicable_candidate_count": not_applicable_count,
            "candidate_manifest": "tv_monthly_refresh_candidate_manifest.json",
            "note": "候補生成のみ。本番tv_snapshot.jsonは変更していません。",
            "success_condition": "coveredはrating+analyst_count+avg_target_price、covered_partialはrating+avg_target_priceで候補化",
        }
        lines = [
            f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", "",
            "## ステータス", "",
            f"- 米国株監視リスト：{len(items)}件",
            f"- 反映候補：{len(candidates)}件",
            f"- 完全取得候補：{full_count}件",
            f"- 一部取得候補：{partial_count}件",
            f"- 対象外候補：{not_applicable_count}件",
            f"- 値は同じ・確認済み：{len(unchanged)}件",
            f"- 取得失敗・確認候補：{len(failed)}件",
            "", "## 方針", "",
            "- covered：rating + analyst_count + avg_target_price が揃った候補",
            "- covered_partial：rating + avg_target_price は取れたが、analyst_count は未取得でも候補化",
            "- not_applicable：EWYなどETFの対象外明示",
            "", "## 候補", "",
        ]
        if not candidates:
            lines += ["候補なし", ""]
        for i, c in enumerate(candidates, 1):
            new = c["new"]
            lines += [
                f"### {i}. {c['symbol']} {c.get('name') or ''}", "",
                f"- coverage：{new.get('coverage_status')}",
                f"- rating：{new.get('rating') or 'なし'}",
                f"- analyst_count：{new.get('analyst_count') if new.get('analyst_count') is not None else '未取得'}",
                f"- avg_target_price：{fmt_price(new.get('avg_target_price'), 'US') if new.get('avg_target_price') else 'なし'}",
                f"- command：`{c['command']}`",
                "",
            ]
        if failed:
            lines += ["## 取得失敗・確認候補", ""]
            for f in failed[:50]:
                result = f.get("result") or {}
                missing = ", ".join(result.get("missing") or [])
                lines.append(f"- {f['symbol']}：{missing or result.get('error') or '取得条件未達'}")
            lines.append("")
        write_report(STEM, "\n".join(lines), {"status": status, "manifest": manifest, "candidates": candidates, "unchanged": unchanged, "failed": failed}, status)
        return 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
