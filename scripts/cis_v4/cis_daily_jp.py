#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from typing import Any, Dict, List

from cis_core import (
    expected_daily_trade_date,
    fmt_change,
    fmt_pct,
    fmt_price,
    load_watchlist,
    now_jst,
    fetch_price,
    timestamp_jst,
    write_error_report,
    write_report,
)

STEM = "daily_jp"
TITLE = "CIS 日本株日次騰落"


def main() -> int:
    try:
        expected_date = expected_daily_trade_date("JP")
        items = [x for x in load_watchlist(True) if x.market == "JP"]
        rows: List[Dict[str, Any]] = []
        for item in items:
            p = fetch_price(item, weekly=False)
            stale_price = bool(p.stale_price or p.market_closed)
            rows.append(
                {
                    "symbol": item.symbol,
                    "market": item.market,
                    "name": item.name,
                    "description": item.name,
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
                }
            )

        rows.sort(key=lambda r: (1, 0) if r["daily_pct"] is None else (0, -r["daily_pct"]))
        total = len(items)
        success = sum(1 for r in rows if r.get("daily_pct") is not None)
        missing = max(0, total - success)
        price_stale = [r["symbol"] for r in rows if r.get("stale_price")]

        warnings: List[str] = []
        message = ""
        if total and success == 0:
            warnings.append("日本株価格が全銘柄で未取得です。取得障害の可能性があります。")
        if total and len(price_stale) == total:
            message = f"価格未更新：日本株の価格日付が想定取引日 {expected_date} より古いです。"
            warnings.append(message)
        elif price_stale:
            warnings.append(f"価格日付が古い銘柄があります：{len(price_stale)}銘柄（想定：{expected_date}）")
        if missing:
            warnings.append(f"価格未取得の銘柄があります：{missing}銘柄")

        if total and success == 0:
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
            "price_success_count": success,
            "price_missing_count": missing,
            "jp_count": total,
            "price_stale_count": len(price_stale),
            "price_stale_symbols": price_stale,
            "market_closed_count": len(price_stale),
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
            f"- 価格取得成功：{success}/{total}",
            f"- 価格未取得：{missing}",
            f"- 価格日付が古い銘柄：{len(price_stale)}",
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
            lines += ["## 日本株｜前日比順", ""]

            for i, r in enumerate([x for x in rows if not x.get("stale_price")], 1):
                lines += [
                    f"### {i}. {r['symbol']}｜{r.get('description') or r.get('name')}",
                    "",
                    f"- 価格日付：{r.get('latest_date') or '未取得'}",
                    f"- 終値：{fmt_price(r.get('latest_price'), 'JP')}",
                    f"- 前日比：{fmt_change(r.get('daily_change'), 'JP')}",
                    f"- 前日比％：**{fmt_pct(r.get('daily_pct'))}**",
                ]
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
