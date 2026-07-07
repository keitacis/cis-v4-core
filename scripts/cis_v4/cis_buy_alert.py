#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from cis_core import (
    JST,
    expected_daily_trade_date,
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
NEAR_MAIN_PCT = 15.0
FALLBACK_COUNT = 10


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
    if latest is None or target is None or latest == 0:
        return None
    return (target - latest) / latest * 100.0


def gap_above_target_pct(latest: Optional[float], target: Optional[float]) -> Optional[float]:
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


def row_sort_key(r: Dict[str, Any]) -> Tuple[int, bool, float, float, str, str]:
    priority = int(r.get("priority", 99))
    gap = r.get("gap_above_main_pct")
    daily_pct = r.get("daily_pct")
    sort_gap = 999999.0 if gap is None else abs(float(gap)) if priority < 9 else max(float(gap), 0.0)
    sort_daily = 999999.0 if daily_pct is None else float(daily_pct)  # more negative first
    return (priority, gap is None, sort_gap, sort_daily, str(r.get("market") or ""), str(r.get("symbol") or ""))


def display_bucket(r: Dict[str, Any]) -> Optional[str]:
    if r.get("missing_buyzone") or r.get("latest_price") is None or r.get("stale_price"):
        return None
    priority = int(r.get("priority", 99))
    if priority == 0:
        return "強く買いたい"
    if priority == 1:
        return "本命買い"
    if priority == 2:
        return "打診買い"
    gap = r.get("gap_above_main_pct")
    if gap is not None and 0 <= float(gap) <= NEAR_MAIN_PCT:
        return "買い場接近"
    return None


def is_tv_covered(status: Optional[str]) -> bool:
    return status in {"covered", "covered_partial"}


def render_tv_lines(r: Dict[str, Any], market: str) -> List[str]:
    if market != "US" or not is_tv_covered(r.get("tv_coverage_status")):
        return []
    lines = [
        f"- TVレーティング：{r.get('tv_rating') or '未取得'}",
        "- TVアナリスト人数：" + str(r.get("tv_analyst_count") if r.get("tv_analyst_count") is not None else "未取得"),
        f"- TV平均目標株価：{fmt_price(r.get('tv_avg_target_price'), market)}",
        f"- 直近終値→TV平均目標株価：{fmt_pct(r.get('tv_upside_pct'))}",
    ]
    return lines


def render_card(i: int, r: Dict[str, Any]) -> List[str]:
    market = r.get("market")
    lines = [f"### {i}. {r['symbol']}｜{r.get('description') or r.get('name')}", ""]
    lines += [
        f"- 直近終値：{fmt_price(r.get('latest_price'), market)}",
        f"- 前日比：{fmt_change(r.get('daily_change'), market)} / {fmt_pct(r.get('daily_pct'))}",
        f"- 打診買い価格：{fmt_price(r.get('watch_price'), market)}",
        f"- 本命買い価格：{fmt_price(r.get('main_buy_price'), market)}",
        f"- 強く買いたい価格：{fmt_price(r.get('strong_buy_price'), market)}",
        f"- 本命買い価格までの距離：{fmt_pct(r.get('gap_above_main_pct'))}",
        f"- 判定：**{r.get('display_bucket') or r.get('judgement')}**",
        f"- 価格日付：{r.get('latest_date') or '未取得'}",
    ]
    lines += render_tv_lines(r, market)
    lines.append("")
    return lines


