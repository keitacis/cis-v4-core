#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 safe preflight.

Non-destructive compatibility check for introducing CIS v4 next to an existing
CIS repository.  Unlike a shallow existence check, this preflight intentionally
uses the same strict validators as daily/weekly/master scripts so malformed
master data is discovered before the user starts the v4 workflow chain.
"""
from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

JST = timezone(timedelta(hours=9))
SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[2] if SCRIPT.parent.name == "cis_v4" else SCRIPT.parents[1]
DATA = ROOT / "data"
DOCS_V4 = ROOT / "docs" / "v4"
DOCS_LATEST = DOCS_V4 / "latest"
OUTPUT_V4 = ROOT / "output" / "v4"

for d in [DOCS_LATEST, OUTPUT_V4]:
    d.mkdir(parents=True, exist_ok=True)

# Import after ROOT resolution; the script directory is on sys.path when run by Python.
import cis_core as core  # type: ignore  # noqa: E402
from cis_core import (  # type: ignore  # noqa: E402
    load_watchlist,
    load_company_master,
    load_tv_snapshot,
    load_buyzone_master,
    load_settings,
    read_json_strict,
    validate_history_json,
    validate_watchlist_company_consistency,
)

LEGACY_WORKFLOW_NAMES = [
    "daily_us.yml", "daily_jp.yml", "buy_alert.yml", "weekly_performance.yml",
    "cis_home.yml", "watchlist_update.yml", "master_update.yml",
    "monthly_maintenance.yml", "master_init_template.yml",
]
V4_WORKFLOW_NAMES = [
    "cis_v4_preflight.yml", "cis_v4_apply_seed.yml", "cis_v4_daily_us.yml",
    "cis_v4_daily_jp.yml", "cis_v4_buy_alert.yml", "cis_v4_weekly_performance.yml",
    "cis_v4_home.yml", "cis_v4_watchlist_update.yml", "cis_v4_master_update.yml",
    "cis_v4_monthly_maintenance.yml", "cis_v4_master_init_template.yml",
]
ROOT_MASTER_FILES = [
    "watchlist_master.csv", "company_master.csv", "buyzone_master.json",
    "tv_snapshot.json", "cis_settings.json", "watchlist_history.json",
    "master_update_history.json",
]
SEED_FILES = ROOT_MASTER_FILES


def now() -> datetime:
    return datetime.now(JST)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


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
        elif line.startswith("### "):
            if in_ul:
                body.append("</ul>"); in_ul = False
            body.append(f"<h3>{html.escape(line[4:])}</h3>")
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
    return """<!doctype html><html lang='ja'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>CIS v4 Preflight</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:16px;line-height:1.55}li{margin:6px 0}pre{white-space:pre-wrap;background:#f6f6f6;border-radius:10px;padding:12px;overflow:auto}h1,h2,h3{line-height:1.25}</style></head><body><p><a href='../index.html'>CISホームへ戻る</a></p>""" + "\n".join(body) + "<p><a href='../index.html'>CISホームへ戻る</a></p></body></html>"


def _json_items_count(path: Path, name: str) -> int:
    return validate_history_json(path, name)


def _check_history_file(name: str) -> Tuple[str, List[str], str]:
    path = DATA / name
    if not path.exists():
        return f"⚪ data/{name}: 未作成", [f"data/{name} が未作成です。Apply Seedまたは移行で作成してください。"], "missing"
    try:
        count = _json_items_count(path, name)
        return f"✅ data/{name}: 厳格JSON確認OK / count={count}", [], "ok"
    except Exception as e:
        return f"❌ data/{name}: 不正 / {type(e).__name__}: {e}", [f"data/{name} が不正です: {e}"], "error"


def _strict_check_root_file(name: str, validator: Callable[[], Any], counter: Callable[[Any], int]) -> Tuple[str, List[str], str]:
    path = DATA / name
    if not path.exists():
        return f"⚪ data/{name}: 未作成", [f"data/{name} が未作成です。Apply Seedまたは移行で作成してください。"], "missing"
    try:
        obj = validator()
        return f"✅ data/{name}: v4厳格検査OK / count={counter(obj)}", [], "ok"
    except Exception as e:
        return f"❌ data/{name}: v4厳格検査NG / {type(e).__name__}: {e}", [f"data/{name} はv4互換ではありません: {e}"], "error"


def check_root_masters() -> Tuple[List[str], List[str], Dict[str, Any]]:
    lines: List[str] = []
    problems: List[str] = []
    states: Dict[str, str] = {}
    checks = [
        ("company_master.csv", load_company_master, lambda obj: len(obj)),
        ("watchlist_master.csv", lambda: load_watchlist(active_only=False), lambda obj: len(obj)),
        ("tv_snapshot.json", load_tv_snapshot, lambda obj: len(obj)),
        ("buyzone_master.json", load_buyzone_master, lambda obj: len(obj)),
        ("cis_settings.json", load_settings, lambda obj: len(obj)),
    ]
    for name, fn, counter in checks:
        line, errs, state = _strict_check_root_file(name, fn, counter)
        lines.append(line); problems.extend(errs); states[name] = state
    for name in ["watchlist_history.json", "master_update_history.json"]:
        line, errs, state = _check_history_file(name)
        lines.append(line); problems.extend(errs); states[name] = state
    # Cross-file consistency can only be evaluated when both masters exist and
    # their individual parsers have passed.  If one is missing, Preflight should
    # keep reporting the missing file rather than producing a misleading
    # secondary consistency error.
    if states.get("watchlist_master.csv") == "ok" and states.get("company_master.csv") == "ok":
        try:
            info = validate_watchlist_company_consistency()
            extra = int(info.get("extra_company_count", 0))
            suffix = f" / company_master側の追加候補={extra}件" if extra else ""
            lines.append("✅ root watchlist/company整合性: OK" + suffix)
        except Exception as e:
            lines.append(f"❌ root watchlist/company整合性: NG / {type(e).__name__}: {e}")
            problems.append(f"root watchlist/company整合性NG: {e}")
            states["watchlist_company_consistency"] = "error"
    missing = [n for n, s in states.items() if s == "missing"]
    invalid = [n for n, s in states.items() if s == "error"]
    meta = {"missing": missing, "invalid": invalid, "all_missing": len(missing) == len(ROOT_MASTER_FILES), "all_ok": not missing and not invalid}
    return lines, problems, meta


def _with_data_dir(temp_data_dir: Path, fn: Callable[[], Any]) -> Any:
    """Run a cis_core validator against a different data directory.

    Used only by Preflight to validate data/v4_seed without copying it to root
    data/.  This keeps the check non-destructive.
    """
    original = core.DATA_DIR
    try:
        core.DATA_DIR = temp_data_dir
        return fn()
    finally:
        core.DATA_DIR = original


def _strict_check_seed_file(name: str, validator: Callable[[], Any], counter: Callable[[Any], int]) -> Tuple[str, List[str], str]:
    seed_dir = DATA / "v4_seed"
    path = seed_dir / name
    if not path.exists():
        return f"❌ data/v4_seed/{name}: なし", [f"data/v4_seed/{name} がありません。"], "error"
    try:
        obj = _with_data_dir(seed_dir, validator)
        return f"✅ data/v4_seed/{name}: v4厳格検査OK / count={counter(obj)}", [], "ok"
    except Exception as e:
        return f"❌ data/v4_seed/{name}: v4厳格検査NG / {type(e).__name__}: {e}", [f"data/v4_seed/{name} はv4 seedとして不正です: {e}"], "error"


def _strict_check_seed_history(name: str) -> Tuple[str, List[str], str]:
    seed_dir = DATA / "v4_seed"
    path = seed_dir / name
    if not path.exists():
        return f"❌ data/v4_seed/{name}: なし", [f"data/v4_seed/{name} がありません。"], "error"
    try:
        count = validate_history_json(path, name)
        return f"✅ data/v4_seed/{name}: 厳格JSON確認OK / count={count}", [], "ok"
    except Exception as e:
        return f"❌ data/v4_seed/{name}: 不正 / {type(e).__name__}: {e}", [f"data/v4_seed/{name} が不正です: {e}"], "error"


def check_seed() -> Tuple[List[str], List[str]]:
    lines: List[str] = []
    problems: List[str] = []
    seed_dir = DATA / "v4_seed"
    if not seed_dir.exists():
        problems.append("data/v4_seed がありません。seed退避方式になっていません。")
        return ["❌ data/v4_seed: なし"], problems

    checks = [
        ("company_master.csv", load_company_master, lambda obj: len(obj)),
        ("watchlist_master.csv", lambda: load_watchlist(active_only=False), lambda obj: len(obj)),
        ("tv_snapshot.json", load_tv_snapshot, lambda obj: len(obj)),
        ("buyzone_master.json", load_buyzone_master, lambda obj: len(obj)),
        ("cis_settings.json", load_settings, lambda obj: len(obj)),
    ]
    states: Dict[str, str] = {}
    for name, fn, counter in checks:
        line, errs, state = _strict_check_seed_file(name, fn, counter)
        lines.append(line)
        problems.extend(errs)
        states[name] = state
    for name in ["watchlist_history.json", "master_update_history.json"]:
        line, errs, state = _strict_check_seed_history(name)
        lines.append(line)
        problems.extend(errs)
        states[name] = state
    if states.get("watchlist_master.csv") == "ok" and states.get("company_master.csv") == "ok":
        try:
            info = _with_data_dir(seed_dir, validate_watchlist_company_consistency)
            extra = int(info.get("extra_company_count", 0))
            suffix = f" / company_master側の追加候補={extra}件" if extra else ""
            lines.append("✅ data/v4_seed watchlist/company整合性: OK" + suffix)
        except Exception as e:
            lines.append(f"❌ data/v4_seed watchlist/company整合性: NG / {type(e).__name__}: {e}")
            problems.append(f"data/v4_seed watchlist/company整合性NG: {e}")
    return lines, problems


def check_workflows() -> Tuple[List[str], List[str]]:
    wf_dir = ROOT / ".github" / "workflows"
    lines: List[str] = []
    problems: List[str] = []
    for name in V4_WORKFLOW_NAMES:
        lines.append(("✅" if (wf_dir / name).exists() else "❌") + f" .github/workflows/{name}")
        if not (wf_dir / name).exists():
            problems.append(f".github/workflows/{name} がありません。")
    legacy = [name for name in LEGACY_WORKFLOW_NAMES if (wf_dir / name).exists()]
    if legacy:
        lines.append("⚠️ 旧/同名Workflow候補あり: " + ", ".join(legacy))
        lines.append("旧Workflowはまだ削除せず、v4手動確認後にscheduleだけ停止してください。")
    else:
        lines.append("✅ 既知の旧Workflow同名衝突なし")
    return lines, problems


def check_scripts() -> Tuple[List[str], List[str]]:
    script_dir = ROOT / "scripts" / "cis_v4"
    expected = [
        "cis_core.py", "cis_daily_us.py", "cis_daily_jp.py", "cis_buy_alert.py",
        "cis_weekly_performance.py", "cis_home.py", "cis_watchlist_update.py",
        "cis_master_update.py", "cis_monthly_maintenance.py", "cis_master_init_template.py",
        "cis_v4_preflight.py", "cis_v4_apply_seed.py",
    ]
    lines: List[str] = []
    problems: List[str] = []
    for name in expected:
        p = script_dir / name
        if p.exists():
            lines.append(f"✅ scripts/cis_v4/{name}")
        else:
            lines.append(f"❌ scripts/cis_v4/{name}")
            problems.append(f"scripts/cis_v4/{name} がありません。")
    return lines, problems


def next_actions(meta: Dict[str, Any]) -> List[str]:
    missing = meta.get("missing", [])
    invalid = meta.get("invalid", [])
    if invalid:
        return [
            "root dataマスターにv4非互換または破損があります。Apply Seedで上書きせず、まず該当ファイルを確認してください。",
            "既存データを残す場合は、CSV/JSONの不正行・重複・active誤値・TV/BUYZONE不整合を修正してからPreflightを再実行します。",
            "既存データを使わずseedで作り直す場合も、先にバックアップ方針を決めてから `CIS v4 Apply Seed` の overwrite_after_backup を使います。",
        ]
    if meta.get("all_missing"):
        return [
            "root dataマスターが未作成です。`CIS v4 Apply Seed` を mode=missing_only で実行してください。",
            "Apply Seed後、もう一度Preflightを実行してv4厳格検査OKになるか確認してください。",
        ]
    if missing:
        return [
            "root dataマスターが一部不足しています。`CIS v4 Apply Seed` の mode=missing_only で不足ファイルだけ作成できます。",
            "Apply Seedは既存ファイルを上書きしません。完了後、Preflightを再実行してください。",
            "不足ファイル: " + ", ".join(missing),
        ]
    return [
        "root dataマスターはv4厳格検査OKです。次に `CIS v4 Master Init Template` を手動実行してください。",
        "BUYZONE/TradingViewの不足を確認し、`CIS v4 Master Update` で初期投入してください。",
        "その後、日次US/日次JP/週間/買い場を手動実行し、`docs/v4/index.html` を確認します。",
    ]


def build() -> int:
    generated = now()
    sections: List[Tuple[str, List[str]]] = []
    all_problems: List[str] = []

    fatal_problems: List[str] = []
    for title, fn in [("スクリプト", check_scripts), ("Workflow", check_workflows), ("seed退避データ", check_seed)]:
        lines, problems = fn()
        sections.append((title, lines))
        all_problems.extend(problems)
        fatal_problems.extend(problems)

    root_lines, root_problems, root_meta = check_root_masters()
    sections.append(("root dataマスター v4厳格検査", root_lines))
    all_problems.extend(root_problems)

    invalid = root_meta.get("invalid", [])
    status = "error" if (fatal_problems or invalid) else ("partial" if all_problems else "ok")
    status_label = "✅ 構成OK（まだ運用開始前。次は初期マスター投入/手動確認）" if status == "ok" else ("❌ エラー" if status == "error" else "⚠️ 要確認")

    md = [
        "# CIS v4 Preflight",
        "",
        f"生成日時：{generated.strftime('%Y/%m/%d %H:%M JST')}",
        "",
        f"総合判定：{status_label}",
        "",
        "このPreflightは破壊的変更を行いません。既存CISを上書きせず、v4投入前の衝突・不足・root dataマスターのv4互換性を確認します。",
        "",
    ]
    if all_problems:
        md += ["## 要確認", ""] + [f"- {p}" for p in all_problems] + [""]
    if status == "ok":
        md += [
            "## 重要",
            "",
            "- このOKは『ファイル構成とroot dataの形式がv4で読める』という意味です。",
            "- まだCIS運用開始ではありません。BUYZONEとTradingViewの初期投入、各レポートの手動確認が必要です。",
            "",
        ]
    md += ["## 次にやること", ""] + [f"- {a}" for a in next_actions(root_meta)] + [""]
    for title, lines in sections:
        md += [f"## {title}", ""] + [f"- {line}" for line in lines] + [""]
    md += [
        "## 安全メモ",
        "",
        "- v4 Workflowは `cis_v4_` 接頭辞付きで、旧Workflowと並走できる前提です。",
        "- 初回確認が終わるまで、v4の自動scheduleは有効化しません。",
        "- PreflightでNGが出たroot dataを、seedで無条件上書きしないでください。",
        "",
    ]
    md_text = "\n".join(md)
    payload = {"status": status, "generated_at_jst": generated.isoformat(), "problems": all_problems, "root_data": root_meta}
    for base in [DOCS_LATEST, OUTPUT_V4]:
        write_text(base / "cis_v4_preflight_latest.md", md_text)
        write_text(base / "cis_v4_preflight_latest.html", simple_html(md_text))
        write_json(base / "cis_v4_preflight_latest.json", payload)
        write_json(base / "cis_v4_preflight_status_latest.json", payload)
    return 1 if status == "error" else 0


if __name__ == "__main__":
    try:
        sys.exit(build())
    except Exception as e:
        generated = now()
        msg = f"{type(e).__name__}: {e}"
        md = "\n".join([
            "# CIS v4 Preflight",
            "",
            f"生成日時：{generated.strftime('%Y/%m/%d %H:%M JST')}",
            "",
            "総合判定：❌ エラー",
            "",
            "## エラー",
            "",
            f"- {msg}",
            "",
        ])
        payload = {"status": "error", "generated_at_jst": generated.isoformat(), "error": msg}
        for base in [DOCS_LATEST, OUTPUT_V4]:
            write_text(base / "cis_v4_preflight_latest.md", md)
            write_text(base / "cis_v4_preflight_latest.html", simple_html(md))
            write_json(base / "cis_v4_preflight_status_latest.json", payload)
        sys.exit(1)
