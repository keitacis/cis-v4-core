#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 R10.4: scheduled workflow catch-up and diagnostics.

This script does three jobs:
1) Diagnose whether daily reports are stale after their expected scheduled windows.
2) Record recent GitHub Actions workflow-run history when GITHUB_TOKEN is available.
3) Regenerate stale reports automatically, then rebuild Home.

The goal is not to hand-wave the issue as "GitHub schedule is unstable".
It persists evidence: report status JSON, payload row price dates, expected price
dates, generated_at timestamps, recent schedule/workflow_dispatch runs, decisions,
and subprocess exit codes.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from cis_core import (
    DOCS_LATEST_DIR,
    JST,
    expected_daily_trade_date,
    now_jst,
    timestamp_jst,
    write_report,
)

STEM = "schedule_catchup"
TITLE = "CIS 自動更新取りこぼし確認 R10.4"

# Python weekday: Monday=0 ... Sunday=6.
TASKS = {
    "daily_us": {
        "label": "米国株日次騰落",
        "script": "scripts/cis_v4/cis_daily_us.py",
        "workflow_file": "cis_v4_daily_us.yml",
        "markets": ["US"],
        "min_hour_jst": 9,
        "active_weekdays": [1, 2, 3, 4, 5],  # Tue-Sat JST, after US close.
        "reason": "米国株日次の朝更新が未反映",
    },
    "buy_alert_us": {
        "stem": "buy_alert",
        "label": "買い場アラート（米国価格）",
        "script": "scripts/cis_v4/cis_buy_alert.py",
        "workflow_file": "cis_v4_buy_alert.yml",
        "markets": ["US"],
        "min_hour_jst": 10,
        "active_weekdays": [0, 1, 2, 3, 4],  # Mon-Fri JST, matching current Buy Alert schedule.
        "reason": "買い場アラートの米国価格更新が未反映",
    },
    "daily_jp": {
        "label": "日本株日次騰落",
        "script": "scripts/cis_v4/cis_daily_jp.py",
        "workflow_file": "cis_v4_daily_jp.yml",
        "markets": ["JP"],
        "min_hour_jst": 19,
        "active_weekdays": [0, 1, 2, 3, 4],  # Mon-Fri JST, after TSE close.
        "reason": "日本株日次の夕方更新が未反映",
    },
    "buy_alert_jp": {
        "stem": "buy_alert",
        "label": "買い場アラート（日本価格）",
        "script": "scripts/cis_v4/cis_buy_alert.py",
        "workflow_file": "cis_v4_buy_alert.yml",
        "markets": ["JP"],
        "min_hour_jst": 19,
        "active_weekdays": [0, 1, 2, 3, 4],
        "reason": "買い場アラートの日本価格更新が未反映",
    },
}

_WORKFLOW_RUN_CACHE: Dict[str, Dict[str, Any]] = {}


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def load_status(stem: str) -> Dict[str, Any]:
    data = read_json(DOCS_LATEST_DIR / f"{stem}_status_latest.json", {})
    return data if isinstance(data, dict) else {}


def load_payload(stem: str) -> Dict[str, Any]:
    data = read_json(DOCS_LATEST_DIR / f"{stem}_latest.json", {})
    return data if isinstance(data, dict) else {}


