#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply CIS v4 R12.1 degradation overwrite guard.

R12.1 prevents a known failure mode: a healthy latest report can be overwritten
later by an all-price-stale report when a price source returns old data during
night/early-morning runs. It keeps the existing report body/json, writes only a
warning status for the protected report, and stores the rejected degraded attempt
as a separate diagnostic artifact.
"""
from __future__ import annotations

import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "scripts" / "cis_v4" / "cis_core.py"
HOME = ROOT / "scripts" / "cis_v4" / "cis_home.py"
README = ROOT / "README_degradation_guard_r12.md"

CORE_MARKER = "# --- CIS R12 degradation overwrite guard START ---"

R12_CORE_CODE = r'''
# --- CIS R12 degradation overwrite guard START ---
_R12_PROTECTED_STEMS = {"daily_jp", "daily_us", "buy_alert"}
_R12_DEGRADED_STATUSES = {"price_stale"}

def _r12_report_file_write(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> None:
    paths = report_paths(stem)
    for k in ["output_md", "docs_md"]:
        write_text(paths[k], markdown)
    write_text(paths["docs_html"], markdown_to_simple_html(markdown, stem))
    for k in ["output_json", "docs_json"]:
        write_json(paths[k], payload)
    for k in ["output_status", "docs_status"]:
        write_json(paths[k], status)

def _r12_status_write_only(stem: str, status: Dict[str, Any]) -> None:
    paths = report_paths(stem)
    for k in ["output_status", "docs_status"]:
        write_json(paths[k], status)

def _r12_date_values(status: Dict[str, Any]) -> List[str]:
    vals: List[str] = []
    for k in ["expected_price_date", "expected_us_price_date", "expected_jp_price_date"]:
        v = status.get(k)
        if v:
            s = str(v)[:10]
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
                vals.append(s)
    return sorted(set(vals))

def _r12_is_degraded(stem: str, status: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    if stem not in _R12_PROTECTED_STEMS:
        return False
    s = str((status or {}).get("status") or "")
    if s in _R12_DEGRADED_STATUSES:
        return True
    stale = safe_int((status or {}).get("price_stale_count"))
    totals = [
        safe_int((status or {}).get("jp_count")),
        safe_int((status or {}).get("us_count")),
        safe_int((status or {}).get("watchlist_count")),
        safe_int((status or {}).get("price_success_count")),
    ]
    totals = [x for x in totals if x is not None and x > 0]
    if stale is not None and stale > 0 and totals and stale >= max(totals):
        return True
    return False

def _r12_existing_can_be_preserved(stem: str, incoming_status: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
    paths = report_paths(stem)
    existing = read_json(paths["docs_status"], default={}) or {}
    if not isinstance(existing, dict):
        return False, {}, "existing_status_not_dict"
    if existing.get("status") not in {"ok", "partial"}:
        return False, existing, f"existing_status_not_preservable:{existing.get('status')}"
    existing_dates = _r12_date_values(existing)
    incoming_dates = _r12_date_values(incoming_status)
    if existing_dates and incoming_dates and max(existing_dates) < max(incoming_dates):
        return False, existing, f"existing_expected_date_older:{existing_dates} < {incoming_dates}"
    return True, existing, "preserve_existing_latest"

def _r12_guard_markdown(stem: str, incoming_status: Dict[str, Any], existing_status: Dict[str, Any], reason: str, original_markdown: str) -> str:
    now = now_jst().strftime('%Y/%m/%d %H:%M JST')
    lines = [
        "# CIS 劣化上書き防止 R12",
        "",
        f"生成日時：{now}",
        "",
        "## 判定",
        "",
        f"- 対象：{stem}",
        f"- 判定：既存の正常レポートを保持しました。",
        f"- 理由：{reason}",
        f"- 既存レポート生成：{existing_status.get('generated_at_jst') or '不明'}",
        f"- 今回ステータス：{incoming_status.get('status') or '不明'}",
        "",
        "## 重要",
        "",
        "この実行では、古い価格日付の結果で latest 本文・latest JSON を上書きしていません。",
        "警告ステータスと診断用の rejected attempt だけを保存します。",
        "",
        "---",
        "",
        "## 上書きせず退避した今回レポート",
        "",
        original_markdown,
        "",
    ]
    return "\n".join(lines)

def _r12_handle_degraded_write(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> bool:
    if not _r12_is_degraded(stem, status, payload):
        return False
    keep, existing, reason = _r12_existing_can_be_preserved(stem, status)
    if not keep:
        return False
    now_iso = timestamp_jst()
    attempt_stem = f"{stem}_degraded_attempt"
    attempt_status = dict(status or {})
    attempt_status.update({
        "status": "partial",
        "generated_at_jst": now_iso,
        "r12_degraded_attempt": True,
        "protected_stem": stem,
        "r12_preserve_reason": reason,
    })
    attempt_payload = {
        "status": attempt_status,
        "protected_stem": stem,
        "incoming_status": status,
        "existing_status": existing,
        "incoming_payload": payload,
    }
    _r12_report_file_write(
        attempt_stem,
        _r12_guard_markdown(stem, status, existing, reason, markdown),
        attempt_payload,
        attempt_status,
    )
    message = f"劣化上書き防止：{stem} の正常なlatest本文を保持しました。今回の価格未更新結果は退避しました。"
    protected_status = dict(status or {})
    protected_status.update({
        "status": "partial",
        "generated_at_jst": now_iso,
        "message": message,
        "warnings": [message] + [str(x) for x in (status or {}).get("warnings", []) if str(x) != message],
        "r12_degradation_guard": True,
        "protected_existing_report": True,
        "protected_stem": stem,
        "protected_report_generated_at_jst": existing.get("generated_at_jst"),
        "incoming_status_before_guard": (status or {}).get("status"),
        "degraded_attempt_stem": attempt_stem,
        "degraded_attempt_latest_html": f"{attempt_stem}_latest.html",
        "existing_status_before_guard": existing,
    })
    _r12_status_write_only(stem, protected_status)
    guard_status = {
        "status": "partial",
        "generated_at_jst": now_iso,
        "message": message,
        "protected_stem": stem,
        "protected_report_generated_at_jst": existing.get("generated_at_jst"),
        "degraded_attempt_stem": attempt_stem,
        "warnings": [message],
    }
    guard_payload = {
        "status": guard_status,
        "protected_stem": stem,
        "incoming_status": status,
        "existing_status": existing,
        "degraded_attempt_stem": attempt_stem,
    }
    guard_md = "\n".join([
        "# CIS 劣化上書き防止 R12",
        "",
        f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
        "",
        "## 直近の保護",
        "",
        f"- 対象：{stem}",
        f"- 状態：{message}",
        f"- 保持した既存レポート生成：{existing.get('generated_at_jst') or '不明'}",
        f"- 退避先：{attempt_stem}",
        "",
    ])
    _r12_report_file_write("degradation_guard", guard_md, guard_payload, guard_status)
    return True

def write_report(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> None:
    if _r12_handle_degraded_write(stem, markdown, payload, status):
        return
    _r12_report_file_write(stem, markdown, payload, status)
# --- CIS R12 degradation overwrite guard END ---
'''.strip()


def patch_core() -> bool:
    text = CORE.read_text(encoding="utf-8")
    if CORE_MARKER in text:
        return False
    pattern = (
        r'def write_report\(stem: str, markdown: str, payload: Dict\[str, Any\], status: Dict\[str, Any\]\) -> None: '
        r'paths = report_paths\(stem\) '
        r'for k in \["output_md", "docs_md"\]: write_text\(paths\[k\], markdown\) '
        r'write_text\(paths\["docs_html"\], markdown_to_simple_html\(markdown, stem\)\) '
        r'for k in \["output_json", "docs_json"\]: write_json\(paths\[k\], payload\) '
        r'for k in \["output_status", "docs_status"\]: write_json\(paths\[k\], status\)'
    )
    new_text, n = re.subn(pattern, R12_CORE_CODE, text, count=1)
    if n != 1:
        raise RuntimeError("Could not find current write_report implementation in cis_core.py")
    CORE.write_text(new_text, encoding="utf-8")
    return True


def patch_home() -> bool:
    """Teach Home to show R12 guard reason in daily cards.

    No new always-visible card is added, so users do not see a permanent
    'missing degradation guard' card. The affected daily card itself becomes
    partial with an explicit R12 message when protection fires.
    """
    text = HOME.read_text(encoding="utf-8")
    marker = "# --- CIS R12 alert reason START ---"
    if marker in text:
        return False
    old = 'if status == "price_stale": warnings = st.get("warnings") or []'
    new = (
        marker
        + '\n    if st.get("r12_degradation_guard"):\n'
        + '        return str(st.get("message") or "劣化上書き防止が作動しました")\n'
        + '    # --- CIS R12 alert reason END ---\n    '
        + old
    )
    if old not in text:
        raise RuntimeError("Could not find alert_reason price_stale branch in cis_home.py")
    text = text.replace(old, new, 1)
    HOME.write_text(text, encoding="utf-8")
    return True


def write_readme() -> None:
    README.write_text(
        """# CIS v4 R12.1 劣化上書き防止パッチ

