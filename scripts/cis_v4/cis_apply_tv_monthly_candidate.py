#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safely apply the latest CIS v4 TradingView monthly refresh candidate.

This script is the single guardrail for the iPhone one-tap TV candidate apply
workflow.  It validates the latest monthly refresh status, candidate manifest,
command file hash, command count and candidate age before invoking Master Update.

Important: do not split this validation and apply logic across separate GitHub
Actions steps.  A failed validation must never be followed by a Master Update.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from cis_core import DOCS_LATEST_DIR, ROOT, now_jst, read_json_strict, timestamp_jst, write_error_report, write_report

STEM = "apply_tv_monthly_candidate"
TITLE = "CIS TV月次候補反映"
VALID_STATUS = {"ok", "partial"}
VALID_MODES = {"apply_all_success", "changed_only"}
DEFAULT_MAX_AGE_DAYS = 45


def fail(message: str) -> None:
    raise RuntimeError(message)


def parse_mode() -> str:
    mode = os.getenv("APPLY_TV_MODE") or os.getenv("MODE") or (sys.argv[1] if len(sys.argv) > 1 else "apply_all_success")
    mode = str(mode).strip()
    if mode not in VALID_MODES:
        fail(f"modeが不正です: {mode} / apply_all_success または changed_only を指定してください。")
    return mode


def max_age_days() -> int:
    raw = os.getenv("CIS_TV_CANDIDATE_MAX_AGE_DAYS", str(DEFAULT_MAX_AGE_DAYS))
    try:
        n = int(str(raw).strip())
    except Exception:
        fail(f"CIS_TV_CANDIDATE_MAX_AGE_DAYS が整数ではありません: {raw}")
    if n <= 0:
        fail(f"CIS_TV_CANDIDATE_MAX_AGE_DAYS は正の整数が必要です: {raw}")
    return n


def parse_iso_dt(value: Any, label: str) -> datetime:
    if not value:
        fail(f"{label} がありません。")
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception as e:
        fail(f"{label} を日時として読めません: {value} / {type(e).__name__}: {e}")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_latest_status_and_manifest() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    status_path = DOCS_LATEST_DIR / "tv_monthly_refresh_status_latest.json"
    manifest_path = DOCS_LATEST_DIR / "tv_monthly_refresh_candidate_manifest.json"
    if not status_path.exists():
        fail("TradingView月次確認の最新statusがありません。先に CIS v4 TV Monthly Refresh を実行してください。")
    if not manifest_path.exists():
        fail("TradingView月次候補manifestがありません。先に CIS v4 TV Monthly Refresh を実行してください。")
    status = read_json_strict(status_path, default={}) or {}
    manifest = read_json_strict(manifest_path, default={}) or {}
    if not isinstance(status, dict):
        fail("TradingView月次確認statusがobjectではありません。")
    if not isinstance(manifest, dict):
        fail("TradingView月次候補manifestがobjectではありません。")
    return status, manifest


