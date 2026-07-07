#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 R9 patch: TV Monthly Refresh no_coverage/not_applicable exclusion.

Purpose:
- KITT / OPTX can stay in the watchlist and price reports.
- If data/tv_snapshot.json already marks a US symbol as no_coverage or not_applicable,
  TV Monthly Refresh should not scan it and should not count it as a failed TV fetch.
- This patch modifies only scripts/cis_v4/cis_tv_monthly_refresh.py.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "scripts" / "cis_v4" / "cis_tv_monthly_refresh.py"

MARKER = "CIS_V4_TV_MONTHLY_NO_COVERAGE_R9"

INSERT_NORMAL = '''\n            # CIS_V4_TV_MONTHLY_NO_COVERAGE_R9\n            # If a symbol is already explicitly registered as no_coverage/not_applicable,\n            # do not try to fetch TradingView analyst data again and do not count it as failure.\n            old = old_map.get(item.key)\n            old_cov = getattr(old, "coverage_status", None)\n            if old_cov in {"no_coverage", "not_applicable"}:\n                new = {\n                    "symbol": sym,\n                    "market": "US",\n                    "coverage_status": old_cov,\n                    "rating": None,\n                    "analyst_count": None,\n                    "avg_target_price": None,\n                    "source": getattr(old, "source", None) or "CIS tv_snapshot",\n                    "reason": getattr(old, "reason", None) or ("TradingView analyst forecast not tracked" if old_cov == "no_coverage" else "TradingView analyst forecast not applicable"),\n                }\n                unchanged.append({\n                    "key": item.key,\n                    "symbol": sym,\n                    "name": item.name,\n                    "old": old.__dict__ if old else None,\n                    "new": new,\n                    "resolution_label": "保存済み対象外/カバレッジなし：月次取得対象外",\n                })\n                continue\n'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"target pattern not found: {label}")
    return text.replace(old, new, 1)


def main() -> int:
    if not TARGET.exists():
        raise FileNotFoundError(TARGET)
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("R9 already applied")
        return 0

    # First try the normally formatted source.
    normal_target = """        for item in items:\n            sym = item.symbol\n            if sym in ETF_NOT_APPLICABLE:\n"""
    normal_replacement = """        for item in items:\n            sym = item.symbol\n""" + INSERT_NORMAL + """            if sym in ETF_NOT_APPLICABLE:\n"""

    if normal_target in text:
        text = replace_once(text, normal_target, normal_replacement, "monthly loop normal")
    else:
        # Some previous patches compressed the file heavily. Use a compact fallback.
        compact_target = "for item in items: sym = item.symbol if sym in ETF_NOT_APPLICABLE:"
        compact_replacement = (
            "for item in items: sym = item.symbol\n"
            + INSERT_NORMAL
            + "            if sym in ETF_NOT_APPLICABLE:"
        )
        text = replace_once(text, compact_target, compact_replacement, "monthly loop compact")

    # Clarify the report policy text. Do not fail if the wording changed.
    policy_old = '"- not_applicable：EWYなどETFの対象外明示",'
    policy_new = (
        '"- not_applicable：EWYなどETFの対象外明示",\n'
        '        "- no_coverage / not_applicable：保存済み対象外は月次取得失敗に数えない",'
    )
    if policy_old in text and "保存済み対象外は月次取得失敗に数えない" not in text:
        text = text.replace(policy_old, policy_new, 1)

    # Add an explicit note to the status JSON if possible.
    status_note_old = '"note": "候補生成のみ。本番tv_snapshot.jsonは変更していません。",'
    status_note_new = (
        '"note": "候補生成のみ。本番tv_snapshot.jsonは変更していません。no_coverage/not_applicableは月次取得失敗に数えません。",'
    )
    if status_note_old in text:
        text = text.replace(status_note_old, status_note_new, 1)

    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print("Applied CIS v4 TV Monthly no_coverage R9 patch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
