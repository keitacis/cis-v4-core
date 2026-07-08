#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 R11.2: external workflow_dispatch entrypoint.

R11.2 is intentionally NOT scheduled by GitHub cron. It is meant to be
triggered from an external scheduler via GitHub's workflow_dispatch API.

Compared with R11.1:
- Fixes write_report compatibility with current cis_core.py.
- Makes freshness checks stricter when rows are missing latest_date.
- Broadens auto windows so delayed GitHub runner start does not turn into no-op.

Modes:
- auto:              time-aware freshness check; run only stale/needed reports
- us_morning:        daily US -> buy alert -> Home
- us_retry:          daily US -> Home
- buy_alert_morning: buy alert -> Home
- jp_evening:        daily JP -> buy alert -> Home
- jp_retry:          daily JP -> Home
- catchup:           schedule catchup R10 -> Home
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from cis_core import DOCS_LATEST_DIR, JST, expected_daily_trade_date, now_jst, write_report

TITLE = "CIS 外部起動確認 R11.2"
STEM = "external_dispatch"
ROOT = Path(__file__).resolve().parents[2]

SCRIPT_DAILY_US = "scripts/cis_v4/cis_daily_us.py"
SCRIPT_DAILY_JP = "scripts/cis_v4/cis_daily_jp.py"
SCRIPT_BUY_ALERT = "scripts/cis_v4/cis_buy_alert.py"
SCRIPT_CATCHUP = "scripts/cis_v4/cis_schedule_catchup_r10.py"
SCRIPT_HOME = "scripts/cis_v4/cis_home.py"

EXPLICIT_MODES: Dict[str, List[str]] = {
    "us_morning": [SCRIPT_DAILY_US, SCRIPT_BUY_ALERT],
    "us_retry": [SCRIPT_DAILY_US],
    "buy_alert_morning": [SCRIPT_BUY_ALERT],
    "jp_evening": [SCRIPT_DAILY_JP, SCRIPT_BUY_ALERT],
    "jp_retry": [SCRIPT_DAILY_JP],
    "catchup": [SCRIPT_CATCHUP],
}

ALL_MODES = sorted(["auto", *EXPLICIT_MODES.keys()])


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


def rows_for_market(payload: Dict[str, Any], market: str) -> List[Dict[str, Any]]:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        return []
    want = market.upper()
    out: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict) and str(row.get("market") or "").upper() == want:
            out.append(row)
    return out


def date_ge(a: Optional[str], b: str) -> bool:
    if not a:
        return False
    try:
        return str(a)[:10] >= str(b)[:10]
    except Exception:
        return False


def market_rows_fresh(stem: str, market: str, min_hour_jst: int) -> Tuple[bool, Dict[str, Any]]:
    """Return whether a report has fresh rows for a market after the intended window.

    market_closed/price_stale generated after the task's own check window is treated as
    a terminal, already-handled signal so external retries do not loop forever.
    """
    now = now_jst()
    status = load_status(stem)
    payload = load_payload(stem)
    generated = parse_dt(status.get("generated_at_jst"))
    generated_today = bool(generated and generated.date() == now.date())
    generated_after_window = bool(generated and generated.hour >= min_hour_jst)
    rows = rows_for_market(payload, market)
    row_dates = sorted({str(r.get("latest_date") or "")[:10] for r in rows if r.get("latest_date")})
    expected = expected_daily_trade_date(market)

    detail = {
        "stem": stem,
        "market": market,
        "status": status.get("status", "missing"),
        "generated_at_jst": status.get("generated_at_jst"),
        "expected_price_date": expected,
        "row_dates": row_dates,
        "min_hour_jst": min_hour_jst,
    }

    if generated_today and generated_after_window and status.get("status") in {"market_closed", "price_stale"}:
        detail["fresh_reason"] = f"terminal_status:{status.get('status')}"
        return True, detail

    if not generated_today:
        detail["stale_reason"] = "not_generated_today"
        return False, detail
    if not rows:
        detail["stale_reason"] = "no_market_rows"
        return False, detail
    # Every market row should carry a price date for freshness checks.
    # Python all([]) is True, so explicitly reject empty/missing date sets.
    dated_row_count = sum(1 for r in rows if r.get("latest_date"))
    detail["row_count"] = len(rows)
    detail["dated_row_count"] = dated_row_count
    if dated_row_count == 0:
        detail["stale_reason"] = "no_latest_dates"
        return False, detail
    if dated_row_count < len(rows):
        detail["stale_reason"] = "some_rows_missing_latest_date"
        return False, detail
    if all(date_ge(d, expected) for d in row_dates):
        detail["fresh_reason"] = "row_dates_ge_expected"
        return True, detail
    detail["stale_reason"] = "row_dates_lt_expected"
    return False, detail


