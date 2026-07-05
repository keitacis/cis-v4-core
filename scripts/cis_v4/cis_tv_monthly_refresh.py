#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 TradingView monthly refresh candidate generator.

This is deliberately a *candidate generator*, not a blind auto-writer.
Monthly runs fetch TradingView analyst snapshot candidates, compare them with
saved data/tv_snapshot.json, and write iPhone-friendly apply commands.

Design:
- Fetch only active US watchlist symbols.
- Never modify data/tv_snapshot.json directly.
- Failed/ambiguous fetches are reported and excluded from apply commands.
- A separate workflow can apply the generated candidate commands with one tap.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from cis_core import (
    DATA_DIR,
    DOCS_LATEST_DIR,
    OUTPUT_DIR,
    TVSnapshot,
    fmt_price,
    load_tv_snapshot,
    load_watchlist,
    now_jst,
    parse_tv_rating,
    read_json_strict,
    safe_float,
    safe_int,
    timestamp_jst,
    validate_symbol_for_market,
    write_error_report,
    write_json,
    write_report,
    write_text,
)

STEM = "tv_monthly_refresh"
TITLE = "CIS TradingView月次自動確認"

# Without exchange hints in the master, try common US venues.  The first valid
# TradingView response with all required analyst fields wins.
EXCHANGE_CANDIDATES = ["NASDAQ", "NYSE", "AMEX", "NYSEARCA", "BATS", "OTC"]

# Candidate column sets. TradingView occasionally changes screener field names,
# so try conservative alternatives. Unknown columns should only fail this
# refresh report; they must never damage the saved snapshot.
SCANNER_COLUMN_SETS = [
    ["name", "description", "exchange", "analyst_rating", "number_of_analysts", "target_price_average"],
    ["name", "description", "exchange", "Analyst Rating", "number_of_analysts", "target_price_average"],
    ["name", "description", "exchange", "recommendation_mark", "number_of_analysts", "target_price_average"],
    ["name", "description", "exchange", "analysts_count", "target_price_average", "analyst_rating"],
]

CANDIDATE_MANIFEST_FILENAME = "tv_monthly_refresh_candidate_manifest.json"
CANDIDATE_FILE_PATTERNS = [
    "tv_monthly_refresh_apply_commands*.txt",
    "tv_monthly_refresh_changed_only_commands*.txt",
    "tv_monthly_refresh_apply_iphone_part_*.txt",
    "tv_monthly_refresh_changed_only_iphone_part_*.txt",
    CANDIDATE_MANIFEST_FILENAME,
]

RATING_TEXT_ALIASES = {
    "STRONG BUY": "Strong Buy",
    "BUY": "Buy",
    "OUTPERFORM": "Buy",
    "OVERWEIGHT": "Buy",
    "HOLD": "Neutral",
    "NEUTRAL": "Neutral",
    "EQUAL-WEIGHT": "Neutral",
    "MARKET PERFORM": "Neutral",
    "SELL": "Sell",
    "UNDERPERFORM": "Sell",
    "UNDERWEIGHT": "Sell",
    "STRONG SELL": "Strong Sell",
}


@dataclass
class FetchedTV:
    symbol: str
    market: str
    coverage_status: str
    rating: Optional[str]
    analyst_count: Optional[int]
    avg_target_price: Optional[float]
    source: str
    exchange: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

    def to_command(self) -> str:
        reason = f"TradingView monthly auto-check {now_jst().strftime('%Y/%m')}"
        if self.coverage_status == "covered":
            return f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|{reason}"
        return f"TV US {self.symbol}|{self.coverage_status}|{reason}"


