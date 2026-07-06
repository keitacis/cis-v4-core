#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 TradingView monthly refresh candidate generator.

CIS_V4_TV_REFRESH_INTEGRATED_FIX_V2_SAFE

This is deliberately a *candidate generator*, not a blind auto-writer.
Monthly runs fetch TradingView analyst snapshot candidates, compare them with
saved data/tv_snapshot.json, and write iPhone-friendly apply commands.

Design:
- Fetch only active US watchlist symbols.
- Never modify data/tv_snapshot.json directly.
- Failed/ambiguous fetches are reported and excluded from apply commands.
- TradingView scanner fields confirmed by TV Probe are preferred:
  price_target_average / price_target_high / price_target_low / recommendation_mark.
- Existing CIS internal command/snapshot naming remains compatible:
  avg_target_price and TV US symbol|rating|analyst_count|avg_target_price.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from cis_core import (
    DOCS_LATEST_DIR,
    OUTPUT_DIR,
    TVSnapshot,
    load_tv_snapshot,
    load_watchlist,
    now_jst,
    parse_tv_rating,
    read_json_strict,
    safe_float,
    safe_int,
    timestamp_jst,
    validate_symbol_for_market,
    write_error_report,
    write_json,
    write_report,
    write_text,
)

STEM = "tv_monthly_refresh"
TITLE = "CIS TradingView月次自動確認"
EXCHANGE_CANDIDATES = ["NASDAQ", "NYSE", "AMEX", "NYSEARCA", "BATS", "OTC"]

