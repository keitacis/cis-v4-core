#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from cis_core import (
    JST,
    expected_daily_trade_date,
    fmt_change,
    fmt_pct,
    fmt_price,
    get_tv_snapshot_stale_days,
    load_tv_snapshot,
    load_watchlist,
    now_jst,
    fetch_price,
    timestamp_jst,
    tv_upside,
    write_error_report,
    write_report,
)

STEM = "weekly_performance"
TITLE = "CIS 週間騰落"
TV_STALE_DAYS = 45


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


def tv_na_text(status: Optional[str]) -> str:
    if status == "no_coverage":
        return "カバレッジなし"
    if status == "not_applicable":
        return "対象外"
    return "未取得"


def is_tv_covered(status: Optional[str]) -> bool:
    return status in {"covered", "covered_partial"}


def build_rows() -> List[Dict[str, Any]]:
    items = load_watchlist(active_only=True)
    tv_map = load_tv_snapshot()
    rows: List[Dict[str, Any]] = []
    for item in items:
        p = fetch_price(item, weekly=True)
        tv = tv_map.get(item.key) if item.market == "US" else None
        updated_at = tv.updated_at if tv else None
        expected_date = expected_daily_trade_date(item.market)
        stale_price = bool(p.latest_date and p.latest_date < expected_date)
        rows.append(
            {
                "symbol": item.symbol,
                "market": item.market,
                "name": item.name,
                "description": item.name if item.market == "JP" else (item.description or item.notes),
                "latest_price": p.latest_price,
                "weekly_base_price": p.weekly_base_price,
                "weekly_change": p.weekly_change,
                "weekly_pct": p.weekly_pct,
                "latest_date": p.latest_date,
                "previous_date": p.previous_date,
                "expected_price_date": expected_date,
                "stale_price": stale_price,
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
            }
        )
    rows.sort(key=lambda r: (1, 0) if r["weekly_pct"] is None else (0, -r["weekly_pct"]))
    return rows


