#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from cis_core import (
    DATA_DIR,
    JST,
    load_buyzone_master,
    load_tv_snapshot,
    load_watchlist,
    get_tv_snapshot_stale_days,
    now_jst,
    read_json_strict,
    timestamp_jst,
    validate_history_json,
    write_error_report,
    write_report,
)

STEM = "monthly_maintenance"
TITLE = "CIS 月次メンテナンス"
TV_STALE_DAYS = 45  # fallback; real value is loaded from data/cis_settings.json in main()


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


def load_history(limit: int = 20) -> List[Dict[str, Any]]:
    validate_history_json(DATA_DIR / "master_update_history.json", "master_update_history.json")
    data = read_json_strict(DATA_DIR / "master_update_history.json", default={"items": []}) or {"items": []}
    rows = data.get("items") if isinstance(data, dict) else []
    return list(reversed(rows[-limit:]))


def main() -> int:
    global TV_STALE_DAYS
    try:
        TV_STALE_DAYS = get_tv_snapshot_stale_days()
        items = load_watchlist(True)
        us_items = [x for x in items if x.market == "US"]
        tv = load_tv_snapshot()
        bz = load_buyzone_master()

        active_keys = {x.key for x in items}
        active_us_keys = {x.key for x in us_items}
        missing_tv = [x.key for x in us_items if x.key not in tv]
        covered_tv = [k for k, snap in tv.items() if snap.coverage_status == "covered"]
        no_coverage_tv = [k for k, snap in tv.items() if snap.coverage_status == "no_coverage"]
        not_applicable_tv = [k for k, snap in tv.items() if snap.coverage_status == "not_applicable"]
        stale_tv = []
        for k, snap in tv.items():
            a = age_days(snap.updated_at)
            if a is None or a > TV_STALE_DAYS:
                stale_tv.append(k)
        extra_tv = [k for k in tv.keys() if k not in active_us_keys]
        missing_bz = [x.key for x in items if x.key not in bz]
        extra_bz = [k for k in bz.keys() if k not in active_keys]
        history = load_history()

        warnings = []
        if missing_tv:
            warnings.append(f"TradingView未設定：{len(missing_tv)}銘柄")
        if stale_tv:
            warnings.append(f"TradingView鮮度注意：{len(stale_tv)}銘柄")
        if extra_tv:
            warnings.append(f"TradingViewにactive外データあり：{len(extra_tv)}銘柄")
        if missing_bz:
            warnings.append(f"買い場基準未設定：{len(missing_bz)}銘柄")
        if extra_bz:
            warnings.append(f"買い場基準にactive外データあり：{len(extra_bz)}銘柄")

        status_level = "partial" if warnings else "ok"
        status = {
            "status": status_level,
            "generated_at_jst": timestamp_jst(),
            "watchlist_count": len(items),
            "us_count": len(us_items),
            "tv_count": len(tv),
            "tv_covered_count": len(covered_tv),
            "tv_no_coverage_count": len(no_coverage_tv),
            "tv_not_applicable_count": len(not_applicable_tv),
            "tv_missing_count": len(missing_tv),
            "tv_stale_or_unknown_count": len(stale_tv),
            "tv_extra_count": len(extra_tv),
            "buyzone_count": len(bz),
            "buyzone_missing_count": len(missing_bz),
            "buyzone_extra_count": len(extra_bz),
            "warnings": warnings,
        }

        lines = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += [
            "## ステータス",
            "",
            f"- 監視銘柄：{len(items)}",
            f"- 米国株：{len(us_items)}",
            f"- TradingView保存：{len(tv)}",
            f"- TradingView covered：{len(covered_tv)}",
            f"- TradingView カバレッジなし：{len(no_coverage_tv)}",
            f"- TradingView 対象外：{len(not_applicable_tv)}",
            f"- TradingView未設定：{len(missing_tv)}",
            f"- TradingView鮮度注意：{len(stale_tv)}",
            f"- TradingView active外：{len(extra_tv)}",
            f"- 買い場基準：{len(bz)}",
            f"- 買い場基準未設定：{len(missing_bz)}",
            f"- 買い場基準 active外：{len(extra_bz)}",
            "",
        ]
        if warnings:
            lines += ["## 要確認", ""] + [f"- ⚠️ {w}" for w in warnings] + [""]
        lines += ["## TradingView 未設定/鮮度注意/対象外", ""]
        if not missing_tv and not stale_tv and not extra_tv and not no_coverage_tv and not not_applicable_tv:
            lines += ["変更・確認対象なし", ""]
        else:
            for x in missing_tv[:50]:
                lines.append(f"- 未設定：{x}")
            for x in stale_tv[:50]:
                lines.append(f"- 鮮度注意：{x}")
            for x in no_coverage_tv[:50]:
                lines.append(f"- カバレッジなし：{x}")
            for x in not_applicable_tv[:50]:
                lines.append(f"- 対象外：{x}")
            for x in extra_tv[:50]:
                lines.append(f"- active外：{x}")
            lines.append("")

        lines += ["## 買い場基準 未設定/active外", ""]
        if not missing_bz and not extra_bz:
            lines += ["未設定・active外なし", ""]
        else:
            lines += [f"- 未設定：{x}" for x in missing_bz[:80]]
            lines += [f"- active外：{x}" for x in extra_bz[:80]]
            lines.append("")

        lines += ["## 直近のマスター更新", ""]
        if not history:
            lines += ["履歴なし", ""]
        else:
            for h in history[:20]:
                lines.append(f"- {h.get('updated_at','')}｜{h.get('kind')} {h.get('market')} {h.get('symbol')}")
            lines.append("")

        write_report(STEM, "\n".join(lines), {"status": status, "history": history}, status)
        return 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