def normalize_rating(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # Some feeds expose analyst consensus as numeric.  Do not over-trust an
        # unknown scale.  Only accept obvious 1-5 style scores if observed.
        n = float(value)
        if 4.5 <= n <= 5:
            return "Strong Buy"
        if 3.5 <= n < 4.5:
            return "Buy"
        if 2.5 <= n < 3.5:
            return "Neutral"
        if 1.5 <= n < 2.5:
            return "Sell"
        if 1.0 <= n < 1.5:
            return "Strong Sell"
        return None
    text = str(value).strip()
    if not text or text in {"-", "—", "N/A", "None", "null"}:
        return None
    cleaned = re.sub(r"[_\-]+", " ", text).strip().upper()
    cleaned = re.sub(r"\s+", " ", cleaned)
    alias = RATING_TEXT_ALIASES.get(cleaned)
    if alias:
        return alias
    try:
        return parse_tv_rating(text)
    except Exception:
        return None


def candidate_from_values(symbol: str, values: Dict[str, Any], source: str, exchange: Optional[str] = None) -> Optional[FetchedTV]:
    rating_keys = ["analyst_rating", "Analyst Rating", "recommendation_mark", "rating", "recommendation"]
    count_keys = ["number_of_analysts", "analysts_count", "analyst_count", "analyst_count_current"]
    target_keys = ["target_price_average", "price_target_average", "average_target_price", "avg_target_price", "target_price_avg"]
    rating = None
    for k in rating_keys:
        rating = normalize_rating(values.get(k))
        if rating:
            break
    analyst_count = None
    for k in count_keys:
        analyst_count = safe_int(values.get(k))
        if analyst_count is not None:
            break
    avg_target = None
    for k in target_keys:
        avg_target = safe_float(values.get(k))
        if avg_target is not None:
            break
    if rating and analyst_count and analyst_count > 0 and avg_target and avg_target > 0:
        return FetchedTV(symbol=symbol, market="US", coverage_status="covered", rating=rating, analyst_count=analyst_count, avg_target_price=avg_target, source=source, exchange=exchange, raw=values)
    return None


def load_fixture() -> Dict[str, FetchedTV]:
    path = os.getenv("CIS_TV_REFRESH_FIXTURE") or os.getenv("CIS_TV_REFRESH_TEST_FIXTURE")
    if not path:
        return {}
    data = read_json_strict(Path(path), default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, FetchedTV] = {}
    if not isinstance(rows, list):
        raise ValueError("TV refresh fixture は items:list 形式が必要です。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"TV refresh fixture items[{idx}] がobjectではありません。")
        symbol = validate_symbol_for_market("US", row.get("symbol"))
        cov = str(row.get("coverage_status") or "covered")
        if cov == "covered":
            rating = normalize_rating(row.get("rating"))
            analyst_count = safe_int(row.get("analyst_count"))
            avg_target = safe_float(row.get("avg_target_price"))
            if not rating or not analyst_count or not avg_target:
                raise ValueError(f"fixture covered行が不正です: US:{symbol}")
            out[f"US:{symbol}"] = FetchedTV(symbol, "US", "covered", rating, analyst_count, avg_target, "fixture", row.get("exchange"), row)
        else:
            out[f"US:{symbol}"] = FetchedTV(symbol, "US", cov, None, None, None, "fixture", row.get("exchange"), row)
    return out


def _regex_json_value(text: str, keys: Iterable[str]) -> Any:
    for key in keys:
        # Match JSON-like "key": value; keep this conservative because it is only a fallback.
        m = re.search(r'"' + re.escape(key) + r'"\s*:\s*("[^"]*"|-?\d+(?:\.\d+)?|null)', text)
        if not m:
            continue
        raw = m.group(1)
        if raw == "null":
            return None
        if raw.startswith('"'):
            return raw.strip('"')
        try:
            return float(raw)
        except Exception:
            return raw
    return None


def fetch_from_tradingview_forecast_page(symbol: str) -> Tuple[Optional[FetchedTV], Optional[str]]:
    errors: List[str] = []
    for ex in EXCHANGE_CANDIDATES:
        url = f"https://www.tradingview.com/symbols/{ex}-{symbol}/forecast/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (CIS-v4-tv-refresh)", "Accept": "text/html,*/*"})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
            values = {
                "analyst_rating": _regex_json_value(text, ["analyst_rating", "Analyst Rating", "recommendation", "recommendation_mark"]),
                "number_of_analysts": _regex_json_value(text, ["number_of_analysts", "analysts_count", "analyst_count"]),
                "target_price_average": _regex_json_value(text, ["target_price_average", "price_target_average", "average_target_price", "avg_target_price"]),
            }
            cand = candidate_from_values(symbol, values, source="TradingView forecast page", exchange=ex)
            if cand:
                return cand, None
            errors.append(f"{ex}: forecast fields not found")
        except urllib.error.HTTPError as e:
            errors.append(f"{ex}: HTTPError {e.code}")
        except Exception as e:
            errors.append(f"{ex}: {type(e).__name__}: {e}")
    return None, " / ".join(errors[-3:]) if errors else "forecast page取得不可"


