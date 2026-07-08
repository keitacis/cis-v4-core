#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from cis_core import expected_daily_trade_date, DOCS_LATEST_DIR, html_escape, load_settings, load_status, now_jst, status_badge, write_json, write_text

ITEMS = [
    ("buy_alert", "買い場アラート", "buy_alert_latest.html", "毎日見る", 2),
    ("daily_us", "米国株騰落", "daily_us_latest.html", "毎日見る", 3),
    ("daily_jp", "日本株騰落", "daily_jp_latest.html", "毎日見る", 2),
    ("schedule_catchup", "自動更新取りこぼし確認", "schedule_catchup_latest.html", "メンテナンス", 2),
    ("weekly_performance", "週間騰落", "weekly_performance_latest.html", "週末見る", 9),
    ("cis_v4_preflight", "CIS v4 Preflight", "cis_v4_preflight_latest.html", "メンテナンス", 45),
    ("cis_v4_apply_seed", "CIS v4 Apply Seed", "cis_v4_apply_seed_latest.html", "メンテナンス", 45),
    ("watchlist_template", "監視リスト追加・変更テンプレート", "watchlist_template_latest.html", "メンテナンス", 90),
    ("watchlist_update", "監視リスト更新", "watchlist_update_latest.html", "メンテナンス", 90),
    ("master_init_template", "初期マスター投入テンプレート", "master_init_template_latest.html", "メンテナンス", 45),
    ("tv_monthly_refresh", "TradingView月次自動確認", "tv_monthly_refresh_latest.html", "メンテナンス", 45),
    ("apply_tv_monthly_candidate", "TradingView月次候補反映", "apply_tv_monthly_candidate_latest.html", "メンテナンス", 45),
    ("master_update", "TV・買い場基準更新", "master_update_latest.html", "メンテナンス", 45),
    ("monthly_maintenance", "月次メンテナンス", "monthly_maintenance_latest.html", "メンテナンス", 45),
]


def format_jst(value: Any) -> str:
    """Return iPhone-readable JST time for status timestamps."""
    if not value:
        return "未生成"
    text = str(value)
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return dt.strftime("%Y/%m/%d %H:%M JST")
    except Exception:
        return text


def mark_stale(st: Dict[str, Any], max_age_days: int) -> Dict[str, Any]:
    out = dict(st)
    gen = out.get("generated_at_jst")
    if out.get("status") in {"missing", "error"} or not gen:
        return out
    try:
        dt = datetime.fromisoformat(str(gen))
        age_days = (now_jst() - dt).total_seconds() / 86400
        if age_days > max_age_days:
            out["original_status"] = out.get("status")
            out["status"] = "stale"
            out["stale_age_days"] = round(age_days, 1)
    except Exception:
        out["original_status"] = out.get("status")
        out["status"] = "stale"
        out["stale_age_days"] = None
    return out




