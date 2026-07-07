#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 price freshness + Buy Alert UX patch R7.

This patch intentionally rewrites only the report generator scripts and makes
small, targeted compatibility edits to cis_core.py / cis_home.py.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "cis_v4"
WORKFLOWS = ROOT / ".github" / "workflows"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def replace_function_until(text: str, func_name: str, next_func_name: str, replacement: str) -> tuple[str, int]:
    """Replace a top-level function even if the target file is compacted."""
    start_m = re.search(rf'(^|\n)def\s+{re.escape(func_name)}\s*\(', text)
    if not start_m:
        start_m = re.search(rf'\sdef\s+{re.escape(func_name)}\s*\(', text)
    if not start_m:
        return text, 0
    start = start_m.start()
    if text[start:start+1].isspace() and text[start:start+1] != "\n":
        start += 1
    next_m = re.search(rf'def\s+{re.escape(next_func_name)}\s*\(', text[start + 1:])
    if not next_m:
        return text, 0
    next_start = start + 1 + next_m.start()
    return text[:start].rstrip() + "\n\n" + replacement.strip() + "\n\n" + text[next_start:].lstrip(), 1


def patch_core() -> None:
    path = SCRIPTS / "cis_core.py"
    text = path.read_text(encoding="utf-8")
    replacement = """def status_badge(status: str) -> str:
    return {
        "ok": "✅ 更新済み",
        "partial": "⚠️ 一部注意",
        "error": "❌ エラー",
        "price_stale": "⚠️ 価格未更新",
        "market_closed": "休場",
        "missing": "⚪ 未生成",
        "stale": "⚠️ 古い",
    }.get(status, f"⚪ {status}")
"""
    new_text, n = replace_function_until(text, "status_badge", "load_status", replacement)
    if n != 1:
        raise RuntimeError("cis_core.py status_badge patch failed")
    # Keep DEFAULT_SETTINGS operational time metadata aligned with R6 workflows.
    new_text = new_text.replace('"daily_jp_time_jst": "16:10"', '"daily_jp_time_jst": "17:40"')
    new_text = new_text.replace('"buy_alert_time_jst": "08:00"', '"buy_alert_time_jst": "08:20"')
    # Keep fallback-time defaults aligned too, in case data/cis_settings.json is absent.
    if '"daily_us_backup_time_jst"' not in new_text:
        new_text = new_text.replace('"daily_us_time_jst": "07:15",', '"daily_us_time_jst": "07:15", "daily_us_backup_time_jst": "08:45",')
    if '"daily_jp_backup_time_jst"' not in new_text:
        new_text = new_text.replace('"daily_jp_time_jst": "17:40",', '"daily_jp_time_jst": "17:40", "daily_jp_backup_time_jst": "18:40",')
    if '"buy_alert_backup_time_jst"' not in new_text:
        new_text = new_text.replace('"buy_alert_time_jst": "08:20",', '"buy_alert_time_jst": "08:20", "buy_alert_backup_time_jst": "09:20",')
    path.write_text(new_text, encoding="utf-8")
    print("patched scripts/cis_v4/cis_core.py status_badge")


