#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from cis_core import (
    JST,
    fmt_change,
    fmt_pct,
    fmt_price,
    load_tv_snapshot,
    load_watchlist,
    get_tv_snapshot_stale_days,
    now_jst,
    fetch_price,
    timestamp_jst,
    tv_upside,
    write_error_report,
    write_report,
)

STEM = "weekly_performance"
TITLE = "CIS 週間騰落"
TV_STALE_DAYS = 45  # fallback; real value is loaded from data/cis_settings.json in main()


def tv_age_days(updated_at: Optional[str]) -> Optional[float]:
    if not updated_at:
        return None
    try:
        dt = datetime.fromisoformat(str(updated_at))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        return (now_jst() - dt.astimezone(JST)).total_seconds() / 86400
    except Exception:
        return None


def tv_freshness_label(updated_at: Optional[str]) -> str:
    age = tv_age_days(updated_at)
    if age is None:
        return "鮮度不明"
    if age > TV_STALE_DAYS:
        return f"古い可能性あり（{age:.0f}日前）"
    return f"{age:.0f}日前更新"


def tv_status_label(status: Optional[str]) -> str:
    if status == "covered":
        return "アナリスト予想あり"
    if status == "no_coverage":
        return "カバレッジなし"
    if status == "not_applicable":
        return "対象外"
    return "未設定"


def tv_na_text(status: Optional[str]) -> str:
    if status == "no_coverage":
        return "カバレッジなし"
    if status == "not_applicable":
        return "対象外"
    return "未取得"


def build_rows() -> List[Dict[str, Any]]:
    items = load_watchlist(active_only=True)
    tv_map = load_tv_snapshot()
    rows: List[Dict[str, Any]] = []
    for item in items:
        p = fetch_price(item, weekly=True)
        tv = tv_map.get(item.key) if item.market == "US" else None
        updated_at = tv.updated_at if tv else None
        rows.append({
            "symbol": item.symbol,
            "market": item.market,
            "name": item.name,
            "description": item.name if item.market == "JP" else (item.description or item.notes),
            "latest_price": p.latest_price,
            "weekly_base_price": p.weekly_base_price,
            "weekly_change": p.weekly_change,
            "weekly_pct": p.weekly_pct,
            "price_source": p.source,
            "price_error": p.error,
            "tv_coverage_status": tv.coverage_status if tv else None,
            "tv_reason": tv.reason if tv else "",
            "tv_rating": tv.rating if tv else None,
            "tv_analyst_count": tv.analyst_count if tv else None,
            "tv_avg_target_price": tv.avg_target_price if tv else None,
            "tv_upside_pct": tv_upside(p.latest_price, tv),
            "tv_updated_at": updated_at,
            "tv_age_days": tv_age_days(updated_at),
            "tv_freshness": tv_freshness_label(updated_at),
        })
    rows.sort(key=lambda r: (1, 0) if r["weekly_pct"] is None else (0, -r["weekly_pct"]))
    return rows


