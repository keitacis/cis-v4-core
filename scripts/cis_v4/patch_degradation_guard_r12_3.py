#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply CIS v4 R12.3 degradation guard.

R12.3 intentionally avoids fragile regex replacement for write_report().
The current cis_core.py may be formatted with many definitions on one physical
line, so this patch replaces the substring between `def write_report(` and
`def write_error_report(`.
"""
from __future__ import annotations

from pathlib import Path
import py_compile
import textwrap

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "scripts" / "cis_v4" / "cis_core.py"
README = ROOT / "README_degradation_guard_r12.md"

R12_BLOCK = r'''
# --- CIS R12 degradation guard START ---
DEGRADATION_GUARD_STEMS = {"daily_jp", "daily_us", "buy_alert"}


def _r12_status_name(status: Dict[str, Any]) -> str:
    if not isinstance(status, dict):
        return ""
    return str(status.get("status") or "").strip().lower()


def _r12_existing_status_for_guard(stem: str) -> Dict[str, Any]:
    try:
        data = read_json(report_paths(stem)["docs_status"], default={}) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _r12_should_guard_degradation(stem: str, payload: Dict[str, Any], status: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Return True when a stale follow-up run should not overwrite a good latest.

    This is deliberately conservative. It only blocks first-class price_stale
    reports for the daily/buy-alert reports after a previous ok/partial latest
    already exists. Missing/error reports are not hidden by this guard.
    """
    if stem not in DEGRADATION_GUARD_STEMS:
        return False, {}
    if _r12_status_name(status) != "price_stale":
        return False, {}
    existing = _r12_existing_status_for_guard(stem)
    existing_status = _r12_status_name(existing)
    if existing_status not in {"ok", "partial"}:
        return False, existing
    return True, existing


def _r12_write_degraded_attempt(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> None:
    attempt_stem = f"{stem}_degraded_attempt"
    paths = report_paths(attempt_stem)
    attempt_status = dict(status or {})
    attempt_status["degradation_guard_attempt"] = True
    attempt_status["guarded_stem"] = stem
    attempt_status["stored_at_jst"] = timestamp_jst()
    for k in ["output_md", "docs_md"]:
        write_text(paths[k], markdown)
    write_text(paths["docs_html"], markdown_to_simple_html(markdown, attempt_stem))
    attempt_payload = payload if isinstance(payload, dict) else {"payload": payload}
    for k in ["output_json", "docs_json"]:
        write_json(paths[k], attempt_payload)
    for k in ["output_status", "docs_status"]:
        write_json(paths[k], attempt_status)


def write_report(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> None:
    paths = report_paths(stem)
    should_guard, existing = _r12_should_guard_degradation(stem, payload, status)
    if should_guard:
        _r12_write_degraded_attempt(stem, markdown, payload, status)
        guarded_status = dict(existing or {})
        guarded_status["status"] = "partial"
        guarded_status["generated_at_jst"] = timestamp_jst()
        guarded_status["degradation_guard_triggered"] = True
        guarded_status["degradation_guard_version"] = "R12.3"
        guarded_status["degradation_guard_source_status"] = _r12_status_name(status)
        guarded_status["retained_latest_generated_at_jst"] = existing.get("generated_at_jst")
        guarded_status["degraded_attempt_stem"] = f"{stem}_degraded_attempt"
        guarded_status["message"] = (
            "劣化上書き防止：価格未更新の実行結果だったため、"
            f"{stem} の正常なlatest本文を保持しました。"
        )
        warnings = []
        incoming_warnings = status.get("warnings") if isinstance(status, dict) else None
        if isinstance(incoming_warnings, list):
            warnings.extend(str(x) for x in incoming_warnings[:3])
        warnings.insert(0, guarded_status["message"])
        guarded_status["warnings"] = warnings
        for k in ["output_status", "docs_status"]:
            write_json(paths[k], guarded_status)
        return

    for k in ["output_md", "docs_md"]:
        write_text(paths[k], markdown)
    write_text(paths["docs_html"], markdown_to_simple_html(markdown, stem))
    for k in ["output_json", "docs_json"]:
        write_json(paths[k], payload)
    for k in ["output_status", "docs_status"]:
        write_json(paths[k], status)

# --- CIS R12 degradation guard END ---
'''.strip() + "\n"

README_TEXT = """# CIS v4 Degradation Guard R12.3

R12.3 applied.

- Protected stems: `daily_jp`, `daily_us`, `buy_alert`
- Guard condition: incoming report status is `price_stale` and existing latest status is `ok` or `partial`
- Behavior: retain latest Markdown/HTML/JSON, update status to `partial`, and save the rejected stale run as `*_degraded_attempt_latest.*`

This patch intentionally replaces the current `write_report()` implementation by locating the text range from `def write_report(` to `def write_error_report(`. This avoids brittle regex matching against the current compact formatting of `cis_core.py`.
"""


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> tuple[str, bool]:
    start = text.find(start_marker)
    if start < 0:
        return text, False
    end = text.find(end_marker, start)
    if end < 0:
        return text, False
    return text[:start] + replacement + text[end:], True


def patch_core() -> bool:
    text = CORE.read_text(encoding="utf-8")
    marker_start = "# --- CIS R12 degradation guard START ---"
    marker_end = "# --- CIS R12 degradation guard END ---"

    if marker_start in text and marker_end in text:
        block_start = text.find(marker_start)
        block_end = text.find(marker_end, block_start)
        block_end = text.find("\n", block_end)
        if block_end < 0:
            block_end = len(text)
        else:
            block_end += 1
        new_text = text[:block_start] + R12_BLOCK + text[block_end:]
    else:
        new_text, ok = replace_between(text, "def write_report(", "def write_error_report(", R12_BLOCK)
        if not ok:
            raise RuntimeError("Could not find write_report boundaries in cis_core.py")

    if new_text != text:
        CORE.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = patch_core()
    README.write_text(README_TEXT, encoding="utf-8")
    py_compile.compile(str(CORE), doraise=True)
    print("R12.3 degradation guard applied" if changed else "R12.3 degradation guard already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