def patch_home() -> None:
    path = SCRIPTS / "cis_home.py"
    text = path.read_text(encoding="utf-8")
    replacement = """def alert_reason(stem: str, st: Dict[str, Any]) -> str:
    # Compact reason text for the Home 要確認 box.
    status = str(st.get("status", "missing"))
    if status == "price_stale":
        warnings = st.get("warnings") or []
        if isinstance(warnings, list) and warnings:
            return str(warnings[0])
        return str(st.get("message") or "価格日付が想定より古いです")
    if stem == "tv_monthly_refresh" and status == "partial":
        changed = int(st.get("candidate_change_count") or 0)
        failed = int(st.get("failed_count") or 0)
        parts: List[str] = []
        if changed:
            parts.append(f"TV変更候補{changed}件")
        if failed:
            parts.append(f"TV取得失敗{failed}件")
        return " / ".join(parts) if parts else "TradingView月次確認に一部注意があります"
    if stem == "master_init_template" and status == "partial":
        parts: List[str] = []
        bz_missing = int(st.get("buyzone_missing_count") or 0)
        bz_invalid = int(st.get("buyzone_invalid_count") or 0)
        tv_missing = int(st.get("tv_missing_count") or 0)
        if bz_missing:
            parts.append(f"BUYZONE未設定{bz_missing}件")
        if bz_invalid:
            parts.append(f"BUYZONE不正{bz_invalid}件")
        if tv_missing:
            parts.append(f"TV未設定{tv_missing}件")
        return " / ".join(parts) if parts else "初期マスターに一部注意があります"
    if status == "stale":
        if st.get("dependency_stale"):
            return str(st.get("dependency_reason") or "関連マスター更新後、未再生成")
        age = st.get("stale_age_days")
        return f"更新から{age}日経過" if age is not None else "更新時刻を確認できません"
    reason = st.get("error") or st.get("errors") or st.get("problems") or st.get("message") or status
    if isinstance(reason, list):
        reason = " / ".join(str(x) for x in reason[:3])
    return str(reason)
"""
    new_text, n = replace_function_until(text, "alert_reason", "card_markdown", replacement)
    if n != 1:
        raise RuntimeError("cis_home.py alert_reason replacement failed")
    new_text = new_text.replace('{"error", "partial", "stale"}', '{"error", "partial", "stale", "price_stale"}')
    new_text = new_text.replace("{'error', 'partial', 'stale'}", "{'error', 'partial', 'stale', 'price_stale'}")
    path.write_text(new_text, encoding="utf-8")
    print("patched scripts/cis_v4/cis_home.py price_stale handling")



DAILY_US = r'''
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
                    f"- TradingViewレーティング：{r.get('tv_rating') or na}",
                    f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",
                    f"- 平均目標株価：{fmt_price(r.get('tv_avg_target_price'), 'US') if is_tv_covered(cov) else na}",
                    f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get('tv_upside_pct')) if is_tv_covered(cov) else na}",
                ]
                if is_tv_covered(cov):
                    lines.append(f"- TV更新：{r.get('tv_freshness')}")
                if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:
                    lines.append(f"- TVメモ：{r.get('tv_reason')}")
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
'''


DAILY_JP = r'''
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

        write_report(STEM, "\n".join(lines), {"status": status, "rows": rows}, status)
        return 1 if level == "error" else 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
'''


BUY_ALERT = r'''
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
'''


WEEKLY = r'''
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
            f"- TradingViewレーティング：{r.get('tv_rating') or na}",
            f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",
            f"- 平均目標株価：{fmt_price(r.get('tv_avg_target_price'), 'US') if is_tv_covered(cov) else na}",
            f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get('tv_upside_pct')) if is_tv_covered(cov) else na}",
            f"- TV更新：{r.get('tv_freshness')}",
        ]
        if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:
            lines.append(f"- TVメモ：{r.get('tv_reason')}")
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
            and r.get("tv_coverage_status")
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
'''



DAILY_US_WORKFLOW = """name: CIS v4 Daily US

on:
  workflow_dispatch:
  schedule:
    # JST 火〜土07:15。米国市場の前営業日終値ベースで自動更新する。
    - cron: '15 22 * * 1-5'
    # JST 火〜土08:45。価格ソース反映遅延・Actions遅延対策の予備実行。
    - cron: '45 23 * * 1-5'

permissions:
  contents: write

concurrency:
  group: cis-v4-global-${{ github.ref }}
  cancel-in-progress: false

jobs:
  daily-us:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Sync latest branch
        run: git pull --rebase --autostash

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas

      - name: Run daily US
        id: run_report
        continue-on-error: true
        run: python scripts/cis_v4/cis_daily_us.py

      - name: Rebuild CIS home
        id: rebuild_home
        if: always()
        continue-on-error: true
        run: python scripts/cis_v4/cis_home.py

      - name: Commit outputs
        if: always()
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          for p in output/v4 docs/v4; do
            if [ -e "$p" ]; then
              git add "$p"
            else
              echo "skip missing path: $p"
            fi
          done
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update CIS daily US"
            git pull --rebase --autostash
            git push
          fi

      - name: Fail if report failed
        if: steps.run_report.outcome == 'failure' || steps.rebuild_home.outcome == 'failure'
        run: exit 1
"""

