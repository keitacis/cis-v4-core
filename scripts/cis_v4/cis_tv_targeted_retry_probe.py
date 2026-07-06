#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CIS v4 TradingView targeted retry probe.

Diagnostic only.
- Reads docs/v4/latest/tv_monthly_refresh_latest.json.
- Probes only failed TradingView Monthly Refresh symbols, with priority on large/mid names.
- Writes docs/v4/latest/tv_targeted_retry_probe_latest.{html,md,json}
  and output/tv_targeted_retry_probe_*.json.
- Does NOT modify data/tv_snapshot.json, Master, Apply, Daily, Weekly, Buy Alert, or Home.
"""

from __future__ import annotations

import csv
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(".")
LATEST_DIR = ROOT / "docs" / "v4" / "latest"
OUTPUT_DIR = ROOT / "output"

MONTHLY_JSON = LATEST_DIR / "tv_monthly_refresh_latest.json"
WATCHLIST_CSV = ROOT / "data" / "watchlist_master.csv"

OUT_HTML = LATEST_DIR / "tv_targeted_retry_probe_latest.html"
OUT_MD = LATEST_DIR / "tv_targeted_retry_probe_latest.md"
OUT_JSON = LATEST_DIR / "tv_targeted_retry_probe_latest.json"

JST = dt.timezone(dt.timedelta(hours=9), "JST")

# These are intentionally the failed names that are more suspicious as "real no coverage"
# because they are large/mid or broadly followed.
PRIORITY_SYMBOLS = [
    "DIS", "V", "VRTX", "ANET", "DDOG", "SNOW", "QCOM", "ETN",
    "AEM", "COHR", "CRSP", "DKNG", "BEAM", "MSTR", "ZETA", "PL",
]

# Conservative primary exchange hints. The probe also tests fallback exchanges.
EXCHANGE_HINTS = {
    "AEM": "NYSE",
    "ANET": "NYSE",
    "AXTI": "NASDAQ",
    "BEAM": "NASDAQ",
    "COHR": "NYSE",
    "CRSP": "NASDAQ",
    "DDOG": "NASDAQ",
    "DIS": "NYSE",
    "DKNG": "NASDAQ",
    "ETN": "NYSE",
    "EWY": "AMEX",
    "HSAI": "NASDAQ",
    "KITT": "NASDAQ",
    "KVYO": "NYSE",
    "MSTR": "NASDAQ",
    "OPTX": "NASDAQ",
    "PL": "NYSE",
    "POET": "NASDAQ",
    "QCOM": "NASDAQ",
    "SNOW": "NYSE",
    "V": "NYSE",
    "VRTX": "NASDAQ",
    "ZETA": "NYSE",
}

COMMON_EXCHANGES = ["NASDAQ", "NYSE", "AMEX", "NYSEARCA", "BATS", "OTC"]

CONFIRMED_COLUMNS = [
    "name",
    "description",
    "exchange",
    "close",
    "currency",
    "recommendation_mark",
    "number_of_analysts",
    "price_target_average",
    "price_target_high",
    "price_target_low",
    "analyst_rating_strong_buy",
    "analyst_rating_buy",
    "analyst_rating_hold",
    "analyst_rating_sell",
    "analyst_rating_strong_sell",
]

LEGACY_COLUMNS = [
    "name",
    "description",
    "exchange",
    "close",
    "currency",
    "recommendation_mean",
    "recommendation_mark",
    "analyst_rating",
    "analyst_rating_count",
    "analyst_count",
    "number_of_analysts",
    "target_price_average",
    "target_price_high",
    "target_price_low",
    "target_price_median",
    "price_target_mean",
    "price_target_average",
    "price_target_high",
    "price_target_low",
    "price_target_median",
]

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST)


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_watchlist() -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    if not WATCHLIST_CSV.exists():
        return out
    with WATCHLIST_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            sym = (row.get("symbol") or "").strip().upper()
            if sym:
                out[sym] = row
    return out


def uniq(xs: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in xs:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def exchanges_for(symbol: str, previous_attempts: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    prev = []
    for a in previous_attempts or []:
        ex = (a.get("exchange") or a.get("tv_exchange") or "").strip().upper()
        if ex:
            prev.append(ex)
    return uniq([EXCHANGE_HINTS.get(symbol, ""), *prev, *COMMON_EXCHANGES])


def http_json_post(url: str, payload: Dict[str, Any], timeout: int = 20) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[int]]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Accept": "application/json,text/plain,*/*",
            "Origin": "https://www.tradingview.com",
            "Referer": "https://www.tradingview.com/",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body), None, getattr(resp, "status", None)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            body = ""
        return None, f"HTTPError {e.code}: {body}", e.code
    except Exception as e:
        return None, f"{type(e).__name__}: {e}", None


def scan_symbol(exchange: str, symbol: str, columns: List[str]) -> Dict[str, Any]:
    tv_symbol = f"{exchange}:{symbol}"
    payload = {
        "symbols": {"tickers": [tv_symbol], "query": {"types": []}},
        "columns": columns,
    }
    data, error, status = http_json_post("https://scanner.tradingview.com/america/scan", payload)
    result: Dict[str, Any] = {
        "tv_symbol": tv_symbol,
        "exchange": exchange,
        "http_status": status,
        "error": error,
        "fields": {},
        "non_null_fields": [],
    }
    if not data:
        return result
    rows = data.get("data") or []
    if not rows:
        result["error"] = result["error"] or "scanner returned no rows"
        return result
    row = rows[0]
    values = row.get("d") or []
    fields = {}
    non_null = []
    for col, val in zip(columns, values):
        fields[col] = val
        if val is not None and val != "":
            non_null.append(col)
    result["fields"] = fields
    result["non_null_fields"] = non_null
    return result


def http_get_text(url: str, timeout: int = 20) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.tradingview.com/",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return body, None, getattr(resp, "status", None)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            body = ""
        return None, f"HTTPError {e.code}: {body}", e.code
    except Exception as e:
        return None, f"{type(e).__name__}: {e}", None


def forecast_probe(exchange: str, symbol: str) -> Dict[str, Any]:
    url = f"https://www.tradingview.com/symbols/{exchange}-{symbol}/forecast/"
    body, error, status = http_get_text(url)
    result: Dict[str, Any] = {
        "url": url,
        "exchange": exchange,
        "http_status": status,
        "error": error,
        "length": len(body or ""),
        "title": None,
        "analyst_count_matches": [],
        "has_analyst_rating_text": False,
        "has_price_target_text": False,
        "snippet": None,
    }
    if not body:
        return result
    title_m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    if title_m:
        result["title"] = html.unescape(re.sub(r"\s+", " ", title_m.group(1)).strip())
    counts = set()
    patterns = [
        r"Based\s+on\s+(\d{1,4})\s+analysts?",
        r"based\s+on\s+(\d{1,4})\s+analysts?",
        r"(\d{1,4})\s+analysts?\s+offering",
        r"(\d{1,4})\s+analysts?\s+giving",
        r"(\d{1,4})\s+analysts?\s+have",
    ]
    for pat in patterns:
        for m in re.finditer(pat, body, re.I):
            counts.add(int(m.group(1)))
    result["analyst_count_matches"] = sorted(counts)
    result["has_analyst_rating_text"] = bool(re.search(r"Analyst rating", body, re.I))
    result["has_price_target_text"] = bool(re.search(r"Price Target|price target|Forecast", body, re.I))
    # Keep a short diagnostic snippet around "Analyst rating" or "Based on".
    idx = -1
    for needle in ["Based on", "Analyst rating", "Price Target"]:
        idx = body.lower().find(needle.lower())
        if idx >= 0:
            break
    if idx >= 0:
        snippet = body[max(0, idx - 250): idx + 650]
        snippet = re.sub(r"<[^>]+>", " ", snippet)
        snippet = html.unescape(re.sub(r"\s+", " ", snippet)).strip()
        result["snippet"] = snippet[:1000]
    return result


def val(fields: Dict[str, Any], names: List[str]) -> Any:
    for n in names:
        v = fields.get(n)
        if v is not None and v != "":
            return v
    return None


def score_attempt(attempt: Dict[str, Any]) -> int:
    fields = attempt.get("confirmed", {}).get("fields", {})
    legacy = attempt.get("legacy", {}).get("fields", {})
    forecast = attempt.get("forecast", {})
    score = 0
    if val(fields, ["recommendation_mark"]) is not None:
        score += 4
    if val(fields, ["price_target_average"]) is not None:
        score += 4
    if val(fields, ["number_of_analysts"]) is not None:
        score += 3
    if forecast.get("analyst_count_matches"):
        score += 3
    if val(legacy, ["target_price_average", "price_target_mean", "price_target_average"]) is not None:
        score += 2
    if val(legacy, ["recommendation_mean", "recommendation_mark", "analyst_rating"]) is not None:
        score += 2
    if attempt.get("confirmed", {}).get("http_status") == 200:
        score += 1
    if forecast.get("http_status") == 200:
        score += 1
    return score


def classify(symbol: str, asset_type: str, best: Dict[str, Any], attempts: List[Dict[str, Any]]) -> Dict[str, str]:
    if asset_type.lower() in {"etf", "fund"} or symbol in {"EWY"}:
        return {
            "classification": "対象外候補",
            "action": "not_applicable候補。ETF/ファンド系は個別株アナリスト予想の対象外として扱う方向。",
        }
    fields = best.get("confirmed", {}).get("fields", {})
    legacy = best.get("legacy", {}).get("fields", {})
    forecast = best.get("forecast", {})
    has_rating = val(fields, ["recommendation_mark"]) is not None or val(legacy, ["recommendation_mean", "recommendation_mark", "analyst_rating"]) is not None
    has_target = val(fields, ["price_target_average"]) is not None or val(legacy, ["target_price_average", "price_target_mean", "price_target_average"]) is not None
    has_count = val(fields, ["number_of_analysts"]) is not None or bool(forecast.get("analyst_count_matches"))
    if has_rating and has_target and has_count:
        return {
            "classification": "追加取得可能候補",
            "action": "Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。",
        }
    if has_rating or has_target or has_count:
        return {
            "classification": "部分データあり",
            "action": "片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。",
        }
    primary_errors = []
    for a in attempts:
        fc = a.get("forecast", {})
        if fc.get("http_status") in (403, 404):
            primary_errors.append(str(fc.get("http_status")))
    if primary_errors and all(e == "403" for e in primary_errors):
        return {
            "classification": "forecast 403候補",
            "action": "GitHub Actions環境からforecast本文が制限されている可能性。scanner側だけで取れるか追加検証。",
        }
    if primary_errors and all(e == "404" for e in primary_errors):
        return {
            "classification": "symbol/forecastなし候補",
            "action": "TradingView forecast URLまたはsymbol候補が違う可能性。symbol解決を追加検証。",
        }
    return {
        "classification": "カバレッジなし候補",
        "action": "現方式ではrating・平均目標・人数が揃わない。ただし大型銘柄ならno_coverage固定前に再確認。",
    }


def load_failed(monthly: Dict[str, Any]) -> List[Dict[str, Any]]:
    failed = monthly.get("failed")
    if isinstance(failed, list):
        return failed
    # Defensive fallback for possible nested structures.
    manifest = monthly.get("manifest") or {}
    failed = manifest.get("failed")
    if isinstance(failed, list):
        return failed
    return []


def main() -> int:
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = now_jst()
    target_mode = os.environ.get("TV_TARGET_MODE", "priority_failed").strip() or "priority_failed"

    if not MONTHLY_JSON.exists():
        report = {
            "status": "error",
            "generated_at_jst": generated.isoformat(),
            "error": f"missing source json: {MONTHLY_JSON}",
        }
        write_outputs(report)
        return 0

    monthly = read_json(MONTHLY_JSON)
    watchlist = read_watchlist()
    failed = load_failed(monthly)

    failed_by_symbol: Dict[str, Dict[str, Any]] = {}
    for item in failed:
        sym = (item.get("symbol") or item.get("key", "").split(":")[-1]).strip().upper()
        if sym:
            failed_by_symbol[sym] = item

    if target_mode == "all_failed":
        targets = list(failed_by_symbol.keys())
    else:
        targets = [s for s in PRIORITY_SYMBOLS if s in failed_by_symbol]
        if not targets:
            targets = list(failed_by_symbol.keys())

    results: List[Dict[str, Any]] = []

    for sym in targets:
        item = failed_by_symbol.get(sym, {})
        meta = watchlist.get(sym, {})
        asset_type = (meta.get("asset_type") or "").strip().lower()
        previous_attempts = ((item.get("diagnostic") or {}).get("scanner_attempts") or [])
        exchanges = exchanges_for(sym, previous_attempts)

        attempts = []
        for ex in exchanges:
            confirmed = scan_symbol(ex, sym, CONFIRMED_COLUMNS)
            # Sleep lightly to avoid hammering TV.
            time.sleep(0.15)
            legacy = scan_symbol(ex, sym, LEGACY_COLUMNS)
            time.sleep(0.15)
            forecast = forecast_probe(ex, sym)
            time.sleep(0.15)
            attempts.append({
                "exchange": ex,
                "confirmed": confirmed,
                "legacy": legacy,
                "forecast": forecast,
                "score": 0,
            })
            attempts[-1]["score"] = score_attempt(attempts[-1])

        attempts_sorted = sorted(attempts, key=lambda x: x.get("score", 0), reverse=True)
        best = attempts_sorted[0] if attempts_sorted else {}
        c = classify(sym, asset_type, best, attempts_sorted)
        results.append({
            "symbol": sym,
            "name": meta.get("name") or item.get("name") or "",
            "asset_type": asset_type or meta.get("asset_type") or "",
            "category": meta.get("category") or "",
            "notes": meta.get("notes") or "",
            "original_reason": item.get("reason") or "",
            "previous_exchange_candidates": [a.get("exchange") for a in previous_attempts if a.get("exchange")],
            "target_mode": target_mode,
            "classification": c["classification"],
            "recommended_action": c["action"],
            "best_exchange": best.get("exchange"),
            "best_score": best.get("score"),
            "best_summary": summarize_attempt(best),
            "attempts": attempts_sorted,
        })

    summary: Dict[str, int] = {}
    for r in results:
        summary[r["classification"]] = summary.get(r["classification"], 0) + 1

    report = {
        "status": "ok",
        "generated_at_jst": generated.isoformat(),
        "target_mode": target_mode,
        "source_json": str(MONTHLY_JSON),
        "failed_total_in_source": len(failed_by_symbol),
        "targets_tested": len(results),
        "priority_symbols": PRIORITY_SYMBOLS,
        "classification_summary": summary,
        "results": results,
        "note": "Diagnostic only. tv_snapshot.json, Master, Apply, Daily, Weekly, Buy Alert, and Home are not modified.",
    }
    write_outputs(report)
    return 0


def summarize_attempt(attempt: Dict[str, Any]) -> Dict[str, Any]:
    fields = attempt.get("confirmed", {}).get("fields", {})
    legacy = attempt.get("legacy", {}).get("fields", {})
    fc = attempt.get("forecast", {})
    return {
        "confirmed_http": attempt.get("confirmed", {}).get("http_status"),
        "legacy_http": attempt.get("legacy", {}).get("http_status"),
        "forecast_http": fc.get("http_status"),
        "close": val(fields, ["close"]),
        "currency": val(fields, ["currency"]),
        "recommendation_mark": val(fields, ["recommendation_mark"]),
        "number_of_analysts": val(fields, ["number_of_analysts"]),
        "price_target_average": val(fields, ["price_target_average"]),
        "price_target_high": val(fields, ["price_target_high"]),
        "price_target_low": val(fields, ["price_target_low"]),
        "legacy_rating": val(legacy, ["recommendation_mean", "recommendation_mark", "analyst_rating"]),
        "legacy_target": val(legacy, ["target_price_average", "price_target_mean", "price_target_average"]),
        "forecast_analyst_count_matches": fc.get("analyst_count_matches"),
        "forecast_title": fc.get("title"),
        "forecast_error": fc.get("error"),
    }


def esc(x: Any) -> str:
    return html.escape("" if x is None else str(x))


def render_md(report: Dict[str, Any]) -> str:
    lines = []
    gen = report.get("generated_at_jst", "")
    lines.append("# CIS TradingView Targeted Retry Probe")
    lines.append("")
    lines.append(f"生成日時: {gen}")
    lines.append("")
    lines.append("## これは何をするレポートか")
    lines.append("")
    lines.append("- Monthly Refreshで失敗した銘柄のうち、大型・中型など取りこぼしが疑われる銘柄をTradingViewだけで再診断します。")
    lines.append("- このレポートは診断専用です。tv_snapshot.json、Master、Apply、Daily、Weekly、Buy Alert、Homeは変更しません。")
    lines.append("")
    lines.append("## ステータス")
    lines.append("")
    lines.append(f"- target_mode: {report.get('target_mode')}")
    lines.append(f"- 元JSON失敗件数: {report.get('failed_total_in_source')}")
    lines.append(f"- 再診断対象: {report.get('targets_tested')}")
    lines.append("")
    lines.append("## 分類サマリー")
    lines.append("")
    for k, v in (report.get("classification_summary") or {}).items():
        lines.append(f"- {k}: {v}件")
    lines.append("")
    lines.append("## 銘柄別")
    lines.append("")
    for i, r in enumerate(report.get("results") or [], 1):
        b = r.get("best_summary") or {}
        lines.append(f"### {i}. {r.get('symbol')} {r.get('name')}")
        lines.append("")
        lines.append(f"- 判定: {r.get('classification')}")
        lines.append(f"- 推奨アクション: {r.get('recommended_action')}")
        lines.append(f"- best_exchange: {r.get('best_exchange')} / score: {r.get('best_score')}")
        lines.append(f"- scanner confirmed HTTP: {b.get('confirmed_http')}")
        lines.append(f"- forecast HTTP: {b.get('forecast_http')}")
        lines.append(f"- recommendation_mark: {b.get('recommendation_mark')}")
        lines.append(f"- price_target_average: {b.get('price_target_average')}")
        lines.append(f"- number_of_analysts: {b.get('number_of_analysts')}")
        lines.append(f"- forecast analyst count matches: {b.get('forecast_analyst_count_matches')}")
        lines.append(f"- forecast title: {b.get('forecast_title')}")
        if b.get("forecast_error"):
            lines.append(f"- forecast error: {b.get('forecast_error')}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_html(report: Dict[str, Any]) -> str:
    gen = report.get("generated_at_jst", "")
    parts = []
    parts.append("<!doctype html><html lang='ja'><head><meta charset='utf-8'>")
    parts.append("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    parts.append("<title>CIS TradingView Targeted Retry Probe</title>")
    parts.append("<style>")
    parts.append("""
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.65;margin:24px;max-width:980px}
h1{font-size:2rem} h2{margin-top:2rem}
.card{border:1px solid #ddd;border-radius:16px;padding:16px;margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;background:#eee;margin-right:4px}
pre{white-space:pre-wrap;word-break:break-word;background:#f6f6f6;padding:12px;border-radius:12px;font-size:.9rem}
table{border-collapse:collapse;width:100%;font-size:.95rem}
td,th{border-bottom:1px solid #eee;text-align:left;padding:6px}
.muted{color:#666}
""")
    parts.append("</style></head><body>")
    parts.append("<p><a href='../'>CISホームへ戻る</a></p>")
    parts.append("<h1>CIS TradingView Targeted Retry Probe</h1>")
    parts.append(f"<p>生成日時：{esc(gen)}</p>")
    parts.append("<h2>これは何をするレポートか</h2>")
    parts.append("<ul>")
    parts.append("<li>Monthly Refreshで失敗した銘柄のうち、大型・中型など取りこぼしが疑われる銘柄をTradingViewだけで再診断します。</li>")
    parts.append("<li>診断専用です。tv_snapshot.json、Master、Apply、Daily、Weekly、Buy Alert、Homeは変更しません。</li>")
    parts.append("</ul>")
    parts.append("<h2>ステータス</h2>")
    parts.append("<ul>")
    parts.append(f"<li>target_mode：{esc(report.get('target_mode'))}</li>")
    parts.append(f"<li>元JSON失敗件数：{esc(report.get('failed_total_in_source'))}</li>")
    parts.append(f"<li>再診断対象：{esc(report.get('targets_tested'))}</li>")
    parts.append("</ul>")
    parts.append("<h2>分類サマリー</h2><ul>")
    for k, v in (report.get("classification_summary") or {}).items():
        parts.append(f"<li>{esc(k)}：{esc(v)}件</li>")
    parts.append("</ul>")
    parts.append("<h2>銘柄別</h2>")
    for i, r in enumerate(report.get("results") or [], 1):
        b = r.get("best_summary") or {}
        parts.append("<div class='card'>")
        parts.append(f"<h3>{i}. {esc(r.get('symbol'))} {esc(r.get('name'))}</h3>")
        parts.append(f"<p><span class='badge'>{esc(r.get('classification'))}</span></p>")
        parts.append(f"<p><b>推奨アクション：</b>{esc(r.get('recommended_action'))}</p>")
        parts.append("<table>")
        rows = [
            ("best_exchange", r.get("best_exchange")),
            ("best_score", r.get("best_score")),
            ("scanner confirmed HTTP", b.get("confirmed_http")),
            ("legacy HTTP", b.get("legacy_http")),
            ("forecast HTTP", b.get("forecast_http")),
            ("close", b.get("close")),
            ("currency", b.get("currency")),
            ("recommendation_mark", b.get("recommendation_mark")),
            ("price_target_average", b.get("price_target_average")),
            ("number_of_analysts", b.get("number_of_analysts")),
            ("forecast analyst count matches", b.get("forecast_analyst_count_matches")),
            ("forecast title", b.get("forecast_title")),
            ("forecast error", b.get("forecast_error")),
        ]
        for a, bval in rows:
            parts.append(f"<tr><th>{esc(a)}</th><td>{esc(bval)}</td></tr>")
        parts.append("</table>")
        parts.append("<details><summary>attempt詳細</summary>")
        parts.append(f"<pre>{esc(json.dumps(r.get('attempts'), ensure_ascii=False, indent=2))}</pre>")
        parts.append("</details>")
        parts.append("</div>")
    parts.append("</body></html>")
    return "\n".join(parts)


def write_outputs(report: Dict[str, Any]) -> None:
    write_json(OUT_JSON, report)
    # timestamped copy
    ts = now_jst().strftime("%Y%m%d_%H%M%S")
    write_json(OUTPUT_DIR / f"tv_targeted_retry_probe_{ts}.json", report)
    OUT_MD.write_text(render_md(report), encoding="utf-8", newline="\n")
    OUT_HTML.write_text(render_html(report), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    raise SystemExit(main())
