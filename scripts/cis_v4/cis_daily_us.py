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

STEM = "daily_us"
TITLE = "CIS 米国株日次騰落"
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


def main() -> int:
    global TV_STALE_DAYS
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        items = [x for x in load_watchlist(True) if x.market == "US"]
        tv_map = load_tv_snapshot()
        rows: List[Dict[str, Any]] = []
        for item in items:
            p = fetch_price(item, weekly=False)
            tv = tv_map.get(item.key)
            updated_at = tv.updated_at if tv else None
            rows.append({
                "symbol": item.symbol,
                "market": item.market,
                "name": item.name,
                "description": item.description or item.notes,
                "latest_price": p.latest_price,
                "daily_change": p.daily_change,
                "daily_pct": p.daily_pct,
                "latest_date": p.latest_date,
                "previous_date": p.previous_date,
                "market_closed": p.market_closed,
                "stale_price": p.stale_price,
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
        rows.sort(key=lambda r: (1, 0) if r["daily_pct"] is None else (0, -r["daily_pct"]))
        total = len(items)
        price_success = sum(1 for r in rows if r.get("daily_pct") is not None)
        price_missing = max(0, total - price_success)
        closed = sum(1 for r in rows if r.get("market_closed"))
        tv_count = sum(1 for r in rows if r.get("tv_coverage_status") in {"covered", "no_coverage", "not_applicable"})
        tv_missing = [r["symbol"] for r in rows if not r.get("tv_coverage_status")]
        tv_no_coverage = [r["symbol"] for r in rows if r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in rows if r.get("tv_coverage_status") == "not_applicable"]
        stale_tv = [r["symbol"] for r in rows if r.get("tv_coverage_status") and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)]
        warnings = []
        if total and price_success == 0:
            warnings.append("米国株価格が全銘柄で未取得です。")
        elif total and closed == total:
            warnings.append("米国市場は休場または価格更新前の可能性があります。古い日付を当日更新として扱いません。")
        else:
            if price_missing:
                warnings.append(f"価格未取得の銘柄があります：{price_missing}銘柄")
            if closed:
                warnings.append(f"価格日付が古い銘柄があります：{closed}銘柄")
        if tv_missing:
            warnings.append(f"TradingViewスナップショット未設定：{len(tv_missing)}銘柄")
        if stale_tv:
            warnings.append(f"TradingViewスナップショットの鮮度注意：{len(stale_tv)}銘柄")
        if total and price_success == 0:
            level = "error"
        elif total and closed == total:
            level = "market_closed"
        else:
            level = "partial" if warnings else "ok"
        status = {
            "status": level,
            "generated_at_jst": timestamp_jst(),
            "price_success_count": price_success,
            "price_missing_count": price_missing,
            "us_count": total,
            "market_closed_count": closed,
            "tv_saved_or_explicit_count": tv_count,
            "tv_missing_count": len(tv_missing),
            "tv_no_coverage_count": len(tv_no_coverage),
            "tv_not_applicable_count": len(tv_not_applicable),
            "tv_stale_or_unknown_count": len(stale_tv),
            "tv_missing_symbols": tv_missing,
            "tv_stale_or_unknown_symbols": stale_tv,
            "warnings": warnings,
        }
        lines = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += ["## ステータス", "", f"- 価格取得成功：{price_success}/{total}", f"- 価格未取得：{price_missing}", f"- 休場/日付注意：{closed}", f"- TradingView保存/対象外明示：{tv_count}/{total}", f"- TradingView未設定：{len(tv_missing)}", f"- カバレッジなし：{len(tv_no_coverage)}", f"- 対象外：{len(tv_not_applicable)}", f"- TradingView鮮度注意：{len(stale_tv)}", ""]
        if warnings:
            lines += ["## 注意", ""] + [f"- ⚠️ {w}" for w in warnings] + [""]
        lines += ["## 米国株｜前日比順", ""]
        for i, r in enumerate(rows, 1):
            ac = r.get("tv_analyst_count")
            cov = r.get("tv_coverage_status")
            na = tv_na_text(cov)
            lines += [
                f"### {i}. {r['symbol']}｜{r.get('description') or r.get('name')}",
                "",
                f"- 価格日付：{r.get('latest_date') or '未取得'}",
                f"- 終値：{fmt_price(r.get('latest_price'), 'US')}",
                f"- 前日比：{fmt_change(r.get('daily_change'), 'US')}",
                f"- 前日比％：**{fmt_pct(r.get('daily_pct'))}**",
                f"- TradingView区分：{tv_status_label(cov)}",
                f"- TradingViewレーティング：{r.get('tv_rating') or na}",
                f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",
                f"- 平均目標株価：{fmt_price(r.get('tv_avg_target_price'), 'US') if cov == 'covered' else na}",
                f"- 現在価格→平均目標株価乖離率：{fmt_pct(r.get('tv_upside_pct')) if cov == 'covered' else na}",
                f"- TV更新：{r.get('tv_freshness')}",
            ]
            if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:
                lines.append(f"- TVメモ：{r.get('tv_reason')}")
            if r.get("market_closed"):
                lines.append("- 注意：休場または価格更新前の可能性あり")
            lines.append("")
        write_report(STEM, "\n".join(lines), {"status": status, "rows": rows}, status)
        return 1 if level == "error" else 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