DAILY_JP_WORKFLOW = """name: CIS v4 Daily JP

on:
  workflow_dispatch:
  schedule:
    # JST 月〜金17:40。東証15:30引け後、外部価格ソース反映待ちを入れて自動更新する。
    - cron: '40 8 * * 1-5'
    # JST 月〜金18:40。価格ソース反映遅延・Actions遅延対策の予備実行。
    - cron: '40 9 * * 1-5'

permissions:
  contents: write

concurrency:
  group: cis-v4-global-${{ github.ref }}
  cancel-in-progress: false

jobs:
  daily-jp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Sync latest branch
        run: git pull --rebase --autostash

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas

      - name: Run daily JP
        id: run_report
        continue-on-error: true
        run: python scripts/cis_v4/cis_daily_jp.py

      - name: Rebuild CIS home
        id: rebuild_home
        if: always()
        continue-on-error: true
        run: python scripts/cis_v4/cis_home.py

      - name: Commit outputs
        if: always()
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          for p in output/v4 docs/v4; do
            if [ -e "$p" ]; then
              git add "$p"
            else
              echo "skip missing path: $p"
            fi
          done
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update CIS daily JP"
            git pull --rebase --autostash
            git push
          fi

      - name: Fail if report failed
        if: steps.run_report.outcome == 'failure' || steps.rebuild_home.outcome == 'failure'
        run: exit 1
"""

BUY_ALERT_WORKFLOW = """name: CIS v4 Buy Alert

on:
  workflow_dispatch:
  schedule:
    # JST 月〜金08:20。米国市場の前営業日終値反映を待って買い場アラートを自動更新する。
    - cron: '20 23 * * 0-4'
    # JST 月〜金09:20。価格ソース反映遅延・Actions遅延対策の予備実行。
    - cron: '20 0 * * 1-5'

permissions:
  contents: write

concurrency:
  group: cis-v4-global-${{ github.ref }}
  cancel-in-progress: false

jobs:
  buy-alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Sync latest branch
        run: git pull --rebase --autostash

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas

      - name: Run buy alert
        id: run_report
        continue-on-error: true
        run: python scripts/cis_v4/cis_buy_alert.py

      - name: Rebuild CIS home
        id: rebuild_home
        if: always()
        continue-on-error: true
        run: python scripts/cis_v4/cis_home.py

      - name: Commit outputs
        if: always()
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          for p in output/v4 docs/v4; do
            if [ -e "$p" ]; then
              git add "$p"
            else
              echo "skip missing path: $p"
            fi
          done
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update CIS buy alert"
            git pull --rebase --autostash
            git push
          fi

      - name: Fail if buy alert failed
        if: steps.run_report.outcome == 'failure' || steps.rebuild_home.outcome == 'failure'
        run: exit 1
"""


def patch_workflows() -> None:
    write(WORKFLOWS / "cis_v4_daily_us.yml", DAILY_US_WORKFLOW)
    write(WORKFLOWS / "cis_v4_daily_jp.yml", DAILY_JP_WORKFLOW)
    write(WORKFLOWS / "cis_v4_buy_alert.yml", BUY_ALERT_WORKFLOW)
    print("patched daily/buy-alert workflow schedules")


def patch_settings() -> None:
    """Keep data/cis_settings.json aligned with the workflow cron times.

    The workflow cron remains the source of truth, but this JSON is displayed
    and used as operational metadata. Leaving old times here would make the
    Home/maintenance view misleading after R7.
    """
    path = ROOT / "data" / "cis_settings.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                data = {}
        except Exception as e:
            raise RuntimeError(f"cis_settings.json read failed: {type(e).__name__}: {e}") from e
    else:
        data = {}
    data.update({
        "timezone": data.get("timezone") or "Asia/Tokyo",
        "daily_us_time_jst": "07:15",
        "daily_us_backup_time_jst": "08:45",
        "daily_jp_time_jst": "17:40",
        "daily_jp_backup_time_jst": "18:40",
        "buy_alert_time_jst": "08:20",
        "buy_alert_backup_time_jst": "09:20",
        "weekly_performance_time_jst": data.get("weekly_performance_time_jst") or "Saturday 18:30",
    })
    data["note"] = "GitHub Actionsの自動実行時刻はworkflowのcronが実体です。R7以降、日次系は価格ソース反映遅延に備えて予備実行を併用します。"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched data/cis_settings.json schedule metadata")

