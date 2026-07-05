#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIS v4 Core shared utilities.

Design principles:
- Code contains processing logic only.
- data/*.csv/json contains watchlist, descriptions, buy-zone rules and TradingView snapshots.
- Reports write to output/v4/* and docs/v4/latest/* during the safe migration phase.
- Failures overwrite latest report with an explicit error page so stale reports do not look fresh.
- iPhone-first Markdown: card/list style, no wide tables.
"""
from __future__ import annotations

import csv
import html
import json
import math
import os
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yfinance as yf  # type: ignore
except Exception:  # pragma: no cover
    yf = None

JST = timezone(timedelta(hours=9))
# scripts are namespaced under scripts/cis_v4 during the safe migration phase.
# Resolve repository root robustly so the same code also works if copied back to scripts/.
_SCRIPT_PATH = Path(__file__).resolve()
ROOT = _SCRIPT_PATH.parents[2] if _SCRIPT_PATH.parent.name == "cis_v4" else _SCRIPT_PATH.parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output" / "v4"
DOCS_DIR = ROOT / "docs"
DOCS_V4_DIR = DOCS_DIR / "v4"
DOCS_LATEST_DIR = DOCS_V4_DIR / "latest"
BACKUP_DIR = DATA_DIR / "backups"

for _d in [DATA_DIR, OUTPUT_DIR, DOCS_V4_DIR, DOCS_LATEST_DIR, BACKUP_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

MARKETS = {"US", "JP"}
TV_COVERAGE_STATUSES = {"covered", "no_coverage", "not_applicable"}
TV_COVERAGE_ALIASES = {
    "COVERED": "covered",
    "あり": "covered",
    "カバーあり": "covered",
    "NO_COVERAGE": "no_coverage",
    "NO COVERAGE": "no_coverage",
    "NONE": "no_coverage",
    "なし": "no_coverage",
    "カバレッジなし": "no_coverage",
    "アナリストなし": "no_coverage",
    "NOT_APPLICABLE": "not_applicable",
    "NOT APPLICABLE": "not_applicable",
    "N/A": "not_applicable",
    "NA": "not_applicable",
    "対象外": "not_applicable",
    "ETF": "not_applicable",
}


VALID_TV_RATINGS = {
    "STRONG BUY": "Strong Buy",
    "BUY": "Buy",
    "NEUTRAL": "Neutral",
    "HOLD": "Neutral",
    "SELL": "Sell",
    "STRONG SELL": "Strong Sell",
    "強い買い": "Strong Buy",
    "買い": "Buy",
    "中立": "Neutral",
    "売り": "Sell",
    "強い売り": "Strong Sell",
}

ACTIVE_TRUE_VALUES = {"true", "1", "yes", "y", "active", "有効", "監視", "on"}
ACTIVE_FALSE_VALUES = {"false", "0", "no", "n", "inactive", "停止", "off"}


def normalize_coverage_status(value: Any) -> str:
    raw = str(value or "covered").strip()
    if not raw:
        return "covered"
    key = raw.upper()
    if key in TV_COVERAGE_ALIASES:
        return TV_COVERAGE_ALIASES[key]
    low = raw.lower().replace("-", "_").replace(" ", "_")
    if low in TV_COVERAGE_STATUSES:
        return low
    raise ValueError(f"TradingView coverage_status が不正です: {value!r}")


def parse_tv_rating(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("TradingViewレーティングが空です。")
    canon = VALID_TV_RATINGS.get(raw.upper()) or VALID_TV_RATINGS.get(raw)
    if not canon:
        allowed = ", ".join(["Strong Buy", "Buy", "Neutral", "Sell", "Strong Sell"])
        raise ValueError(f"TradingViewレーティング形式エラー: {raw} / allowed: {allowed}")
    return canon


def parse_active_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    raw = str(value if value is not None else "").strip()
    low = raw.lower()
    if low in ACTIVE_TRUE_VALUES:
        return True
    if low in ACTIVE_FALSE_VALUES:
        return False
    raise ValueError(
        "active値が不正です: "
        f"{value!r} / allowed: true,false,1,0,yes,no,active,inactive"
    )




def _is_blank_like(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return False
    raw = str(value).strip()
    if raw == "":
        return True
    return raw.lower() in {"none", "null", "n/a", "na"} or raw in {"-", "—", "未取得"}


def _is_blank_or_zero_numeric(value: Any) -> bool:
    if _is_blank_like(value):
        return True
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        try:
            return float(value) == 0
        except Exception:
            return False
    raw = str(value).strip().replace(",", "").replace("$", "").replace("¥", "").replace("円", "")
    try:
        return float(raw) == 0
    except Exception:
        return False


def validate_tv_noncovered_blank_fields(row: Dict[str, Any], label: str) -> None:
    """For no_coverage/not_applicable rows, rating/targets must not carry values.

    This prevents Master Update or ordinary report generation from silently
    normalizing away stray analyst data on unrelated updates.
    """
    problems = []
    if not _is_blank_like(row.get("rating")):
        problems.append(f"rating={row.get('rating')!r}")
    if not _is_blank_or_zero_numeric(row.get("analyst_count")):
        problems.append(f"analyst_count={row.get('analyst_count')!r}")
    if not _is_blank_or_zero_numeric(row.get("avg_target_price")):
        problems.append(f"avg_target_price={row.get('avg_target_price')!r}")
    if problems:
        raise ValueError(
            f"tv_snapshot.json のno_coverage/not_applicable行にアナリスト値が残っています: {label} / "
            + ", ".join(problems)
        )


def validate_symbol_for_market(market: str, symbol: str) -> str:
    m = str(market or "").strip().upper()
    s = normalize_symbol(symbol)
    if m == "JP":
        s = clean_jp_symbol(s)
        if not re.fullmatch(r"\d{4}", s):
            raise ValueError(f"JP銘柄コードは4桁数字のみ許可です: {symbol!r}")
        return s
    if m == "US":
        # Allows normal US tickers and ETF symbols such as BRK.B / BRK-B.
        if not re.fullmatch(r"[A-Z0-9][A-Z0-9.-]{0,14}", s):
            raise ValueError(f"USティッカー形式が不正です: {symbol!r}")
        return s
    raise ValueError(f"market が不正です: {market!r}")


def now_jst() -> datetime:
    return datetime.now(JST)


def today_jst() -> str:
    return now_jst().strftime("%Y-%m-%d")


def _previous_weekday(d):
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def expected_daily_trade_date(market: str) -> str:
    """Approximate expected latest trading date for stale/holiday detection.

    This is not a full exchange holiday calendar. It is a conservative guard:
    when yfinance only has an older trading date than expected, reports mark
    the run as market_closed instead of pretending old data is today's update.
    """
    n = now_jst()
    if market == "JP":
        base = n.date() if n.hour >= 15 else (n.date() - timedelta(days=1))
    else:
        # At JST morning after the US close, the latest US trading date is usually yesterday.
        base = n.date() - timedelta(days=1 if n.hour >= 7 else 2)
    return _previous_weekday(base).isoformat()


def timestamp_jst() -> str:
    return now_jst().isoformat()


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if math.isnan(float(value)):
            return None
        return float(value)
    s = str(value).strip()
    if not s or s in {"-", "—", "未取得", "N/A", "None", "null"}:
        return None
    s = s.replace(",", "").replace("$", "").replace("¥", "").replace("円", "")
    s = s.replace("%", "").replace("人", "")
    try:
        return float(s)
    except Exception:
        return None


def safe_int(value: Any) -> Optional[int]:
    f = safe_float(value)
    if f is None:
        return None
    return int(round(f))


def normalize_symbol(symbol: Any) -> str:
    s = str(symbol or "").strip().upper()
    for prefix in ["NASDAQ:", "NYSE:", "AMEX:", "TSE:", "TYO:"]:
        s = s.replace(prefix, "")
    s = s.replace(".US", "")
    return s


def clean_jp_symbol(symbol: Any) -> str:
    return normalize_symbol(symbol).replace(".T", "")


def is_jp_symbol(symbol: Any) -> bool:
    s = normalize_symbol(symbol)
    return bool(re.fullmatch(r"\d{4}(\.T)?", s))


def yf_symbol(symbol: str, market: str) -> str:
    s = normalize_symbol(symbol)
    if market == "JP":
        return clean_jp_symbol(s) + ".T"
    return s


def fmt_pct(v: Optional[float]) -> str:
    if v is None:
        return "未取得"
    return f"{v:+.2f}%"


def fmt_price(v: Optional[float], market: str) -> str:
    if v is None:
        return "未取得"
    if market == "JP":
        return f"{v:,.0f}円"
    return f"${v:,.2f}"


def fmt_change(v: Optional[float], market: str) -> str:
    if v is None:
        return "未取得"
    sign = "+" if v >= 0 else "-"
    n = abs(v)
    if market == "JP":
        return f"{sign}{n:,.0f}円"
    return f"{sign}${n:,.2f}"


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_json_strict(path: Path, default: Any = None) -> Any:
    """Read JSON without silently discarding malformed master files.

    Missing files may use a default, but existing invalid JSON is a hard error.
    This is important for CIS master data such as TradingView and buy-zone
    files: treating a broken file as empty can overwrite good historical data.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"JSON読み込みエラー: {path.relative_to(ROOT)} / {type(e).__name__}: {e}") from e


DEFAULT_SETTINGS = {
    "timezone": "Asia/Tokyo",
    "daily_us_time_jst": "07:15",
    "daily_jp_time_jst": "16:10",
    "buy_alert_time_jst": "08:00",
    "weekly_performance_time_jst": "Saturday 18:30",
    "monthly_maintenance_day": "1",
    "tv_snapshot_review_frequency": "monthly",
    "tv_snapshot_stale_days": 45,
    "buyzone_review_frequency": "monthly",
    "iphone_home": "docs/v4/index.html",
    "home_stale_days": {
        "buy_alert": 2,
        "daily_us": 3,
        "daily_jp": 3,
        "weekly_performance": 9,
        "watchlist_template": 90,
        "watchlist_update": 90,
        "master_init_template": 45,
        "master_update": 45,
        "monthly_maintenance": 45,
        "tv_monthly_refresh": 45
    },
    "note": "GitHub Actionsの自動実行時刻はworkflowのcronで管理します。cis_settings.jsonを変更してもcron時刻は自動では変わりません。"
}


def _deep_merge_settings(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            nested = dict(out[k])
            nested.update(v)
            out[k] = nested
        else:
            out[k] = v
    return out


def load_settings() -> Dict[str, Any]:
    """Load data/cis_settings.json and validate settings actually used by code.

    Missing settings fall back to DEFAULT_SETTINGS.  Existing malformed JSON or
    invalid numeric settings are hard errors so the visible configuration never
    lies about the running behavior.
    """
    path = DATA_DIR / "cis_settings.json"
    raw = read_json_strict(path, default={}) or {}
    if not isinstance(raw, dict):
        raise ValueError("cis_settings.json はobject形式である必要があります。")
    settings = _deep_merge_settings(DEFAULT_SETTINGS, raw)
    try:
        settings["tv_snapshot_stale_days"] = int(settings.get("tv_snapshot_stale_days", 45))
    except Exception as e:
        raise ValueError("cis_settings.json のtv_snapshot_stale_daysは整数が必要です。") from e
    if settings["tv_snapshot_stale_days"] <= 0:
        raise ValueError("cis_settings.json のtv_snapshot_stale_daysは1以上が必要です。")
    home = settings.get("home_stale_days")
    if not isinstance(home, dict):
        raise ValueError("cis_settings.json のhome_stale_daysはobject形式が必要です。")
    normalized_home = {}
    for k, v in home.items():
        try:
            n = int(v)
        except Exception as e:
            raise ValueError(f"cis_settings.json のhome_stale_days.{k} は整数が必要です。") from e
        if n <= 0:
            raise ValueError(f"cis_settings.json のhome_stale_days.{k} は1以上が必要です。")
        normalized_home[str(k)] = n
    settings["home_stale_days"] = normalized_home
    return settings


def get_tv_snapshot_stale_days() -> int:
    return int(load_settings().get("tv_snapshot_stale_days", 45))

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def backup_file(path: Path, reason: str) -> Optional[Path]:
    if not path.exists():
        return None
    safe_reason = re.sub(r"[^A-Za-z0-9_-]+", "_", reason)[:40] or "backup"
    ts = now_jst().strftime("%Y%m%d_%H%M%S")
    out = BACKUP_DIR / f"{path.name}.{ts}.{safe_reason}.bak"
    shutil.copy2(path, out)
    return out


@dataclass
class WatchItem:
    symbol: str
    market: str
    name: str
    asset_type: str
    active: bool
    category: str
    added_date: str
    notes: str
    description: str = ""

    @property
    def key(self) -> str:
        return f"{self.market}:{self.symbol}"

    @property
    def yf_symbol(self) -> str:
        return yf_symbol(self.symbol, self.market)


@dataclass
class PricePoint:
    symbol: str
    market: str
    latest_price: Optional[float]
    previous_price: Optional[float]
    daily_change: Optional[float]
    daily_pct: Optional[float]
    weekly_base_price: Optional[float]
    weekly_change: Optional[float]
    weekly_pct: Optional[float]
    source: str
    error: Optional[str] = None
    market_closed: bool = False
    latest_date: Optional[str] = None
    previous_date: Optional[str] = None
    stale_price: bool = False


@dataclass
class TVSnapshot:
    symbol: str
    market: str
    coverage_status: str = "covered"
    rating: Optional[str] = None
    analyst_count: Optional[int] = None
    avg_target_price: Optional[float] = None
    strong_buy_count: Optional[int] = None
    buy_count: Optional[int] = None
    hold_count: Optional[int] = None
    sell_count: Optional[int] = None
    strong_sell_count: Optional[int] = None
    updated_at: Optional[str] = None
    source: str = "TradingView"
    reason: str = ""

    @property
    def is_covered(self) -> bool:
        return self.coverage_status == "covered"

    @property
    def is_tv_ok(self) -> bool:
        if self.coverage_status in {"no_coverage", "not_applicable"}:
            return True
        return bool(self.rating) and self.analyst_count is not None and self.analyst_count > 0 and self.avg_target_price is not None and self.avg_target_price > 0


def _bool(value: Any) -> bool:
    # Backward-compatible wrapper used by older call sites.
    # Deliberately strict: typos such as "flase" must not become active=true.
    return parse_active_value(value)


def _require_csv_columns(path: Path, fieldnames: Optional[List[str]], required: Iterable[str]) -> None:
    if fieldnames is None:
        raise ValueError(f"CSVヘッダーがありません: {path.relative_to(ROOT)}")
    missing = [c for c in required if c not in fieldnames]
    if missing:
        raise ValueError(f"CSV必須列不足: {path.relative_to(ROOT)} / {', '.join(missing)}")


def _normalized_market_symbol_from_row(row: Dict[str, Any], path: Path, row_no: int) -> Tuple[str, str]:
    market = str(row.get("market") or "").strip().upper()
    try:
        symbol = validate_symbol_for_market(market, str(row.get("symbol") or ""))
    except Exception as e:
        raise ValueError(f"銘柄行が不正です: {path.relative_to(ROOT)} 行{row_no} market={market!r} symbol={row.get('symbol')!r} / {e}") from e
    return market, symbol


def load_company_master() -> Dict[str, Dict[str, str]]:
    path = DATA_DIR / "company_master.csv"
    out: Dict[str, Dict[str, str]] = {}
    if not path.exists():
        return out
    required = ["symbol", "market", "name", "description", "theme"]
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        _require_csv_columns(path, reader.fieldnames, required)
        for row_no, row in enumerate(reader, start=2):
            market, symbol = _normalized_market_symbol_from_row(row, path, row_no)
            k = f"{market}:{symbol}"
            if k in out:
                raise ValueError(f"company_master.csv に重複銘柄があります: {k} 行{row_no}")
            out[k] = {key: str(value or "") for key, value in row.items()}
            out[k]["market"] = market
            out[k]["symbol"] = symbol
    return out


def load_watchlist(active_only: bool = True) -> List[WatchItem]:
    path = DATA_DIR / "watchlist_master.csv"
    if not path.exists():
        raise FileNotFoundError("data/watchlist_master.csv が見つかりません。")
    companies = load_company_master()
    required = ["symbol", "market", "name", "asset_type", "active", "category", "added_date", "notes"]
    items: List[WatchItem] = []
    seen = set()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        _require_csv_columns(path, reader.fieldnames, required)
        for row_no, row in enumerate(reader, start=2):
            market, symbol = _normalized_market_symbol_from_row(row, path, row_no)
            k = f"{market}:{symbol}"
            if k in seen:
                raise ValueError(f"watchlist_master.csv に重複銘柄があります: {k} 行{row_no}")
            seen.add(k)
            try:
                active = parse_active_value(row.get("active"))
            except Exception as e:
                raise ValueError(f"watchlist_master.csv のactive値が不正です: {k} 行{row_no} / {e}") from e
            if active_only and not active:
                continue
            comp = companies.get(k, {})
            items.append(WatchItem(
                symbol=symbol,
                market=market,
                name=str(row.get("name") or comp.get("name") or symbol).strip(),
                asset_type=str(row.get("asset_type") or "stock").strip(),
                active=active,
                category=str(row.get("category") or "").strip(),
                added_date=str(row.get("added_date") or "").strip(),
                notes=str(row.get("notes") or "").strip(),
                description=str(comp.get("description") or row.get("notes") or "").strip(),
            ))
    if not items:
        raise ValueError("active=true の監視銘柄が0件です。")
    return items


def load_tv_snapshot() -> Dict[str, TVSnapshot]:
    path = DATA_DIR / "tv_snapshot.json"
    data = read_json_strict(path, default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, TVSnapshot] = {}
    if rows in [None, ""]:
        return out
    if not isinstance(rows, list):
        raise ValueError("tv_snapshot.json のitemsがlistではありません。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"tv_snapshot.json のitems[{idx}]がobjectではありません。")
        market = str(row.get("market") or "US").upper()
        try:
            symbol = validate_symbol_for_market(market, str(row.get("symbol") or ""))
        except Exception as e:
            raise ValueError(f"tv_snapshot.json の銘柄行が不正です: items[{idx}] / {e}") from e
        if market != "US":
            raise ValueError(f"tv_snapshot.json はUS銘柄のみです: items[{idx}] {market}:{symbol}")
        coverage_status = normalize_coverage_status(row.get("coverage_status") or "covered")
        rating = str(row.get("rating") or "").strip() or None
        analyst_count = safe_int(row.get("analyst_count"))
        avg_target_price = safe_float(row.get("avg_target_price"))
        if coverage_status == "covered":
            try:
                rating = parse_tv_rating(rating)
            except Exception as e:
                raise ValueError(f"tv_snapshot.json のratingが不正です: US:{symbol} items[{idx}] / {e}") from e
            if analyst_count is None or analyst_count <= 0 or avg_target_price is None or avg_target_price <= 0:
                raise ValueError(f"tv_snapshot.json のcovered行は analyst_count>0 / avg_target_price>0 が必要です: US:{symbol} items[{idx}]")
        else:
            try:
                validate_tv_noncovered_blank_fields(row, f"US:{symbol} items[{idx}]")
            except Exception as e:
                raise ValueError(str(e)) from e
            rating = None
            analyst_count = None
            avg_target_price = None
        k = f"US:{symbol}"
        if k in out:
            raise ValueError(f"tv_snapshot.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = TVSnapshot(
            symbol=symbol,
            market="US",
            coverage_status=coverage_status,
            rating=rating,
            analyst_count=analyst_count,
            avg_target_price=avg_target_price,
            strong_buy_count=safe_int(row.get("strong_buy_count")),
            buy_count=safe_int(row.get("buy_count")),
            hold_count=safe_int(row.get("hold_count")),
            sell_count=safe_int(row.get("sell_count")),
            strong_sell_count=safe_int(row.get("strong_sell_count")),
            updated_at=str(row.get("updated_at") or "").strip() or None,
            source=str(row.get("source") or "TradingView"),
            reason=str(row.get("reason") or "").strip(),
        )
    return out

def load_buyzone_master() -> Dict[str, Dict[str, Any]]:
    data = read_json_strict(DATA_DIR / "buyzone_master.json", default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, Dict[str, Any]] = {}
    if rows in [None, ""]:
        return out
    if not isinstance(rows, list):
        raise ValueError("buyzone_master.json のitemsがlistではありません。")
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"buyzone_master.json のitems[{idx}]がobjectではありません。")
        market = str(row.get("market") or "").upper()
        try:
            symbol = validate_symbol_for_market(market, str(row.get("symbol") or ""))
        except Exception as e:
            raise ValueError(f"buyzone_master.json の銘柄行が不正です: items[{idx}] / {e}") from e
        watch_price = safe_float(row.get("watch_price"))
        main_buy_price = safe_float(row.get("main_buy_price"))
        strong_buy_price = safe_float(row.get("strong_buy_price"))
        if watch_price is None or main_buy_price is None or strong_buy_price is None:
            raise ValueError(f"buyzone_master.json の買い場価格が未設定です: {market}:{symbol} items[{idx}]")
        if watch_price <= 0 or main_buy_price <= 0 or strong_buy_price <= 0:
            raise ValueError(f"buyzone_master.json の買い場価格は正の数値が必要です: {market}:{symbol} items[{idx}]")
        if not (strong_buy_price <= main_buy_price <= watch_price):
            raise ValueError(f"buyzone_master.json の価格順序が不正です: {market}:{symbol} items[{idx}]")
        updated_at = str(row.get("updated_at") or "").strip()
        if not updated_at:
            raise ValueError(f"buyzone_master.json のupdated_atが未設定です: {market}:{symbol} items[{idx}]")
        reason = str(row.get("reason") or "").strip()
        if not reason:
            raise ValueError(f"buyzone_master.json のreasonが未設定です: {market}:{symbol} items[{idx}]")
        k = f"{market}:{symbol}"
        if k in out:
            raise ValueError(f"buyzone_master.json に重複銘柄があります: {k} items[{idx}]")
        out[k] = dict(row, market=market, symbol=symbol, watch_price=watch_price, main_buy_price=main_buy_price, strong_buy_price=strong_buy_price)
    return out



def _json_items_strict(data: Any, name: str) -> List[Dict[str, Any]]:
    """Return JSON list/items rows and require every item to be an object.

    Several maintenance scripts call .get() on history rows.  A malformed
    history file such as {"items":[123]} must therefore be caught at
    Preflight/Apply Seed time instead of failing later during monthly
    maintenance.
    """
    rows = data.get("items") if isinstance(data, dict) else data
    if rows in [None, ""]:
        return []
    if not isinstance(rows, list):
        raise ValueError(f"{name} は list または items:list 形式が必要です。")
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{name} のitems[{idx}]がobjectではありません。")
        out.append(row)
    return out


def validate_history_json(path: Path, name: Optional[str] = None) -> int:
    """Strictly validate a CIS history JSON file and return item count."""
    label = name or path.name
    data = read_json_strict(path, default={"items": []}) or {"items": []}
    return len(_json_items_strict(data, label))


def validate_watchlist_company_consistency() -> Dict[str, Any]:
    """Require every watchlist row to have a matching company_master row.

    company_master may contain extra rows for dormant/future candidates, but a
    watched symbol without a company row means descriptions/themes can silently
    disappear from reports.  Treat that as a master-data error.
    """
    companies = load_company_master()
    items = load_watchlist(active_only=False)
    watch_keys = [item.key for item in items]
    company_keys = set(companies.keys())
    missing_company = [k for k in watch_keys if k not in company_keys]
    extra_company = sorted(k for k in company_keys if k not in set(watch_keys))
    if missing_company:
        sample = ", ".join(missing_company[:20])
        suffix = f" ほか{len(missing_company)-20}件" if len(missing_company) > 20 else ""
        raise ValueError(
            "watchlist_master.csv の銘柄が company_master.csv にありません: "
            + sample + suffix
        )
    return {
        "watchlist_count": len(watch_keys),
        "company_count": len(company_keys),
        "extra_company_count": len(extra_company),
        "extra_company": extra_company[:50],
    }

def _load_test_price_snapshot() -> Dict[str, Dict[str, Any]]:
    if os.getenv("CIS_TEST_MODE") != "1":
        return {}
    data = read_json(DATA_DIR / "price_snapshot.json", default={}) or {}
    rows = data.get("items") if isinstance(data, dict) else data
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(rows, list):
        for r in rows:
            if not isinstance(r, dict):
                continue
            market = str(r.get("market") or "").upper()
            sym = normalize_symbol(r.get("symbol"))
            if market == "JP":
                sym = clean_jp_symbol(sym)
            if market in MARKETS and sym:
                out[f"{market}:{sym}"] = r
    return out


def fetch_price(item: WatchItem, weekly: bool = False) -> PricePoint:
    test_prices = _load_test_price_snapshot()
    snap = test_prices.get(item.key)
    if snap:
        latest = safe_float(snap.get("latest_price"))
        prev = safe_float(snap.get("previous_price"))
        weekly_base = safe_float(snap.get("weekly_base_price"))
        daily_change = latest - prev if latest is not None and prev is not None else None
        daily_pct = daily_change / prev * 100 if daily_change is not None and prev else None
        weekly_change = latest - weekly_base if latest is not None and weekly_base is not None else None
        weekly_pct = weekly_change / weekly_base * 100 if weekly_change is not None and weekly_base else None
        latest_date = str(snap.get("latest_date") or today_jst())
        previous_date = str(snap.get("previous_date") or "") or None
        stale = False if weekly else latest_date < expected_daily_trade_date(item.market)
        return PricePoint(
            item.symbol, item.market, latest, prev, daily_change, daily_pct, weekly_base, weekly_change, weekly_pct,
            "price_snapshot(TEST_MODE)", None, stale, latest_date, previous_date, stale
        )

    if yf is None:
        return PricePoint(item.symbol, item.market, None, None, None, None, None, None, None, "none", "yfinance import failed")
    try:
        period = "1mo" if weekly else "7d"
        hist = yf.Ticker(item.yf_symbol).history(period=period, interval="1d", auto_adjust=False)
        if hist is None or hist.empty or "Close" not in hist:
            return PricePoint(item.symbol, item.market, None, None, None, None, None, None, None, "yfinance", "empty history")
        close_series = hist["Close"].dropna()
        closes = [float(x) for x in close_series.tolist()]
        dates = [str(getattr(idx, "date", lambda: idx)())[:10] for idx in close_series.index]
        if len(closes) < 2:
            latest = closes[-1] if closes else None
            latest_date = dates[-1] if dates else None
            return PricePoint(item.symbol, item.market, latest, None, None, None, None, None, None, "yfinance", "not enough data", True, latest_date, None, True)
        latest = closes[-1]
        prev = closes[-2]
        latest_date = dates[-1]
        previous_date = dates[-2]
        daily_change = latest - prev
        daily_pct = daily_change / prev * 100 if prev else None
        weekly_base = None
        if weekly:
            try:
                latest_dt = datetime.fromisoformat(str(latest_date)).date()
                threshold = latest_dt - timedelta(days=7)
                candidates = [(d, c) for d, c in zip(dates, closes) if datetime.fromisoformat(str(d)).date() <= threshold]
                weekly_base = candidates[-1][1] if candidates else closes[0]
            except Exception:
                weekly_base = closes[-6] if len(closes) >= 6 else closes[0]
        else:
            weekly_base = closes[-6] if len(closes) >= 6 else closes[0]
        weekly_change = latest - weekly_base if weekly_base is not None else None
        weekly_pct = weekly_change / weekly_base * 100 if weekly_change is not None and weekly_base else None
        stale = False
        err = None
        closed = False
        if not weekly:
            expected = expected_daily_trade_date(item.market)
            if latest_date < expected:
                stale = True
                closed = True
                err = f"latest trade date {latest_date} is older than expected {expected}; market closed or delayed data"
        return PricePoint(item.symbol, item.market, latest, prev, daily_change, daily_pct, weekly_base, weekly_change, weekly_pct, "yfinance", err, closed, latest_date, previous_date, stale)
    except Exception as e:
        return PricePoint(item.symbol, item.market, None, None, None, None, None, None, None, "yfinance", f"{type(e).__name__}: {e}")


def tv_upside(latest_price: Optional[float], tv: Optional[TVSnapshot]) -> Optional[float]:
    if latest_price is None or not tv or tv.coverage_status != "covered" or tv.avg_target_price is None or latest_price == 0:
        return None
    return (tv.avg_target_price - latest_price) / latest_price * 100.0




def tv_distribution_dict(tv: Optional[TVSnapshot]) -> Dict[str, int]:
    """Return stored TradingView analyst distribution counts.

    Keys are normalized CIS field names. Missing legacy rows return {} so older
    snapshots remain valid until the next monthly refresh populates distribution.
    """
    if not tv or tv.coverage_status != "covered":
        return {}
    pairs = [
        ("strong_buy_count", getattr(tv, "strong_buy_count", None)),
        ("buy_count", getattr(tv, "buy_count", None)),
        ("hold_count", getattr(tv, "hold_count", None)),
        ("sell_count", getattr(tv, "sell_count", None)),
        ("strong_sell_count", getattr(tv, "strong_sell_count", None)),
    ]
    if all(v is None for _k, v in pairs):
        return {}
    out: Dict[str, int] = {}
    for k, v in pairs:
        n = safe_int(v)
        out[k] = int(n) if n is not None and n >= 0 else 0
    return out


def tv_distribution_total(tv: Optional[TVSnapshot]) -> Optional[int]:
    counts = tv_distribution_dict(tv)
    if not counts:
        return None
    return sum(counts.values())


def tv_distribution_label(tv: Optional[TVSnapshot]) -> str:
    counts = tv_distribution_dict(tv)
    if not counts:
        return "未取得"
    return (
        f"強買{counts.get('strong_buy_count', 0)} / "
        f"買{counts.get('buy_count', 0)} / "
        f"中立{counts.get('hold_count', 0)} / "
        f"売{counts.get('sell_count', 0)} / "
        f"強売{counts.get('strong_sell_count', 0)}"
    )
def report_paths(stem: str) -> Dict[str, Path]:
    return {
        "output_md": OUTPUT_DIR / f"{stem}_latest.md",
        "output_json": OUTPUT_DIR / f"{stem}_latest.json",
        "output_status": OUTPUT_DIR / f"{stem}_status.json",
        "docs_md": DOCS_LATEST_DIR / f"{stem}_latest.md",
        "docs_html": DOCS_LATEST_DIR / f"{stem}_latest.html",
        "docs_json": DOCS_LATEST_DIR / f"{stem}_latest.json",
        "docs_status": DOCS_LATEST_DIR / f"{stem}_status_latest.json",
    }


def _inline_markdown(text: Any) -> str:
    """Escape text and convert a tiny subset of Markdown inline syntax."""
    escaped = html_escape(text).replace("**", "")
    # Convert [label](href) after escaping. href is kept conservative for local report links.
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    def repl(m: re.Match[str]) -> str:
        label = m.group(1)
        href = m.group(2).replace("'", "&#x27;").replace('"', "&quot;")
        return f"<a href='{href}'>{label}</a>"
    return pattern.sub(repl, escaped)


def markdown_to_simple_html(markdown: str, title: str = "CIS") -> str:
    """Convert the limited CIS Markdown format to iPhone-friendly HTML.

    Supports headings, cards, bullets, links and fenced code blocks. Code blocks
    are essential for Master Init Template pages because the user copies commands
    from an iPhone.
    """
    body: List[str] = []
    in_ul = False
    in_card = False
    in_pre = False
    pre_lines: List[str] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            body.append("</ul>")
            in_ul = False

    def close_card() -> None:
        nonlocal in_card
        close_ul()
        if in_card:
            body.append("</div>")
            in_card = False

    def close_pre() -> None:
        nonlocal in_pre, pre_lines
        if in_pre:
            body.append("<pre><code>%s</code></pre>" % html_escape("\n".join(pre_lines)))
            pre_lines = []
            in_pre = False

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_pre:
                close_pre()
            else:
                close_ul()
                in_pre = True
                pre_lines = []
            continue
        if in_pre:
            pre_lines.append(line)
            continue
        if not line:
            close_ul()
            continue
        if line.startswith("# "):
            close_card()
            body.append(f"<h1>{_inline_markdown(line[2:])}</h1>")
        elif line.startswith("## "):
            close_card()
            body.append(f"<h2>{_inline_markdown(line[3:])}</h2>")
        elif line.startswith("### "):
            close_card()
            in_card = True
            body.append(f"<div class='card'><h3>{_inline_markdown(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{_inline_markdown(line[2:])}</li>")
        else:
            close_ul()
            body.append(f"<p>{_inline_markdown(line)}</p>")
    close_pre()
    close_card()
    return """<!doctype html><html lang='ja'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>%s</title><style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:16px;line-height:1.55;background:#f7f7f7}h1{font-size:26px}.card{background:#fff;border-radius:14px;padding:12px;margin:12px 0;box-shadow:0 1px 4px #ddd}li{margin:6px 0}a{font-size:18px}pre{background:#111;color:#fff;border-radius:12px;padding:12px;white-space:pre-wrap;word-break:break-word;overflow-x:auto;font-size:14px;line-height:1.45}</style></head><body><p><a href='../index.html'>CISホームへ戻る</a></p>%s<p><a href='../index.html'>CISホームへ戻る</a></p></body></html>""" % (html_escape(title), "\n".join(body))


def write_report(stem: str, markdown: str, payload: Dict[str, Any], status: Dict[str, Any]) -> None:
    paths = report_paths(stem)
    for k in ["output_md", "docs_md"]:
        write_text(paths[k], markdown)
    write_text(paths["docs_html"], markdown_to_simple_html(markdown, stem))
    for k in ["output_json", "docs_json"]:
        write_json(paths[k], payload)
    for k in ["output_status", "docs_status"]:
        write_json(paths[k], status)


def write_error_report(stem: str, title: str, message: str) -> None:
    status = {"status": "error", "generated_at_jst": timestamp_jst(), "error": message}
    md = f"# {title}\n\n生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}\n\n## エラー\n\n{message}\n"
    write_report(stem, md, {"status": status, "rows": []}, status)


def status_badge(status: str) -> str:
    return {
        "ok": "✅ 更新済み",
        "partial": "⚠️ 一部注意",
        "error": "❌ エラー",
        "market_closed": "休場",
        "missing": "⚪ 未生成",
        "stale": "⚠️ 古い",
    }.get(status, f"⚪ {status}")


def load_status(stem: str) -> Dict[str, Any]:
    path = DOCS_LATEST_DIR / f"{stem}_status_latest.json"
    if not path.exists():
        return {"status": "missing"}
    data = read_json(path, default={}) or {}
    if not isinstance(data, dict):
        return {"status": "missing"}
    return data


def md_link(label: str, href: str) -> str:
    return f"[{label}]({href})"


def html_escape(s: Any) -> str:
    return html.escape(str(s or ""))