def unique_scripts(scripts: Sequence[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    for script in scripts:
        if script not in seen:
            out.append(script)
            seen.add(script)
    return out


def auto_plan() -> Tuple[List[str], List[Dict[str, Any]]]:
    now = now_jst()
    wd = now.weekday()  # Monday=0 ... Sunday=6
    hour = now.hour
    scripts: List[str] = []
    decisions: List[Dict[str, Any]] = []

    def decide(label: str, active: bool, stem: str, market: str, min_hour: int, script: str) -> None:
        if not active:
            decisions.append({"label": label, "active": False, "reason": "outside_window"})
            return
        fresh, detail = market_rows_fresh(stem, market, min_hour)
        item = {"label": label, "active": True, "fresh": fresh, **detail}
        decisions.append(item)
        if not fresh:
            scripts.append(script)

    # Morning external cron can run hourly around 07:25-10:25 JST.
    decide(
        "米国株日次",
        active=(wd in {1, 2, 3, 4, 5} and 7 <= hour <= 13),  # Tue-Sat JST
        stem="daily_us",
        market="US",
        min_hour=7,
        script=SCRIPT_DAILY_US,
    )
    decide(
        "買い場アラート（米国価格）",
        active=(wd in {0, 1, 2, 3, 4} and 8 <= hour <= 13),  # Mon-Fri JST
        stem="buy_alert",
        market="US",
        min_hour=8,
        script=SCRIPT_BUY_ALERT,
    )

    # Evening external cron can run hourly around 18:25-20:25 JST.
    decide(
        "日本株日次",
        active=(wd in {0, 1, 2, 3, 4} and 18 <= hour <= 22),
        stem="daily_jp",
        market="JP",
        min_hour=18,
        script=SCRIPT_DAILY_JP,
    )
    decide(
        "買い場アラート（日本価格）",
        active=(wd in {0, 1, 2, 3, 4} and 18 <= hour <= 22),
        stem="buy_alert",
        market="JP",
        min_hour=18,
        script=SCRIPT_BUY_ALERT,
    )

    return unique_scripts(scripts), decisions


def run_step(script: str) -> Dict[str, Any]:
    started = now_jst()
    cmd = [sys.executable, script]
    result: Dict[str, Any] = {
        "script": script,
        "started_at_jst": started.isoformat(),
        "cmd": cmd,
    }
    path = ROOT / script
    if not path.exists():
        result.update({"exit_code": 127, "ok": False, "error": "script not found"})
        return result
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=900,
    )
    finished = now_jst()
    result.update({
        "finished_at_jst": finished.isoformat(),
        "duration_seconds": round((finished - started).total_seconds(), 3),
        "exit_code": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    })
    return result


def build_markdown(payload: Dict[str, Any]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        f"生成日時：{payload['generated_at_jst']}",
        f"mode：{payload['mode']}",
        f"source：{payload['source']}",
        f"status：{payload['status']}",
        f"planned_steps：{payload.get('planned_step_count', 0)}",
        "",
    ]
    if payload.get("auto_decisions"):
        lines += ["## auto判定", ""]
        for d in payload.get("auto_decisions", []):
            label = d.get("label")
            if not d.get("active"):
                lines.append(f"- {label}：対象時間外")
            elif d.get("fresh"):
                lines.append(f"- ✅ {label}：最新扱い / dates={d.get('row_dates')}")
            else:
                lines.append(f"- ⚠️ {label}：再生成対象 / reason={d.get('stale_reason')} / dates={d.get('row_dates')} / expected={d.get('expected_price_date')}")
        lines.append("")
    lines += ["## 実行ステップ", ""]
    if not payload.get("steps"):
        lines.append("- 実行対象なし（no-op）")
    for i, step in enumerate(payload.get("steps", []), 1):
        mark = "✅" if step.get("ok") else "❌"
        lines.append(f"{i}. {mark} `{step.get('script')}` exit={step.get('exit_code')}")
        if step.get("duration_seconds") is not None:
            lines.append(f"   - duration：{step.get('duration_seconds')}s")
        if not step.get("ok"):
            if step.get("error"):
                lines.append(f"   - error：{step.get('error')}")
            if step.get("stderr_tail"):
                lines.append("   - stderr tail：")
                lines.append("```text")
                lines.append(str(step.get("stderr_tail"))[-1500:])
                lines.append("```")
    lines.append("")
    lines.append("## 役割")
    lines.append("")
    lines.append("このレポートは、GitHub scheduleに頼らず外部スケジューラからworkflow_dispatchされた実行記録です。")
    lines.append("CIS本体の表示は、各レポートとHomeの更新日時を優先して確認してください。")
    lines.append("")
    return "\n".join(lines)


def plan_for_mode(mode: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    if mode == "auto":
        return auto_plan()
    return list(EXPLICIT_MODES[mode]), []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=ALL_MODES)
    parser.add_argument("--source", default="manual")
    args = parser.parse_args(argv)

    generated = now_jst()
    scripts, auto_decisions = plan_for_mode(args.mode)
    steps: List[Dict[str, Any]] = []
    status = "ok"

    for script in scripts:
        step = run_step(script)
        steps.append(step)
        if not step.get("ok"):
            status = "error"
            break

    finished_before_home = now_jst()
    payload: Dict[str, Any] = {
        "schema_version": "r11.2",
        "status": status,
        "generated_at_jst": generated.isoformat(),
        "finished_at_jst": finished_before_home.isoformat(),
        "timestamp_jst": generated.isoformat(),
        "mode": args.mode,
        "source": args.source,
        "planned_scripts": scripts,
        "planned_step_count": len(scripts),
        "steps": steps,
        "step_count": len(steps),
        "ok_count": sum(1 for s in steps if s.get("ok")),
        "auto_decisions": auto_decisions,
    }

    # On no-op auto runs, do not touch docs/Home. This keeps hourly external checks
    # from producing noisy commits when everything is already fresh or outside windows.
    if args.mode == "auto" and not scripts:
        print(build_markdown(payload))
        return 0

    def status_doc(current_status: str) -> Dict[str, Any]:
        return {
            "status": current_status,
            "generated_at_jst": generated.isoformat(),
            "finished_at_jst": now_jst().isoformat(),
            "mode": args.mode,
            "source": args.source,
            "planned_step_count": len(scripts),
            "step_count": len(steps),
            "ok_count": sum(1 for s in steps if s.get("ok")),
            "has_error": current_status != "ok",
        }

    body = build_markdown(payload)
    write_report(STEM, body, payload, status_doc(status))

    # Rebuild Home after writing external_dispatch so the generated report is available
    # for any current/future Home card integration, and core cards reflect the latest runs.
    home_step = run_step(SCRIPT_HOME)
    payload["home_step"] = home_step
    if not home_step.get("ok"):
        status = "error"
        payload["status"] = "error"
        payload["home_error"] = True
        body = build_markdown(payload)
        write_report(STEM, body, payload, status_doc("error"))

    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
