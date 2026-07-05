#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch CIS v4 TradingView logic for analyst distribution.

v6 fix: remove fragile monthly report distribution-line insertion that caused IndentationError. Distribution is still persisted in candidate commands/tv_snapshot and shown in Daily US, Weekly Performance, and Buy Alert after apply. Compile gate remains enabled.

This patch intentionally uses TradingView data only. It does not add Yahoo,
MarketWatch, TipRanks, MarketBeat, or any other substitute data provider.

Scope:
- Extend tv_snapshot rows with optional analyst distribution counts.
- Fetch TradingView analyst distribution when available.
- Persist distribution through Master Update / Apply TV Monthly Candidate.
- Display distribution in Daily US, Weekly Performance, and Buy Alert.
- Keep upside/乖離率 as a report-time calculation from latest price and avg target.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "cis_v4"

DISTRIBUTION_FIELDS = [
    "strong_buy_count",
    "buy_count",
    "hold_count",
    "sell_count",
    "strong_sell_count",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def sub_once(text: str, pattern: str, repl: str, label: str, flags: int = re.S) -> str:
    new_text, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError(f"patch target not found: {label}")
    return new_text


def replace_exact_or_regex(text: str, old: str, new: str, pattern: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    return sub_once(text, pattern, new, label)


def patch_core() -> None:
    path = SCRIPTS / "cis_core.py"
    text = read(path)

    if "strong_buy_count: Optional[int]" not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)avg_target_price:\s*Optional\[float\]\s*=\s*None\s*$',
            r'\g<indent>avg_target_price: Optional[float] = None\n'
            r'\g<indent>strong_buy_count: Optional[int] = None\n'
            r'\g<indent>buy_count: Optional[int] = None\n'
            r'\g<indent>hold_count: Optional[int] = None\n'
            r'\g<indent>sell_count: Optional[int] = None\n'
            r'\g<indent>strong_sell_count: Optional[int] = None',
            "TVSnapshot distribution fields",
            flags=re.M,
        )

    if 'strong_buy_count=safe_int(row.get("strong_buy_count"))' not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)avg_target_price=avg_target_price,\s*$',
            r'\g<indent>avg_target_price=avg_target_price,\n'
            r'\g<indent>strong_buy_count=safe_int(row.get("strong_buy_count")),\n'
            r'\g<indent>buy_count=safe_int(row.get("buy_count")),\n'
            r'\g<indent>hold_count=safe_int(row.get("hold_count")),\n'
            r'\g<indent>sell_count=safe_int(row.get("sell_count")),\n'
            r'\g<indent>strong_sell_count=safe_int(row.get("strong_sell_count")),',
            "load_tv_snapshot constructor distribution fields",
            flags=re.M,
        )

    helper = '''\n\ndef tv_distribution_dict(tv: Optional[TVSnapshot]) -> Dict[str, int]:\n    """Return stored TradingView analyst distribution counts.\n\n    Keys are normalized CIS field names. Missing legacy rows return {} so older\n    snapshots remain valid until the next monthly refresh populates distribution.\n    """\n    if not tv or tv.coverage_status != "covered":\n        return {}\n    pairs = [\n        ("strong_buy_count", getattr(tv, "strong_buy_count", None)),\n        ("buy_count", getattr(tv, "buy_count", None)),\n        ("hold_count", getattr(tv, "hold_count", None)),\n        ("sell_count", getattr(tv, "sell_count", None)),\n        ("strong_sell_count", getattr(tv, "strong_sell_count", None)),\n    ]\n    if all(v is None for _k, v in pairs):\n        return {}\n    out: Dict[str, int] = {}\n    for k, v in pairs:\n        n = safe_int(v)\n        out[k] = int(n) if n is not None and n >= 0 else 0\n    return out\n\n\ndef tv_distribution_total(tv: Optional[TVSnapshot]) -> Optional[int]:\n    counts = tv_distribution_dict(tv)\n    if not counts:\n        return None\n    return sum(counts.values())\n\n\ndef tv_distribution_label(tv: Optional[TVSnapshot]) -> str:\n    counts = tv_distribution_dict(tv)\n    if not counts:\n        return "未取得"\n    return (\n        f"強買{counts.get('strong_buy_count', 0)} / "\n        f"買{counts.get('buy_count', 0)} / "\n        f"中立{counts.get('hold_count', 0)} / "\n        f"売{counts.get('sell_count', 0)} / "\n        f"強売{counts.get('strong_sell_count', 0)}"\n    )\n'''
    if "def tv_distribution_label" not in text:
        text = sub_once(
            text,
            r'(def\s+tv_upside\(.*?\n\s*return\s+\(tv\.avg_target_price\s*-\s*latest_price\)\s*/\s*latest_price\s*\*\s*100\.0\s*\n)',
            r'\1' + helper,
            "tv_distribution helper insertion",
        )

    write(path, text)


