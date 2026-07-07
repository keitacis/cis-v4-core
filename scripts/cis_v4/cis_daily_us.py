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

STEM = "daily_us"
TITLE = "CIS 米国株日次騰落"
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


def main() -> int:
    global TV_STALE_DAYS
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        expected_date = expected_daily_trade_date("US")
        items = [x for x in load_watchlist(True) if x.market == "US"]
        tv_map = load_tv_snapshot()
        expected_us = expected_daily_trade_date("US")
        expected_jp = expected_daily_trade_date("JP")
        rows: List[Dict[str, Any]] = []

        for item in items:
            p = fetch_price(item, weekly=False)
            tv = tv_map.get(item.key)
            updated_at = tv.updated_at if tv else None
            stale_price = bool(p.stale_price or p.market_closed)
            rows.append(
                {
                    "symbol": item.symbol,
                    "market": item.market,
                    "name": item.name,
                    "description": item.description or item.notes,
                    "latest_price": p.latest_price,
                    "daily_change": p.daily_change,
                    "daily_pct": p.daily_pct,
                    "latest_date": p.latest_date,
                    "previous_date": p.previous_date,
                    "expected_price_date": expected_date,
                    "market_closed": p.market_closed,
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

        rows.sort(key=lambda r: (1, 0) if r["daily_pct"] is None else (0, -r["daily_pct"]))
        total = len(items)
        price_success = sum(1 for r in rows if r.get("daily_pct") is not None)
        price_missing = max(0, total - price_success)
        price_stale = [r["symbol"] for r in rows if r.get("stale_price")]
        tv_count = sum(1 for r in rows if r.get("tv_coverage_status") in {"covered", "covered_partial", "no_coverage", "not_applicable"})
        tv_missing = [r["symbol"] for r in rows if not r.get("tv_coverage_status")]
        tv_no_coverage = [r["symbol"] for r in rows if r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in rows if r.get("tv_coverage_status") == "not_applicable"]
        stale_tv = [
            r["symbol"]
            for r in rows
            if r.get("tv_coverage_status") in {"covered", "covered_partial"}
            and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)
        ]

        warnings: List[str] = []
        message = ""
        if total and price_success == 0:
            warnings.append("米国株価格が全銘柄で未取得です。")
        if total and len(price_stale) == total:
            message = f"価格未更新：米国株の価格日付が想定取引日 {expected_date} より古いです。"
            warnings.append(message)
        elif price_stale:
            warnings.append(f"価格日付が古い銘柄があります：{len(price_stale)}銘柄（想定：{expected_date}）")
        if price_missing:
            warnings.append(f"価格未取得の銘柄があります：{price_missing}銘柄")
        if tv_missing:
            warnings.append(f"TradingViewスナップショット未設定：{len(tv_missing)}銘柄")
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
            "expected_price_date": expected_date,
            "price_success_count": price_success,
            "price_missing_count": price_missing,
            "us_count": total,
            "price_stale_count": len(price_stale),
            "price_stale_symbols": price_stale,
            "market_closed_count": len(price_stale),  # backward compatibility for old Home/status readers
            "tv_saved_or_explicit_count": tv_count,
            "tv_missing_count": len(tv_missing),
            "tv_no_coverage_count": len(tv_no_coverage),
            "tv_not_applicable_count": len(tv_not_applicable),
            "tv_stale_or_unknown_count": len(stale_tv),
            "tv_missing_symbols": tv_missing,
            "tv_stale_or_unknown_symbols": stale_tv,
            "warnings": warnings,
        }

        lines = [
            f"# {TITLE}",
            "",
            f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
            f"想定価格日付：{expected_date}",
            "",
            "## ステータス",
            "",
            f"- 価格取得成功：{price_success}/{total}",
            f"- 価格未取得：{price_missing}",
            f"- 価格日付が古い銘柄：{len(price_stale)}",
            f"- TradingView保存/対象外明示：{tv_count}/{total}",
            f"- TradingView未設定：{len(tv_missing)}",
            f"- カバレッジなし：{len(tv_no_coverage)}",
            f"- 対象外：{len(tv_not_applicable)}",
            f"- TradingView鮮度注意：{len(stale_tv)}",
            "",
        ]
        if warnings:
            lines += ["## 注意", ""] + [f"- ⚠️ {w}" for w in warnings] + [""]
        if level == "price_stale":
            lines += [
                "## 価格未更新のためランキング非表示",
                "",
                f"全銘柄の価格日付が想定価格日付 {expected_date} より古いため、前日比ランキングは表示しません。",
                "",
                "### 価格日付が古い銘柄",
                "",
                ", ".join(price_stale) if price_stale else "対象なし",
                "",
            ]
        else:
            lines += ["## 米国株｜前日比順", ""]

            for i, r in enumerate([x for x in rows if not x.get("stale_price")], 1):
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
                    lines.append(f"- 注意：価格日付が想定より古いです（想定：{expected_date}）")
                lines.append("")

        if level != "price_stale":
            stale_rows = [r for r in rows if r.get("stale_price")]
            if stale_rows:
                lines += ["## 価格日付が古い銘柄（ランキング対象外）", ""]
                for r in stale_rows:
                    lines += [
                        f"- {r['symbol']}｜価格日付：{r.get('latest_date') or '未取得'}｜想定：{r.get('expected_price_date')}",
                    ]
                lines.append("")

        write_report(STEM, "\n".join(lines), {"status": status, "rows": rows}, status)
        return 1 if level == "error" else 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
