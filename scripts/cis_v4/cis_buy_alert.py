#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from cis_core import (
    JST,
    fmt_change,
    fmt_pct,
    fmt_price,
    get_tv_snapshot_stale_days,
    load_buyzone_master,
    load_tv_snapshot,
    load_watchlist,
    now_jst,
    fetch_price,
    safe_float,
    timestamp_jst,
    tv_upside,
    write_error_report,
    write_report,
)

STEM = "buy_alert"
TITLE = "CIS 買い場アラート"


def judgement(latest: Optional[float], watch: Optional[float], main: Optional[float], strong: Optional[float]) -> Tuple[str, int]:
    if latest is None:
        return "価格未取得", 90
    if strong is not None and latest <= strong:
        return "強く買いたい価格圏", 0
    if main is not None and latest <= main:
        return "本命買い価格圏", 1
    if watch is not None and latest <= watch:
        return "打診買い価格圏", 2
    return "待ち", 9


def distance_pct_target_minus_latest(latest: Optional[float], target: Optional[float]) -> Optional[float]:
    """Legacy display metric: target - latest as pct of latest.

    Negative means the price is still above the target. Kept because earlier
    reports used this wording, but sorting uses gap_above_main_pct below.
    """
    if latest is None or target is None or latest == 0:
        return None
    return (target - latest) / latest * 100.0


def gap_above_target_pct(latest: Optional[float], target: Optional[float]) -> Optional[float]:
    """Positive when latest is above the target; smaller positive = closer buy-zone."""
    if latest is None or target is None or latest == 0:
        return None
    return (latest - target) / latest * 100.0


def age_days(updated_at: Optional[str]) -> Optional[float]:
    if not updated_at:
        return None
    try:
        dt = datetime.fromisoformat(str(updated_at))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        return (now_jst() - dt.astimezone(JST)).total_seconds() / 86400
    except Exception:
        return None


def tv_status_label(status: Optional[str]) -> str:
    return {
        "covered": "アナリスト予想あり",
        "no_coverage": "カバレッジなし",
        "not_applicable": "対象外",
        None: "未設定",
        "": "未設定",
    }.get(status, str(status))


def fmt_rule_updated_at(value: Any) -> str:
    """Compact buy-zone rule timestamp for mobile display."""
    if value is None:
        return "未設定"
    text = str(value).strip()
    if not text:
        return "未設定"
    try:
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        dt = dt.astimezone(JST)
        # Keep minutes, drop seconds/microseconds/timezone noise.
        return dt.strftime("%Y/%m/%d %H:%M JST")
    except Exception:
        # Safe fallback for date-like strings. Do not destroy unknown manual notes.
        if "T" in text:
            return text.split("T", 1)[0].replace("-", "/")
        if len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-":
            return text[:10].replace("-", "/")
        return text

def validate_rule(rule: Optional[Dict[str, Any]]) -> List[str]:
    if not rule:
        return ["買い場基準未設定"]
    errors: List[str] = []
    watch = safe_float(rule.get("watch_price"))
    main = safe_float(rule.get("main_buy_price"))
    strong = safe_float(rule.get("strong_buy_price"))
    if watch is None or watch <= 0:
        errors.append("打診買い価格が未設定または不正")
    if main is None or main <= 0:
        errors.append("本命買い価格が未設定または不正")
    if strong is None or strong <= 0:
        errors.append("強く買いたい価格が未設定または不正")
    if not errors and not (strong <= main <= watch):
        errors.append("価格の大小関係が不正（強く買いたい <= 本命 <= 打診 が必要）")
    if not str(rule.get("updated_at") or "").strip():
        errors.append("updated_at未設定")
    return errors


def row_sort_key(r: Dict[str, Any]) -> Tuple[int, int, bool, float, str, str]:
    if r.get("missing_buyzone"):
        return (1, 99, True, 999999.0, str(r.get("market") or ""), str(r.get("symbol") or ""))
    priority = int(r.get("priority", 99))
    gap = r.get("gap_above_main_pct")
    if gap is None:
        sort_gap = 999999.0
    elif priority == 9:
        # 待ち銘柄は「本命買い価格に近い順」。+1%が+50%より先。
        sort_gap = max(float(gap), 0.0)
    else:
        # 価格圏内は判定優先。同じ判定内では本命付近を先にする。
        sort_gap = abs(float(gap))
    return (0, priority, gap is None, sort_gap, str(r.get("market") or ""), str(r.get("symbol") or ""))