def main() -> int:
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        items = load_watchlist(True)
        bz = load_buyzone_master()
        tv_map = load_tv_snapshot()
        expected_us = expected_daily_trade_date("US")
        expected_jp = expected_daily_trade_date("JP")
        rows: List[Dict[str, Any]] = []
        missing_or_invalid: List[Dict[str, Any]] = []

        for item in items:
            tv = tv_map.get(item.key) if item.market == "US" else None
            tv_age = age_days(tv.updated_at) if tv else None
            tv_info = {
                "tv_coverage_status": tv.coverage_status if tv else ("not_required" if item.market != "US" else None),
                "tv_rating": tv.rating if tv else None,
                "tv_analyst_count": tv.analyst_count if tv else None,
                "tv_avg_target_price": tv.avg_target_price if tv else None,
                "tv_updated_at": tv.updated_at if tv else None,
                "tv_age_days": round(tv_age, 1) if tv_age is not None else None,
                "tv_stale": bool(
                    item.market == "US"
                    and (not tv or tv.coverage_status in {"covered", "covered_partial"})
                    and (not tv or tv_age is None or tv_age > TV_STALE_DAYS)
                ),
                "tv_source": tv.source if tv else None,
                "tv_reason": tv.reason if tv else None,
            }
            rule = bz.get(item.key)
            rule_errors = validate_rule(rule)
            if rule_errors:
                missing_or_invalid.append({"key": item.key, "errors": rule_errors})
                rows.append(
                    {
                        "symbol": item.symbol,
                        "market": item.market,
                        "name": item.name,
                        "description": item.name if item.market == "JP" else (item.description or item.notes),
                        "rule_errors": rule_errors,
                        "missing_buyzone": True,
                        **tv_info,
                    }
                )
                continue

            p = fetch_price(item, weekly=False)
            assert rule is not None
            watch = safe_float(rule.get("watch_price"))
            main_buy = safe_float(rule.get("main_buy_price"))
            strong = safe_float(rule.get("strong_buy_price"))
            label, priority = judgement(p.latest_price, watch, main_buy, strong)
            stale_price = bool(p.stale_price or p.market_closed)
            row = {
                "symbol": item.symbol,
                "market": item.market,
                "name": item.name,
                "description": item.name if item.market == "JP" else (item.description or item.notes),
                "latest_price": p.latest_price,
                "daily_change": p.daily_change,
                "daily_pct": p.daily_pct,
                "latest_date": p.latest_date,
                "market_closed": p.market_closed,
                "stale_price": stale_price,
                "price_error": p.error,
                "watch_price": watch,
                "main_buy_price": main_buy,
                "strong_buy_price": strong,
                "distance_to_main_pct": distance_pct_target_minus_latest(p.latest_price, main_buy),
                "gap_above_main_pct": gap_above_target_pct(p.latest_price, main_buy),
                "tv_upside_pct": tv_upside(p.latest_price, tv),
                "judgement": label,
                "priority": priority,
                "rule_updated_at": rule.get("updated_at"),
                "rule_reason": rule.get("reason"),
                **tv_info,
            }
            row["display_bucket"] = display_bucket(row)
            rows.append(row)

        price_checked = [r for r in rows if not r.get("missing_buyzone")]
        price_available_count = sum(1 for r in price_checked if r.get("latest_price") is not None)
        stale_count = sum(1 for r in price_checked if r.get("stale_price"))
        hard_price_missing_count = sum(1 for r in price_checked if r.get("latest_price") is None)
        us_rows = [r for r in rows if r.get("market") == "US"]
        tv_missing = [r["symbol"] for r in us_rows if not r.get("tv_coverage_status")]
        tv_stale = [r["symbol"] for r in us_rows if r.get("tv_stale")]
        tv_covered = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") in {"covered", "covered_partial"}]
        tv_no_coverage = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") == "no_coverage"]
        tv_not_applicable = [r["symbol"] for r in us_rows if r.get("tv_coverage_status") == "not_applicable"]

        warnings: List[str] = []
        message = ""
        if missing_or_invalid:
            warnings.append(f"買い場基準未設定/不正：{len(missing_or_invalid)}銘柄")
        if price_checked and price_available_count == 0:
            warnings.append("買い場基準はありますが、全銘柄で価格が未取得です。")
        if price_checked and stale_count == len(price_checked):
            message = "価格未更新：全銘柄の価格日付が古いため、通常の買い場判定として扱いません。"
            warnings.append(message)
        elif stale_count:
            warnings.append(f"価格日付が古い銘柄があります：{stale_count}銘柄（想定：米国 {expected_us} / 日本 {expected_jp}）")
        if hard_price_missing_count:
            warnings.append(f"価格未取得：{hard_price_missing_count}銘柄")
        if tv_missing:
            warnings.append(f"TradingView未設定：{len(tv_missing)}銘柄")
        if tv_stale:
            warnings.append(f"TradingView鮮度注意：{len(tv_stale)}銘柄")

        if missing_or_invalid:
            level = "error"
        elif price_checked and price_available_count == 0:
            level = "error"
        elif price_checked and stale_count == len(price_checked):
            level = "price_stale"
        else:
            level = "partial" if warnings else "ok"

        fresh_rows = [r for r in price_checked if r.get("latest_price") is not None and not r.get("stale_price")]
        for r in fresh_rows:
            r["display_bucket"] = display_bucket(r)
        grouped = {
            "強く買いたい": sorted([r for r in fresh_rows if r.get("display_bucket") == "強く買いたい"], key=row_sort_key),
            "本命買い": sorted([r for r in fresh_rows if r.get("display_bucket") == "本命買い"], key=row_sort_key),
            "打診買い": sorted([r for r in fresh_rows if r.get("display_bucket") == "打診買い"], key=row_sort_key),
            "買い場接近": sorted([r for r in fresh_rows if r.get("display_bucket") == "買い場接近"], key=row_sort_key),
        }
        display_rows = [r for group in grouped.values() for r in group]
        fallback_rows: List[Dict[str, Any]] = []
        if not display_rows:
            fallback_rows = sorted(fresh_rows, key=row_sort_key)[:FALLBACK_COUNT]

        status = {
            "status": level,
            "generated_at_jst": timestamp_jst(),
            "message": message,
            "expected_us_price_date": expected_us,
            "expected_jp_price_date": expected_jp,
            "watchlist_count": len(items),
            "price_success_count": price_available_count,
            "price_error_count": hard_price_missing_count,
            "price_stale_count": stale_count,
            "price_stale_symbols": [r["symbol"] for r in price_checked if r.get("stale_price")],
            "market_closed_count": stale_count,
            "invalid_buyzone_count": len(missing_or_invalid),
            "invalid_buyzone": missing_or_invalid,
            "strong_buy_count": len(grouped["強く買いたい"]),
            "main_buy_count": len(grouped["本命買い"]),
            "watch_buy_count": len(grouped["打診買い"]),
            "near_buy_count": len(grouped["買い場接近"]),
            "display_count": len(display_rows) if display_rows else len(fallback_rows),
            "fallback_display": bool(fallback_rows),
            "tv_covered_count": len(tv_covered),
            "tv_no_coverage_count": len(tv_no_coverage),
            "tv_not_applicable_count": len(tv_not_applicable),
            "tv_missing_count": len(tv_missing),
            "tv_stale_or_unknown_count": len(tv_stale),
            "tv_missing_symbols": tv_missing,
            "tv_stale_or_unknown_symbols": tv_stale,
            "warnings": warnings,
        }

        lines = [
            f"# {TITLE}",
            "",
            f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
            f"想定価格日付：米国 {expected_us} / 日本 {expected_jp}",
            "",
            "## サマリー",
            "",
            f"- 強く買いたい：{len(grouped['強く買いたい'])}件",
            f"- 本命買い：{len(grouped['本命買い'])}件",
            f"- 打診買い：{len(grouped['打診買い'])}件",
            f"- 買い場接近：{len(grouped['買い場接近'])}件",
            f"- 表示対象：{status['display_count']}件",
            "",
            "並び順：判定が強い順 → 本命買い価格までの距離が近い順 → 前日比の下落率が大きい順",
            "",
            "## ステータス",
            "",
            f"- 対象銘柄：{len(items)}",
            f"- 価格取得成功：{price_available_count}/{len(price_checked)}",
            f"- 価格日付が古い銘柄：{stale_count}",
            f"- 買い場基準不備：{len(missing_or_invalid)}",
            f"- TradingView未設定：{len(tv_missing)}",
            f"- カバレッジなし：{len(tv_no_coverage)}",
            f"- 対象外：{len(tv_not_applicable)}",
            f"- TradingView鮮度注意：{len(tv_stale)}",
            "",
        ]
        if warnings:
            lines += ["## 注意", ""] + [f"- ⚠️ {w}" for w in warnings] + [""]

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

        if level == "price_stale":
            lines += [
                "## 価格未更新のため買い場判定非表示",
                "",
                "全銘柄の価格日付が想定より古いため、買い場判定カードは表示しません。",
                "",
                "### 価格日付が古い銘柄",
                "",
                ", ".join(status.get("price_stale_symbols") or []) if status.get("price_stale_symbols") else "対象なし",
                "",
            ]
        else:
            lines += ["## 買い場判定", ""]
            card_no = 1
            if display_rows:
                for label in ["強く買いたい", "本命買い", "打診買い", "買い場接近"]:
                    group = grouped[label]
                    if not group:
                        continue
                    lines += [f"## {label}：{len(group)}件", ""]
                    for r in group:
                        lines += render_card(card_no, r)
                        card_no += 1
            else:
                lines += ["## 該当なしのため、接近順候補", "", f"強く買いたい／本命買い／打診買い／買い場接近が0件のため、本命買い価格に近い順で上位{len(fallback_rows)}件を表示します。", ""]
                for r in fallback_rows:
                    lines += render_card(card_no, r)
                    card_no += 1

        write_report(STEM, "\n".join(lines), {"status": status, "rows": rows}, status)
        return 1 if level == "error" else 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