R12.1 は、正常な latest レポートがある状態で、後続実行が全銘柄 `price_stale` / 価格未更新を返した場合に、その悪い結果で latest 本文・latest JSON を上書きしないためのガードです。

## 目的

- 夜中・早朝の価格ソース遅延で、正常だった `daily_jp_latest` などが価格未更新レポートに劣化上書きされるのを防ぐ。
- 既存の正常レポート本文と JSON は保持する。
- ただし、ステータスは `partial` にして Home の要確認に表示する。
- 上書きしなかった悪い結果は `<stem>_degraded_attempt_latest.*` に退避する。

## 対象

- `daily_jp`
- `daily_us`
- `buy_alert`

## 期待されるiPhone表示

日本株で夜中に古い価格データが返った場合、`価格未更新 日本株騰落` に本文まで上書きされず、日本株カードは `一部注意` として「劣化上書き防止」が表示されます。夕方に正常価格が取得できれば通常の `更新済み` に戻ります。

## 適用後の確認

1. `CIS v4 Degradation Guard Patch R12.1` を手動実行。
2. 緑成功を確認。
3. 必要なら Home を1回実行。
4. 翌朝、夜中の価格未更新で daily_jp latest 本文が劣化上書きされていないか確認。
""",
        encoding="utf-8",
    )


def main() -> int:
    changed = []
    if patch_core():
        changed.append(str(CORE.relative_to(ROOT)))
    if patch_home():
        changed.append(str(HOME.relative_to(ROOT)))
    write_readme()
    changed.append(str(README.relative_to(ROOT)))
    py_compile.compile(str(CORE), doraise=True)
    py_compile.compile(str(HOME), doraise=True)
    print("R12.1 patch applied. Changed:")
    for item in changed:
        print("-", item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