def parse_dt(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        return dt.astimezone(JST)
    except Exception:
        return None


def date_lt(a: Optional[str], b: str) -> bool:
    if not a:
        return True
    try:
        return str(a)[:10] < str(b)[:10]
    except Exception:
        return True


def rows_for_markets(payload: Dict[str, Any], markets: Sequence[str]) -> List[Dict[str, Any]]:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        return []
    want = {m.upper() for m in markets}
    out: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        market = str(row.get("market") or "").upper()
        if market in want:
            out.append(row)
    return out


def task_stem(task_key: str, task: Dict[str, Any]) -> str:
    return str(task.get("stem") or task_key)


def expected_for_markets(markets: Sequence[str]) -> Dict[str, str]:
    return {m: expected_daily_trade_date(m) for m in markets}


def github_api_json(path: str) -> Dict[str, Any]:
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo:
        return {"available": False, "reason": "GITHUB_TOKEN/GITHUB_REPOSITORY not available"}
    url = f"https://api.github.com/repos/{repo}/{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "cis-v4-schedule-catchup-r10",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:500]
        except Exception:
            pass
        return {"available": False, "http_status": e.code, "error": body or str(e)}
    except Exception as e:
        return {"available": False, "error": f"{type(e).__name__}: {e}"}


def recent_workflow_runs(workflow_file: str) -> Dict[str, Any]:
    if workflow_file in _WORKFLOW_RUN_CACHE:
        return _WORKFLOW_RUN_CACHE[workflow_file]
    data = github_api_json(f"actions/workflows/{workflow_file}/runs?per_page=10")
    if not data or data.get("available") is False:
        result = {"available": False, "error": data.get("error") or data.get("reason") or data}
    else:
        runs = []
        for r in data.get("workflow_runs", [])[:10]:
            if not isinstance(r, dict):
                continue
            runs.append({
                "event": r.get("event"),
                "status": r.get("status"),
                "conclusion": r.get("conclusion"),
                "created_at": r.get("created_at"),
                "run_started_at": r.get("run_started_at"),
                "updated_at": r.get("updated_at"),
                "html_url": r.get("html_url"),
            })
        result = {"available": True, "runs": runs}
    _WORKFLOW_RUN_CACHE[workflow_file] = result
    return result


def inspect_task(task_key: str, task: Dict[str, Any]) -> Dict[str, Any]:
    now = now_jst()
    stem = task_stem(task_key, task)
    markets = [str(m).upper() for m in task.get("markets", [])]
    workflow_file = str(task.get("workflow_file") or "")
    runs = recent_workflow_runs(workflow_file) if workflow_file else {"available": False, "reason": "workflow_file missing"}
    status = load_status(stem)
    payload = load_payload(stem)
    rows = rows_for_markets(payload, markets)
    expected = expected_for_markets(markets)
    generated = parse_dt(status.get("generated_at_jst"))
    row_dates = sorted({str(r.get("latest_date") or "")[:10] for r in rows if r.get("latest_date")})

    min_hour = int(task.get("min_hour_jst", 0))
    active_weekdays = {int(x) for x in task.get("active_weekdays", [])}
    if active_weekdays and now.weekday() not in active_weekdays:
        return {
            "task": task_key,
            "stem": stem,
            "label": task.get("label"),
            "checked": False,
            "needs_regen": False,
            "reason": f"判定対象外曜日：weekday={now.weekday()}",
            "status_before": status.get("status", "missing"),
            "generated_at_jst_before": status.get("generated_at_jst"),
            "row_dates": row_dates,
            "expected_price_dates": expected,
            "recent_workflow_runs": runs,
        }
    if now.hour < min_hour:
        return {
            "task": task_key,
            "stem": stem,
            "label": task.get("label"),
            "checked": False,
            "needs_regen": False,
            "reason": f"判定前：JST {min_hour}:00 以降に確認",
            "status_before": status.get("status", "missing"),
            "generated_at_jst_before": status.get("generated_at_jst"),
            "row_dates": row_dates,
            "expected_price_dates": expected,
            "recent_workflow_runs": runs,
        }

    reasons: List[str] = []
    if not status:
        reasons.append("status JSONが未生成")
    elif status.get("status") in {"missing", "error"}:
        reasons.append(f"status={status.get('status')}")

    generated_today = bool(generated and generated.date() == now.date())
    if generated is None:
        reasons.append("generated_at_jstが未取得")
    elif not generated_today:
        reasons.append(f"生成日が当日ではない：{generated.strftime('%Y-%m-%d')}")

    # If today's report already ran and explicitly says market_closed/price_stale,
    # do not keep regenerating just because the latest trade date is older than
    # the approximate expected date. That is the normal holiday/delayed-data signal.
    # Treat market_closed/price_stale as a terminal signal only when the
    # report was generated after this task's own expected check window.
    # This matters for buy_alert: a morning US-side price_stale report must
    # not suppress the evening JP-side catch-up.
    generated_after_window = bool(generated and generated.hour >= min_hour)
    today_known_non_ok = (
        generated_today
        and generated_after_window
        and status.get("status") in {"market_closed", "price_stale"}
    )

    if not today_known_non_ok:
        if not rows:
            reasons.append("対象marketのrowsが未取得")
        else:
            for market in markets:
                exp = expected[market]
                m_rows = rows_for_markets(payload, [market])
                m_dates = [str(r.get("latest_date") or "")[:10] for r in m_rows if r.get("latest_date")]
                if not m_dates:
                    reasons.append(f"{market}価格日付が全件未取得")
                elif all(date_lt(d, exp) for d in m_dates):
                    reasons.append(f"{market}価格日付が想定{exp}より古い：{sorted(set(m_dates))}")

    return {
        "task": task_key,
        "stem": stem,
        "label": task.get("label"),
        "checked": True,
        "needs_regen": bool(reasons),
        "reasons": reasons,
        "status_before": status.get("status", "missing"),
        "generated_at_jst_before": status.get("generated_at_jst"),
        "row_dates": row_dates,
        "expected_price_dates": expected,
        "recent_workflow_runs": runs,
    }


def run_script(script: str) -> Dict[str, Any]:
    cmd = [sys.executable, script]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "command": " ".join(cmd),
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def status_snapshot(stem: str, markets: Sequence[str]) -> Dict[str, Any]:
    status = load_status(stem)
    payload = load_payload(stem)
    rows = rows_for_markets(payload, markets)
    row_dates = sorted({str(r.get("latest_date") or "")[:10] for r in rows if r.get("latest_date")})
    return {
        "status": status.get("status", "missing"),
        "generated_at_jst": status.get("generated_at_jst"),
        "row_dates": row_dates,
    }


def build_lines(decisions: List[Dict[str, Any]], executed: List[Dict[str, Any]]) -> str:
    now = now_jst()
    lines = [
        f"# {TITLE}",
        "",
        f"生成日時：{now.strftime('%Y/%m/%d %H:%M JST')}",
        "",
        "## 判定サマリー",
        "",
    ]
    if not decisions:
        lines.append("- 判定対象なし")
    for d in decisions:
        label = d.get("label") or d.get("task")
        if not d.get("checked"):
            lines.append(f"- {label}：判定対象外/判定前（{d.get('reason')}）")
        elif d.get("needs_regen"):
            lines.append(f"- ⚠️ {label}：再生成対象 / {' / '.join(d.get('reasons') or [])}")
        else:
            lines.append(f"- ✅ {label}：最新扱い")
    lines += ["", "## 実行結果", ""]
    if not executed:
        lines.append("- 再生成なし")
    for e in executed:
        lines.append(f"- {e.get('label')}：exit={e.get('returncode')} / `{e.get('command')}`")
        after = e.get("status_after")
        if isinstance(after, dict):
            lines.append(f"  - after：status={after.get('status')} / generated={after.get('generated_at_jst')} / dates={after.get('row_dates')}")
    lines += ["", "## 詳細", ""]
    for d in decisions:
        lines += [
            f"### {d.get('label') or d.get('task')}",
            "",
            f"- status_before：{d.get('status_before')}",
            f"- generated_at_before：{d.get('generated_at_jst_before')}",
            f"- expected_price_dates：{d.get('expected_price_dates')}",
            f"- row_dates：{d.get('row_dates')}",
        ]
        runs = d.get("recent_workflow_runs") or {}
        lines.append(f"- recent_workflow_runs_available：{runs.get('available')}")
        for r in (runs.get("runs") or [])[:5]:
            lines.append(
                "  - "
                f"event={r.get('event')} / status={r.get('status')} / conclusion={r.get('conclusion')} / "
                f"started={r.get('run_started_at')} / updated={r.get('updated_at')}"
            )
        if not runs.get("available"):
            lines.append(f"  - workflow_runs_error：{runs.get('error')}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    decisions: List[Dict[str, Any]] = []
    executed: List[Dict[str, Any]] = []
    already_run: set[str] = set()

    try:
        for key, task in TASKS.items():
            d = inspect_task(key, task)
            decisions.append(d)
            if not d.get("needs_regen"):
                continue
            script = str(task["script"])
            if script in already_run:
                continue
            result = run_script(script)
            result["task"] = key
            result["label"] = task.get("label")
            result["status_after"] = status_snapshot(task_stem(key, task), task.get("markets", []))
            executed.append(result)
            already_run.add(script)

        home_result = run_script("scripts/cis_v4/cis_home.py")
        home_result["task"] = "home"
        home_result["label"] = "CISホーム再生成"
        home_result["status_after"] = status_snapshot("index", [])
        executed.append(home_result)

        failed = [e for e in executed if int(e.get("returncode") or 0) != 0]
        regenerated = [e for e in executed if e.get("task") != "home"]
        status_value = "error" if failed else "ok"
        status = {
            "status": status_value,
            "generated_at_jst": timestamp_jst(),
            "checked_count": sum(1 for d in decisions if d.get("checked")),
            "regen_count": len(regenerated),
            "recovered_count": len(regenerated) if not failed else 0,
            "failed_count": len(failed),
            "decisions": decisions,
            "executed": executed,
        }
        write_report(STEM, build_lines(decisions, executed), {"status": status, "decisions": decisions, "executed": executed}, status)
        return 1 if failed else 0
    except Exception as e:
        status = {
            "status": "error",
            "generated_at_jst": timestamp_jst(),
            "error": f"{type(e).__name__}: {e}",
            "decisions": decisions,
            "executed": executed,
        }
        lines = f"# {TITLE}\n\n生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}\n\n## エラー\n\n{status['error']}\n"
        write_report(STEM, lines, {"status": status, "decisions": decisions, "executed": executed}, status)
        return 1


if __name__ == "__main__":
    sys.exit(main())