def render(rows: List[Dict[str, Any]], status: Dict[str, Any]) -> str:
    us = [r for r in rows if r["market"] == "US"]
    jp = [r for r in rows if r["market"] == "JP"]
    lines = [
        f"# {TITLE}",
        "",
        f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
        "",
        "## ステータス",
        "",
        f"- 対象銘柄：{len(rows)}",
        f"- 価格取得成功：{status.get('price_success_count')}/{len(rows)}",
        f"- 価格未取得：{status.get('price_missing_count', 0)}",
        f"- 米国株TV保存/対象外明示：{status.get('us_tv_saved_or_explicit_count')}/{status.get('us_count')}",
        f"- 米国株TV未設定：{status.get('us_tv_missing_count')}",
        f"- 米国株カバレッジなし：{status.get('us_tv_no_coverage_count')}",
        f"- 米国株TV対象外：{status.get('us_tv_not_applicable_count')}",
        f"- 米国株TV鮮度注意：{status.get('us_tv_stale_or_unknown_count')}",
        "",
    ]
    for w in status.get("warnings", []):
        lines.append(f"- ⚠️ {w}")
    if status.get("warnings"):
        lines.append("")

    lines += ["## 米国株・米国ETF｜週間騰落率順", ""]
    if not us:
        lines += ["対象なし", ""]
    for i, r in enumerate(us, 1):
        title = f"{r['symbol']}｜{r.get('description') or r.get('name')}"
        ac = r.get("tv_analyst_count")
        cov = r.get("tv_coverage_status")
        na = tv_na_text(cov)
        lines += [
            f"### {i}. {title}",
            "",
            f"- 週間騰落率：**{fmt_pct(r.get('weekly_pct'))}**",
            f"- 週間価格差：{fmt_change(r.get('weekly_change'), 'US')}",
            f"- TradingView区分：{tv_status_label(cov)}",
            f"- TradingViewレーティング：{r.get('tv_rating') or na}",
            f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",
            f"- 平均目標株価：{fmt_price(r.get('tv_avg_target_price'), 'US') if cov == 'covered' else na}",
            f"- 現在価格→平均目標株価乖離率：{fmt_pct(r.get('tv_upside_pct')) if cov == 'covered' else na}",
            f"- TV更新：{r.get('tv_freshness')}",
        ]
        if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:
            lines.append(f"- TVメモ：{r.get('tv_reason')}")
        lines.append("")

    lines += ["## 日本株｜週間騰落率順", ""]
    if not jp:
        lines += ["対象なし", ""]
    for i, r in enumerate(jp, 1):
        title = f"{r['symbol']}｜{r.get('description') or r.get('name')}"
        lines += [
            f"### {i}. {title}",
            "",
            f"- 週間騰落率：**{fmt_pct(r.get('weekly_pct'))}**",
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    global TV_STALE_DAYS
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        rows = build_rows()
        total = len(rows)
        price_success = sum(1 for r in rows if r.get("weekly_pct") is not None)
        price_missing = max(0, total - price_success)
        us_count = sum(1 for r in rows if r["market"] == "US")
        tv_complete_count = sum(
            1 for r in rows
            if r["market"] == "US" and r.get("tv_coverage_status") in {"covered", "no_coverage", "not_applicable"}
        )
        tv_missing = [r["symbol"] for r in rows if r["market"] == "US" and not r.get("tv_coverage_status")]
        tv_no_coverage = [r["symbol"] for r in rows if r["market"] == "US" and r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in rows if r["market"] == "US" and r.get("tv_coverage_status") == "not_applicable"]
        stale_tv = [
            r["symbol"] for r in rows
            if r["market"] == "US" and r.get("tv_coverage_status") and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)
        ]
        warnings = []
        if total and price_success == 0:
            warnings.append("全銘柄の週間価格が未取得です。")
        elif price_missing:
            warnings.append(f"週間価格未取得の銘柄があります：{price_missing}銘柄")
        if tv_missing:
            warnings.append(f"米国株TradingViewスナップショット未設定：{len(tv_missing)}銘柄")
        if stale_tv:
            warnings.append(f"TradingViewスナップショットの鮮度注意：{len(stale_tv)}銘柄")
        level = "error" if total and price_success == 0 else ("partial" if warnings else "ok")
        status = {
            "status": level,
            "generated_at_jst": timestamp_jst(),
            "price_success_count": price_success,
            "price_missing_count": price_missing,
            "watchlist_count": total,
            "us_count": us_count,
            "us_tv_saved_or_explicit_count": tv_complete_count,
            "us_tv_missing_count": len(tv_missing),
            "us_tv_no_coverage_count": len(tv_no_coverage),
            "us_tv_not_applicable_count": len(tv_not_applicable),
            "us_tv_stale_or_unknown_count": len(stale_tv),
            "us_tv_missing_symbols": tv_missing,
            "us_tv_stale_or_unknown_symbols": stale_tv,
            "warnings": warnings,
        }
        write_report(STEM, render(rows, status), {"status": status, "rows": rows}, status)
        return 1 if level == "error" else 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
