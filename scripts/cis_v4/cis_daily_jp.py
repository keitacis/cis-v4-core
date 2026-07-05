#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
from typing import Any, Dict, List
from cis_core import fmt_change, fmt_pct, fmt_price, load_watchlist, now_jst, fetch_price, timestamp_jst, write_error_report, write_report

STEM = "daily_jp"
TITLE = "CIS 日本株日次騰落"

def main() -> int:
    try:
        items = [x for x in load_watchlist(True) if x.market == "JP"]
        rows: List[Dict[str, Any]] = []
        for item in items:
            p = fetch_price(item, weekly=False)
            rows.append({
                "symbol": item.symbol,
                "market": item.market,
                "name": item.name,
                "description": item.name if item.market == "JP" else (item.description or item.notes),
                "latest_price": p.latest_price,
                "daily_change": p.daily_change,
                "daily_pct": p.daily_pct,
                "latest_date": p.latest_date,
                "previous_date": p.previous_date,
                "market_closed": p.market_closed,
                "stale_price": p.stale_price,
                "price_source": p.source,
                "price_error": p.error,
            })
        rows.sort(key=lambda r: (1, 0) if r["daily_pct"] is None else (0, -r["daily_pct"]))
        total = len(items)
        success = sum(1 for r in rows if r.get("daily_pct") is not None)
        missing = max(0, total - success)
        closed = sum(1 for r in rows if r.get("market_closed"))
        warnings = []
        if total and success == 0:
            warnings.append("日本株価格が全銘柄で未取得です。休場または取得障害の可能性があります。")
        elif total and closed == total:
            warnings.append("日本株は休場または価格更新前の可能性があります。古い日付を当日更新として扱いません。")
        else:
            if missing:
                warnings.append(f"価格未取得の銘柄があります：{missing}銘柄")
            if closed:
                warnings.append(f"価格日付が古い銘柄があります：{closed}銘柄")
        if total and success == 0:
            level = "error"
        elif total and closed == total:
            level = "market_closed"
        else:
            level = "partial" if warnings else "ok"
        status = {"status": level, "generated_at_jst": timestamp_jst(), "price_success_count": success, "price_missing_count": missing, "jp_count": total, "market_closed_count": closed, "warnings": warnings}
        lines = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", "", "## ステータス", "", f"- 価格取得成功：{success}/{total}", f"- 価格未取得：{missing}", f"- 休場/日付注意：{closed}", "", "## 日本株｜前日比順", ""]
        for w in warnings:
            lines.append(f"- ⚠️ {w}")
        if warnings:
            lines.append("")
        for i, r in enumerate(rows, 1):
            lines += [
                f"### {i}. {r['symbol']}｜{r.get('description') or r.get('name')}",
                "",
                f"- 価格日付：{r.get('latest_date') or '未取得'}",
                f"- 終値：{fmt_price(r.get('latest_price'), 'JP')}",
                f"- 前日比：{fmt_change(r.get('daily_change'), 'JP')}",
                f"- 前日比％：**{fmt_pct(r.get('daily_pct'))}**",
            ]
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