def patch_master_update() -> None:
    path = SCRIPTS / "cis_master_update.py"
    text = read(path)

    new_make_tv_update = '''def make_tv_update(cmd: Dict[str, Any]) -> Dict[str, Any]:\n    if cmd["market"] != "US":\n        raise ValueError(f"TV更新はUSのみ対応です: {cmd['raw']}")\n    parts = cmd["parts"]\n    if len(parts) < 2:\n        raise ValueError(\n            f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"\n            f"または TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜strong_buy｜buy｜hold｜sell｜strong_sell｜reason 形式です: {cmd['raw']}"\n        )\n\n    def nonnegative_int(value: Any, label: str) -> int:\n        n = safe_int(value)\n        if n is None or n < 0:\n            raise ValueError(f"{label} は0以上の整数が必要です: {value}")\n        return int(n)\n\n    def parse_distribution(start: int, analyst_count: int) -> Tuple[Dict[str, int], int]:\n        dist = {\n            "strong_buy_count": nonnegative_int(parts[start], "Strong Buy人数"),\n            "buy_count": nonnegative_int(parts[start + 1], "Buy人数"),\n            "hold_count": nonnegative_int(parts[start + 2], "Hold/Neutral人数"),\n            "sell_count": nonnegative_int(parts[start + 3], "Sell人数"),\n            "strong_sell_count": nonnegative_int(parts[start + 4], "Strong Sell人数"),\n        }\n        total = sum(dist.values())\n        if total <= 0:\n            raise ValueError(f"アナリスト分布の合計が0です: {cmd['raw']}")\n        if analyst_count != total:\n            raise ValueError(\n                f"アナリスト人数と分布合計が一致しません: analyst_count={analyst_count} distribution_total={total} / {cmd['raw']}"\n            )\n        return dist, total\n\n    first = parts[1]\n    explicit_status = is_coverage_token(first)\n    coverage_status = parse_coverage_status(first) if explicit_status else "covered"\n    if coverage_status == "covered":\n        distribution: Dict[str, int] = {}\n        if explicit_status:\n            if len(parts) not in {5, 6, 10, 11}:\n                raise ValueError(\n                    f"covered更新は TV US SYMBOL｜covered｜rating｜analyst_count｜avg_target_price｜reason、"\n                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"\n                )\n            rating = parse_rating(parts[2])\n            analyst_count = require_positive_int(parts[3], "アナリスト人数")\n            avg_target_price = require_positive_number(parts[4], "平均目標株価")\n            if len(parts) in {10, 11}:\n                distribution, _total = parse_distribution(5, analyst_count)\n                reason = parts[10] if len(parts) == 11 else "月次更新"\n            else:\n                reason = parts[5] if len(parts) == 6 else "月次更新"\n        else:\n            if len(parts) not in {4, 5, 9, 10}:\n                raise ValueError(\n                    f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"\n                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"\n                )\n            rating = parse_rating(parts[1])\n            analyst_count = require_positive_int(parts[2], "アナリスト人数")\n            avg_target_price = require_positive_number(parts[3], "平均目標株価")\n            if len(parts) in {9, 10}:\n                distribution, _total = parse_distribution(4, analyst_count)\n                reason = parts[9] if len(parts) == 10 else "月次更新"\n            else:\n                reason = parts[4] if len(parts) == 5 else "月次更新"\n        out = {\n            "symbol": cmd["symbol"],\n            "market": "US",\n            "coverage_status": "covered",\n            "rating": rating,\n            "analyst_count": analyst_count,\n            "avg_target_price": avg_target_price,\n            "updated_at": timestamp_jst(),\n            "source": "TradingView",\n            "reason": reason,\n        }\n        if distribution:\n            out.update(distribution)\n        return out\n\n    if len(parts) not in {2, 3}:\n        raise ValueError(\n            f"{coverage_status}更新は TV US SYMBOL｜{coverage_status}｜reason 形式です。"\n            f"rating/人数/目標株価/分布など余計な列は入れないでください: {cmd['raw']}"\n        )\n    reason = parts[2] if len(parts) == 3 else ("TradingViewにアナリスト予想なし" if coverage_status == "no_coverage" else "TradingView対象外")\n    return {\n        "symbol": cmd["symbol"],\n        "market": "US",\n        "coverage_status": coverage_status,\n        "rating": None,\n        "analyst_count": None,\n        "avg_target_price": None,\n        "updated_at": timestamp_jst(),\n        "source": "TradingView",\n        "reason": reason,\n    }\n\n'''
    if "parse_distribution(start" not in text:
        text = sub_once(
            text,
            r'def\s+make_tv_update\(cmd:\s*Dict\[str,\s*Any\]\)\s*->\s*Dict\[str,\s*Any\]:.*?(?=def\s+make_buyzone_update)',
            new_make_tv_update,
            "replace make_tv_update",
        )

    if '"strong_buy_count"' not in re.search(r'def\s+diff\(', text).string if False else text:
        # Keep existing diff() generic; only the TV call field list needs expanding.
        pass
    text = text.replace(
        'fields = ["coverage_status", "rating", "analyst_count", "avg_target_price", "source", "reason"]',
        'fields = ["coverage_status", "rating", "analyst_count", "avg_target_price", "strong_buy_count", "buy_count", "hold_count", "sell_count", "strong_sell_count", "source", "reason"]',
        1,
    )

    write(path, text)