def validate_candidate(mode: str) -> Tuple[Path, Dict[str, Any], Dict[str, Any]]:
    status, manifest = load_latest_status_and_manifest()

    status_value = status.get("status")
    manifest_status = manifest.get("status")
    if status_value not in VALID_STATUS:
        fail(f"TradingView月次確認statusが {status_value!r} です。error状態の候補は反映しません。")
    if manifest_status not in VALID_STATUS:
        fail(f"TradingView月次候補manifest statusが {manifest_status!r} です。error状態の候補は反映しません。")

    status_ts = status.get("generated_at_jst")
    manifest_ts = manifest.get("generated_at_jst")
    if manifest_ts != status_ts:
        fail("manifestと最新statusの生成時刻が一致しません。候補ファイルが古い可能性があります。")

    generated_dt = parse_iso_dt(manifest_ts, "manifest generated_at_jst")
    age_days = (now_jst() - generated_dt).total_seconds() / 86400
    limit_days = max_age_days()
    if age_days > limit_days:
        fail(f"TradingView月次候補が古すぎます。生成から{age_days:.1f}日経過 / 上限{limit_days}日。月次確認を再実行してください。")

    primary = manifest.get("primary_files")
    if not isinstance(primary, dict):
        fail("manifestのprimary_filesが不正です。")
    filename = primary.get(mode)
    if not filename or not isinstance(filename, str):
        fail(f"manifestにmode={mode}用の候補ファイルがありません。")

    command_files = manifest.get("command_files")
    if not isinstance(command_files, dict):
        fail("manifestのcommand_filesが不正です。")
    meta = command_files.get(filename)
    if not isinstance(meta, dict):
        fail(f"候補ファイルがmanifestに登録されていません: {filename}")

    cmd_path = DOCS_LATEST_DIR / filename
    try:
        cmd_path.relative_to(DOCS_LATEST_DIR)
    except Exception:
        fail(f"候補ファイルのパスが不正です: {cmd_path}")
    if not cmd_path.exists() or cmd_path.stat().st_size <= 0:
        fail(f"候補コマンドファイルが存在しないか空です: {cmd_path}")

    actual_hash = sha256_file(cmd_path)
    expected_hash = meta.get("sha256")
    if not expected_hash or actual_hash != expected_hash:
        fail("候補コマンドファイルのhashがmanifestと一致しません。古い候補・編集済み候補は反映しません。")

    nonempty_lines = [line for line in cmd_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    line_count = int(meta.get("line_count") or 0)
    if line_count != len(nonempty_lines):
        fail(f"候補コマンド行数がmanifestと一致しません: manifest={line_count} actual={len(nonempty_lines)}")
    count_key = "apply_command_count" if mode == "apply_all_success" else "changed_command_count"
    manifest_count = int(manifest.get(count_key) or 0)
    if manifest_count <= 0:
        fail(f"mode={mode} で反映可能なコマンドが0件です。")
    if manifest_count != len(nonempty_lines):
        fail(f"manifestのコマンド件数と候補ファイル行数が一致しません: {manifest_count} vs {len(nonempty_lines)}")

    return cmd_path, status, manifest


def run_master_update(cmd_path: Path) -> int:
    commands = cmd_path.read_text(encoding="utf-8")
    env = dict(os.environ)
    env["COMMANDS"] = commands
    script = ROOT / "scripts" / "cis_v4" / "cis_master_update.py"
    result = subprocess.run([sys.executable, str(script)], cwd=str(ROOT), env=env, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        fail(f"Master Updateが失敗しました。exit={result.returncode}")
    return result.returncode


def write_success_report(mode: str, cmd_path: Path, status: Dict[str, Any], manifest: Dict[str, Any]) -> None:
    count_key = "apply_command_count" if mode == "apply_all_success" else "changed_command_count"
    count = int(manifest.get(count_key) or 0)
    generated_at = timestamp_jst()
    md = "\n".join([
        f"# {TITLE}",
        "",
        f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
        "",
        "## 反映結果",
        "",
        "- status：ok",
        f"- mode：{mode}",
        f"- 候補ファイル：{cmd_path.name}",
        f"- 反映コマンド数：{count}件",
        f"- 候補生成日時：{manifest.get('generated_at_jst')}",
        "- 反映方法：Master Update経由",
        "",
        "TVスナップショットはMaster Update経由で反映済みです。Daily US / Weekly / Buy Alert は保存済み tv_snapshot.json を再利用します。",
        "",
    ])
    report_status = {
        "status": "ok",
        "generated_at_jst": generated_at,
        "mode": mode,
        "command_file": cmd_path.name,
        "applied_command_count": count,
        "candidate_generated_at_jst": manifest.get("generated_at_jst"),
    }
    write_report(STEM, md, {"status": report_status, "tv_refresh_status": status, "manifest": manifest}, report_status)


def main() -> int:
    mode = ""
    try:
        mode = parse_mode()
        cmd_path, status, manifest = validate_candidate(mode)
        run_master_update(cmd_path)
        write_success_report(mode, cmd_path, status, manifest)
        return 0
    except Exception as e:
        message = f"{type(e).__name__}: {e}"
        write_error_report(STEM, TITLE, message)
        print(message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