def scanner_request(tickers: List[str], columns: List[str]) -> Dict[str, Any]:
    payload = {
        "symbols": {"tickers": tickers, "query": {"types": []}},
        "columns": columns,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://scanner.tradingview.com/america/scan",
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (CIS-v4-tv-refresh)",
            "Accept": "application/json,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_from_tradingview_symbol(symbol: str) -> Tuple[Optional[FetchedTV], Optional[str]]:
    tickers = [f"{ex}:{symbol}" for ex in EXCHANGE_CANDIDATES]
    errors: List[str] = []
    for columns in SCANNER_COLUMN_SETS:
        try:
            res = scanner_request(tickers, columns)
            rows = res.get("data") if isinstance(res, dict) else None
            if not isinstance(rows, list):
                errors.append("scanner response has no data list")
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                sym = str(row.get("s") or "")
                d = row.get("d")
                if not isinstance(d, list):
                    continue
                values = {col: d[i] if i < len(d) else None for i, col in enumerate(columns)}
                exchange = sym.split(":", 1)[0] if ":" in sym else values.get("exchange")
                cand = candidate_from_values(symbol, values, source="TradingView scanner", exchange=exchange)
                if cand:
                    return cand, None
            errors.append("required analyst fields not found")
        except urllib.error.HTTPError as e:
            errors.append(f"HTTPError {e.code}")
        except Exception as e:
            errors.append(f"{type(e).__name__}: {e}")
    page_cand, page_err = fetch_from_tradingview_forecast_page(symbol)
    if page_cand:
        return page_cand, None
    if page_err:
        errors.append(page_err)
    return None, " / ".join(errors[-4:]) if errors else "取得不可"


def tv_snapshot_to_dict(s: TVSnapshot) -> Dict[str, Any]:
    return {
        "symbol": s.symbol,
        "market": s.market,
        "coverage_status": s.coverage_status,
        "rating": s.rating,
        "analyst_count": s.analyst_count,
        "avg_target_price": s.avg_target_price,
        "updated_at": s.updated_at,
        "source": s.source,
        "reason": s.reason,
    }


def diff_fields(old: Optional[TVSnapshot], new: FetchedTV) -> List[str]:
    if old is None:
        return ["新規取得"]
    out: List[str] = []
    checks = [
        ("coverage_status", old.coverage_status, new.coverage_status),
        ("rating", old.rating, new.rating),
        ("analyst_count", old.analyst_count, new.analyst_count),
        ("avg_target_price", old.avg_target_price, new.avg_target_price),
    ]
    for label, a, b in checks:
        if a != b:
            if label == "avg_target_price":
                aa = "未設定" if a in [None, ""] else f"{float(a):.2f}"
                bb = "未設定" if b in [None, ""] else f"{float(b):.2f}"
            else:
                aa = a if a not in [None, ""] else "未設定"
                bb = b if b not in [None, ""] else "未設定"
            out.append(f"{label}: {aa} → {bb}")
    return out


def split_lines(lines: List[str], size: int = 15) -> List[List[str]]:
    return [lines[i:i + size] for i in range(0, len(lines), size)]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cleanup_candidate_files() -> None:
    """Remove old apply-candidate artifacts before a new refresh starts.

    This prevents a failed refresh from leaving stale command files that could be
    applied later from an iPhone by mistake.  The latest report/status files are
    intentionally kept because write_report/write_error_report will overwrite
    them with the current run result.
    """
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        for pattern in CANDIDATE_FILE_PATTERNS:
            for path in base.glob(pattern):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass


def write_empty_candidate_manifest(status: str, error: Optional[str] = None) -> None:
    manifest = {
        "version": 1,
        "status": status,
        "generated_at_jst": timestamp_jst(),
        "apply_command_count": 0,
        "changed_command_count": 0,
        "command_files": {},
    }
    if error:
        manifest["error"] = error
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        write_json(base / CANDIDATE_MANIFEST_FILENAME, manifest)


def write_candidate_files(commands: List[str], changed_commands: List[str], status_level: str, generated_at_jst: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    paths: Dict[str, Any] = {}
    manifest_files: Dict[str, Any] = {}

    def record_file(filename: str, content: str) -> None:
        for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
            write_text(base / filename, content)
        paths[filename] = str((DOCS_LATEST_DIR / filename).relative_to(DOCS_LATEST_DIR.parent))
        manifest_files[filename] = {
            "sha256": sha256_text(content),
            "line_count": len([ln for ln in content.splitlines() if ln.strip()]),
            "bytes_utf8": len(content.encode("utf-8")),
        }

    full = "\n".join(commands).strip() + ("\n" if commands else "")
    changed = "\n".join(changed_commands).strip() + ("\n" if changed_commands else "")
    one_line = " ; ".join(commands)
    changed_one_line = " ; ".join(changed_commands)

    record_file("tv_monthly_refresh_apply_commands.txt", full)
    record_file("tv_monthly_refresh_changed_only_commands.txt", changed)
    record_file("tv_monthly_refresh_apply_commands_iphone_1line.txt", one_line + ("\n" if one_line else ""))
    record_file("tv_monthly_refresh_changed_only_commands_iphone_1line.txt", changed_one_line + ("\n" if changed_one_line else ""))

    split_links: Dict[str, List[str]] = {"apply": [], "changed_only": []}
    for prefix, source_lines in [("apply", commands), ("changed_only", changed_commands)]:
        for i, chunk in enumerate(split_lines(source_lines, 15), start=1):
            text = "\n".join(chunk) + "\n"
            one = " ; ".join(chunk) + "\n"
            filename = f"tv_monthly_refresh_{prefix}_iphone_part_{i:02d}.txt"
            one_filename = f"tv_monthly_refresh_{prefix}_iphone_part_{i:02d}_1line.txt"
            record_file(filename, text)
            record_file(one_filename, one)
            split_links[prefix].append(filename)
            split_links[prefix].append(one_filename)

    manifest = {
        "version": 1,
        "status": status_level,
        "generated_at_jst": generated_at_jst,
        "apply_command_count": len(commands),
        "changed_command_count": len(changed_commands),
        "summary": summary,
        "command_files": manifest_files,
        "primary_files": {
            "apply_all_success": "tv_monthly_refresh_apply_commands.txt",
            "changed_only": "tv_monthly_refresh_changed_only_commands.txt",
        },
    }
    for base in [DOCS_LATEST_DIR, OUTPUT_DIR]:
        write_json(base / CANDIDATE_MANIFEST_FILENAME, manifest)
    paths[CANDIDATE_MANIFEST_FILENAME] = str((DOCS_LATEST_DIR / CANDIDATE_MANIFEST_FILENAME).relative_to(DOCS_LATEST_DIR.parent))
    paths["split_links"] = split_links
    paths["manifest"] = manifest
    return paths

def main() -> int:
    cleanup_candidate_files()
    try:
        items = [x for x in load_watchlist(True) if x.market == "US"]
        old_tv = load_tv_snapshot()
        fixture = load_fixture()
        fetched: Dict[str, FetchedTV] = {}
        failed: List[Dict[str, Any]] = []

        for item in items:
            if item.key in fixture:
                fetched[item.key] = fixture[item.key]
                continue
            cand, err = fetch_from_tradingview_symbol(item.symbol)
            if cand:
                fetched[item.key] = cand
            else:
                failed.append({"key": item.key, "symbol": item.symbol, "reason": err or "取得不可"})

        candidates: List[Dict[str, Any]] = []
        unchanged: List[Dict[str, Any]] = []
        changed_commands: List[str] = []
        apply_commands: List[str] = []

        for item in items:
            cand = fetched.get(item.key)
            if not cand:
                continue
            old = old_tv.get(item.key)
            diffs = diff_fields(old, cand)
            command = cand.to_command()
            row = {
                "key": item.key,
                "symbol": item.symbol,
                "name": item.name,
                "exchange": cand.exchange,
                "old": tv_snapshot_to_dict(old) if old else None,
                "new": asdict(cand),
                "diffs": diffs,
                "command": command,
            }
            apply_commands.append(command)
            if diffs:
                candidates.append(row)
                changed_commands.append(command)
            else:
                unchanged.append(row)

        status_level = "partial" if candidates or failed else "ok"
        generated_at = timestamp_jst()
        summary = {
            "us_watchlist_count": len(items),
            "fetched_count": len(fetched),
            "candidate_change_count": len(candidates),
            "unchanged_count": len(unchanged),
            "failed_count": len(failed),
        }
        candidate_paths = write_candidate_files(apply_commands, changed_commands, status_level, generated_at, summary)

        status = {
            "status": status_level,
            "generated_at_jst": generated_at,
            "us_watchlist_count": len(items),
            "fetched_count": len(fetched),
            "candidate_change_count": len(candidates),
            "unchanged_count": len(unchanged),
            "failed_count": len(failed),
            "apply_command_count": len(apply_commands),
            "changed_command_count": len(changed_commands),
            "candidate_manifest": CANDIDATE_MANIFEST_FILENAME,
            "note": "候補生成のみ。本番tv_snapshot.jsonは変更していません。",
        }

        lines: List[str] = [f"# {TITLE}", "", f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}", ""]
        lines += [
            "## これは何をするレポートか",
            "",
            "- 月1でTradingView候補値を自動確認し、保存済み tv_snapshot.json と比較します。",
            "- このレポート自体は tv_snapshot.json を直接書き換えません。",
            "- 取得できた銘柄だけ、反映用コマンドを自動生成します。取得失敗銘柄の既存値は守ります。",
            "- iPhoneでは、問題なさそうなら GitHub Actions の `CIS v4 Apply TV Monthly Candidate` を実行すると、コピー作業なしで候補を反映できます。",
            "",
            "## ステータス",
            "",
            f"- 米国株監視リスト：{len(items)}件",
            f"- 自動取得成功：{len(fetched)}件",
            f"- 値の変更候補：{len(candidates)}件",
            f"- 値は同じ・確認済み：{len(unchanged)}件",
            f"- 取得失敗・手動確認候補：{len(failed)}件",
            "",
        ]
        lines += ["## iPhone用・反映導線", ""]
        if apply_commands:
            lines += [
                "### 推奨：コピーなしで反映する",
                "",
                "- GitHub Actions → `CIS v4 Apply TV Monthly Candidate` → `Run workflow` を押してください。",
                "- このWorkflowは、この月次確認で取得できた銘柄だけをMaster Updateに渡します。",
                "- 取得失敗銘柄は反映対象外なので、既存値は維持されます。",
                "",
                "### 手動で貼る場合",
                "",
                "iPhoneでは、まず分割版を使うのが安全です。",
                "",
            ]
            apply_parts = [x for x in candidate_paths.get("split_links", {}).get("apply", []) if x.endswith("_1line.txt")]
            changed_parts = [x for x in candidate_paths.get("split_links", {}).get("changed_only", []) if x.endswith("_1line.txt")]
            if apply_parts:
                lines.append("#### 全成功取得分・iPhone分割1行版")
                lines.append("")
                for fn in apply_parts:
                    lines.append(f"- [{fn}]({fn})")
                lines.append("")
            if changed_parts:
                lines.append("#### 変更ありだけ・iPhone分割1行版")
                lines.append("")
                for fn in changed_parts:
                    lines.append(f"- [{fn}]({fn})")
                lines.append("")
            lines += [
                "#### PC向け・全件",
                "",
                "- [全成功取得分・1行版](tv_monthly_refresh_apply_commands_iphone_1line.txt)",
                "- [変更ありだけ・1行版](tv_monthly_refresh_changed_only_commands_iphone_1line.txt)",
                "- [全成功取得分・改行版](tv_monthly_refresh_apply_commands.txt)",
                "- [変更ありだけ・改行版](tv_monthly_refresh_changed_only_commands.txt)",
                "- [候補manifest](tv_monthly_refresh_candidate_manifest.json)",
                "",
            ]
        else:
            lines += ["反映できる自動取得結果がありません。", ""]

        lines += ["## 値の変更候補", ""]
        if not candidates:
            lines += ["変更候補なし", ""]
        else:
            for c in candidates:
                new = c["new"]
                old = c["old"] or {}
                lines += [f"### {c['key']} {c['name']}", ""]
                lines.append(f"- 旧：{old.get('coverage_status','未設定')} / {old.get('rating','未設定')} / {old.get('analyst_count','未設定')}人 / {old.get('avg_target_price','未設定')}")
                lines.append(f"- 新：{new.get('coverage_status')} / {new.get('rating')} / {new.get('analyst_count')}人 / {new.get('avg_target_price')}")
                lines.append(f"- 取引所候補：{c.get('exchange') or '未取得'}")
                for d in c["diffs"]:
                    lines.append(f"- 差分：{d}")
                lines.append("")

        lines += ["## 値は同じ・確認済み", ""]
        if not unchanged:
            lines += ["なし", ""]
        else:
            for c in unchanged[:80]:
                new = c["new"]
                lines.append(f"- {c['key']}：{new.get('rating')} / {new.get('analyst_count')}人 / {new.get('avg_target_price')}")
            if len(unchanged) > 80:
                lines.append(f"- ほか{len(unchanged)-80}件")
            lines.append("")

        lines += ["## 取得失敗・手動確認候補", ""]
        if not failed:
            lines += ["なし", ""]
        else:
            lines += ["取得失敗銘柄は候補コマンドから除外しています。既存の tv_snapshot.json は守られます。", ""]
            for f in failed:
                lines.append(f"- {f['key']}：{f['reason']}")
            lines.append("")

        payload = {"status": status, "manifest": candidate_paths.get("manifest"), "candidates": candidates, "unchanged": unchanged, "failed": failed, "apply_commands": apply_commands, "changed_commands": changed_commands}
        write_report(STEM, "\n".join(lines), payload, status)
        return 0
    except Exception as e:
        cleanup_candidate_files()
        write_empty_candidate_manifest("error", f"{type(e).__name__}: {e}")
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