def patch_tv_monthly_refresh() -> None:
    path = SCRIPTS / "cis_tv_monthly_refresh.py"
    text = read(path)

    scanner_sets = '''SCANNER_COLUMN_SETS = [\n    ["name", "description", "exchange", "analyst_rating", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],\n    ["name", "description", "exchange", "analyst_rating", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],\n    ["name", "description", "exchange", "Analyst Rating", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],\n    ["name", "description", "exchange", "recommendation_mark", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],\n    ["name", "description", "exchange", "analyst_rating", "analysts_count", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],\n]\nCANDIDATE_MANIFEST_FILENAME ='''
    if "analyst_rating_strong_buy" not in text.split("CANDIDATE_MANIFEST_FILENAME", 1)[0]:
        text = sub_once(
            text,
            r'SCANNER_COLUMN_SETS\s*=\s*\[.*?\]\s*CANDIDATE_MANIFEST_FILENAME\s*=',
            scanner_sets,
            "SCANNER_COLUMN_SETS with distribution",
        )

    fetched_tv_block = '''@dataclass\nclass FetchedTV:\n    symbol: str\n    market: str\n    coverage_status: str\n    rating: Optional[str]\n    analyst_count: Optional[int]\n    avg_target_price: Optional[float]\n    source: str\n    exchange: Optional[str] = None\n    raw: Optional[Dict[str, Any]] = None\n    strong_buy_count: Optional[int] = None\n    buy_count: Optional[int] = None\n    hold_count: Optional[int] = None\n    sell_count: Optional[int] = None\n    strong_sell_count: Optional[int] = None\n\n    def distribution_values(self) -> List[Optional[int]]:\n        return [self.strong_buy_count, self.buy_count, self.hold_count, self.sell_count, self.strong_sell_count]\n\n    def distribution_total(self) -> Optional[int]:\n        vals = self.distribution_values()\n        if all(v is None for v in vals):\n            return None\n        return sum(int(v or 0) for v in vals)\n\n    def distribution_label(self) -> str:\n        total = self.distribution_total()\n        if total is None:\n            return "未取得"\n        return f"強買{self.strong_buy_count or 0} / 買{self.buy_count or 0} / 中立{self.hold_count or 0} / 売{self.sell_count or 0} / 強売{self.strong_sell_count or 0}"\n\n    def to_command(self) -> str:\n        reason = f"TradingView monthly auto-check {now_jst().strftime('%Y/%m')}"\n        if self.coverage_status == "covered":\n            total = self.distribution_total()\n            if total and self.analyst_count == total:\n                return (\n                    f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|"\n                    f"{self.strong_buy_count or 0}|{self.buy_count or 0}|{self.hold_count or 0}|{self.sell_count or 0}|{self.strong_sell_count or 0}|{reason}"\n                )\n            return f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|{reason}"\n        return f"TV US {self.symbol}|{self.coverage_status}|{reason}"\n\n'''
    if "distribution_values(self)" not in text:
        text = sub_once(
            text,
            r'@dataclass\s+class\s+FetchedTV:.*?(?=def\s+normalize_rating)',
            fetched_tv_block,
            "FetchedTV distribution dataclass",
        )

    candidate_block = '''def _first_int(values: Dict[str, Any], keys: Iterable[str]) -> Optional[int]:\n    for k in keys:\n        n = safe_int(values.get(k))\n        if n is not None:\n            return n\n    return None\n\n\ndef distribution_from_values(values: Dict[str, Any]) -> Dict[str, Optional[int]]:\n    return {\n        "strong_buy_count": _first_int(values, ["analyst_rating_strong_buy", "strong_buy", "strongBuy", "recommendation_strong_buy", "analyst_strong_buy"]),\n        "buy_count": _first_int(values, ["analyst_rating_buy", "buy", "recommendation_buy", "analyst_buy"]),\n        "hold_count": _first_int(values, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral", "recommendation_hold", "analyst_hold"]),\n        "sell_count": _first_int(values, ["analyst_rating_sell", "sell", "recommendation_sell", "analyst_sell"]),\n        "strong_sell_count": _first_int(values, ["analyst_rating_strong_sell", "strong_sell", "strongSell", "recommendation_strong_sell", "analyst_strong_sell"]),\n    }\n\n\ndef distribution_total(dist: Dict[str, Optional[int]]) -> Optional[int]:\n    vals = list(dist.values())\n    if all(v is None for v in vals):\n        return None\n    total = sum(int(v or 0) for v in vals)\n    return total if total > 0 else None\n\n\ndef candidate_from_values(symbol: str, values: Dict[str, Any], source: str, exchange: Optional[str] = None) -> Optional[FetchedTV]:\n    rating_keys = ["analyst_rating", "Analyst Rating", "recommendation_mark", "rating", "recommendation"]\n    count_keys = ["number_of_analysts", "analysts_count", "analyst_count", "analyst_count_current"]\n    target_keys = ["target_price_average", "price_target_average", "average_target_price", "avg_target_price", "target_price_avg"]\n    rating = None\n    for k in rating_keys:\n        rating = normalize_rating(values.get(k))\n        if rating:\n            break\n    dist = distribution_from_values(values)\n    dist_total = distribution_total(dist)\n    analyst_count = dist_total\n    if analyst_count is None:\n        for k in count_keys:\n            analyst_count = safe_int(values.get(k))\n            if analyst_count is not None:\n                break\n    avg_target = None\n    for k in target_keys:\n        avg_target = safe_float(values.get(k))\n        if avg_target is not None:\n            break\n    if rating and analyst_count and analyst_count > 0 and avg_target and avg_target > 0:\n        return FetchedTV(\n            symbol=symbol,\n            market="US",\n            coverage_status="covered",\n            rating=rating,\n            analyst_count=analyst_count,\n            avg_target_price=avg_target,\n            source=source,\n            exchange=exchange,\n            raw=values,\n            **dist,\n        )\n    return None\n\n'''
    if "def distribution_from_values" not in text:
        text = sub_once(
            text,
            r'def\s+candidate_from_values\(symbol:\s*str,\s*values:\s*Dict\[str,\s*Any\],\s*source:\s*str,\s*exchange:\s*Optional\[str\]\s*=\s*None\)\s*->\s*Optional\[FetchedTV\]:.*?(?=def\s+load_fixture)',
            candidate_block,
            "candidate_from_values distribution",
        )

    load_fixture_block = '''def load_fixture() -> Dict[str, FetchedTV]:\n    path = os.getenv("CIS_TV_REFRESH_FIXTURE") or os.getenv("CIS_TV_REFRESH_TEST_FIXTURE")\n    if not path:\n        return {}\n    data = read_json_strict(Path(path), default={}) or {}\n    rows = data.get("items") if isinstance(data, dict) else data\n    out: Dict[str, FetchedTV] = {}\n    if not isinstance(rows, list):\n        raise ValueError("TV refresh fixture は items:list 形式が必要です。")\n    for idx, row in enumerate(rows, start=1):\n        if not isinstance(row, dict):\n            raise ValueError(f"TV refresh fixture items[{idx}] がobjectではありません。")\n        symbol = validate_symbol_for_market("US", row.get("symbol"))\n        cov = str(row.get("coverage_status") or "covered")\n        if cov == "covered":\n            rating = normalize_rating(row.get("rating"))\n            analyst_count = safe_int(row.get("analyst_count"))\n            avg_target = safe_float(row.get("avg_target_price"))\n            if not rating or not analyst_count or not avg_target:\n                raise ValueError(f"fixture covered行が不正です: US:{symbol}")\n            out[f"US:{symbol}"] = FetchedTV(\n                symbol, "US", "covered", rating, analyst_count, avg_target, "fixture", row.get("exchange"), row,\n                strong_buy_count=safe_int(row.get("strong_buy_count")),\n                buy_count=safe_int(row.get("buy_count")),\n                hold_count=safe_int(row.get("hold_count")),\n                sell_count=safe_int(row.get("sell_count")),\n                strong_sell_count=safe_int(row.get("strong_sell_count")),\n            )\n        else:\n            out[f"US:{symbol}"] = FetchedTV(symbol, "US", cov, None, None, None, "fixture", row.get("exchange"), row)\n    return out\n\n'''
    if 'strong_buy_count=safe_int(row.get("strong_buy_count"))' not in text:
        text = sub_once(text, r'def\s+load_fixture\(\)\s*->\s*Dict\[str,\s*FetchedTV\]:.*?(?=def\s+_regex_json_value)', load_fixture_block, "load_fixture distribution")

    forecast_block = '''def fetch_from_tradingview_forecast_page(symbol: str) -> Tuple[Optional[FetchedTV], Optional[str]]:\n    errors: List[str] = []\n    for ex in EXCHANGE_CANDIDATES:\n        url = f"https://www.tradingview.com/symbols/{ex}-{symbol}/forecast/"\n        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (CIS-v4-tv-refresh)", "Accept": "text/html,*/*"})\n        try:\n            with urllib.request.urlopen(req, timeout=25) as resp:\n                text = resp.read().decode("utf-8", errors="ignore")\n            values = {\n                "analyst_rating": _regex_json_value(text, ["analyst_rating", "Analyst Rating", "recommendation", "recommendation_mark"]),\n                "number_of_analysts": _regex_json_value(text, ["number_of_analysts", "analysts_count", "analyst_count"]),\n                "target_price_average": _regex_json_value(text, ["target_price_average", "price_target_average", "average_target_price", "avg_target_price"]),\n                "analyst_rating_strong_buy": _regex_json_value(text, ["analyst_rating_strong_buy", "strong_buy", "strongBuy"]),\n                "analyst_rating_buy": _regex_json_value(text, ["analyst_rating_buy", "buy"]),\n                "analyst_rating_hold": _regex_json_value(text, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral"]),\n                "analyst_rating_sell": _regex_json_value(text, ["analyst_rating_sell", "sell"]),\n                "analyst_rating_strong_sell": _regex_json_value(text, ["analyst_rating_strong_sell", "strong_sell", "strongSell"]),\n            }\n            cand = candidate_from_values(symbol, values, source="TradingView forecast page", exchange=ex)\n            if cand:\n                return cand, None\n            errors.append(f"{ex}: forecast fields not found")\n        except urllib.error.HTTPError as e:\n            errors.append(f"{ex}: HTTPError {e.code}")\n        except Exception as e:\n            errors.append(f"{ex}: {type(e).__name__}: {e}")\n    return None, " / ".join(errors[-3:]) if errors else "forecast page取得不可"\n\n'''
    if '"analyst_rating_strong_buy": _regex_json_value' not in text:
        text = sub_once(text, r'def\s+fetch_from_tradingview_forecast_page\(symbol:\s*str\)\s*->\s*Tuple\[Optional\[FetchedTV\],\s*Optional\[str\]\]:.*?(?=def\s+scanner_request)', forecast_block, "forecast page distribution")

    tv_snapshot_to_dict = '''def tv_snapshot_to_dict(s: TVSnapshot) -> Dict[str, Any]:\n    return {\n        "symbol": s.symbol,\n        "market": s.market,\n        "coverage_status": s.coverage_status,\n        "rating": s.rating,\n        "analyst_count": s.analyst_count,\n        "avg_target_price": s.avg_target_price,\n        "strong_buy_count": getattr(s, "strong_buy_count", None),\n        "buy_count": getattr(s, "buy_count", None),\n        "hold_count": getattr(s, "hold_count", None),\n        "sell_count": getattr(s, "sell_count", None),\n        "strong_sell_count": getattr(s, "strong_sell_count", None),\n        "updated_at": s.updated_at,\n        "source": s.source,\n        "reason": s.reason,\n    }\n\n'''
    if '"strong_buy_count": getattr(s, "strong_buy_count", None)' not in text:
        text = sub_once(text, r'def\s+tv_snapshot_to_dict\(s:\s*TVSnapshot\)\s*->\s*Dict\[str,\s*Any\]:.*?(?=def\s+diff_fields)', tv_snapshot_to_dict, "tv_snapshot_to_dict distribution")

    diff_fields_block = '''def diff_fields(old: Optional[TVSnapshot], new: FetchedTV) -> List[str]:\n    if old is None:\n        return ["新規取得"]\n    out: List[str] = []\n    checks = [\n        ("coverage_status", old.coverage_status, new.coverage_status),\n        ("rating", old.rating, new.rating),\n        ("analyst_count", old.analyst_count, new.analyst_count),\n        ("avg_target_price", old.avg_target_price, new.avg_target_price),\n        ("strong_buy_count", getattr(old, "strong_buy_count", None), new.strong_buy_count),\n        ("buy_count", getattr(old, "buy_count", None), new.buy_count),\n        ("hold_count", getattr(old, "hold_count", None), new.hold_count),\n        ("sell_count", getattr(old, "sell_count", None), new.sell_count),\n        ("strong_sell_count", getattr(old, "strong_sell_count", None), new.strong_sell_count),\n    ]\n    for label, a, b in checks:\n        if a != b:\n            if label == "avg_target_price":\n                aa = "未設定" if a in [None, ""] else f"{float(a):.2f}"\n                bb = "未設定" if b in [None, ""] else f"{float(b):.2f}"\n            else:\n                aa = a if a not in [None, ""] else "未設定"\n                bb = b if b not in [None, ""] else "未設定"\n            out.append(f"{label}: {aa} → {bb}")\n    return out\n\n'''
    if '"strong_sell_count", getattr(old, "strong_sell_count", None)' not in text:
        text = sub_once(text, r'def\s+diff_fields\(old:\s*Optional\[TVSnapshot\],\s*new:\s*FetchedTV\)\s*->\s*List\[str\]:.*?(?=def\s+split_lines)', diff_fields_block, "diff_fields distribution checks")

    # v6 deliberately does not patch the human-readable monthly report list for
    # distribution display. The distribution counts are still carried in generated
    # apply commands, persisted through Master Update, and displayed in Daily US,
    # Weekly Performance, and Buy Alert after apply. Avoiding this report-only
    # insertion removes the indentation risk that stopped v5 at py_compile.

    write(path, text)