def render(rows: List[Dict[str, Any]], status: Dict[str, Any]) -> str:
    stale_rows = [r for r in rows if r.get("stale_price")]
    us = [r for r in rows if r["market"] == "US" and not r.get("stale_price")]
    jp = [r for r in rows if r["market"] == "JP" and not r.get("stale_price")]
    lines = [
        f"# {TITLE}",
        "",
        f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
        f"想定最新価格日付：米国 {status.get('expected_us_price_date')} / 日本 {status.get('expected_jp_price_date')}",
        "",
        "## ステータス",
        "",
        f"- 対象銘柄：{len(rows)}",
        f"- 価格取得成功：{status.get('price_success_count')}/{len(rows)}",
        f"- 価格未取得：{status.get('price_missing_count', 0)}",
        f"- 最新価格日付が古い銘柄：{status.get('price_stale_count', 0)}",
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

    if status.get("status") == "price_stale":
        lines += [
            "## 価格未更新のため週間ランキング非表示",
            "",
            "最新価格日付が全銘柄で想定より古いため、週間騰落ランキングは表示しません。",
            "",
            "### 価格日付が古い銘柄",
            "",
            ", ".join(status.get("price_stale_symbols") or []) if status.get("price_stale_symbols") else "対象なし",
            "",
        ]
        return "\n".join(lines)

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
            f"- 最新価格日付：{r.get('latest_date') or '未取得'}",
            f"- 比較元価格：{fmt_price(r.get('weekly_base_price'), 'US')}",
            f"- 週間騰落率：**{fmt_pct(r.get('weekly_pct'))}**",
            f"- 週間価格差：{fmt_change(r.get('weekly_change'), 'US')}",
        ]
        if is_tv_covered(cov):
            lines += [
                f"- TradingViewレーティング：{r.get('tv_rating') or '未取得'}",
                f"- アナリスト人数：{ac}人" if ac is not None else "- アナリスト人数：未取得",
                f"- 平均目標株価：{fmt_price(r.get('tv_avg_target_price'), 'US')}",
                f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get('tv_upside_pct'))}",
                f"- TV更新：{r.get('tv_freshness')}",
            ]
        elif cov in {"no_coverage", "not_applicable"}:
            lines.append(f"- TradingView：{na}")
            if r.get("tv_reason"):
                lines.append(f"- TVメモ：{r.get('tv_reason')}")
        else:
            lines.append("- TradingView：未取得")
        if r.get("stale_price"):
            lines.append(f"- 注意：最新価格日付が想定より古いです（想定：{r.get('expected_price_date')}）")
        lines.append("")

    lines += ["## 日本株｜週間騰落率順", ""]
    if not jp:
        lines += ["対象なし", ""]
    for i, r in enumerate(jp, 1):
        title = f"{r['symbol']}｜{r.get('description') or r.get('name')}"
        lines += [
            f"### {i}. {title}",
            "",
            f"- 最新価格日付：{r.get('latest_date') or '未取得'}",
            f"- 比較元価格：{fmt_price(r.get('weekly_base_price'), 'JP')}",
            f"- 週間騰落率：**{fmt_pct(r.get('weekly_pct'))}**",
            f"- 週間価格差：{fmt_change(r.get('weekly_change'), 'JP')}",
        ]
        if r.get("stale_price"):
            lines.append(f"- 注意：最新価格日付が想定より古いです（想定：{r.get('expected_price_date')}）")
        lines.append("")
    if stale_rows and status.get("status") != "price_stale":
        lines += ["## 価格日付が古い銘柄（週間ランキング対象外）", ""]
        for r in stale_rows:
            market = r.get("market")
            lines.append(
                f"- {r['symbol']}｜最新価格日付：{r.get('latest_date') or '未取得'}｜想定：{r.get('expected_price_date')}｜週間騰落率：{fmt_pct(r.get('weekly_pct'))}"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    global TV_STALE_DAYS
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        rows = build_rows()
        total = len(rows)
        price_success = sum(1 for r in rows if r.get("weekly_pct") is not None)
        price_missing = max(0, total - price_success)
        price_stale = [r["symbol"] for r in rows if r.get("stale_price")]
        us_count = sum(1 for r in rows if r["market"] == "US")
        expected_us = expected_daily_trade_date("US")
        expected_jp = expected_daily_trade_date("JP")
        tv_complete_count = sum(
            1
            for r in rows
            if r["market"] == "US" and r.get("tv_coverage_status") in {"covered", "covered_partial", "no_coverage", "not_applicable"}
        )
        tv_missing = [r["symbol"] for r in rows if r["market"] == "US" and not r.get("tv_coverage_status")]
        tv_no_coverage = [r["symbol"] for r in rows if r["market"] == "US" and r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in rows if r["market"] == "US" and r.get("tv_coverage_status") == "not_applicable"]
        stale_tv = [
            r["symbol"]
            for r in rows
            if r["market"] == "US"
            and r.get("tv_coverage_status") in {"covered", "covered_partial"}
            and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)
        ]
        warnings: List[str] = []
        message = ""
        if total and price_success == 0:
            warnings.append("全銘柄の週間価格が未取得です。")
        if total and len(price_stale) == total:
            message = "価格未更新：週間騰落の最新価格日付が全銘柄で想定より古いです。"
            warnings.append(message)
        elif price_stale:
            warnings.append(f"最新価格日付が古い銘柄があります：{len(price_stale)}銘柄")
        if price_missing:
            warnings.append(f"週間価格未取得の銘柄があります：{price_missing}銘柄")
        if tv_missing:
            warnings.append(f"米国株TradingViewスナップショット未設定：{len(tv_missing)}銘柄")
        if stale_tv:
            warnings.append(f"TradingViewスナップショットの鮮度注意：{len(stale_tv)}銘柄")

        if total and price_success == 0:
            level = "error"
        elif total and len(price_stale) == total:
            level = "price_stale"
        else:
            level = "partial" if warnings else "ok"

        status = {
            "status": level,
            "generated_at_jst": timestamp_jst(),
            "message": message,
            "expected_us_price_date": expected_us,
            "expected_jp_price_date": expected_jp,
            "price_success_count": price_success,
            "price_missing_count": price_missing,
            "price_stale_count": len(price_stale),
            "price_stale_symbols": price_stale,
            "market_closed_count": len(price_stale),
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
