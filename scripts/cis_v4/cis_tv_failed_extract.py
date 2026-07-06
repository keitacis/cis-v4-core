#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CIS v4 TradingView failed extract report.

Diagnostic-only helper:
- Reads the latest TV Monthly Refresh JSON.
- Extracts failed/manual-check TradingView symbols.
- Writes mobile-friendly HTML/MD/JSON reports.
- Does not modify tv_snapshot.json, master data, or Apply workflows.
"""

from __future__ import annotations

import datetime as _dt
import html
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
DOCS_LATEST = ROOT / "docs" / "v4" / "latest"
OUTPUT_DIR = ROOT / "output"
SOURCE_CANDIDATES = [
    DOCS_LATEST / "tv_monthly_refresh_latest.json",
    OUTPUT_DIR / "tv_monthly_refresh_latest.json",
]

ETF_SYMBOLS = {
    "EWY",
}

CORE_MISSING_ORDER = ["rating", "avg_target_price", "analyst_count"]


def now_jst() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=9)))


def format_jst(dt: _dt.datetime) -> str:
    return dt.strftime("%Y/%m/%d %H:%M JST")


def load_source() -> Tuple[Path, Dict[str, Any]]:
    for path in SOURCE_CANDIDATES:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return path, json.load(f)
    raise FileNotFoundError(
        "tv_monthly_refresh_latest.json not found in docs/v4/latest or output"
    )


def iter_failed_lists(obj: Any, path: str = "") -> Iterable[Tuple[str, List[Dict[str, Any]]]]:
    """Find likely failed lists recursively without assuming a fixed schema."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            p = f"{path}.{key}" if path else key
            if key in {"failed", "failures", "manual_candidates", "manual_check", "failed_candidates"}:
                if isinstance(value, list) and all(isinstance(x, dict) for x in value):
                    yield p, value
            yield from iter_failed_lists(value, p)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from iter_failed_lists(item, f"{path}[{i}]")