def parse_status_time(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def mark_dependency_stale(statuses: Dict[str, Dict[str, Any]]) -> None:
    """Mark reports stale when a master/watchlist update is newer than them.

    This prevents iPhone Home from showing an old buy-alert as green after the
    buy-zone master or watchlist has just changed.
    """
    def newer(src: str, dst: str) -> bool:
        src_st = statuses.get(src, {})
        dst_st = statuses.get(dst, {})
        if src_st.get("status") not in {"ok", "partial"}:
            return False
        if dst_st.get("status") in {"missing", "error"}:
            return False
        src_dt = parse_status_time(src_st.get("generated_at_jst"))
        dst_dt = parse_status_time(dst_st.get("generated_at_jst"))
        return bool(src_dt and dst_dt and src_dt > dst_dt)

    rules = [
        ("master_update", "buy_alert", "TV・買い場基準更新後、買い場アラート未再生成"),
        ("master_update", "daily_us", "TV更新後、米国株騰落未再生成"),
        ("master_update", "weekly_performance", "TV更新後、週間騰落未再生成"),
        ("watchlist_update", "buy_alert", "監視リスト更新後、買い場アラート未再生成"),
        ("watchlist_update", "daily_us", "監視リスト更新後、米国株騰落未再生成"),
        ("watchlist_update", "daily_jp", "監視リスト更新後、日本株騰落未再生成"),
        ("watchlist_update", "weekly_performance", "監視リスト更新後、週間騰落未再生成"),
        ("master_update", "master_init_template", "マスター更新後、初期マスター投入テンプレート未再生成"),
        ("watchlist_update", "master_init_template", "監視リスト更新後、初期マスター投入テンプレート未再生成"),
    ]
    for src, dst, reason in rules:
        if newer(src, dst):
            st = statuses.get(dst)
            if not st:
                continue
            st.setdefault("original_status", st.get("status"))
            st["status"] = "stale"
            st["dependency_stale"] = True
            st["dependency_source"] = src
            st["dependency_reason"] = reason



def mark_tv_monthly_candidate_applied(statuses: Dict[str, Dict[str, Any]]) -> None:
    """Hide already-applied TV change candidates from the Home alert box.

    TV Monthly Refresh intentionally keeps its original report/status as a
    historical snapshot.  After Apply TV Monthly Candidate succeeds, Home should
    not keep warning the user that the same change candidates still need action.
    It should only keep genuine remaining work, such as fetch failures.
    """
    tv = statuses.get("tv_monthly_refresh")
    applied = statuses.get("apply_tv_monthly_candidate")
    if not isinstance(tv, dict) or not isinstance(applied, dict):
        return
    if applied.get("status") != "ok":
        return
    tv_generated = str(tv.get("generated_at_jst") or "")
    applied_candidate_generated = str(applied.get("candidate_generated_at_jst") or "")
    if not tv_generated or not applied_candidate_generated or tv_generated != applied_candidate_generated:
        return
    changed = int(tv.get("candidate_change_count") or 0)
    failed = int(tv.get("failed_count") or 0)
    if changed <= 0:
        return
    tv["tv_candidate_applied"] = True
    tv["tv_candidate_applied_at_jst"] = applied.get("generated_at_jst")
    tv["candidate_change_count_before_apply"] = changed
    tv["candidate_change_count"] = 0
    tv["candidate_change_count_suppressed"] = changed
    if failed > 0:
        tv["tv_candidate_applied_note"] = f"TV変更候補{changed}件は反映済みです。TV取得失敗{failed}件は残っています。"
    else:
        tv["tv_candidate_applied_note"] = f"TV変更候補{changed}件は反映済みです。"
        if tv.get("status") == "partial":
            tv.setdefault("original_status", "partial")
            tv["status"] = "ok"


# --- CIS R10 daily freshness guard START ---
def _r10_read_payload(stem: str) -> Dict[str, Any]:
    path = DOCS_LATEST_DIR / f"{stem}_latest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _r10_generated_today(st: Dict[str, Any]) -> bool:
    dt = parse_status_time(st.get("generated_at_jst"))
    return bool(dt and dt.astimezone(now_jst().tzinfo).date() == now_jst().date())


def _r10_rows_for_market(stem: str, market: str) -> List[Dict[str, Any]]:
    payload = _r10_read_payload(stem)
    rows = payload.get("rows")
    if not isinstance(rows, list):
        return []
    out: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict) and str(row.get("market") or "").upper() == market:
            out.append(row)
    return out


def _r10_price_dates_stale(stem: str, market: str, expected: str) -> bool:
    rows = _r10_rows_for_market(stem, market)
    if not rows:
        return True
    dates = [str(r.get("latest_date") or "")[:10] for r in rows if r.get("latest_date")]
    if not dates:
        return True
    return all(d < expected for d in dates)


