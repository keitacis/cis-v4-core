#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 TradingView monthly refresh v3 partial coverage patch R7.

Safety goals:
- No direct data/tv_snapshot.json modification in this patch workflow.
- Add covered_partial as a first-class TV snapshot state.
- Keep covered strict: rating + analyst_count + avg_target_price are required.
- Allow covered_partial: rating + avg_target_price are required, analyst_count is optional.
- Keep no_coverage / not_applicable strict and blank.
- Generate Monthly Refresh candidates only; Apply still goes through the guarded Apply workflow.
"""
from __future__ import annotations

import importlib
import os
import py_compile
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "cis_v4"

CORE = SCRIPTS / "cis_core.py"
MASTER = SCRIPTS / "cis_master_update.py"
MONTHLY = SCRIPTS / "cis_tv_monthly_refresh.py"
DAILY = SCRIPTS / "cis_daily_us.py"
WEEKLY = SCRIPTS / "cis_weekly_performance.py"
BUY = SCRIPTS / "cis_buy_alert.py"

CORE_MARKER_START = "# --- CIS R7 TV covered_partial compatibility START ---"
CORE_MARKER_END = "# --- CIS R7 TV covered_partial compatibility END ---"
MASTER_MARKER_START = "# --- CIS R7 TV covered_partial master update START ---"
MASTER_MARKER_END = "# --- CIS R7 TV covered_partial master update END ---"
BUY_MARKER_START = "# --- CIS R7 TV covered_partial buy alert compatibility START ---"
BUY_MARKER_END = "# --- CIS R7 TV covered_partial buy alert compatibility END ---"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def remove_marked_blocks(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
    return pattern.sub("", text)


def replace_required(text: str, old: str, new: str, label: str, min_count: int = 1) -> str:
    count = text.count(old)
    if count < min_count:
        raise RuntimeError(f"replace target not found enough: {label} count={count} min={min_count}")
    return text.replace(old, new)


def insert_before_main_guard(text: str, block: str, label: str) -> str:
    guard = 'if __name__ == "__main__":'
    idx = text.rfind(guard)
    if idx < 0:
        raise RuntimeError(f"main guard not found: {label}")
    return text[:idx].rstrip() + "\n\n" + block.strip() + "\n\n" + text[idx:]


CORE_BLOCK = r'''
# --- CIS R7 TV covered_partial compatibility START ---
# R7: Treat TradingView partial coverage as a first-class state.
# covered         : rating + analyst_count + avg_target_price required
# covered_partial : rating + avg_target_price required, analyst_count optional
TV_COVERAGE_STATUSES = set(TV_COVERAGE_STATUSES) | {"covered_partial"}
TV_COVERAGE_ALIASES.update({
    "COVERED_PARTIAL": "covered_partial",
    "COVERED PARTIAL": "covered_partial",
    "PARTIAL": "covered_partial",
    "一部取得": "covered_partial",
    "アナリスト予想あり（一部取得）": "covered_partial",
})

def normalize_coverage_status(value: Any) -> str:  # type: ignore[override]
    raw = str(value or "covered").strip()
    if not raw:
        return "covered"
    key = raw.upper()
    if key in TV_COVERAGE_ALIASES:
        return TV_COVERAGE_ALIASES[key]
    low = raw.lower().replace("-", "_").replace(" ", "_")
    if low in TV_COVERAGE_STATUSES:
        return low
    raise ValueError(f"TradingView coverage_status が不正です: {value!r}")

def _tv_r7_is_covered(self: TVSnapshot) -> bool:
    return self.coverage_status in {"covered", "covered_partial"}

def _tv_r7_is_tv_ok(self: TVSnapshot) -> bool:
    if self.coverage_status in {"no_coverage", "not_applicable"}:
        return True
    if self.coverage_status == "covered":
        return bool(self.rating) and self.analyst_count is not None and self.analyst_count > 0 and self.avg_target_price is not None and self.avg_target_price > 0
    if self.coverage_status == "covered_partial":
        return bool(self.rating) and self.avg_target_price is not None and self.avg_target_price > 0 and (self.analyst_count is None or self.analyst_count > 0)
    return False

TVSnapshot.is_covered = property(_tv_r7_is_covered)  # type: ignore[assignment]
TVSnapshot.is_tv_ok = property(_tv_r7_is_tv_ok)  # type: ignore[assignment]

def load_tv_snapshot() -> Dict[str, TVSnapshot]:  # type: ignore[override]
    path = DATA_DIR / "tv_snapshot.json"
    data = read_json_strict(path, default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, TVSnapshot] = {}
    if rows in [None, ""]:
        return out
    if not isinstance(rows, list):
        raise ValueError("tv_snapshot.json のitemsがlistではありません。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"tv_snapshot.json のitems[{idx}]がobjectではありません。")
        market = str(row.get("market") or "US").upper()
        try:
            symbol = validate_symbol_for_market(market, str(row.get("symbol") or ""))
        except Exception as e:
            raise ValueError(f"tv_snapshot.json の銘柄行が不正です: items[{idx}] / {e}") from e
        if market != "US":
            raise ValueError(f"tv_snapshot.json はUS銘柄のみです: items[{idx}] {market}:{symbol}")
        coverage_status = normalize_coverage_status(row.get("coverage_status") or "covered")
        rating = str(row.get("rating") or "").strip() or None
        analyst_count = safe_int(row.get("analyst_count"))
        avg_target_price = safe_float(row.get("avg_target_price"))
        if coverage_status == "covered":
            try:
                rating = parse_tv_rating(rating)
            except Exception as e:
                raise ValueError(f"tv_snapshot.json のratingが不正です: US:{symbol} items[{idx}] / {e}") from e
            if analyst_count is None or analyst_count <= 0 or avg_target_price is None or avg_target_price <= 0:
                raise ValueError(f"tv_snapshot.json のcovered行は analyst_count>0 / avg_target_price>0 が必要です: US:{symbol} items[{idx}]")
        elif coverage_status == "covered_partial":
            try:
                rating = parse_tv_rating(rating)
            except Exception as e:
                raise ValueError(f"tv_snapshot.json のcovered_partial行のratingが不正です: US:{symbol} items[{idx}] / {e}") from e
            if avg_target_price is None or avg_target_price <= 0:
                raise ValueError(f"tv_snapshot.json のcovered_partial行は avg_target_price>0 が必要です: US:{symbol} items[{idx}]")
            if analyst_count is not None and analyst_count <= 0:
                raise ValueError(f"tv_snapshot.json のcovered_partial行の analyst_count は未取得または正の整数が必要です: US:{symbol} items[{idx}]")
        else:
            try:
                validate_tv_noncovered_blank_fields(row, f"US:{symbol} items[{idx}]")
            except Exception as e:
                raise ValueError(str(e)) from e
            rating = None
            analyst_count = None
            avg_target_price = None
        k = f"US:{symbol}"
        if k in out:
            raise ValueError(f"tv_snapshot.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = TVSnapshot(
            symbol=symbol,
            market="US",
            coverage_status=coverage_status,
            rating=rating,
            analyst_count=analyst_count,
            avg_target_price=avg_target_price,
            strong_buy_count=safe_int(row.get("strong_buy_count")),
            buy_count=safe_int(row.get("buy_count")),
            hold_count=safe_int(row.get("hold_count")),
            sell_count=safe_int(row.get("sell_count")),
            strong_sell_count=safe_int(row.get("strong_sell_count")),
            updated_at=str(row.get("updated_at") or "").strip() or None,
            source=str(row.get("source") or "TradingView"),
            reason=str(row.get("reason") or "").strip(),
        )
    return out

def tv_upside(latest_price: Optional[float], tv: Optional[TVSnapshot]) -> Optional[float]:  # type: ignore[override]
    if latest_price is None or not tv or tv.coverage_status not in {"covered", "covered_partial"} or tv.avg_target_price is None or latest_price == 0:
        return None
    return (tv.avg_target_price - latest_price) / latest_price * 100.0

def tv_distribution_dict(tv: Optional[TVSnapshot]) -> Dict[str, int]:  # type: ignore[override]
    if not tv or tv.coverage_status not in {"covered", "covered_partial"}:
        return {}
    pairs = [
        ("strong_buy_count", getattr(tv, "strong_buy_count", None)),
        ("buy_count", getattr(tv, "buy_count", None)),
        ("hold_count", getattr(tv, "hold_count", None)),
        ("sell_count", getattr(tv, "sell_count", None)),
        ("strong_sell_count", getattr(tv, "strong_sell_count", None)),
    ]
    if all(v is None for _k, v in pairs):
        return {}
    out: Dict[str, int] = {}
    for k, v in pairs:
        n = safe_int(v)
        out[k] = int(n) if n is not None and n >= 0 else 0
    return out
# --- CIS R7 TV covered_partial compatibility END ---
'''

MASTER_BLOCK = r'''
# --- CIS R7 TV covered_partial master update START ---
# Override index_tv / make_tv_update before main() runs so Master Update can accept
# covered_partial without weakening covered strictness.
def index_tv(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:  # type: ignore[override]
    """Validate and index existing TradingView master rows strictly, with partial support."""
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
        elif coverage_status == "covered_partial":
            rating = parse_rating(r.get("rating"))
            avg_target_price = require_positive_number(r.get("avg_target_price"), f"tv_snapshot.json items[{idx}] 平均目標株価")
            analyst_count = safe_int(r.get("analyst_count"))
            if analyst_count is not None and analyst_count <= 0:
                raise ValueError(f"tv_snapshot.json items[{idx}] covered_partial のアナリスト人数は未取得または正の整数が必要です。")
            base.update(rating=rating, analyst_count=analyst_count, avg_target_price=avg_target_price)
        else:
            validate_tv_noncovered_blank_fields(r, f"US:{symbol} items[{idx}]")
            base.update(rating=None, analyst_count=None, avg_target_price=None)
        k = key(market, symbol)
        if k in out:
            raise ValueError(f"tv_snapshot.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = base
    return out

def make_tv_update(cmd: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore[override]
    if cmd["market"] != "US":
        raise ValueError(f"TV更新はUSのみ対応です: {cmd['raw']}")
    parts = cmd["parts"]
    if len(parts) < 2:
        raise ValueError(
            f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"
            f"または TV US SYMBOL｜covered_partial｜rating｜analyst_count省略可｜avg_target_price｜reason 形式です: {cmd['raw']}"
        )

    def nonnegative_int(value: Any, label: str) -> int:
        n = safe_int(value)
        if n is None or n < 0:
            raise ValueError(f"{label} は0以上の整数が必要です: {value}")
        return int(n)

    def parse_distribution(start: int, analyst_count: int) -> Tuple[Dict[str, int], int]:
        dist = {
            "strong_buy_count": nonnegative_int(parts[start], "Strong Buy人数"),
            "buy_count": nonnegative_int(parts[start + 1], "Buy人数"),
            "hold_count": nonnegative_int(parts[start + 2], "Hold/Neutral人数"),
            "sell_count": nonnegative_int(parts[start + 3], "Sell人数"),
            "strong_sell_count": nonnegative_int(parts[start + 4], "Strong Sell人数"),
        }
        total = sum(dist.values())
        if total <= 0:
            raise ValueError(f"アナリスト分布の合計が0です: {cmd['raw']}")
        if analyst_count != total:
            raise ValueError(
                f"アナリスト人数と分布合計が一致しません: analyst_count={analyst_count} distribution_total={total} / {cmd['raw']}"
            )
        return dist, total

    first = parts[1]
    explicit_status = is_coverage_token(first)
    coverage_status = parse_coverage_status(first) if explicit_status else "covered"

    if coverage_status == "covered":
        distribution: Dict[str, int] = {}
        if explicit_status:
            if len(parts) not in {5, 6, 10, 11}:
                raise ValueError(
                    f"covered更新は TV US SYMBOL｜covered｜rating｜analyst_count｜avg_target_price｜reason、"
                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[2])
            analyst_count = require_positive_int(parts[3], "アナリスト人数")
            avg_target_price = require_positive_number(parts[4], "平均目標株価")
            if len(parts) in {10, 11}:
                distribution, _total = parse_distribution(5, analyst_count)
                reason = parts[10] if len(parts) == 11 else "月次更新"
            else:
                reason = parts[5] if len(parts) == 6 else "月次更新"
        else:
            if len(parts) not in {4, 5, 9, 10}:
                raise ValueError(
                    f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"
                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[1])
            analyst_count = require_positive_int(parts[2], "アナリスト人数")
            avg_target_price = require_positive_number(parts[3], "平均目標株価")
            if len(parts) in {9, 10}:
                distribution, _total = parse_distribution(4, analyst_count)
                reason = parts[9] if len(parts) == 10 else "月次更新"
            else:
                reason = parts[4] if len(parts) == 5 else "月次更新"
        out = {
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
        if distribution:
            out.update(distribution)
        return out

    if coverage_status == "covered_partial":
        if not explicit_status:
            raise ValueError(f"covered_partial は明示形式のみ対応です: TV US SYMBOL｜covered_partial｜rating｜analyst_count省略可｜avg_target_price｜reason")
        if len(parts) not in {5, 6}:
            raise ValueError(
                f"covered_partial更新は TV US SYMBOL｜covered_partial｜rating｜analyst_count省略可｜avg_target_price｜reason 形式です。"
                f"余計な列または不足列があります: {cmd['raw']}"
            )
        rating = parse_rating(parts[2])
        analyst_raw = str(parts[3] if len(parts) > 3 else "").strip()
        analyst_count = safe_int(analyst_raw) if analyst_raw not in {"", "-", "—", "未取得", "なし", "None", "null", "N/A", "na", "NA"} else None
        if analyst_count is not None and analyst_count <= 0:
            raise ValueError(f"covered_partial のアナリスト人数は未取得または正の整数が必要です: {cmd['raw']}")
        avg_target_price = require_positive_number(parts[4], "平均目標株価")
        reason = parts[5] if len(parts) == 6 else "TradingView monthly auto-check partial"
        return {
            "symbol": cmd["symbol"],
            "market": "US",
            "coverage_status": "covered_partial",
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
            f"rating/人数/目標株価/分布など余計な列は入れないでください: {cmd['raw']}"
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
# --- CIS R7 TV covered_partial master update END ---
'''

MONTHLY_SCRIPT = r'''#!/usr/bin/env python3
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
'''


def patch_core() -> None:
    text = read(CORE)
    text = remove_marked_blocks(text, CORE_MARKER_START, CORE_MARKER_END)
    write(CORE, text.rstrip() + "\n\n" + CORE_BLOCK.strip() + "\n")


def patch_master() -> None:
    text = read(MASTER)
    text = remove_marked_blocks(text, MASTER_MARKER_START, MASTER_MARKER_END)
    text = insert_before_main_guard(text, MASTER_BLOCK, "cis_master_update.py")
    write(MASTER, text)


def patch_daily_weekly(path: Path, label: str) -> None:
    text = read(path)
    text = text.replace(
        'if status == "covered": return "アナリスト予想あり"',
        'if status in {"covered", "covered_partial"}: return "アナリスト予想あり（一部取得）" if status == "covered_partial" else "アナリスト予想あり"'
    )
    text = text.replace('{"covered", "no_coverage", "not_applicable"}', '{"covered", "covered_partial", "no_coverage", "not_applicable"}')
    text = text.replace('if cov == "covered" else na', "if cov in {'covered', 'covered_partial'} else na")
    text = text.replace("if cov == 'covered' else na", "if cov in {'covered', 'covered_partial'} else na")
    if "covered_partial" not in text:
        raise RuntimeError(f"covered_partial not injected into {label}")
    if 'cov in {"covered", "covered_partial"}' in text:
        raise RuntimeError(f"unsafe double-quoted set detected in f-string-sensitive {label}")
    write(path, text)


def patch_buy_alert() -> None:
    text = read(BUY)
    text = remove_marked_blocks(text, BUY_MARKER_START, BUY_MARKER_END)

    # Do not rely on the exact existing tv_status_label layout. The current file is
    # aggressively compacted, so append a deterministic override before main() runs.
    label_block = f"""
{BUY_MARKER_START}
def tv_status_label(status: Optional[str]) -> str:  # type: ignore[override]
    return {{
        "covered": "アナリスト予想あり",
        "covered_partial": "アナリスト予想あり（一部取得）",
        "no_coverage": "カバレッジなし",
        "not_applicable": "対象外",
        "not_required": "日本株は対象外",
        None: "未設定",
        "": "未設定",
    }}.get(status, str(status))
{BUY_MARKER_END}
"""
    text = insert_before_main_guard(text, label_block, "cis_buy_alert.py")

    # Count partial coverage as TradingView-covered for status summaries.
    text = text.replace(
        'r.get("tv_coverage_status") == "covered"',
        'r.get("tv_coverage_status") in {"covered", "covered_partial"}'
    )
    text = text.replace(
        "r.get('tv_coverage_status') == 'covered'",
        "r.get('tv_coverage_status') in {'covered', 'covered_partial'}"
    )
    text = text.replace('米国株TradingView covered', '米国株TradingView 予想あり')

    if BUY_MARKER_START not in text or 'covered_partial' not in text:
        raise RuntimeError("covered_partial buy_alert compatibility block not injected")
    write(BUY, text)


def patch_monthly() -> None:
    write(MONTHLY, MONTHLY_SCRIPT)


def clean_pycache() -> None:
    for p in ROOT.rglob("__pycache__"):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)


def compile_all() -> None:
    for path in [CORE, MASTER, MONTHLY, DAILY, WEEKLY, BUY]:
        py_compile.compile(str(path), doraise=True)
    clean_pycache()


def runtime_tests() -> None:
    sys.path.insert(0, str(SCRIPTS))
    for mod in ["cis_core", "cis_master_update", "cis_daily_us", "cis_weekly_performance", "cis_buy_alert", "cis_tv_monthly_refresh"]:
        if mod in sys.modules:
            del sys.modules[mod]
    monthly = importlib.import_module("cis_tv_monthly_refresh")
    core = importlib.import_module("cis_core")
    assert core.normalize_coverage_status("covered_partial") == "covered_partial"
    tv = core.TVSnapshot(symbol="BEAM", market="US", coverage_status="covered_partial", rating="Strong Buy", analyst_count=None, avg_target_price=49.87)
    assert tv.is_covered is True
    assert tv.is_tv_ok is True
    assert core.tv_upside(34.79, tv) is not None
    master = importlib.import_module("cis_master_update")
    cmd = master.parse_line("TV US BEAM|covered_partial|Strong Buy|-|49.87|test")
    upd = master.make_tv_update(cmd)
    assert upd["coverage_status"] == "covered_partial"
    assert upd["analyst_count"] is None
    assert abs(float(upd["avg_target_price"]) - 49.87) < 0.001
    cmd2 = master.parse_line("TV US BEAM|covered_partial|Strong Buy|15|49.87|test")
    upd2 = master.make_tv_update(cmd2)
    assert upd2["analyst_count"] == 15
    cmd3 = master.parse_line("TV US EWY|not_applicable|ETFのため対象外")
    upd3 = master.make_tv_update(cmd3)
    assert upd3["coverage_status"] == "not_applicable"
    daily_text = read(DAILY)
    weekly_text = read(WEEKLY)
    if "cov in {'covered', 'covered_partial'}" not in daily_text:
        raise RuntimeError("daily_us display condition for covered_partial missing")
    if "cov in {'covered', 'covered_partial'}" not in weekly_text:
        raise RuntimeError("weekly display condition for covered_partial missing")

    sample_cmd = monthly.command_for({"symbol": "BEAM", "coverage_status": "covered_partial", "rating": "Strong Buy", "analyst_count": None, "avg_target_price": 49.87})
    if "||" in sample_cmd or "|covered_partial|Strong Buy|-|49.87|" not in sample_cmd:
        raise RuntimeError(f"covered_partial command placeholder is unsafe: {sample_cmd}")

    buy = importlib.import_module("cis_buy_alert")
    assert buy.tv_status_label("covered_partial") == "アナリスト予想あり（一部取得）"
    buy_text = read(BUY)
    if BUY_MARKER_START not in buy_text:
        raise RuntimeError("buy_alert covered_partial compatibility block missing")
    if 'r.get("tv_coverage_status") in {"covered", "covered_partial"}' not in buy_text and "r.get('tv_coverage_status') in {'covered', 'covered_partial'}" not in buy_text:
        raise RuntimeError("buy_alert covered_partial count condition missing")


def main() -> int:
    required = [CORE, MASTER, DAILY, WEEKLY, BUY]
    for p in required:
        if not p.exists():
            raise FileNotFoundError(p)
    patch_core()
    patch_master()
    patch_daily_weekly(DAILY, "daily_us")
    patch_daily_weekly(WEEKLY, "weekly_performance")
    patch_buy_alert()
    patch_monthly()
    compile_all()
    runtime_tests()
    clean_pycache()
    print("R7 patch applied and safety tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