def main() -> int:
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        items = load_watchlist(True)
        bz = load_buyzone_master()
        tv_map = load_tv_snapshot()
        rows: List[Dict[str, Any]] = []
        missing_or_invalid: List[Dict[str, Any]] = []

        for item in items:
            tv = tv_map.get(item.key) if item.market == "US" else None
            tv_age = age_days(tv.updated_at) if tv else None
            tv_info = {
                "tv_coverage_status": tv.coverage_status if tv else ("not_required" if item.market != "US" else None),
                "tv_status_label": "日本株は対象外" if item.market != "US" else tv_status_label(tv.coverage_status if tv else None),
                "tv_rating": tv.rating if tv else None,
                "tv_analyst_count": tv.analyst_count if tv else None,
                "tv_avg_target_price": tv.avg_target_price if tv else None,
                "tv_updated_at": tv.updated_at if tv else None,
                "tv_age_days": round(tv_age, 1) if tv_age is not None else None,
                "tv_stale": bool(item.market == "US" and (not tv or tv_age is None or tv_age > TV_STALE_DAYS)),
                "tv_source": tv.source if tv else None,
                "tv_reason": tv.reason if tv else None,
            }

            rule = bz.get(item.key)
            rule_errors = validate_rule(rule)
            if rule_errors:
                missing_or_invalid.append({"key": item.key, "errors": rule_errors})
                rows.append({
                    "symbol": item.symbol,
                    "market": item.market,
                    "name": item.name,
                    "description": item.name if item.market == "JP" else (item.description or item.notes),
                    "rule_errors": rule_errors,
                    "missing_buyzone": True,
                    **tv_info,
                })
                continue

            p = fetch_price(item, weekly=False)
            assert rule is not None
            watch = safe_float(rule.get("watch_price"))
            main_buy = safe_float(rule.get("main_buy_price"))
            strong = safe_float(rule.get("strong_buy_price"))
            label, priority = judgement(p.latest_price, watch, main_buy, strong)
            upside = tv_upside(p.latest_price, tv)
            rows.append({
                "symbol": item.symbol,
                "market": item.market,
                "name": item.name,
                "description": item.name if item.market == "JP" else (item.description or item.notes),
                "latest_price": p.latest_price,
                "daily_change": p.daily_change,
                "daily_pct": p.daily_pct,
                "latest_date": p.latest_date,
                "market_closed": p.market_closed,
                "stale_price": p.stale_price,
                "price_error": p.error,
                "watch_price": watch,
                "main_buy_price": main_buy,
                "strong_buy_price": strong,
                "distance_to_main_pct": distance_pct_target_minus_latest(p.latest_price, main_buy),
                "gap_above_main_pct": gap_above_target_pct(p.latest_price, main_buy),
                "tv_upside_pct": upside,
                "judgement": label,
                "priority": priority,
                "rule_updated_at": rule.get("updated_at"),
                "rule_reason": rule.get("reason"),
                **tv_info,
            })

        # Buy alert must be strict: all active symbols require complete rules and fresh enough prices.
        price_checked = [r for r in rows if not r.get("missing_buyzone")]
        price_available_count = sum(1 for r in price_checked if r.get("latest_price") is not None)
        stale_or_closed_count = sum(1 for r in price_checked if r.get("market_closed") or r.get("stale_price"))
        hard_price_missing_count = sum(1 for r in price_checked if r.get("latest_price") is None)
        us_rows = [r for r in rows if r.get("market") == "US"]
        tv_missing = [r["symbol"] for r in us_rows if not r.get("tv_coverage_status")]
        tv_stale = [r["symbol"] for r in us_rows if r.get("tv_stale")]
        tv_covered = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") == "covered"]
        tv_no_coverage = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") == "not_applicable"]

        warnings = []
        if missing_or_invalid:
            warnings.append(f"買い場基準未設定/不正：{len(missing_or_invalid)}銘柄")
        if price_checked and price_available_count == 0:
            warnings.append("買い場基準はありますが、全銘柄で価格が未取得です。")
        if price_checked and stale_or_closed_count == len(price_checked):
            warnings.append("全銘柄が休場または価格更新前の可能性があります。古い価格を正常更新扱いしません。")
        elif stale_or_closed_count:
            warnings.append(f"休場/日付注意：{stale_or_closed_count}銘柄")
        if hard_price_missing_count:
            warnings.append(f"価格未取得：{hard_price_missing_count}銘柄")
        if tv_missing:
            warnings.append(f"TradingView未設定：{len(tv_missing)}銘柄")
        if tv_stale:
            warnings.append(f"TradingView鮮度注意：{len(tv_stale)}銘柄")

        if missing_or_invalid:
            level = "error"
        elif price_checked and price_available_count == 0:
            # If no prices at all, the report cannot make buy decisions.
            level = "error"
        elif price_checked and stale_or_closed_count == len(price_checked):
            level = "market_closed"
        else:
            level = "partial" if warnings else "ok"

        price_success = price_available_count
        market_closed_count = stale_or_closed_count
        price_error_count = hard_price_missing_count + stale_or_closed_count

        rows.sort(key=row_sort_key)

        status = {
            "status": level,
            "generated_at_jst": timestamp_jst(),
            "watchlist_count": len(items),
            "price_success_count": price_success,
            "price_error_count": price_error_count,
            "market_closed_count": market_closed_count,
            "invalid_buyzone_count": len(missing_or_invalid),
            "invalid_buyzone": missing_or_invalid,
            "tv_covered_count": len(tv_covered),
            "tv_no_coverage_count": len(tv_no_coverage),
            "tv_not_applicable_count": len(tv_not_applicable),
            "tv_missing_count": len(tv_missing),
            "tv_stale_or_unknown_count": len(tv_stale),
            "tv_missing_symbols": tv_missing,
            "tv_stale_or_unknown_symbols": tv_stale,
            "warnings": warnings,
        }

        lines = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += [
            "## ステータス", "",
            f"- 対象銘柄：{len(items)}",
            f"- 価格取得成功：{price_success}/{len(price_checked)}",
            f"- 休場/日付注意：{market_closed_count}",
            f"- 買い場基準不備：{len(missing_or_invalid)}",
            f"- 米国株TradingView covered：{len(tv_covered)}",
            f"- TradingView未設定：{len(tv_missing)}",
            f"- カバレッジなし：{len(tv_no_coverage)}",
            f"- 対象外：{len(tv_not_applicable)}",
            f"- TradingView鮮度注意：{len(tv_stale)}",
            "",
        ]

        if missing_or_invalid:
            lines += ["## エラー", "", "買い場アラートは、全active銘柄に完全な `buyzone_master.json` 基準が必要です。", "", "### 修正が必要な銘柄", ""]
            for x in missing_or_invalid:
                lines.append(f"- {x['key']}：{' / '.join(x['errors'])}")
            lines.append("")

        if tv_missing or tv_stale:
            lines += ["## TradingView 要確認", ""]
            if tv_missing:
                lines.append(f"- 未設定：{', '.join(tv_missing[:30])}" + (" ..." if len(tv_missing) > 30 else ""))
            if tv_stale:
                lines.append(f"- 鮮度注意：{', '.join(tv_stale[:30])}" + (" ..." if len(tv_stale) > 30 else ""))
            lines.append("")

        lines += ["## 買い場判定", ""]
        for i, r in enumerate(rows, 1):
            market = r.get("market")
            lines += [f"### {i}. {r['symbol']}｜{r.get('description') or r.get('name')}", ""]
            if r.get("missing_buyzone"):
                lines += [f"- 判定：**基準不備**", f"- 不備：{' / '.join(r.get('rule_errors') or [])}"]
                if market == "US":
                    lines += [f"- TradingView：{r.get('tv_status_label')}"]
                lines.append("")
                continue
            lines += [
                f"- 現在値：{fmt_price(r.get('latest_price'), market)}",
                f"- 前日比：{fmt_change(r.get('daily_change'), market)} / {fmt_pct(r.get('daily_pct'))}",
                f"- 打診買い価格：{fmt_price(r.get('watch_price'), market)}",
                f"- 本命買い価格：{fmt_price(r.get('main_buy_price'), market)}",
                f"- 強く買いたい価格：{fmt_price(r.get('strong_buy_price'), market)}",
                f"- 本命買い価格までの距離：{fmt_pct(r.get('distance_to_main_pct'))}",
                f"- 本命買い価格までの下落余地：{fmt_pct(r.get('gap_above_main_pct'))}",
                f"- 判定：**{r.get('judgement')}**",
                f"- 価格日付：{r.get('latest_date') or '未取得'}",
                f"- 基準更新日：{fmt_rule_updated_at(r.get('rule_updated_at'))}",
                f"- 基準理由：{r.get('rule_reason') or '未記載'}",
            ]
            if market == "US":
                lines += [
                    f"- TradingView：{r.get('tv_status_label')}",
                    f"- TVレーティング：{r.get('tv_rating') or 'なし'}",
                    f"- TVアナリスト人数：{r.get('tv_analyst_count') if r.get('tv_analyst_count') is not None else 'なし'}",
                    f"- TV平均目標株価：{fmt_price(r.get('tv_avg_target_price'), market)}",
                    f"- 現在値→TV平均目標株価：{fmt_pct(r.get('tv_upside_pct'))}",
                    f"- TV更新：{r.get('tv_updated_at') or '未設定'}" + (f"（{r.get('tv_age_days')}日前）" if r.get('tv_age_days') is not None else ""),
                ]
                if r.get("tv_stale"):
                    lines.append("- TV注意：月次更新の確認対象です")
            lines.append("")
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