def mark_daily_freshness(statuses: Dict[str, Dict[str, Any]]) -> None:
    """R10: prevent Home from looking green when only Home was refreshed.

    If a daily report is still yesterday's generated report after its expected
    automatic update window, Home marks it stale even if the report status itself
    is ok. This catches the exact failure mode where CIS v4 Home runs but Daily
    US / Buy Alert / Daily JP scheduled workflows did not fire.
    """
    now = now_jst()
    # Python weekday: Monday=0 ... Sunday=6.
    checks = [
        ("daily_us", "US", 9, {1, 2, 3, 4, 5}, "米国株日次が自動更新予定後も未更新"),
        ("buy_alert", "US", 10, {0, 1, 2, 3, 4}, "買い場アラートの米国価格が自動更新予定後も未更新"),
        ("daily_jp", "JP", 19, {0, 1, 2, 3, 4}, "日本株日次が自動更新予定後も未更新"),
        ("buy_alert", "JP", 19, {0, 1, 2, 3, 4}, "買い場アラートの日本価格が自動更新予定後も未更新"),
    ]
    reasons_by_stem: Dict[str, List[str]] = {}
    for stem, market, min_hour, active_weekdays, reason in checks:
        if now.weekday() not in active_weekdays or now.hour < min_hour:
            continue
        st = statuses.get(stem)
        if not isinstance(st, dict):
            continue
        # Only override reports that are otherwise green-ish. If the report
        # already says market_closed or price_stale, keep that first-class status
        # instead of turning a valid holiday/delay signal into a schedule failure.
        if st.get("status") not in {"ok", "partial"}:
            continue
        expected = expected_daily_trade_date(market)
        stale_generated = not _r10_generated_today(st)
        stale_dates = _r10_price_dates_stale(stem, market, expected)
        if stale_generated or stale_dates:
            detail = reason
            if stale_generated:
                detail += " / 生成日が当日ではありません"
            if stale_dates:
                detail += f" / {market}価格日付が想定{expected}より古い可能性"
            reasons_by_stem.setdefault(stem, []).append(detail)
    for stem, reasons in reasons_by_stem.items():
        st = statuses.get(stem)
        if not st:
            continue
        st.setdefault("original_status", st.get("status"))
        st["status"] = "stale"
        st["dependency_stale"] = True
        st["dependency_source"] = "schedule_catchup"
        st["dependency_reason"] = " / ".join(reasons)
        st["daily_freshness_stale"] = True
# --- CIS R10 daily freshness guard END ---


def alert_reason(stem: str, st: Dict[str, Any]) -> str:
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

def card_markdown(stem: str, label: str, href: str, st: Dict[str, Any]) -> str:
    status = str(st.get("status", "missing"))
    badge = status_badge(status)
    gen = format_jst(st.get("generated_at_jst"))
    lines = [f"### {badge} {label}", "", f"- 更新：{gen}"]
    if status == "missing":
        lines += ["- 状態：まだレポートが作成されていません。GitHub Actionsで該当Workflowを実行すると表示されます。"]
    else:
        if st.get("dependency_stale"):
            lines += [f"- 注意：{st.get('dependency_reason')}" ]
        if st.get("tv_candidate_applied_note"):
            lines += [f"- 状態：{st.get('tv_candidate_applied_note')}" ]
        lines += [f"- [開く]({href})"]
    return "\n".join(lines) + "\n"


def card_html(stem: str, label: str, href: str, st: Dict[str, Any]) -> str:
    status = str(st.get("status", "missing"))
    badge = status_badge(status)
    gen = format_jst(st.get("generated_at_jst"))
    status_class = html_escape(status)
    if status == "missing":
        action = "<p class='muted'>未生成：まだレポートが作成されていません。</p><p class='hint'>GitHub Actionsで該当Workflowを実行すると表示されます。</p>"
    else:
        note = f"<p class='hint'>注意：{html_escape(st.get('dependency_reason'))}</p>" if st.get("dependency_stale") else ""
        if st.get("tv_candidate_applied_note"):
            note += f"<p class='hint'>状態：{html_escape(st.get('tv_candidate_applied_note'))}</p>"
        action = note + f"<p><a href='latest/{html_escape(href)}'>開く</a></p>"
    return f"<div class='card status-{status_class}'><h2>{html_escape(badge)} {html_escape(label)}</h2><p>更新：{html_escape(gen)}</p>{action}</div>"