def get_failed_items(data: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    if isinstance(data.get("failed"), list):
        return "failed", list(data.get("failed") or [])

    candidates = list(iter_failed_lists(data))
    # Prefer a list where entries have symbol/key/reason.
    scored: List[Tuple[int, str, List[Dict[str, Any]]]] = []
    for path, items in candidates:
        score = 0
        if items:
            sample = items[0]
            for k in ("symbol", "key", "reason", "diagnostic"):
                if k in sample:
                    score += 1
        if "failed" in path:
            score += 2
        scored.append((score, path, items))

    if not scored:
        return "not_found", []

    scored.sort(key=lambda x: (x[0], len(x[2])), reverse=True)
    _, path, items = scored[0]
    return path, items


def _first(d: Dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in d and d[key] not in (None, ""):
            return d[key]
    return default


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def extract_attempts(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    diag = item.get("diagnostic") or {}
    attempts = diag.get("scanner_attempts")
    if isinstance(attempts, list):
        return [a for a in attempts if isinstance(a, dict)]

    # Some future schema may store attempts elsewhere.
    for key in ("attempts", "scanner", "resolution_attempts"):
        value = diag.get(key)
        if isinstance(value, list):
            return [a for a in value if isinstance(a, dict)]
    return []


def extract_forecast_errors(item: Dict[str, Any], attempts: List[Dict[str, Any]]) -> Dict[str, str]:
    errors: Dict[str, str] = {}

    diag = item.get("diagnostic") or {}
    top_errors = diag.get("forecast_count_errors")
    if isinstance(top_errors, dict):
        errors.update({str(k): str(v) for k, v in top_errors.items()})

    for att in attempts:
        for key in ("forecast_count_errors", "forecast_errors"):
            value = att.get(key)
            if isinstance(value, dict):
                for ex, msg in value.items():
                    errors[str(ex)] = str(msg)

        # Some attempts may use explicit URL/status fields.
        ex = att.get("exchange") or att.get("tv_exchange")
        err = att.get("forecast_error") or att.get("forecast_status")
        if ex and err and str(err).lower() not in {"ok", "success", "200"}:
            errors[str(ex)] = str(err)

    return errors


def extract_missing(item: Dict[str, Any], attempts: List[Dict[str, Any]]) -> List[str]:
    missing: List[str] = []
    diag = item.get("diagnostic") or {}

    for source in [item, diag, *(attempts or [])]:
        value = source.get("missing") if isinstance(source, dict) else None
        for entry in _as_list(value):
            if isinstance(entry, str) and entry not in missing:
                missing.append(entry)

    reason = str(item.get("reason") or "")
    for key in CORE_MISSING_ORDER:
        if key in reason and key not in missing:
            missing.append(key)

    # Normalize old wording into the report vocabulary.
    normalized = []
    for m in missing:
        m = str(m)
        if m in {"avg_target_price", "target_price", "average_target_price"}:
            m = "avg_target_price"
        if m not in normalized:
            normalized.append(m)
    return normalized


def extract_exchanges(item: Dict[str, Any], attempts: List[Dict[str, Any]]) -> List[str]:
    exchanges: List[str] = []
    for source in [item, *(attempts or [])]:
        if isinstance(source, dict):
            ex = source.get("exchange") or source.get("tv_exchange")
            if ex and str(ex) not in exchanges:
                exchanges.append(str(ex))
    reason = str(item.get("reason") or "")
    for ex in re.findall(r"\b(NASDAQ|NYSE|AMEX|NYSEARCA|BATS|OTC)\b", reason):
        if ex not in exchanges:
            exchanges.append(ex)
    return exchanges


def infer_symbol(item: Dict[str, Any]) -> str:
    key = str(item.get("key") or "")
    symbol = str(item.get("symbol") or "")
    if symbol:
        return symbol
    m = re.match(r"^[A-Z]+:([A-Z0-9.\-]+)$", key)
    if m:
        return m.group(1)
    return key or "UNKNOWN"


def infer_key(item: Dict[str, Any], symbol: str) -> str:
    return str(item.get("key") or (f"US:{symbol}" if symbol else "UNKNOWN"))


def classify(item: Dict[str, Any], symbol: str, missing: List[str], forecast_errors: Dict[str, str]) -> Tuple[str, str]:
    reason = str(item.get("reason") or "")
    reason_l = reason.lower()
    errors_text = " ".join(forecast_errors.values()).lower()

    if symbol in ETF_SYMBOLS or "etf" in reason_l or "fund" in reason_l:
        return ("ETF/対象外候補", "ETFやファンド系はTradingViewの個別株アナリスト予想対象外の可能性があります。")

    if "httperror 403" in errors_text or "http 403" in errors_text or " 403" in errors_text:
        return ("403/アクセス制限候補", "forecast page側が403です。GitHub Actionsからのアクセス制限、またはTradingView側のページ制御の可能性があります。")

    if "httperror 404" in errors_text or "http 404" in errors_text or " 404" in errors_text:
        return ("404/シンボル経路候補", "試したforecast URLが404です。取引所候補の見直し、またはTradingViewにforecastページがない可能性があります。")

    if set(CORE_MISSING_ORDER).issubset(set(missing)):
        return ("カバレッジなし候補", "scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。")

    return ("要手動確認", "失敗理由だけでは追加取得可否を断定できません。")


def summarize_http(errors: Dict[str, str]) -> str:
    if not errors:
        return "なし"
    return " / ".join(f"{ex}: {msg}" for ex, msg in errors.items())


def html_page(title: str, generated: str, source_rel: str, records: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    status_counts = summary["status_counts"]
    http_counts = summary["http_counts"]
    missing_counts = summary["missing_counts"]

    def esc(x: Any) -> str:
        return html.escape(str(x), quote=True)

    cards = []
    for idx, r in enumerate(records, 1):
        err_lines = "".join(
            f"<li><code>{esc(ex)}</code>: {esc(msg)}</li>"
            for ex, msg in (r.get("forecast_errors") or {}).items()
        ) or "<li>なし</li>"
        missing = ", ".join(r.get("missing") or []) or "不明"
        exchanges = ", ".join(r.get("exchanges") or []) or "不明"
        cards.append(f"""
        <section class="card">
          <h2>{idx}. {esc(r["key"])} {esc(r.get("name") or "")}</h2>
          <p><strong>判定候補：</strong>{esc(r["classification"])}</p>
          <p><strong>次の見方：</strong>{esc(r["classification_note"])}</p>
          <p><strong>不足項目：</strong><code>{esc(missing)}</code></p>
          <p><strong>試した取引所：</strong><code>{esc(exchanges)}</code></p>
          <p><strong>理由：</strong>{esc(r.get("reason") or "")}</p>
          <details>
            <summary>forecast / scanner詳細</summary>
            <ul>{err_lines}</ul>
            <pre>{esc(json.dumps(r.get("diagnostic_compact") or {}, ensure_ascii=False, indent=2))}</pre>
          </details>
        </section>
        """)

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
  margin: 0;
  padding: 20px;
  color: #111;
  background: #fafafa;
}}
a {{ color: #0645ad; }}
h1 {{ font-size: 2rem; margin-top: 24px; }}
h2 {{ font-size: 1.35rem; }}
.card {{
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 16px;
  margin: 16px 0;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}}
.summary {{
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 16px;
}}
code, pre {{
  background: #f3f3f3;
  border-radius: 8px;
  padding: 2px 5px;
}}
pre {{
  overflow-x: auto;
  padding: 12px;
  white-space: pre-wrap;
}}
.badge {{
  display: inline-block;
  background: #f2f2f2;
  border-radius: 999px;
  padding: 4px 10px;
  margin: 3px;
}}
</style>
</head>
<body>
<p><a href="../">CISホームへ戻る</a></p>
<h1>{esc(title)}</h1>
<p>生成日時：{esc(generated)}</p>
<div class="summary">
  <h2>これは何をするレポートか</h2>
  <ul>
    <li>Monthly Refreshで取得失敗・手動確認になった銘柄だけを抽出します。</li>
    <li>このレポートは診断専用です。<code>tv_snapshot.json</code>、Master、Apply、Daily/Weekly/Buy Alertは変更しません。</li>
    <li>残件を「追加取得」「対象外」「カバレッジなし」に分けるための材料です。</li>
  </ul>
  <h2>ステータス</h2>
  <ul>
    <li>元JSON：<code>{esc(source_rel)}</code></li>
    <li>失敗抽出件数：{len(records)}件</li>
  </ul>
  <h2>判定候補サマリー</h2>
  <p>{" ".join(f'<span class="badge">{esc(k)}：{v}件</span>' for k, v in status_counts.items())}</p>
  <h2>HTTPエラーサマリー</h2>
  <p>{" ".join(f'<span class="badge">{esc(k)}：{v}件</span>' for k, v in http_counts.items()) or "なし"}</p>
  <h2>不足項目サマリー</h2>
  <p>{" ".join(f'<span class="badge">{esc(k)}：{v}件</span>' for k, v in missing_counts.items()) or "なし"}</p>
</div>
<h1>取得失敗・手動確認候補</h1>
{''.join(cards)}
</body>
</html>
"""


def md_page(title: str, generated: str, source_rel: str, records: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        f"# {title}",
        "",
        f"生成日時：{generated}",
        "",
        "## これは何をするレポートか",
        "",
        "- Monthly Refreshで取得失敗・手動確認になった銘柄だけを抽出します。",
        "- 診断専用です。tv_snapshot.json、Master、Apply、Daily/Weekly/Buy Alertは変更しません。",
        "- 残件を「追加取得」「対象外」「カバレッジなし」に分けるための材料です。",
        "",
        "## ステータス",
        "",
        f"- 元JSON：`{source_rel}`",
        f"- 失敗抽出件数：{len(records)}件",
        "",
        "## 判定候補サマリー",
        "",
    ]
    for k, v in summary["status_counts"].items():
        lines.append(f"- {k}：{v}件")

    lines.extend(["", "## HTTPエラーサマリー", ""])
    if summary["http_counts"]:
        for k, v in summary["http_counts"].items():
            lines.append(f"- {k}：{v}件")
    else:
        lines.append("- なし")

    lines.extend(["", "## 不足項目サマリー", ""])
    if summary["missing_counts"]:
        for k, v in summary["missing_counts"].items():
            lines.append(f"- {k}：{v}件")
    else:
        lines.append("- なし")

    lines.extend(["", "## 取得失敗・手動確認候補", ""])
    for i, r in enumerate(records, 1):
        lines.extend([
            f"### {i}. {r['key']} {r.get('name') or ''}",
            "",
            f"- 判定候補：{r['classification']}",
            f"- 次の見方：{r['classification_note']}",
            f"- 不足項目：`{', '.join(r.get('missing') or []) or '不明'}`",
            f"- 試した取引所：`{', '.join(r.get('exchanges') or []) or '不明'}`",
            f"- 理由：{r.get('reason') or ''}",
            f"- forecast errors：{summarize_http(r.get('forecast_errors') or {})}",
            "",
        ])
    return "\n".join(lines) + "\n"


def compact_diag(item: Dict[str, Any], attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
    diag = item.get("diagnostic") or {}
    compact = {}
    for key in ("distribution_status", "distribution_total", "recommendation_mark_raw",
                "price_target_high", "price_target_low", "count_source", "forecast_count_url"):
        if key in diag:
            compact[key] = diag.get(key)
    compact["attempts"] = []
    for att in attempts:
        compact["attempts"].append({
            "exchange": att.get("exchange"),
            "resolution_status": att.get("resolution_status"),
            "missing": att.get("missing"),
            "rating_field": att.get("rating_field"),
            "target_field": att.get("target_field"),
            "count_source": att.get("count_source"),
            "forecast_count_errors": att.get("forecast_count_errors"),
        })
    return compact


def main() -> None:
    source_path, data = load_source()
    failed_path, failed_items = get_failed_items(data)

    records: List[Dict[str, Any]] = []
    status_counter: Counter[str] = Counter()
    http_counter: Counter[str] = Counter()
    missing_counter: Counter[str] = Counter()

    for item in failed_items:
        if not isinstance(item, dict):
            continue
        symbol = infer_symbol(item)
        key = infer_key(item, symbol)
        name = _first(item, ["name", "company", "description", "display_name"], "")
        attempts = extract_attempts(item)
        missing = extract_missing(item, attempts)
        forecast_errors = extract_forecast_errors(item, attempts)
        exchanges = extract_exchanges(item, attempts)
        classification, note = classify(item, symbol, missing, forecast_errors)

        status_counter[classification] += 1
        for m in missing:
            missing_counter[m] += 1
        for msg in forecast_errors.values():
            m = re.search(r"(HTTPError|HTTP|status)[^\d]*(\d{3})", str(msg), flags=re.I)
            if m:
                http_counter[m.group(2)] += 1
            elif "403" in str(msg):
                http_counter["403"] += 1
            elif "404" in str(msg):
                http_counter["404"] += 1

        records.append({
            "key": key,
            "symbol": symbol,
            "name": name,
            "reason": item.get("reason"),
            "missing": missing,
            "exchanges": exchanges,
            "forecast_errors": forecast_errors,
            "classification": classification,
            "classification_note": note,
            "diagnostic_compact": compact_diag(item, attempts),
        })

    records.sort(key=lambda r: (r["classification"], r["symbol"]))

    generated_dt = now_jst()
    generated = format_jst(generated_dt)
    title = "CIS TradingView失敗23件 抽出レポート"

    summary = {
        "status_counts": dict(status_counter),
        "http_counts": dict(http_counter),
        "missing_counts": dict(missing_counter),
        "failed_path": failed_path,
        "source_path": str(source_path.relative_to(ROOT)),
        "generated_at_jst": generated_dt.isoformat(),
    }

    report = {
        "status": "ok",
        "generated_at_jst": generated_dt.isoformat(),
        "source_path": str(source_path.relative_to(ROOT)),
        "failed_json_path": failed_path,
        "failed_count": len(records),
        "summary": summary,
        "failed": records,
        "note": "Diagnostic only. tv_snapshot.json is not modified.",
    }

    DOCS_LATEST.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    html_out = html_page(title, generated, str(source_path.relative_to(ROOT)), records, summary)
    md_out = md_page(title, generated, str(source_path.relative_to(ROOT)), records, summary)

    (DOCS_LATEST / "tv_failed_latest.html").write_text(html_out, encoding="utf-8")
    (DOCS_LATEST / "tv_failed_latest.md").write_text(md_out, encoding="utf-8")
    (DOCS_LATEST / "tv_failed_latest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    stamp = generated_dt.strftime("%Y%m%d_%H%M%S")
    (OUTPUT_DIR / f"tv_failed_{stamp}.html").write_text(html_out, encoding="utf-8")
    (OUTPUT_DIR / f"tv_failed_{stamp}.md").write_text(md_out, encoding="utf-8")
    (OUTPUT_DIR / f"tv_failed_{stamp}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Generated TV failed extract report: {len(records)} failed records")
    print(f"Source: {source_path.relative_to(ROOT)}")
    print("Docs:")
    print(f"  {DOCS_LATEST / 'tv_failed_latest.html'}")
    print(f"  {DOCS_LATEST / 'tv_failed_latest.md'}")
    print(f"  {DOCS_LATEST / 'tv_failed_latest.json'}")


if __name__ == "__main__":
    main()