def postprocess_r6_outputs() -> None:
    # Final safety cleanups after template writes. Keep this small and deterministic.
    stale_block = '\n        if level != "price_stale":\n            stale_rows = [r for r in rows if r.get("stale_price")]\n            if stale_rows:\n                lines += ["## 価格日付が古い銘柄（ランキング対象外）", ""]\n                for r in stale_rows:\n                    lines += [\n                        f"- {r[\'symbol\']}｜価格日付：{r.get(\'latest_date\') or \'未取得\'}｜想定：{r.get(\'expected_price_date\')}",\n                    ]\n                lines.append("")\n'
    for name in ["cis_daily_us.py", "cis_daily_jp.py"]:
        p = SCRIPTS / name
        t = p.read_text(encoding="utf-8")
        while stale_block + stale_block in t:
            t = t.replace(stale_block + stale_block, stale_block)
        if name == "cis_daily_jp.py" and "ランキング対象外" not in t:
            t = t.replace('\n        write_report(STEM, "\\n".join(lines), {"status": status, "rows": rows}, status)\n', stale_block + '\n        write_report(STEM, "\\n".join(lines), {"status": status, "rows": rows}, status)\n')
        p.write_text(t, encoding="utf-8")

    p = SCRIPTS / "cis_weekly_performance.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace('if r["market"] == "US"\n            and r.get("tv_coverage_status")\n            and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)', 'if r["market"] == "US"\n            and r.get("tv_coverage_status") in {"covered", "covered_partial"}\n            and (r.get("tv_age_days") is None or r.get("tv_age_days", 999) > TV_STALE_DAYS)')
    t = t.replace('            f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\')) if is_tv_covered(cov) else na}",\n            f"- TV更新：{r.get(\'tv_freshness\')}",\n        ]\n        if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:', '            f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\')) if is_tv_covered(cov) else na}",\n        ]\n        if is_tv_covered(cov):\n            lines.append(f"- TV更新：{r.get(\'tv_freshness\')}")\n        if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:')
    p.write_text(t, encoding="utf-8")
    print("postprocessed R6 generated report scripts")