def patch_us_report(path: Path) -> None:
    text = read(path)
    if "tv_distribution_label" not in text.split("from cis_core import", 1)[-1].split(")", 1)[0]:
        text = sub_once(text, r'(\s*tv_upside,\s*\n)', r'\1    tv_distribution_label,\n', f"{path.name} import tv_distribution_label")
    if '"tv_distribution": tv_distribution_label(tv) if tv else "未取得"' not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)"tv_analyst_count":\s*tv\.analyst_count\s*if\s*tv\s*else\s*None,\s*$',
            r'\g<indent>"tv_analyst_count": tv.analyst_count if tv else None,\n\g<indent>"tv_distribution": tv_distribution_label(tv) if tv else "未取得",',
            f"{path.name} row distribution",
            flags=re.M,
        )
    if "アナリスト分布" not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)f"- アナリスト人数：\{ac\}人"\s*if\s*ac\s*is\s*not\s*None\s*else\s*f"- アナリスト人数：\{na\}",\s*$',
            r'\g<indent>f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}",\n\g<indent>"- アナリスト分布：" + str(r.get("tv_distribution") if cov == "covered" else na),',
            f"{path.name} display distribution",
            flags=re.M,
        )
    write(path, text)


def patch_buy_alert() -> None:
    path = SCRIPTS / "cis_buy_alert.py"
    text = read(path)
    if "tv_distribution_label" not in text.split("from cis_core import", 1)[-1].split(")", 1)[0]:
        text = sub_once(text, r'(\s*tv_upside,\s*\n)', r'\1    tv_distribution_label,\n', "buy_alert import tv_distribution_label")
    if '"tv_distribution": tv_distribution_label(tv) if tv else "未取得"' not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)"tv_analyst_count":\s*tv\.analyst_count\s*if\s*tv\s*else\s*None,\s*$',
            r'\g<indent>"tv_analyst_count": tv.analyst_count if tv else None,\n\g<indent>"tv_distribution": tv_distribution_label(tv) if tv else "未取得",',
            "buy_alert row distribution",
            flags=re.M,
        )
    if "TVアナリスト分布" not in text:
        text = sub_once(
            text,
            r'(?m)^(?P<indent>\s*)f"- TVアナリスト人数：\{r\.get\(\'tv_analyst_count\'\) if r\.get\(\'tv_analyst_count\'\) is not None else \'なし\'\}",\s*$',
            r'\g<indent>"- TVアナリスト人数：" + str(r.get("tv_analyst_count") if r.get("tv_analyst_count") is not None else "なし"),\n\g<indent>"- TVアナリスト分布：" + str(r.get("tv_distribution") if r.get("tv_distribution") else "未取得"),',
            "buy_alert display distribution",
            flags=re.M,
        )
    write(path, text)


def main() -> int:
    patch_core()
    patch_master_update()
    patch_tv_monthly_refresh()
    patch_us_report(SCRIPTS / "cis_daily_us.py")
    patch_us_report(SCRIPTS / "cis_weekly_performance.py")
    patch_buy_alert()
    print("TV distribution patch v6 applied. TradingView-only logic; no substitute data providers added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
