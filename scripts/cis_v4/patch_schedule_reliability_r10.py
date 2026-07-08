#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch CIS Home for R10.4 schedule reliability checks.

R10.4 keeps the R10.3 catch-up design but hardens the patcher itself against
minor formatting differences in cis_home.py. The patch still touches only
non-workflow runtime files so GitHub Actions can commit it with contents:write.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / "scripts" / "cis_v4" / "cis_home.py"
BACKUP = ROOT / "data" / "backups" / "cis_home.py.before_r10_schedule_reliability.bak"
MARKER = "# --- CIS R10 daily freshness guard START ---"

R10_BLOCK = r'''
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
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"patch failed: marker not found: {label}")
    return text.replace(old, new, 1)


def ensure_import_json(text: str) -> str:
    if re.search(r"(^|\n)import json(\n|$)", text):
        return text
    future = "from __future__ import annotations\n"
    if future in text:
        return text.replace(future, future + "import json\n", 1)
    if "import sys\n" in text:
        return text.replace("import sys\n", "import sys\nimport json\n", 1)
    raise SystemExit("patch failed: could not find a safe location for import json")


def ensure_core_import(text: str) -> str:
    if "expected_daily_trade_date" in text:
        return text
    pattern = re.compile(r"from cis_core import ([^\n]+)")

    def repl(m: re.Match[str]) -> str:
        names = m.group(1).strip()
        if names.startswith("("):
            return m.group(0)
        return "from cis_core import expected_daily_trade_date, " + names

    new_text, n = pattern.subn(repl, text, count=1)
    if n:
        return new_text
    raise SystemExit("patch failed: could not update cis_core import")


def ensure_schedule_item(text: str) -> str:
    if '"schedule_catchup"' in text:
        return text
    item_line = '("daily_jp", "日本株騰落", "daily_jp_latest.html", "毎日見る", 2),'
    new_item = item_line + '\n    ("schedule_catchup", "自動更新取りこぼし確認", "schedule_catchup_latest.html", "メンテナンス", 2),'
    if item_line in text:
        return text.replace(item_line, new_item, 1)
    weekly = '("weekly_performance", "週間騰落", "weekly_performance_latest.html", "週末見る", 9),'
    if weekly in text:
        return text.replace(weekly, '("schedule_catchup", "自動更新取りこぼし確認", "schedule_catchup_latest.html", "メンテナンス", 2),\n    ' + weekly, 1)
    raise SystemExit("patch failed: could not insert schedule_catchup item")


def ensure_r10_block(text: str) -> str:
    if MARKER in text:
        return text
    marker = "def alert_reason(stem: str, st: Dict[str, Any]) -> str:"
    if marker not in text:
        raise SystemExit("patch failed: alert_reason marker not found")
    return text.replace(marker, R10_BLOCK + "\n\n" + marker, 1)


def ensure_r10_call(text: str) -> str:
    if "mark_daily_freshness(statuses)" in text:
        return text
    marker = "mark_tv_monthly_candidate_applied(statuses)"
    if marker not in text:
        raise SystemExit("patch failed: mark_tv_monthly_candidate_applied call not found")
    return text.replace(marker, marker + "\n    mark_daily_freshness(statuses)", 1)


def main() -> int:
    if not HOME.exists():
        raise SystemExit(f"missing file: {HOME}")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(HOME, BACKUP)

    text = HOME.read_text(encoding="utf-8")
    if MARKER in text and "mark_daily_freshness(statuses)" in text and '"schedule_catchup"' in text:
        print("R10 home freshness guard already present")
        return 0

    text = ensure_import_json(text)
    text = ensure_core_import(text)
    text = ensure_schedule_item(text)
    text = ensure_r10_block(text)
    text = ensure_r10_call(text)

    HOME.write_text(text, encoding="utf-8")
    print("R10.4 schedule reliability patch applied to cis_home.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