SCANNER_COLUMN_SETS = [
    ["name", "description", "exchange", "close", "currency", "recommendation_mark", "number_of_analysts", "price_target_average", "price_target_high", "price_target_low", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "close", "currency", "recommendation_mark", "analysts_count", "price_target_average", "price_target_high", "price_target_low", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "close", "currency", "analyst_rating", "number_of_analysts", "price_target_average", "price_target_high", "price_target_low", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "close", "currency", "recommendation_mark", "number_of_analysts", "target_price_average", "target_price_high", "target_price_low", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "close", "currency", "Analyst Rating", "number_of_analysts", "target_price_average", "target_price_high", "target_price_low", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
]

CANDIDATE_MANIFEST_FILENAME = "tv_monthly_refresh_candidate_manifest.json"
CANDIDATE_FILE_PATTERNS = [
    "tv_monthly_refresh_apply_commands*.txt",
    "tv_monthly_refresh_changed_only_commands*.txt",
    "tv_monthly_refresh_apply_iphone_part_*.txt",
    "tv_monthly_refresh_changed_only_iphone_part_*.txt",
    CANDIDATE_MANIFEST_FILENAME,
]

RATING_TEXT_ALIASES = {
    "STRONG BUY": "Strong Buy", "BUY": "Buy", "OUTPERFORM": "Buy", "OVERWEIGHT": "Buy",
    "HOLD": "Neutral", "NEUTRAL": "Neutral", "EQUAL WEIGHT": "Neutral", "EQUAL-WEIGHT": "Neutral",
    "MARKET PERFORM": "Neutral", "SELL": "Sell", "UNDERPERFORM": "Sell", "UNDERWEIGHT": "Sell",
    "STRONG SELL": "Strong Sell",
}


@dataclass
class FetchedTV:
    symbol: str
    market: str
    coverage_status: str
    rating: Optional[str]
    analyst_count: Optional[int]
    avg_target_price: Optional[float]
    source: str
    exchange: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
    strong_buy_count: Optional[int] = None
    buy_count: Optional[int] = None
    hold_count: Optional[int] = None
    sell_count: Optional[int] = None
    strong_sell_count: Optional[int] = None

    def distribution_values(self) -> List[Optional[int]]:
        return [self.strong_buy_count, self.buy_count, self.hold_count, self.sell_count, self.strong_sell_count]

    def distribution_total(self) -> Optional[int]:
        vals = self.distribution_values()
        if all(v is None for v in vals):
            return None
        total = sum(int(v or 0) for v in vals)
        return total if total > 0 else None

    def distribution_label(self) -> str:
        total = self.distribution_total()
        if total is None:
            return "未取得"
        return f"強買{self.strong_buy_count or 0} / 買{self.buy_count or 0} / 中立{self.hold_count or 0} / 売{self.sell_count or 0} / 強売{self.strong_sell_count or 0}"

    def to_command(self) -> str:
        reason = f"TradingView monthly auto-check {now_jst().strftime('%Y/%m')}"
        if self.coverage_status == "covered":
            if not self.rating or not self.analyst_count or not self.avg_target_price:
                raise ValueError(f"反映コマンド生成に必要なTV値が不足しています: US:{self.symbol}")
            total = self.distribution_total()
            if total and self.analyst_count == total:
                return (
                    f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|"
                    f"{self.strong_buy_count or 0}|{self.buy_count or 0}|{self.hold_count or 0}|{self.sell_count or 0}|{self.strong_sell_count or 0}|{reason}"
                )
            return f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|{reason}"
        return f"TV US {self.symbol}|{self.coverage_status}|{reason}"


def normalize_rating(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        n = float(value)
        if 1.0 <= n < 1.5:
            return "Strong Buy"
        if 1.5 <= n < 2.5:
            return "Buy"
        if 2.5 <= n < 3.5:
            return "Neutral"
        if 3.5 <= n < 4.5:
            return "Sell"
        if 4.5 <= n <= 5.0:
            return "Strong Sell"
        return None
    text = str(value).strip()
    if not text or text in {"-", "—", "N/A", "None", "null"}:
        return None
    cleaned = re.sub(r"[_\-]+", " ", text).strip().upper()
    cleaned = re.sub(r"\s+", " ", cleaned)
    alias = RATING_TEXT_ALIASES.get(cleaned)
    if alias:
        return alias
    try:
        return parse_tv_rating(text)
    except Exception:
        return None


def _first_int(values: Dict[str, Any], keys: Iterable[str]) -> Optional[int]:
    for k in keys:
        n = safe_int(values.get(k))
        if n is not None:
            return n
    return None


def _first_float_with_key(values: Dict[str, Any], keys: Iterable[str]) -> Tuple[Optional[float], Optional[str]]:
    for k in keys:
        n = safe_float(values.get(k))
        if n is not None and n > 0:
            return n, k
    return None, None


def _first_rating_with_key(values: Dict[str, Any], keys: Iterable[str]) -> Tuple[Optional[str], Optional[str]]:
    for k in keys:
        rating = normalize_rating(values.get(k))
        if rating:
            return rating, k
    return None, None


def distribution_from_values(values: Dict[str, Any]) -> Dict[str, Optional[int]]:
    return {
        "strong_buy_count": _first_int(values, ["analyst_rating_strong_buy", "strong_buy", "strongBuy", "recommendation_strong_buy", "analyst_strong_buy"]),
        "buy_count": _first_int(values, ["analyst_rating_buy", "buy", "recommendation_buy", "analyst_buy"]),
        "hold_count": _first_int(values, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral", "recommendation_hold", "analyst_hold"]),
        "sell_count": _first_int(values, ["analyst_rating_sell", "sell", "recommendation_sell", "analyst_sell"]),
        "strong_sell_count": _first_int(values, ["analyst_rating_strong_sell", "strong_sell", "strongSell", "recommendation_strong_sell", "analyst_strong_sell"]),
    }


def distribution_total(dist: Dict[str, Optional[int]]) -> Optional[int]:
    vals = list(dist.values())
    if all(v is None for v in vals):
        return None
    total = sum(int(v or 0) for v in vals)
    return total if total > 0 else None


def parse_analyst_count_from_text(text: str) -> Optional[int]:
    patterns = [
        r"Based\s+on\s+(\d{1,4})\s+analysts?\b",
        r"(\d{1,4})\s+analysts?\s+giving\s+stock\s+ratings",
        r"(\d{1,4})\s+analysts?\s+offering\s+.*?price\s+forecasts?",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            n = safe_int(m.group(1))
            if n and 0 < n < 1000:
                return n
    return None


def _regex_json_value(text: str, keys: Iterable[str]) -> Any:
    for key in keys:
        m = re.search(r'"' + re.escape(key) + r'"\s*:\s*("[^"]*"|-?\d+(?:\.\d+)?|null)', text)
        if not m:
            continue
        raw = m.group(1)
        if raw == "null":
            return None
        if raw.startswith('"'):
            return raw.strip('"')
        try:
            return float(raw)
        except Exception:
            return raw
    return None


def forecast_url(exchange: str, symbol: str) -> str:
    return f"https://www.tradingview.com/symbols/{exchange}-{symbol}/forecast/"


def request_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (CIS-v4-tv-refresh)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def fetch_analyst_count_from_forecast_page(symbol: str, exchange_hint: Optional[str] = None) -> Tuple[Optional[int], Optional[str], List[str]]:
    errors: List[str] = []
    exchanges: List[str] = []
    if exchange_hint:
        exchanges.append(exchange_hint)
    exchanges += [x for x in EXCHANGE_CANDIDATES if x not in exchanges]
    for ex in exchanges:
        url = forecast_url(ex, symbol)
        try:
            text = request_text(url)
            count = parse_analyst_count_from_text(text)
            if count:
                return count, url, errors
            count_json = safe_int(_regex_json_value(text, ["number_of_analysts", "analysts_count", "analyst_count"]))
            if count_json:
                return count_json, url, errors
            errors.append(f"{ex}: forecast analyst count not found")
        except urllib.error.HTTPError as e:
            errors.append(f"{ex}: forecast HTTPError {e.code}")
        except Exception as e:
            errors.append(f"{ex}: forecast {type(e).__name__}: {e}")
    return None, None, errors


def candidate_from_values(symbol: str, values: Dict[str, Any], source: str, exchange: Optional[str] = None, allow_forecast_count: bool = True) -> Tuple[Optional[FetchedTV], Dict[str, Any]]:
    rating_keys = ["analyst_rating", "Analyst Rating", "recommendation_mark", "rating", "recommendation"]
    count_keys = ["number_of_analysts", "analysts_count", "analyst_count", "analyst_count_current"]
    target_keys = ["price_target_average", "target_price_average", "average_target_price", "avg_target_price", "target_price_avg", "target_price_median"]
    high_keys = ["price_target_high", "target_price_high", "target_price_upper", "high_target_price"]
    low_keys = ["price_target_low", "target_price_low", "target_price_lower", "low_target_price"]
    rating, rating_field = _first_rating_with_key(values, rating_keys)
    avg_target, target_field = _first_float_with_key(values, target_keys)
    high_target, high_field = _first_float_with_key(values, high_keys)
    low_target, low_field = _first_float_with_key(values, low_keys)
    dist = distribution_from_values(values)
    dist_total = distribution_total(dist)
    analyst_count = _first_int(values, count_keys)
    count_source = "scanner_field" if analyst_count else None
    forecast_count_url = None
    forecast_errors: List[str] = []
    if analyst_count is None and dist_total:
        analyst_count = dist_total
        count_source = "distribution_total"
    if analyst_count is None and allow_forecast_count:
        analyst_count, forecast_count_url, forecast_errors = fetch_analyst_count_from_forecast_page(symbol, exchange)
        if analyst_count:
            count_source = "forecast_page_text"
    missing: List[str] = []
    if not rating:
        missing.append("rating")
    if not avg_target:
        missing.append("avg_target_price")
    if not analyst_count:
        missing.append("analyst_count")
    meta = {
        "resolution_status": "success" if not missing else "failed",
        "missing": missing,
        "rating_field": rating_field,
        "target_field": target_field,
        "target_high_field": high_field,
        "target_low_field": low_field,
        "count_source": count_source,
        "forecast_count_url": forecast_count_url,
        "forecast_count_errors": forecast_errors[-3:],
        "distribution_status": "available" if dist_total else "unavailable",
        "distribution_total": dist_total,
        "recommendation_mark_raw": values.get("recommendation_mark"),
        "price_target_high": high_target,
        "price_target_low": low_target,
    }
    if missing:
        return None, meta
    raw = dict(values)
    raw["_cis_resolution"] = meta
    return FetchedTV(
        symbol=symbol,
        market="US",
        coverage_status="covered",
        rating=rating,
        analyst_count=int(analyst_count),
        avg_target_price=float(avg_target),
        source=source if count_source != "forecast_page_text" else f"{source} + TradingView forecast page analyst_count",
        exchange=exchange,
        raw=raw,
        **dist,
    ), meta


def load_fixture() -> Dict[str, FetchedTV]:
    path = os.getenv("CIS_TV_REFRESH_FIXTURE") or os.getenv("CIS_TV_REFRESH_TEST_FIXTURE")
    if not path:
        return {}
    data = read_json_strict(Path(path), default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, FetchedTV] = {}
    if not isinstance(rows, list):
        raise ValueError("TV refresh fixture は items:list 形式が必要です。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"TV refresh fixture items[{idx}] がobjectではありません。")
        symbol = validate_symbol_for_market("US", row.get("symbol"))
        cov = str(row.get("coverage_status") or "covered")
        if cov == "covered":
            rating = normalize_rating(row.get("rating"))
            analyst_count = safe_int(row.get("analyst_count"))
            avg_target = safe_float(row.get("avg_target_price"))
            if not rating or not analyst_count or not avg_target:
                raise ValueError(f"fixture covered行が不正です: US:{symbol}")
            out[f"US:{symbol}"] = FetchedTV(
                symbol, "US", "covered", rating, analyst_count, avg_target, "fixture", row.get("exchange"), row,
                strong_buy_count=safe_int(row.get("strong_buy_count")),
                buy_count=safe_int(row.get("buy_count")),
                hold_count=safe_int(row.get("hold_count")),
                sell_count=safe_int(row.get("sell_count")),
                strong_sell_count=safe_int(row.get("strong_sell_count")),
            )
        else:
            out[f"US:{symbol}"] = FetchedTV(symbol, "US", cov, None, None, None, "fixture", row.get("exchange"), row)
    return out


def fetch_from_tradingview_forecast_page(symbol: str) -> Tuple[Optional[FetchedTV], Optional[str], Optional[Dict[str, Any]]]:
    errors: List[str] = []
    last_meta: Optional[Dict[str, Any]] = None
    for ex in EXCHANGE_CANDIDATES:
        url = forecast_url(ex, symbol)
        try:
            text = request_text(url)
            values = {
                "analyst_rating": _regex_json_value(text, ["analyst_rating", "Analyst Rating", "recommendation", "recommendation_mark"]),
                "recommendation_mark": _regex_json_value(text, ["recommendation_mark"]),
                "number_of_analysts": _regex_json_value(text, ["number_of_analysts", "analysts_count", "analyst_count"]),
                "price_target_average": _regex_json_value(text, ["price_target_average", "target_price_average", "average_target_price", "avg_target_price"]),
                "price_target_high": _regex_json_value(text, ["price_target_high", "target_price_high"]),
                "price_target_low": _regex_json_value(text, ["price_target_low", "target_price_low"]),
                "analyst_rating_strong_buy": _regex_json_value(text, ["analyst_rating_strong_buy", "strong_buy", "strongBuy"]),
                "analyst_rating_buy": _regex_json_value(text, ["analyst_rating_buy", "buy"]),
                "analyst_rating_hold": _regex_json_value(text, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral"]),
                "analyst_rating_sell": _regex_json_value(text, ["analyst_rating_sell", "sell"]),
                "analyst_rating_strong_sell": _regex_json_value(text, ["analyst_rating_strong_sell", "strong_sell", "strongSell"]),
            }
            parsed_count = parse_analyst_count_from_text(text)
            if parsed_count:
                values["number_of_analysts"] = parsed_count
            cand, meta = candidate_from_values(symbol, values, source="TradingView forecast page", exchange=ex, allow_forecast_count=False)
            meta["forecast_url"] = url
            last_meta = meta
            if cand:
                return cand, None, meta
            errors.append(f"{ex}: forecast fields missing {','.join(meta.get('missing') or [])}")
        except urllib.error.HTTPError as e:
            errors.append(f"{ex}: forecast HTTPError {e.code}")
        except Exception as e:
            errors.append(f"{ex}: forecast {type(e).__name__}: {e}")
    return None, " / ".join(errors[-4:]) if errors else "forecast page取得不可", last_meta


def scanner_request(tickers: List[str], columns: List[str]) -> Dict[str, Any]:
    payload = {"symbols": {"tickers": tickers, "query": {"types": []}}, "columns": columns}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://scanner.tradingview.com/america/scan",
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (CIS-v4-tv-refresh)", "Accept": "application/json,text/plain,*/*"},
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_from_tradingview_symbol(symbol: str) -> Tuple[Optional[FetchedTV], Optional[str], Dict[str, Any]]:
    tickers = [f"{ex}:{symbol}" for ex in EXCHANGE_CANDIDATES]
    errors: List[str] = []
    probe_meta: Dict[str, Any] = {"scanner_attempts": [], "fallback": None}
    for columns in SCANNER_COLUMN_SETS:
        try:
            res = scanner_request(tickers, columns)
            rows = res.get("data") if isinstance(res, dict) else None
            if not isinstance(rows, list):
                errors.append("scanner response has no data list")
                probe_meta["scanner_attempts"].append({"columns": columns, "error": "no data list"})
                continue
            matched_any = False
            for row in rows:
                if not isinstance(row, dict):
                    continue
                sym = str(row.get("s") or "")
                d = row.get("d")
                if not isinstance(d, list):
                    continue
                matched_any = True
                values = {col: d[i] if i < len(d) else None for i, col in enumerate(columns)}
                exchange = sym.split(":", 1)[0] if ":" in sym else values.get("exchange")
                cand, meta = candidate_from_values(symbol, values, source="TradingView scanner", exchange=exchange)
                meta["columns"] = columns
                meta["exchange"] = exchange
                probe_meta["scanner_attempts"].append(meta)
                if cand:
                    probe_meta["winning_path"] = meta
                    return cand, None, probe_meta
                errors.append(f"scanner fields missing {','.join(meta.get('missing') or [])}")
            if not matched_any:
                errors.append("scanner returned no matching rows")
        except urllib.error.HTTPError as e:
            errors.append(f"scanner HTTPError {e.code}")
            probe_meta["scanner_attempts"].append({"columns": columns, "error": f"HTTPError {e.code}"})
        except Exception as e:
            errors.append(f"scanner {type(e).__name__}: {e}")
            probe_meta["scanner_attempts"].append({"columns": columns, "error": f"{type(e).__name__}: {e}"})
    page_cand, page_err, page_meta = fetch_from_tradingview_forecast_page(symbol)
    probe_meta["fallback"] = {"kind": "forecast_page", "meta": page_meta, "error": page_err}
    if page_cand:
        return page_cand, None, probe_meta
    if page_err:
        errors.append(page_err)
    return None, " / ".join(errors[-6:]) if errors else "取得不可", probe_meta


def tv_snapshot_to_dict(s: Optional[TVSnapshot]) -> Optional[Dict[str, Any]]:
    if s is None:
        return None
    return {
        "symbol": s.symbol, "market": s.market, "coverage_status": s.coverage_status, "rating": s.rating,
        "analyst_count": s.analyst_count, "avg_target_price": s.avg_target_price,
        "strong_buy_count": getattr(s, "strong_buy_count", None), "buy_count": getattr(s, "buy_count", None),
        "hold_count": getattr(s, "hold_count", None), "sell_count": getattr(s, "sell_count", None),
        "strong_sell_count": getattr(s, "strong_sell_count", None), "updated_at": s.updated_at,
        "source": s.source, "reason": s.reason,
    }


def diff_fields(old: Optional[TVSnapshot], new: FetchedTV) -> List[str]:
    if old is None:
        return ["新規取得"]
    out: List[str] = []
    checks = [
        ("coverage_status", old.coverage_status, new.coverage_status),
        ("rating", old.rating, new.rating),
        ("analyst_count", old.analyst_count, new.analyst_count),
        ("avg_target_price", old.avg_target_price, new.avg_target_price),
        ("strong_buy_count", getattr(old, "strong_buy_count", None), new.strong_buy_count),
        ("buy_count", getattr(old, "buy_count", None), new.buy_count),
        ("hold_count", getattr(old, "hold_count", None), new.hold_count),
        ("sell_count", getattr(old, "sell_count", None), new.sell_count),
        ("strong_sell_count", getattr(old, "strong_sell_count", None), new.strong_sell_count),
    ]
    for label, a, b in checks:
        if a != b:
            if label == "avg_target_price":
                aa = "未設定" if a in [None, ""] else f"{float(a):.2f}"
                bb = "未設定" if b in [None, ""] else f"{float(b):.2f}"
            else:
                aa = a if a not in [None, ""] else "未設定"
                bb = b if b not in [None, ""] else "未設定"
            out.append(f"{label}: {aa} → {bb}")
    return out


def split_lines(lines: List[str], size: int = 15) -> List[List[str]]:
    return [lines[i:i + size] for i in range(0, len(lines), size)]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cleanup_candidate_files() -> None:
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        for pattern in CANDIDATE_FILE_PATTERNS:
            for path in base.glob(pattern):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass


def write_empty_candidate_manifest(status: str, error: Optional[str] = None) -> None:
    manifest = {"version": 2, "status": status, "generated_at_jst": timestamp_jst(), "apply_command_count": 0, "changed_command_count": 0, "command_files": {}}
    if error:
        manifest["error"] = error
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        write_json(base / CANDIDATE_MANIFEST_FILENAME, manifest)


def write_candidate_files(commands: List[str], changed_commands: List[str], status_level: str, generated_at_jst: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    paths: Dict[str, Any] = {}
    manifest_files: Dict[str, Any] = {}
    def record_file(filename: str, content: str) -> None:
        for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
            write_text(base / filename, content)
        paths[filename] = str((DOCS_LATEST_DIR / filename).relative_to(DOCS_LATEST_DIR.parent))
        manifest_files[filename] = {"sha256": sha256_text(content), "line_count": len([ln for ln in content.splitlines() if ln.strip()]), "bytes_utf8": len(content.encode("utf-8"))}
    full = "\n".join(commands).strip() + ("\n" if commands else "")
    changed = "\n".join(changed_commands).strip() + ("\n" if changed_commands else "")
    one_line = " ; ".join(commands)
    changed_one_line = " ; ".join(changed_commands)
    record_file("tv_monthly_refresh_apply_commands.txt", full)
    record_file("tv_monthly_refresh_changed_only_commands.txt", changed)
    record_file("tv_monthly_refresh_apply_commands_iphone_1line.txt", one_line + ("\n" if one_line else ""))
    record_file("tv_monthly_refresh_changed_only_commands_iphone_1line.txt", changed_one_line + ("\n" if changed_one_line else ""))
    split_links: Dict[str, List[str]] = {"apply": [], "changed_only": []}
    for prefix, source_lines in [("apply", commands), ("changed_only", changed_commands)]:
        for i, chunk in enumerate(split_lines(source_lines, 15), start=1):
            text = "\n".join(chunk) + "\n"
            one = " ; ".join(chunk) + "\n"
            filename = f"tv_monthly_refresh_{prefix}_iphone_part_{i:02d}.txt"
            one_filename = f"tv_monthly_refresh_{prefix}_iphone_part_{i:02d}_1line.txt"
            record_file(filename, text)
            record_file(one_filename, one)
            split_links[prefix].append(filename)
            split_links[prefix].append(one_filename)
    manifest = {"version": 2, "status": status_level, "generated_at_jst": generated_at_jst, "apply_command_count": len(commands), "changed_command_count": len(changed_commands), "summary": summary, "command_files": manifest_files, "primary_files": {"apply_all_success": "tv_monthly_refresh_apply_commands.txt", "changed_only": "tv_monthly_refresh_changed_only_commands.txt"}}
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        write_json(base / CANDIDATE_MANIFEST_FILENAME, manifest)
    paths[CANDIDATE_MANIFEST_FILENAME] = str((DOCS_LATEST_DIR / CANDIDATE_MANIFEST_FILENAME).relative_to(DOCS_LATEST_DIR.parent))
    paths["split_links"] = split_links
    paths["manifest"] = manifest
    return paths


def resolution_label(cand: FetchedTV) -> str:
    meta = (cand.raw or {}).get("_cis_resolution") or {}
    count_source = meta.get("count_source") or "unknown"
    dist_status = meta.get("distribution_status") or "unknown"
    if count_source == "forecast_page_text":
        count_label = "人数はforecast本文補完"
    elif count_source == "scanner_field":
        count_label = "人数はscanner"
    elif count_source == "distribution_total":
        count_label = "人数は分布合計"
    else:
        count_label = f"人数経路:{count_source}"
    dist_label = "分布あり" if dist_status == "available" else "分布なし"
    return f"{cand.source} / {count_label} / {dist_label}"


def main() -> int:
    cleanup_candidate_files()
    try:
        items = [x for x in load_watchlist(True) if x.market == "US"]
        old_tv = load_tv_snapshot()
        fixture = load_fixture()
        fetched: Dict[str, FetchedTV] = {}
        failed: List[Dict[str, Any]] = []
        diagnostics: Dict[str, Any] = {}
        for item in items:
            if item.key in fixture:
                fetched[item.key] = fixture[item.key]
                diagnostics[item.key] = {"source": "fixture"}
                continue
            cand, err, diag = fetch_from_tradingview_symbol(item.symbol)
            diagnostics[item.key] = diag
            if cand:
                fetched[item.key] = cand
            else:
                failed.append({"key": item.key, "symbol": item.symbol, "reason": err or "取得不可", "diagnostic": diag})
        candidates: List[Dict[str, Any]] = []
        unchanged: List[Dict[str, Any]] = []
        changed_commands: List[str] = []
        apply_commands: List[str] = []
        source_counts: Dict[str, int] = {}
        count_source_counts: Dict[str, int] = {}
        distribution_counts = {"available": 0, "unavailable": 0}
        for item in items:
            cand = fetched.get(item.key)
            if not cand:
                continue
            old = old_tv.get(item.key)
            diffs = diff_fields(old, cand)
            command = cand.to_command()
            meta = (cand.raw or {}).get("_cis_resolution") or {}
            source_counts[cand.source] = source_counts.get(cand.source, 0) + 1
            cs = str(meta.get("count_source") or "unknown")
            count_source_counts[cs] = count_source_counts.get(cs, 0) + 1
            ds = "available" if meta.get("distribution_status") == "available" else "unavailable"
            distribution_counts[ds] += 1
            row = {"key": item.key, "symbol": item.symbol, "name": item.name, "exchange": cand.exchange, "old": tv_snapshot_to_dict(old), "new": asdict(cand), "resolution": meta, "resolution_label": resolution_label(cand), "diffs": diffs, "command": command}
            apply_commands.append(command)
            if diffs:
                candidates.append(row)
                changed_commands.append(command)
            else:
                unchanged.append(row)
        status_level = "partial" if candidates or failed else "ok"
        generated_at = timestamp_jst()
        summary = {"us_watchlist_count": len(items), "fetched_count": len(fetched), "candidate_change_count": len(candidates), "unchanged_count": len(unchanged), "failed_count": len(failed), "source_counts": source_counts, "count_source_counts": count_source_counts, "distribution_counts": distribution_counts, "success_condition": "rating + analyst_count + avg_target_price が揃った銘柄のみ反映候補化"}
        candidate_paths = write_candidate_files(apply_commands, changed_commands, status_level, generated_at, summary)
        status = {"status": status_level, "generated_at_jst": generated_at, "us_watchlist_count": len(items), "fetched_count": len(fetched), "candidate_change_count": len(candidates), "unchanged_count": len(unchanged), "failed_count": len(failed), "apply_command_count": len(apply_commands), "changed_command_count": len(changed_commands), "candidate_manifest": CANDIDATE_MANIFEST_FILENAME, "note": "候補生成のみ。本番tv_snapshot.jsonは変更していません。", "success_condition": summary["success_condition"]}
        lines: List[str] = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += ["## これは何をするレポートか", "", "- 月1でTradingView候補値を自動確認し、保存済み tv_snapshot.json と比較します。", "- このレポート自体は tv_snapshot.json を直接書き換えません。", "- rating + analyst_count + 平均目標株価が揃った銘柄だけ、反映用コマンドを自動生成します。", "- 分布は取れた場合だけ反映コマンドに含めます。取れなくても、rating・人数・平均目標株価が揃っていれば候補化します。", "", "## ステータス", "", f"- 米国株監視リスト：{len(items)}件", f"- 自動取得成功：{len(fetched)}件", f"- 値の変更候補：{len(candidates)}件", f"- 値は同じ・確認済み：{len(unchanged)}件", f"- 取得失敗・手動確認候補：{len(failed)}件", "", "## 取得経路サマリー", ""]
        if source_counts:
            for k, v in sorted(source_counts.items(), key=lambda kv: (-kv[1], kv[0])):
                lines.append(f"- source: {k}：{v}件")
        else:
            lines.append("- source: なし")
        for k, v in sorted(count_source_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- analyst_count経路: {k}：{v}件")
        lines.append(f"- 分布あり：{distribution_counts['available']}件")
        lines.append(f"- 分布なし：{distribution_counts['unavailable']}件")
        lines.append("")
        lines += ["## iPhone用・反映導線", ""]
        if apply_commands:
            lines += ["### 推奨：コピーなしで反映する", "", "- GitHub Actions → `CIS v4 Apply TV Monthly Candidate` → `Run workflow` を押してください。", "- このWorkflowは、この月次確認で取得できた銘柄だけをMaster Updateに渡します。", "- 取得失敗銘柄は反映対象外なので、既存値は維持されます。", "", "### 手動で貼る場合", "", "iPhoneでは、まず分割版を使うのが安全です。", ""]
            apply_parts = [x for x in candidate_paths.get("split_links", {}).get("apply", []) if x.endswith("_1line.txt")]
            changed_parts = [x for x in candidate_paths.get("split_links", {}).get("changed_only", []) if x.endswith("_1line.txt")]
            if apply_parts:
                lines += ["#### 全成功取得分・iPhone分割1行版", ""]
                for fn in apply_parts:
                    lines.append(f"- [{fn}]({fn})")
                lines.append("")
            if changed_parts:
                lines += ["#### 変更ありだけ・iPhone分割1行版", ""]
                for fn in changed_parts:
                    lines.append(f"- [{fn}]({fn})")
                lines.append("")
            lines += ["#### PC向け・全件", "", "- [全成功取得分・1行版](tv_monthly_refresh_apply_commands_iphone_1line.txt)", "- [変更ありだけ・1行版](tv_monthly_refresh_changed_only_commands_iphone_1line.txt)", "- [全成功取得分・改行版](tv_monthly_refresh_apply_commands.txt)", "- [変更ありだけ・改行版](tv_monthly_refresh_changed_only_commands.txt)", "- [候補manifest](tv_monthly_refresh_candidate_manifest.json)", ""]
        else:
            lines += ["反映できる自動取得結果がありません。", ""]
        lines += ["## 値の変更候補", ""]
        if not candidates:
            lines += ["変更候補なし", ""]
        else:
            for c in candidates:
                new = c["new"]
                old = c["old"] or {}
                meta = c.get("resolution") or {}
                lines += [f"### {c['key']} {c['name']}", ""]
                lines.append(f"- 旧：{old.get('coverage_status','未設定')} / {old.get('rating','未設定')} / {old.get('analyst_count','未設定')}人 / {old.get('avg_target_price','未設定')}")
                lines.append(f"- 新：{new.get('coverage_status')} / {new.get('rating')} / {new.get('analyst_count')}人 / {new.get('avg_target_price')}")
                lines.append(f"- 取得経路：{c.get('resolution_label')}")
                lines.append(f"- 取引所候補：{c.get('exchange') or '未取得'}")
                if meta.get("recommendation_mark_raw") is not None:
                    lines.append(f"- recommendation_mark(raw)：{meta.get('recommendation_mark_raw')} → {new.get('rating')}")
                if meta.get("target_field"):
                    lines.append(f"- 平均目標株価フィールド：{meta.get('target_field')}")
                if meta.get("forecast_count_url"):
                    lines.append(f"- analyst_count補完URL：{meta.get('forecast_count_url')}")
                for d in c["diffs"]:
                    lines.append(f"- 差分：{d}")
                lines.append("")
        lines += ["## 値は同じ・確認済み", ""]
        if not unchanged:
            lines += ["なし", ""]
        else:
            for c in unchanged[:80]:
                new = c["new"]
                lines.append(f"- {c['key']}：{new.get('rating')} / {new.get('analyst_count')}人 / {new.get('avg_target_price')} / {c.get('resolution_label')}")
            if len(unchanged) > 80:
                lines.append(f"- ほか{len(unchanged)-80}件")
            lines.append("")
        lines += ["## 取得失敗・手動確認候補", ""]
        if not failed:
            lines += ["なし", ""]
        else:
            lines += ["取得失敗銘柄は候補コマンドから除外しています。既存の tv_snapshot.json は守られます。", ""]
            for f in failed:
                diag = f.get("diagnostic") or {}
                attempts = diag.get("scanner_attempts") or []
                latest_missing = None
                for a in reversed(attempts):
                    if a.get("missing"):
                        latest_missing = ",".join(a.get("missing") or [])
                        break
                suffix = f" / 不足:{latest_missing}" if latest_missing else ""
                lines.append(f"- {f['key']}：{f['reason']}{suffix}")
            lines.append("")
        payload = {"status": status, "manifest": candidate_paths.get("manifest"), "candidates": candidates, "unchanged": unchanged, "failed": failed, "diagnostics": diagnostics, "apply_commands": apply_commands, "changed_commands": changed_commands}
        write_report(STEM, "\n".join(lines), payload, status)
        return 0
    except Exception as e:
        cleanup_candidate_files()
        write_empty_candidate_manifest("error", f"{type(e).__name__}: {e}")
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
