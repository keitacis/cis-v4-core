#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch CIS v4 report display details.

This patch does two small, user-facing fixes in one pass:
1. JP cards show company names, not only theme/description text.
   - US cards keep the current ticker + theme behavior.
2. Buy Alert rule update timestamps are shortened for iPhone readability.
   - Example: 2026-07-05T22:16:43.799841+09:00 -> 2026/07/05 22:16 JST
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REPORT_TARGETS = [
    ROOT / "scripts" / "cis_v4" / "cis_daily_jp.py",
    ROOT / "scripts" / "cis_v4" / "cis_weekly_performance.py",
    ROOT / "scripts" / "cis_v4" / "cis_buy_alert.py",
]
BUY_ALERT = ROOT / "scripts" / "cis_v4" / "cis_buy_alert.py"

JP_OLD = '"description": item.description or item.notes,'
JP_NEW = '"description": item.name if item.market == "JP" else (item.description or item.notes),'

FMT_FUNC_NAME = "fmt_rule_updated_at"
FMT_ANCHOR = 'def validate_rule(rule: Optional[Dict[str, Any]]) -> List[str]:'
FMT_FUNC = '''def fmt_rule_updated_at(value: Any) -> str:\n    """Compact buy-zone rule timestamp for mobile display."""\n    if value is None:\n        return "未設定"\n    text = str(value).strip()\n    if not text:\n        return "未設定"\n    try:\n        dt = datetime.fromisoformat(text)\n        if dt.tzinfo is None:\n            dt = dt.replace(tzinfo=JST)\n        dt = dt.astimezone(JST)\n        # Keep minutes, drop seconds/microseconds/timezone noise.\n        return dt.strftime("%Y/%m/%d %H:%M JST")\n    except Exception:\n        # Safe fallback for date-like strings. Do not destroy unknown manual notes.\n        if "T" in text:\n            return text.split("T", 1)[0].replace("-", "/")\n        if len(text) >= 10 and text[4:5] == "-" and text[7:8] == "-":\n            return text[:10].replace("-", "/")\n        return text\n\n'''

RULE_DATE_OLD = 'f"- 基準更新日：{r.get(\'rule_updated_at\') or \'未設定\'}",'
RULE_DATE_NEW = 'f"- 基準更新日：{fmt_rule_updated_at(r.get(\'rule_updated_at\'))}",'


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"target file not found: {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def patch_jp_company_display(path: Path) -> str:
    text = read(path)
    if JP_NEW in text:
        return f"JP company display already patched: {path}"
    if JP_OLD not in text:
        raise RuntimeError(f"expected JP display pattern not found in {path}: {JP_OLD}")
    write(path, text.replace(JP_OLD, JP_NEW))
    return f"JP company display patched: {path}"


def patch_buy_alert_rule_date(path: Path) -> str:
    text = read(path)
    changed = False

    if FMT_FUNC_NAME not in text:
        if FMT_ANCHOR not in text:
            raise RuntimeError(f"expected format anchor not found in {path}: {FMT_ANCHOR}")
        text = text.replace(FMT_ANCHOR, FMT_FUNC + FMT_ANCHOR, 1)
        changed = True

    if RULE_DATE_NEW not in text:
        if RULE_DATE_OLD not in text:
            raise RuntimeError(f"expected rule date pattern not found in {path}: {RULE_DATE_OLD}")
        text = text.replace(RULE_DATE_OLD, RULE_DATE_NEW, 1)
        changed = True

    if changed:
        write(path, text)
        return f"Buy Alert rule date display patched: {path}"
    return f"Buy Alert rule date display already patched: {path}"


def main() -> int:
    messages = []
    for path in REPORT_TARGETS:
        messages.append(patch_jp_company_display(path))
    messages.append(patch_buy_alert_rule_date(BUY_ALERT))
    print("\n".join(messages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