def simplify_noncovered_tv_lines_r7() -> None:
    """Avoid repeating カバレッジなし across rating/count/target/upside lines."""
    daily_old = '                lines += [\n                    f"### {i}. {r[\'symbol\']}｜{r.get(\'description\') or r.get(\'name\')}",\n                    "",\n                    f"- 価格日付：{r.get(\'latest_date\') or \'未取得\'}",\n                    f"- 終値：{fmt_price(r.get(\'latest_price\'), \'US\')}",\n                    f"- 前日比：{fmt_change(r.get(\'daily_change\'), \'US\')}",\n                    f"- 前日比％：**{fmt_pct(r.get(\'daily_pct\'))}**",\n                    f"- TradingViewレーティング：{r.get(\'tv_rating\') or na}",\n                    f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",\n                    f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\') if is_tv_covered(cov) else na}",\n                    f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\')) if is_tv_covered(cov) else na}",\n                ]\n                if is_tv_covered(cov):\n                    lines.append(f"- TV更新：{r.get(\'tv_freshness\')}")\n                if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:\n                    lines.append(f"- TVメモ：{r.get(\'tv_reason\')}")'
    daily_new = '                lines += [\n                    f"### {i}. {r[\'symbol\']}｜{r.get(\'description\') or r.get(\'name\')}",\n                    "",\n                    f"- 価格日付：{r.get(\'latest_date\') or \'未取得\'}",\n                    f"- 終値：{fmt_price(r.get(\'latest_price\'), \'US\')}",\n                    f"- 前日比：{fmt_change(r.get(\'daily_change\'), \'US\')}",\n                    f"- 前日比％：**{fmt_pct(r.get(\'daily_pct\'))}**",\n                ]\n                if is_tv_covered(cov):\n                    lines += [\n                        f"- TradingViewレーティング：{r.get(\'tv_rating\') or \'未取得\'}",\n                        f"- アナリスト人数：{ac}人" if ac is not None else "- アナリスト人数：未取得",\n                        f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\')}",\n                        f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\'))}",\n                        f"- TV更新：{r.get(\'tv_freshness\')}",\n                    ]\n                elif cov in {"no_coverage", "not_applicable"}:\n                    lines.append(f"- TradingView：{na}")\n                    if r.get("tv_reason"):\n                        lines.append(f"- TVメモ：{r.get(\'tv_reason\')}")\n                else:\n                    lines.append("- TradingView：未取得")'
    weekly_old = '        lines += [\n            f"### {i}. {title}",\n            "",\n            f"- 最新価格日付：{r.get(\'latest_date\') or \'未取得\'}",\n            f"- 比較元価格：{fmt_price(r.get(\'weekly_base_price\'), \'US\')}",\n            f"- 週間騰落率：**{fmt_pct(r.get(\'weekly_pct\'))}**",\n            f"- 週間価格差：{fmt_change(r.get(\'weekly_change\'), \'US\')}",\n            f"- TradingViewレーティング：{r.get(\'tv_rating\') or na}",\n            f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",\n            f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\') if is_tv_covered(cov) else na}",\n            f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\')) if is_tv_covered(cov) else na}",\n        ]\n        if is_tv_covered(cov):\n            lines.append(f"- TV更新：{r.get(\'tv_freshness\')}")\n        if r.get("tv_reason") and cov in {"no_coverage", "not_applicable"}:\n            lines.append(f"- TVメモ：{r.get(\'tv_reason\')}")'
    weekly_new = '        lines += [\n            f"### {i}. {title}",\n            "",\n            f"- 最新価格日付：{r.get(\'latest_date\') or \'未取得\'}",\n            f"- 比較元価格：{fmt_price(r.get(\'weekly_base_price\'), \'US\')}",\n            f"- 週間騰落率：**{fmt_pct(r.get(\'weekly_pct\'))}**",\n            f"- 週間価格差：{fmt_change(r.get(\'weekly_change\'), \'US\')}",\n        ]\n        if is_tv_covered(cov):\n            lines += [\n                f"- TradingViewレーティング：{r.get(\'tv_rating\') or \'未取得\'}",\n                f"- アナリスト人数：{ac}人" if ac is not None else "- アナリスト人数：未取得",\n                f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\')}",\n                f"- 直近終値→平均目標株価乖離率：{fmt_pct(r.get(\'tv_upside_pct\'))}",\n                f"- TV更新：{r.get(\'tv_freshness\')}",\n            ]\n        elif cov in {"no_coverage", "not_applicable"}:\n            lines.append(f"- TradingView：{na}")\n            if r.get("tv_reason"):\n                lines.append(f"- TVメモ：{r.get(\'tv_reason\')}")\n        else:\n            lines.append("- TradingView：未取得")'
    for filename, old, new in [
        ("cis_daily_us.py", daily_old, daily_new),
        ("cis_weekly_performance.py", weekly_old, weekly_new),
    ]:
        p = SCRIPTS / filename
        text = p.read_text(encoding="utf-8")
        if old not in text:
            raise RuntimeError(f"R7 TV compact replacement target not found: {filename}")
        p.write_text(text.replace(old, new), encoding="utf-8")
    print("simplified non-covered TradingView display for R7")

def main() -> int:
    required = [
        SCRIPTS / "cis_core.py",
        SCRIPTS / "cis_home.py",
        SCRIPTS / "cis_daily_us.py",
        SCRIPTS / "cis_daily_jp.py",
        SCRIPTS / "cis_buy_alert.py",
        SCRIPTS / "cis_weekly_performance.py",
        WORKFLOWS / "cis_v4_daily_us.yml",
        WORKFLOWS / "cis_v4_daily_jp.yml",
        WORKFLOWS / "cis_v4_buy_alert.yml",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    patch_core()
    patch_home()
    write(SCRIPTS / "cis_daily_us.py", DAILY_US)
    write(SCRIPTS / "cis_daily_jp.py", DAILY_JP)
    write(SCRIPTS / "cis_buy_alert.py", BUY_ALERT)
    write(SCRIPTS / "cis_weekly_performance.py", WEEKLY)
    postprocess_r6_outputs()
    simplify_noncovered_tv_lines_r7()
    patch_workflows()
    patch_settings()
    print("CIS price freshness + Buy Alert UX patch R7 applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
