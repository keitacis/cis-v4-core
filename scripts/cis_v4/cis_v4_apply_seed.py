#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safely copy CIS v4 seed master files from data/v4_seed to data/.

Default behavior is intentionally conservative: copy only missing files. Existing
root master files are never overwritten unless an explicit confirmation string is
provided.  Before any root data is touched, both the seed set and the staged
resulting master set are validated so broken seed or broken root/seed mixtures
cannot be committed into data/*.
"""
from __future__ import annotations
import html
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

JST = timezone(timedelta(hours=9))
SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[2] if SCRIPT.parent.name == "cis_v4" else SCRIPT.parents[1]
DATA = ROOT / "data"
SEED = DATA / "v4_seed"
BACKUP = DATA / "backups"
DOCS = ROOT / "docs" / "v4" / "latest"
OUTPUT = ROOT / "output" / "v4"
FILES = [
    "watchlist_master.csv", "company_master.csv", "buyzone_master.json",
    "tv_snapshot.json", "cis_settings.json", "watchlist_history.json",
    "master_update_history.json",
]
for d in [BACKUP, DOCS, OUTPUT]:
    d.mkdir(parents=True, exist_ok=True)

# Use the same strict validators as the v4 runtime before copying seed into root data.
# This prevents a broken seed file from polluting data/*.
import cis_core as core  # type: ignore  # noqa: E402
from cis_core import (  # type: ignore  # noqa: E402
    load_watchlist,
    load_company_master,
    load_tv_snapshot,
    load_buyzone_master,
    load_settings,
    validate_history_json,
    validate_watchlist_company_consistency,
)


def now(): return datetime.now(JST)

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8")

def write_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def simple_html(md: str) -> str:
    body: List[str] = []
    in_ul = False
    in_pre = False
    for line in md.splitlines():
        if line.startswith("```"):
            if in_ul:
                body.append("</ul>"); in_ul = False
            if in_pre:
                body.append("</pre>"); in_pre = False
            else:
                body.append("<pre>"); in_pre = True
            continue
        if in_pre:
            body.append(html.escape(line))
            continue
        if line.startswith("# "):
            if in_ul:
                body.append("</ul>"); in_ul = False
            body.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_ul:
                body.append("</ul>"); in_ul = False
            body.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_ul:
                body.append("<ul>"); in_ul = True
            body.append(f"<li>{html.escape(line[2:])}</li>")
        elif not line.strip():
            if in_ul:
                body.append("</ul>"); in_ul = False
        else:
            if in_ul:
                body.append("</ul>"); in_ul = False
            body.append(f"<p>{html.escape(line)}</p>")
    if in_pre:
        body.append("</pre>")
    if in_ul:
        body.append("</ul>")
    return """<!doctype html><html lang='ja'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>CIS v4 Apply Seed</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:16px;line-height:1.55}li{margin:6px 0}pre{white-space:pre-wrap;background:#f6f6f6;border-radius:10px;padding:12px;overflow:auto}h1,h2{line-height:1.25}</style></head><body><p><a href='../index.html'>CISホームへ戻る</a></p>""" + "\n".join(body) + "<p><a href='../index.html'>CISホームへ戻る</a></p></body></html>"

def backup(path: Path, label: str) -> Path:
    ts = now().strftime("%Y%m%d_%H%M%S")
    out = BACKUP / f"{path.name}.{ts}.{label}.bak"
    shutil.copy2(path, out)
    return out


def _with_data_dir(data_dir: Path, fn: Callable[[], Any]) -> Any:
    """Run a cis_core validator against an arbitrary data directory."""
    original = core.DATA_DIR
    try:
        core.DATA_DIR = data_dir
        return fn()
    finally:
        core.DATA_DIR = original


def _history_count(data_dir: Path, name: str) -> int:
    return validate_history_json(data_dir / name, name)


def _validate_master_set(data_dir: Path, label: str, require_all: bool = True) -> Tuple[List[str], Dict[str, Any]]:
    """Validate a complete CIS master set under data_dir.

    Returns human-readable summary lines and count metadata.  Raises on any
    structural error.  The function does not write anything.
    """
    if require_all:
        missing = [name for name in FILES if not (data_dir / name).exists()]
        if missing:
            raise ValueError(f"{label}ファイル不足: " + ", ".join(missing))
    lines: List[str] = []
    meta: Dict[str, Any] = {}
    checks: List[Tuple[str, Callable[[], Any], Callable[[Any], int]]] = [
        ("company_master.csv", load_company_master, lambda obj: len(obj)),
        ("watchlist_master.csv", lambda: load_watchlist(active_only=False), lambda obj: len(obj)),
        ("tv_snapshot.json", load_tv_snapshot, lambda obj: len(obj)),
        ("buyzone_master.json", load_buyzone_master, lambda obj: len(obj)),
        ("cis_settings.json", load_settings, lambda obj: len(obj)),
    ]
    for name, validator, counter in checks:
        if not (data_dir / name).exists():
            continue
        try:
            obj = _with_data_dir(data_dir, validator)
            count = counter(obj)
            meta[name] = count
            lines.append(f"{label}{name}: OK / count={count}")
        except Exception as e:
            raise ValueError(f"{label}{name} がv4マスターとして不正です: {type(e).__name__}: {e}") from e
    for name in ["watchlist_history.json", "master_update_history.json"]:
        if not (data_dir / name).exists():
            continue
        try:
            count = _history_count(data_dir, name)
            meta[name] = count
            lines.append(f"{label}{name}: OK / count={count}")
        except Exception as e:
            raise ValueError(f"{label}{name} が不正です: {type(e).__name__}: {e}") from e
    if (data_dir / "watchlist_master.csv").exists() and (data_dir / "company_master.csv").exists():
        try:
            consistency = _with_data_dir(data_dir, validate_watchlist_company_consistency)
            meta["watchlist_company_consistency"] = consistency
            extra = int(consistency.get("extra_company_count", 0))
            suffix = f" / company_master側の追加候補={extra}件" if extra else ""
            lines.append("watchlist/company整合性: OK" + suffix)
        except Exception as e:
            raise ValueError(f"{label}watchlist/company整合性NG: {type(e).__name__}: {e}") from e
    return lines, meta


def validate_seed_before_copy() -> Tuple[List[str], List[str], Dict[str, Any]]:
    """Return (errors, summary_lines, meta). No seed file is copied when errors exist."""
    if not SEED.exists():
        return ["data/v4_seed がありません。"], [], {}
    errors: List[str] = []
    try:
        lines, meta = _validate_master_set(SEED, "data/v4_seed/", require_all=True)
        return [], lines, meta
    except Exception as e:
        errors.append(str(e))
        return errors, [], {}


def _stage_resulting_data(mode: str) -> Tuple[Path, tempfile.TemporaryDirectory[str]]:
    """Create a temporary data directory representing the post-apply root data."""
    tmp_obj: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory(prefix="cis_v4_apply_seed_stage_")
    tmp = Path(tmp_obj.name)
    if mode == "overwrite_after_backup":
        for name in FILES:
            shutil.copy2(SEED / name, tmp / name)
        return tmp, tmp_obj
    # missing_only: existing root files are protected, missing files come from seed.
    for name in FILES:
        root_path = DATA / name
        src = root_path if root_path.exists() else SEED / name
        shutil.copy2(src, tmp / name)
    return tmp, tmp_obj


def validate_staged_result_before_copy(mode: str) -> Tuple[List[str], List[str], Dict[str, Any]]:
    """Validate the exact master set that would exist after Apply Seed."""
    errors: List[str] = []
    tmp: Path | None = None
    tmp_obj: tempfile.TemporaryDirectory[str] | None = None
    try:
        tmp, tmp_obj = _stage_resulting_data(mode)
        lines, meta = _validate_master_set(tmp, "staged data/", require_all=True)
        return [], lines, meta
    except Exception as e:
        errors.append(str(e))
        return errors, [], {}
    finally:
        if tmp_obj is not None:
            tmp_obj.cleanup()


def _atomic_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp_cis_v4_seed")
    if tmp.exists():
        tmp.unlink()
    shutil.copy2(src, tmp)
    os.replace(tmp, dst)


def build_report(status: str, actions: List[str], errors: List[str], checks: List[str] | None = None) -> int:
    generated = now()
    md = ["# CIS v4 Apply Seed", "", f"生成日時：{generated.strftime('%Y/%m/%d %H:%M JST')}", "", f"総合判定：{status}", ""]
    if errors:
        heading = "保護停止" if status == "partial" else "エラー"
        md += [f"## {heading}", ""] + [f"- {e}" for e in errors] + [""]
    if checks:
        md += ["## 事前検査", ""] + [f"- {c}" for c in checks] + [""]
    md += ["## 実行内容", ""] + ([f"- {a}" for a in actions] or ["- 変更なし"]) + [""]
    md += ["## 注意", "", "- 既存root dataを不用意に上書きしないための安全Workflowです。", "- 既存ファイルがある場合は原則停止します。", "- missing_onlyでも、既存rootとseedを合わせたstaged dataがv4厳格検査NGなら何もコピーしません。", "- 上書きはバックアップ後のみ、明示確認文字列が必要です。", ""]
    text = "\n".join(md)
    payload = {"status": status, "generated_at_jst": generated.isoformat(), "actions": actions, "errors": errors, "checks": checks or []}
    for base in [DOCS, OUTPUT]:
        write(base / "cis_v4_apply_seed_latest.md", text)
        write(base / "cis_v4_apply_seed_latest.html", simple_html(text))
        write_json(base / "cis_v4_apply_seed_status_latest.json", payload)
    return 0 if status == "ok" else 1


def main() -> int:
    mode = os.getenv("CIS_V4_SEED_MODE", "missing_only").strip()
    confirm = os.getenv("CIS_V4_SEED_CONFIRM", "").strip()
    actions: List[str] = []
    errors: List[str] = []
    checks: List[str] = []
    if mode not in {"missing_only", "overwrite_after_backup"}:
        return build_report("error", actions, [f"CIS_V4_SEED_MODE が不正です: {mode}"])
    if mode == "overwrite_after_backup" and confirm != "APPLY_CIS_V4_SEED_OVERWRITE_AFTER_BACKUP":
        return build_report("error", actions, ["上書きには確認文字列 APPLY_CIS_V4_SEED_OVERWRITE_AFTER_BACKUP が必要です。"])

    seed_errors, seed_checks, _seed_meta = validate_seed_before_copy()
    checks.extend(seed_checks)
    if seed_errors:
        actions.append("seedのv4厳格検査で止めました。root dataにはコピーしていません。")
        actions.append("先にCIS v4 Preflightでseed不正内容を確認し、該当ファイルを修正してください。")
        return build_report("error", actions, seed_errors, checks)

    staged_errors, staged_checks, _staged_meta = validate_staged_result_before_copy(mode)
    checks.extend(staged_checks)
    if staged_errors:
        actions.append("seed適用後のstaged data検査で止めました。root dataにはコピーしていません。")
        actions.append("既存root dataとseedを混在させるとv4厳格検査NGになるため、不足ファイルコピーも中止しました。")
        actions.append("先にCIS v4 Preflightでroot dataの不正内容を確認してください。")
        return build_report("error", actions, staged_errors, checks)

    existing = [name for name in FILES if (DATA / name).exists()]
    if mode == "missing_only":
        copied: List[str] = []
        protected: List[str] = []
        try:
            for name in FILES:
                src = SEED / name
                dst = DATA / name
                if dst.exists():
                    protected.append(name)
                    continue
                _atomic_copy(src, dst)
                copied.append(name)
                actions.append(f"コピー: data/v4_seed/{name} → data/{name}")
        except Exception as e:
            for name in copied:
                dst = DATA / name
                try:
                    if dst.exists():
                        dst.unlink()
                except Exception:
                    pass
            actions.append("コピー途中でエラーが出たため、この回にコピーした不足ファイルは削除して戻しました。")
            return build_report("error", actions, [f"コピー失敗: {type(e).__name__}: {e}"], checks)
        if protected:
            errors.append("既存root dataファイルは上書きしていません: " + ", ".join(protected))
            if copied:
                actions.append("不足ファイルのみコピーしました。既存ファイルは保護しました。")
            else:
                actions.append("全root dataファイルが既存だったため、seedコピーは行っていません。")
            actions.append("次にCIS v4 Preflightを再実行し、root dataマスターのv4厳格検査結果を確認してください。")
            actions.append("既存ファイルをseedで置き換える場合は、バックアップ方針を決めてから overwrite_after_backup を使ってください。")
            return build_report("partial", actions, errors, checks)
        return build_report("ok", actions, errors, checks)

    backups: Dict[str, Path] = {}
    replaced: List[str] = []
    try:
        for name in FILES:
            dst = DATA / name
            if dst.exists():
                b = backup(dst, "before_v4_seed_overwrite")
                backups[name] = b
                actions.append(f"バックアップ作成: {b.relative_to(ROOT)}")
        for name in FILES:
            src = SEED / name
            dst = DATA / name
            _atomic_copy(src, dst)
            replaced.append(name)
            actions.append(f"コピー: data/v4_seed/{name} → data/{name}")
    except Exception as e:
        for name in reversed(replaced):
            dst = DATA / name
            try:
                if name in backups:
                    _atomic_copy(backups[name], dst)
                elif dst.exists():
                    dst.unlink()
            except Exception:
                pass
        actions.append("上書きコピー途中でエラーが出たため、可能な範囲でバックアップから復元しました。")
        return build_report("error", actions, [f"上書きコピー失敗: {type(e).__name__}: {e}"], checks)
    return build_report("ok", actions, errors, checks)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.exit(build_report("error", [], [f"{type(e).__name__}: {e}"]))