def write_home_error(message: str) -> None:
    """Write an explicit CIS Home error page so stale home pages do not look current."""
    now = now_jst()
    safe_message = str(message)
    md = "\n".join([
        "# CIS ホーム",
        "",
        f"最終更新：{now.strftime('%Y/%m/%d %H:%M JST')}",
        "",
        "## ❌ CISホーム生成エラー",
        "",
        safe_message,
        "",
        "## 確認ポイント",
        "",
        "- data/cis_settings.json のJSON形式や数値設定を確認してください。",
        "- 直前のGitHub Actionsログも確認してください。",
        "- このページは古いホームを最新に見せないためのエラー表示です。",
        "",
    ])
    status = {"status": "error", "generated_at_jst": now.isoformat(), "error": safe_message, "items": {}}
    write_text(DOCS_LATEST_DIR / "index.md", md)
    write_json(DOCS_LATEST_DIR / "index_status_latest.json", status)
    html = """<!doctype html><html lang='ja'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>CIS</title><style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:16px;line-height:1.55;background:#f7f7f7}.card{background:#fff;border-radius:14px;padding:14px;margin:12px 0;box-shadow:0 1px 4px #ddd}.error{border-left:5px solid #c00}</style></head><body><h1>CIS ホーム</h1><p>最終更新：%s</p><div class='card error'><h2>❌ CISホーム生成エラー</h2><p>%s</p><ul><li>data/cis_settings.json のJSON形式や数値設定を確認してください。</li><li>直前のGitHub Actionsログも確認してください。</li><li>このページは古いホームを最新に見せないためのエラー表示です。</li></ul></div></body></html>""" % (html_escape(now.strftime('%Y/%m/%d %H:%M JST')), html_escape(safe_message))
    write_text(DOCS_LATEST_DIR.parent / "index.html", html)


def build_home() -> int:
    now = now_jst()
    settings = load_settings()
    home_stale_days = settings.get("home_stale_days", {})
    sections: Dict[str, List[str]] = {}
    statuses: Dict[str, Dict[str, Any]] = {}
    alert_lines: List[str] = []
    for stem, label, href, section, max_age_days in ITEMS:
        st = mark_stale(load_status(stem), int(home_stale_days.get(stem, max_age_days)))
        statuses[stem] = st
    mark_dependency_stale(statuses)
    mark_tv_monthly_candidate_applied(statuses)
    mark_daily_freshness(statuses)
    for stem, label, href, section, max_age_days in ITEMS:
        st = statuses.get(stem, {"status": "missing"})
        sections.setdefault(section, []).append(card_markdown(stem, label, href, st))
        if st.get("status") in {"error", "partial", "stale", "price_stale"}:
            alert_lines.append(f"- {label}: {alert_reason(stem, st)}")
    md = ["# CIS ホーム", "", f"最終更新：{now.strftime('%Y/%m/%d %H:%M JST')}", ""]
    if alert_lines:
        md += ["## 要確認", ""] + alert_lines + [""]
    for section in ["毎日見る", "週末見る", "メンテナンス"]:
        md += [f"## {section}", ""] + sections.get(section, ["対象なし\n"])
    md_text = "\n".join(md)
    write_text(DOCS_LATEST_DIR / "index.md", md_text)
    write_json(DOCS_LATEST_DIR / "index_status_latest.json", {"status": "ok", "generated_at_jst": now.isoformat(), "items": statuses})
    cards: List[str] = []
    if alert_lines:
        alert_html = "".join(f"<li>{html_escape(line[2:] if line.startswith('- ') else line)}</li>" for line in alert_lines)
        cards.append(f"<div class='card warn'><h2>要確認</h2><ul>{alert_html}</ul></div>")
    for section in ["毎日見る", "週末見る", "メンテナンス"]:
        cards.append(f"<h2 class='section'>{html_escape(section)}</h2>")
        for stem, label, href, item_section, max_age_days in ITEMS:
            if item_section != section:
                continue
            cards.append(card_html(stem, label, href, statuses.get(stem, {})))
    html = """<!doctype html><html lang='ja'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>CIS</title><style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:16px;line-height:1.55;background:#f7f7f7}h1{font-size:28px}.section{font-size:20px;margin-top:24px}.card{background:#fff;border-radius:14px;padding:14px;margin:12px 0;box-shadow:0 1px 4px #ddd}.warn{border-left:6px solid #d98200}.status-error{border-left:6px solid #c00}.status-partial,.status-stale{border-left:6px solid #d98200}.status-missing{opacity:.82}.muted{color:#555}.hint{font-size:14px;color:#666}a{font-size:18px}</style></head><body><h1>CIS ホーム</h1><p>最終更新：%s</p>%s</body></html>""" % (html_escape(now.strftime('%Y/%m/%d %H:%M JST')), "\n".join(cards))
    write_text(DOCS_LATEST_DIR.parent / "index.html", html)
    return 0


def main() -> int:
    try:
        return build_home()
    except Exception as e:
        write_home_error(f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
