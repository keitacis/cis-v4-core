#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 TradingView probe v2 safe.

Non-destructive diagnostic workflow. It does not modify tv_snapshot.json.
It checks, from GitHub Actions, whether TradingView scanner and forecast pages
are reachable and which analyst-related scanner fields are valid/returned.
"""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "v4" / "latest"
OUT = ROOT / "output"
DOCS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

JST = dt.timezone(dt.timedelta(hours=9))
NOW = dt.datetime.now(JST)

WATCHLIST = ROOT / "data" / "watchlist_master.csv"
PRIORITY = ["AVAV", "PYPL", "META", "EWY", "AEM", "NOW", "QCOM", "ZETA"]
EXCHANGES = ["NASDAQ", "NYSE", "AMEX", "NYSEARCA", "BATS", "OTC"]
SCANNER_URL = "https://scanner.tradingview.com/america/scan"
BASELINE_FIELDS = ["name", "description", "close", "currency"]
CANDIDATE_FIELDS = [
    "analyst_rating",
    "analyst_rating_count",
    "analyst_rating_strong_buy",
    "analyst_rating_buy",
    "analyst_rating_hold",
    "analyst_rating_neutral",
    "analyst_rating_sell",
    "analyst_rating_strong_sell",
    "number_of_analysts",
    "target_price_average",
    "target_price_high",
    "target_price_low",
    "target_price_median",
    "price_target_mean",
    "price_target_average",
    "price_target_high",
    "price_target_low",
    "recommendation_mark",
    "recommendation_mean",
]

HEADERS_BASE = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Referer": "https://www.tradingview.com/",
}
JSON_HEADERS = {
    **HEADERS_BASE,
    "Accept": "application/json,text/plain,*/*",
    "Content-Type": "application/json",
    "Origin": "https://www.tradingview.com",
}
HTML_HEADERS = {
    **HEADERS_BASE,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def load_symbols() -> list[str]:
    found: list[str] = []
    if WATCHLIST.exists():
        with WATCHLIST.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                market = (row.get("market") or row.get("region") or "").strip().upper()
                symbol = (row.get("symbol") or row.get("ticker") or row.get("code") or "").strip().upper()
                if symbol and (market == "US" or symbol in PRIORITY):
                    found.append(symbol)
    ordered: list[str] = []
    for s in PRIORITY:
        if (not found or s in found) and s not in ordered:
            ordered.append(s)
    for s in found:
        if s not in ordered:
            ordered.append(s)
    return ordered[:8]


def post_scanner(tickers: list[str], columns: list[str], ignore_unknown: bool) -> tuple[int | None, Any, str | None]:
    payload = {
        "symbols": {"tickers": tickers, "query": {"types": []}},
        "columns": columns,
        "ignore_unknown_fields": ignore_unknown,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(SCANNER_URL, data=data, headers=JSON_HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(text), None
            except json.JSONDecodeError:
                return resp.status, text[:1200], "json_decode_error"
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:1200]
        return e.code, None, f"HTTPError {e.code}: {body}"
    except Exception as e:  # noqa: BLE001
        return None, None, f"{type(e).__name__}: {e}"


def get_text(url: str) -> tuple[int | None, str, str | None]:
    req = urllib.request.Request(url, headers=HTML_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:1200]
        return e.code, body, f"HTTPError {e.code}"
    except Exception as e:  # noqa: BLE001
        return None, "", f"{type(e).__name__}: {e}"


def extract_data(obj: Any, columns: list[str]) -> tuple[dict[str, Any], int]:
    if not isinstance(obj, dict):
        return {}, 0
    data = obj.get("data") or []
    if not data:
        return {}, 0
    values = data[0].get("d") or []
    returned = dict(zip(columns, values))
    return returned, len(data)


def find_best_tv_symbol(symbol: str) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for exch in EXCHANGES:
        tvsym = f"{exch}:{symbol}"
        status, obj, err = post_scanner([tvsym], BASELINE_FIELDS, ignore_unknown=False)
        returned, rows = extract_data(obj, BASELINE_FIELDS)
        non_null = [k for k, v in returned.items() if v is not None]
        attempt = {
            "tv_symbol": tvsym,
            "status": status,
            "error": err,
            "rows": rows,
            "returned": returned,
            "non_null_fields": non_null,
        }
        attempts.append(attempt)
        if rows and non_null:
            return {"symbol": symbol, "best": attempt, "attempts": attempts}
        time.sleep(0.15)
    return {"symbol": symbol, "best": None, "attempts": attempts}


def probe_fields(best_symbols: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tvsym in best_symbols:
        symbol = tvsym.split(":", 1)[-1]
        field_rows: list[dict[str, Any]] = []
        valid_fields: list[str] = []
        for field in CANDIDATE_FIELDS:
            columns = BASELINE_FIELDS + [field]
            status, obj, err = post_scanner([tvsym], columns, ignore_unknown=False)
            returned, data_rows = extract_data(obj, columns)
            value = returned.get(field)
            ok = status == 200 and data_rows > 0 and err is None
            if ok:
                valid_fields.append(field)
            field_rows.append({
                "field": field,
                "http_status": status,
                "error": err,
                "rows": data_rows,
                "value": value,
                "value_present": value is not None,
            })
            time.sleep(0.12)
        combined_columns = BASELINE_FIELDS + valid_fields
        status, obj, err = post_scanner([tvsym], combined_columns, ignore_unknown=True)
        returned, data_rows = extract_data(obj, combined_columns)
        visible = {k: v for k, v in returned.items() if v is not None}
        rows.append({
            "symbol": symbol,
            "tv_symbol": tvsym,
            "valid_candidate_fields": valid_fields,
            "fields": field_rows,
            "combined_http_status": status,
            "combined_error": err,
            "combined_rows": data_rows,
            "combined_non_null": visible,
        })
    return rows


def compact_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def keyword_snippets(text: str) -> list[str]:
    snippets: list[str] = []
    patterns = [
        "Average price target",
        "Price target",
        "Analyst rating",
        "Strong Buy",
        "Buy",
        "Hold",
        "Sell",
        "target_price",
        "analyst",
        "recommendation",
    ]
    for pat in patterns:
        m = re.search(re.escape(pat), text, re.I)
        if m:
            start = max(0, m.start() - 180)
            end = min(len(text), m.end() + 320)
            snippets.append(compact_space(text[start:end])[:650])
    dedup: list[str] = []
    for s in snippets:
        if s not in dedup:
            dedup.append(s)
    return dedup[:8]


def probe_forecast(best_symbols: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    paths = ["forecast/", "forecast-price-target/"]
    for tvsym in best_symbols[:5]:
        exchange, symbol = tvsym.split(":", 1)
        for path in paths:
            urls = [
                f"https://www.tradingview.com/symbols/{exchange}-{symbol}/{path}",
                f"https://www.tradingview.com/symbols/{symbol}/{path}",
            ]
            for url in urls:
                status, text, err = get_text(url)
                title = ""
                m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
                if m:
                    title = compact_space(html.unescape(m.group(1)))[:180]
                rows.append({
                    "tv_symbol": tvsym,
                    "url": url,
                    "http_status": status,
                    "error": err,
                    "length": len(text),
                    "title": title,
                    "keyword_hits": keyword_snippets(text),
                })
                time.sleep(0.15)
    return rows


def esc(x: Any) -> str:
    if isinstance(x, str):
        return html.escape(x)
    return html.escape(json.dumps(x, ensure_ascii=False))


def write_reports(symbols: list[str], baseline: list[dict[str, Any]], field_probe: list[dict[str, Any]], forecast: list[dict[str, Any]]) -> None:
    best_symbols = [b["best"]["tv_symbol"] for b in baseline if b.get("best")]
    valid_field_union: list[str] = []
    non_null_union: list[str] = []
    for row in field_probe:
        for field in row.get("valid_candidate_fields") or []:
            if field not in valid_field_union:
                valid_field_union.append(field)
        for field in (row.get("combined_non_null") or {}).keys():
            if field not in non_null_union:
                non_null_union.append(field)
    status = {
        "status": "ok",
        "generated_at_jst": NOW.isoformat(),
        "symbols_tested": symbols,
        "best_tv_symbols": best_symbols,
        "baseline_success_symbols": len(best_symbols),
        "candidate_fields_tested": len(CANDIDATE_FIELDS),
        "valid_candidate_fields_union": valid_field_union,
        "non_null_fields_union": non_null_union,
        "forecast_rows": len(forecast),
        "note": "Diagnostic only. tv_snapshot.json is not modified.",
    }
    full = {"status": status, "baseline": baseline, "field_probe": field_probe, "forecast": forecast}
    ts = NOW.strftime("%Y%m%d_%H%M%S")
    (DOCS / "tv_probe_status_latest.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    (DOCS / "tv_probe_latest.json").write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / f"tv_probe_status_{ts}.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / f"tv_probe_{ts}.json").write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")

    md: list[str] = []
    md.append("# CIS TradingView Probe v2 safe\n")
    md.append(f"生成日時：{NOW.strftime('%Y/%m/%d %H:%M JST')}\n")
    md.append("## 目的\n")
    md.append("TradingView取得失敗の原因を、GitHub Actions上で非破壊診断します。`tv_snapshot.json` は変更しません。\n")
    md.append("## ステータス\n")
    for k, v in status.items():
        md.append(f"- {k}: {v}")
    md.append("\n## Baseline scanner access\n")
    for b in baseline:
        best = b.get("best")
        md.append(f"### {b.get('symbol')}")
        if best:
            md.append(f"- best: {best.get('tv_symbol')}")
            md.append(f"- HTTP: {best.get('status')}")
            md.append(f"- fields: {', '.join(best.get('non_null_fields') or [])}")
            md.append("```json")
            md.append(json.dumps(best.get("returned"), ensure_ascii=False, indent=2))
            md.append("```")
        else:
            md.append("- best: なし")
            for a in b.get("attempts") or []:
                md.append(f"  - {a.get('tv_symbol')}: HTTP {a.get('status')} / {a.get('error') or 'no data'}")
    md.append("\n## Candidate field probe\n")
    for row in field_probe:
        md.append(f"### {row.get('tv_symbol')}")
        md.append(f"- valid fields: {', '.join(row.get('valid_candidate_fields') or []) if row.get('valid_candidate_fields') else 'なし'}")
        md.append(f"- combined HTTP: {row.get('combined_http_status')} / {row.get('combined_error') or 'なし'}")
        md.append("```json")
        md.append(json.dumps(row.get("combined_non_null"), ensure_ascii=False, indent=2))
        md.append("```")
        invalid = [f for f in row.get("fields") or [] if f.get("error")]
        if invalid:
            md.append("- error fields:")
            for f in invalid[:20]:
                md.append(f"  - {f.get('field')}: HTTP {f.get('http_status')} / {f.get('error')}")
    md.append("\n## Forecast page probe\n")
    for r in forecast:
        if r.get("keyword_hits") or r.get("error"):
            md.append(f"### {r.get('url')}")
            md.append(f"- HTTP: {r.get('http_status')}")
            md.append(f"- Error: {r.get('error') or 'なし'}")
            md.append(f"- Title: {r.get('title') or 'なし'}")
            md.append(f"- Length: {r.get('length')}")
            for snip in r.get("keyword_hits") or []:
                md.append(f"> {snip}")
    (DOCS / "tv_probe_latest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    html_parts = [
        "<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>CIS TV Probe</title>",
        "<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;padding:20px;max-width:960px;margin:auto}.card{border:1px solid #ddd;border-radius:14px;padding:16px;margin:16px 0;box-shadow:0 2px 8px #0001}pre{white-space:pre-wrap;word-break:break-word;background:#f6f6f6;padding:12px;border-radius:10px}code{background:#f6f6f6;padding:2px 4px;border-radius:4px}</style>",
        "<a href='../'>CISホームへ戻る</a>",
        "<h1>CIS TradingView Probe v2 safe</h1>",
        f"<p>生成日時：{NOW.strftime('%Y/%m/%d %H:%M JST')}</p>",
        "<h2>ステータス</h2><div class='card'><ul>",
    ]
    for k, v in status.items():
        html_parts.append(f"<li><code>{esc(k)}</code>：{esc(v)}</li>")
    html_parts.append("</ul></div><h2>Baseline scanner access</h2>")
    for b in baseline:
        best = b.get("best")
        html_parts.append(f"<div class='card'><h3>{esc(b.get('symbol'))}</h3>")
        if best:
            html_parts.append(f"<p>best: <b>{esc(best.get('tv_symbol'))}</b> / HTTP {esc(best.get('status'))}</p>")
            html_parts.append(f"<p>fields: {esc(', '.join(best.get('non_null_fields') or []))}</p>")
            html_parts.append(f"<pre>{esc(best.get('returned'))}</pre>")
        else:
            html_parts.append("<p>best: なし</p><ul>")
            for a in b.get("attempts") or []:
                html_parts.append(f"<li>{esc(a.get('tv_symbol'))}: HTTP {esc(a.get('status'))} / {esc(a.get('error') or 'no data')}</li>")
            html_parts.append("</ul>")
        html_parts.append("</div>")
    html_parts.append("<h2>Candidate field probe</h2>")
    for row in field_probe:
        html_parts.append(f"<div class='card'><h3>{esc(row.get('tv_symbol'))}</h3>")
        html_parts.append(f"<p>valid fields: {esc(', '.join(row.get('valid_candidate_fields') or []) if row.get('valid_candidate_fields') else 'なし')}</p>")
        html_parts.append(f"<p>combined HTTP: {esc(row.get('combined_http_status'))} / {esc(row.get('combined_error') or 'なし')}</p>")
        html_parts.append(f"<pre>{esc(row.get('combined_non_null'))}</pre></div>")
    html_parts.append("<h2>Forecast page probe</h2>")
    for r in forecast:
        if r.get("keyword_hits") or r.get("error"):
            html_parts.append(f"<div class='card'><h3>{esc(r.get('url'))}</h3><ul><li>HTTP：{esc(r.get('http_status'))}</li><li>Error：{esc(r.get('error') or 'なし')}</li><li>Title：{esc(r.get('title') or 'なし')}</li><li>Length：{esc(r.get('length'))}</li></ul>")
            for snip in r.get("keyword_hits") or []:
                html_parts.append(f"<blockquote>{esc(snip)}</blockquote>")
            html_parts.append("</div>")
    (DOCS / "tv_probe_latest.html").write_text("\n".join(html_parts) + "\n", encoding="utf-8")


def main() -> None:
    symbols = load_symbols()
    baseline = [find_best_tv_symbol(s) for s in symbols]
    best_symbols = [b["best"]["tv_symbol"] for b in baseline if b.get("best")]
    field_probe = probe_fields(best_symbols[:5])
    forecast = probe_forecast(best_symbols[:5])
    write_reports(symbols, baseline, field_probe, forecast)


if __name__ == "__main__":
    main()
