#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch CIS v4 TradingView logic for analyst distribution.

This patch intentionally uses TradingView data only. It does not add Yahoo,
MarketWatch, TipRanks, MarketBeat, or other substitute data providers.

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


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"patch target not found: {label}")
    return text.replace(old, new, 1)


def regex_replace_once(text: str, pattern: str, repl: str, label: str) -> str:
    if repl in text:
        return text
    new_text, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"regex patch target not found: {label}")
    return new_text


def patch_core() -> None:
    path = SCRIPTS / "cis_core.py"
    text = read(path)

    text = replace_once(
        text,
        'avg_target_price: Optional[float] = None updated_at: Optional[str] = None source: str = "TradingView" reason: str = ""',
        'avg_target_price: Optional[float] = None strong_buy_count: Optional[int] = None buy_count: Optional[int] = None hold_count: Optional[int] = None sell_count: Optional[int] = None strong_sell_count: Optional[int] = None updated_at: Optional[str] = None source: str = "TradingView" reason: str = ""',
        "TVSnapshot distribution fields",
    )

    text = replace_once(
        text,
        'avg_target_price=avg_target_price, updated_at=str(row.get("updated_at") or "").strip() or None, source=str(row.get("source") or "TradingView"), reason=str(row.get("reason") or "").strip(), )',
        'avg_target_price=avg_target_price, strong_buy_count=safe_int(row.get("strong_buy_count")), buy_count=safe_int(row.get("buy_count")), hold_count=safe_int(row.get("hold_count")), sell_count=safe_int(row.get("sell_count")), strong_sell_count=safe_int(row.get("strong_sell_count")), updated_at=str(row.get("updated_at") or "").strip() or None, source=str(row.get("source") or "TradingView"), reason=str(row.get("reason") or "").strip(), )',
        "load_tv_snapshot constructor distribution fields",
    )

    helper = '''

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
'''
    if "def tv_distribution_label" not in text:
        text = replace_once(
            text,
            'def tv_upside(latest_price: Optional[float], tv: Optional[TVSnapshot]) -> Optional[float]: if latest_price is None or not tv or tv.coverage_status != "covered" or tv.avg_target_price is None or latest_price == 0: return None return (tv.avg_target_price - latest_price) / latest_price * 100.0',
            'def tv_upside(latest_price: Optional[float], tv: Optional[TVSnapshot]) -> Optional[float]: if latest_price is None or not tv or tv.coverage_status != "covered" or tv.avg_target_price is None or latest_price == 0: return None return (tv.avg_target_price - latest_price) / latest_price * 100.0' + helper,
            "tv_distribution helper insertion",
        )

    write(path, text)


def patch_master_update() -> None:
    path = SCRIPTS / "cis_master_update.py"
    text = read(path)

    new_make_tv_update = r'''def make_tv_update(cmd: Dict[str, Any]) -> Dict[str, Any]:
    if cmd["market"] != "US":
        raise ValueError(f"TV更新はUSのみ対応です: {cmd['raw']}")
    parts = cmd["parts"]
    if len(parts) < 2:
        raise ValueError(
            f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"
            f"または TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜strong_buy｜buy｜hold｜sell｜strong_sell｜reason 形式です: {cmd['raw']}"
        )

    def nonnegative_int(value: Any, label: str) -> int:
        n = safe_int(value)
        if n is None or n < 0:
            raise ValueError(f"{label} は0以上の整数が必要です: {value}")
        return int(n)

    def parse_distribution(start: int, analyst_count: int) -> Tuple[Dict[str, int], int]:
        dist = {
            "strong_buy_count": nonnegative_int(parts[start], "Strong Buy人数"),
            "buy_count": nonnegative_int(parts[start + 1], "Buy人数"),
            "hold_count": nonnegative_int(parts[start + 2], "Hold/Neutral人数"),
            "sell_count": nonnegative_int(parts[start + 3], "Sell人数"),
            "strong_sell_count": nonnegative_int(parts[start + 4], "Strong Sell人数"),
        }
        total = sum(dist.values())
        if total <= 0:
            raise ValueError(f"アナリスト分布の合計が0です: {cmd['raw']}")
        if analyst_count != total:
            raise ValueError(
                f"アナリスト人数と分布合計が一致しません: analyst_count={analyst_count} distribution_total={total} / {cmd['raw']}"
            )
        return dist, total

    first = parts[1]
    explicit_status = is_coverage_token(first)
    coverage_status = parse_coverage_status(first) if explicit_status else "covered"
    if coverage_status == "covered":
        distribution: Dict[str, int] = {}
        if explicit_status:
            # covered｜rating｜count｜avg｜reason  または covered｜rating｜count｜avg｜SB｜B｜H｜S｜SS｜reason
            if len(parts) not in {5, 6, 10, 11}:
                raise ValueError(
                    f"covered更新は TV US SYMBOL｜covered｜rating｜analyst_count｜avg_target_price｜reason、"
                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[2])
            analyst_count = require_positive_int(parts[3], "アナリスト人数")
            avg_target_price = require_positive_number(parts[4], "平均目標株価")
            if len(parts) in {10, 11}:
                distribution, _total = parse_distribution(5, analyst_count)
                reason = parts[10] if len(parts) == 11 else "月次更新"
            else:
                reason = parts[5] if len(parts) == 6 else "月次更新"
        else:
            # rating｜count｜avg｜reason または rating｜count｜avg｜SB｜B｜H｜S｜SS｜reason
            if len(parts) not in {4, 5, 9, 10}:
                raise ValueError(
                    f"TV更新は TV US SYMBOL｜rating｜analyst_count｜avg_target_price｜reason、"
                    f"または分布付き形式です。余計な列または不足列があります: {cmd['raw']}"
                )
            rating = parse_rating(parts[1])
            analyst_count = require_positive_int(parts[2], "アナリスト人数")
            avg_target_price = require_positive_number(parts[3], "平均目標株価")
            if len(parts) in {9, 10}:
                distribution, _total = parse_distribution(4, analyst_count)
                reason = parts[9] if len(parts) == 10 else "月次更新"
            else:
                reason = parts[4] if len(parts) == 5 else "月次更新"
        out = {
            "symbol": cmd["symbol"],
            "market": "US",
            "coverage_status": "covered",
            "rating": rating,
            "analyst_count": analyst_count,
            "avg_target_price": avg_target_price,
            "updated_at": timestamp_jst(),
            "source": "TradingView",
            "reason": reason,
        }
        if distribution:
            out.update(distribution)
        return out

    if len(parts) not in {2, 3}:
        raise ValueError(
            f"{coverage_status}更新は TV US SYMBOL｜{coverage_status}｜reason 形式です。"
            f"rating/人数/目標株価/分布など余計な列は入れないでください: {cmd['raw']}"
        )
    reason = parts[2] if len(parts) == 3 else ("TradingViewにアナリスト予想なし" if coverage_status == "no_coverage" else "TradingView対象外")
    return {
        "symbol": cmd["symbol"],
        "market": "US",
        "coverage_status": coverage_status,
        "rating": None,
        "analyst_count": None,
        "avg_target_price": None,
        "updated_at": timestamp_jst(),
        "source": "TradingView",
        "reason": reason,
    }

'''
    if "parse_distribution(start" not in text:
        text = regex_replace_once(
            text,
            r"def make_tv_update\(cmd: Dict\[str, Any\]\) -> Dict\[str, Any\]:.*?def make_buyzone_update",
            new_make_tv_update + "def make_buyzone_update",
            "replace make_tv_update",
        )

    text = replace_once(
        text,
        'fields = ["coverage_status", "rating", "analyst_count", "avg_target_price", "source", "reason"]',
        'fields = ["coverage_status", "rating", "analyst_count", "avg_target_price", "strong_buy_count", "buy_count", "hold_count", "sell_count", "strong_sell_count", "source", "reason"]',
        "TV diff fields include distribution",
    )

    write(path, text)


def patch_tv_monthly_refresh() -> None:
    path = SCRIPTS / "cis_tv_monthly_refresh.py"
    text = read(path)

    scanner_sets = '''SCANNER_COLUMN_SETS = [
    ["name", "description", "exchange", "analyst_rating", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "analyst_rating", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "Analyst Rating", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "recommendation_mark", "number_of_analysts", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
    ["name", "description", "exchange", "analyst_rating", "analysts_count", "target_price_average", "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell"],
] CANDIDATE_MANIFEST_FILENAME ='''
    if "analyst_rating_strong_buy" not in text.split("CANDIDATE_MANIFEST_FILENAME", 1)[0]:
        text = regex_replace_once(
            text,
            r"SCANNER_COLUMN_SETS = \[.*?\] CANDIDATE_MANIFEST_FILENAME =",
            scanner_sets,
            "SCANNER_COLUMN_SETS with distribution",
        )

    fetched_tv_block = r'''@dataclass class FetchedTV:
    symbol: str
    market: str
    coverage_status: str
    rating: Optional[str]
    analyst_count: Optional[int]
    avg_target_price: Optional[float]
    source: str
    exchange: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
    strong_buy_count: Optional[int] = None
    buy_count: Optional[int] = None
    hold_count: Optional[int] = None
    sell_count: Optional[int] = None
    strong_sell_count: Optional[int] = None

    def distribution_values(self) -> List[Optional[int]]:
        return [self.strong_buy_count, self.buy_count, self.hold_count, self.sell_count, self.strong_sell_count]

    def distribution_total(self) -> Optional[int]:
        vals = self.distribution_values()
        if all(v is None for v in vals):
            return None
        return sum(int(v or 0) for v in vals)

    def distribution_label(self) -> str:
        total = self.distribution_total()
        if total is None:
            return "未取得"
        return f"強買{self.strong_buy_count or 0} / 買{self.buy_count or 0} / 中立{self.hold_count or 0} / 売{self.sell_count or 0} / 強売{self.strong_sell_count or 0}"

    def to_command(self) -> str:
        reason = f"TradingView monthly auto-check {now_jst().strftime('%Y/%m')}"
        if self.coverage_status == "covered":
            total = self.distribution_total()
            if total and self.analyst_count == total:
                return (
                    f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|"
                    f"{self.strong_buy_count or 0}|{self.buy_count or 0}|{self.hold_count or 0}|{self.sell_count or 0}|{self.strong_sell_count or 0}|{reason}"
                )
            return f"TV US {self.symbol}|{self.rating}|{self.analyst_count}|{self.avg_target_price:.2f}|{reason}"
        return f"TV US {self.symbol}|{self.coverage_status}|{reason}"

'''
    if "distribution_values(self)" not in text:
        text = regex_replace_once(
            text,
            r"@dataclass class FetchedTV:.*?def normalize_rating",
            fetched_tv_block + "def normalize_rating",
            "FetchedTV distribution dataclass",
        )

    candidate_block = r'''def _first_int(values: Dict[str, Any], keys: Iterable[str]) -> Optional[int]:
    for k in keys:
        n = safe_int(values.get(k))
        if n is not None:
            return n
    return None


def distribution_from_values(values: Dict[str, Any]) -> Dict[str, Optional[int]]:
    return {
        "strong_buy_count": _first_int(values, ["analyst_rating_strong_buy", "strong_buy", "strongBuy", "recommendation_strong_buy", "analyst_strong_buy"]),
        "buy_count": _first_int(values, ["analyst_rating_buy", "buy", "recommendation_buy", "analyst_buy"]),
        "hold_count": _first_int(values, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral", "recommendation_hold", "analyst_hold"]),
        "sell_count": _first_int(values, ["analyst_rating_sell", "sell", "recommendation_sell", "analyst_sell"]),
        "strong_sell_count": _first_int(values, ["analyst_rating_strong_sell", "strong_sell", "strongSell", "recommendation_strong_sell", "analyst_strong_sell"]),
    }


def distribution_total(dist: Dict[str, Optional[int]]) -> Optional[int]:
    vals = list(dist.values())
    if all(v is None for v in vals):
        return None
    total = sum(int(v or 0) for v in vals)
    return total if total > 0 else None


def candidate_from_values(symbol: str, values: Dict[str, Any], source: str, exchange: Optional[str] = None) -> Optional[FetchedTV]:
    rating_keys = ["analyst_rating", "Analyst Rating", "recommendation_mark", "rating", "recommendation"]
    count_keys = ["number_of_analysts", "analysts_count", "analyst_count", "analyst_count_current"]
    target_keys = ["target_price_average", "price_target_average", "average_target_price", "avg_target_price", "target_price_avg"]
    rating = None
    for k in rating_keys:
        rating = normalize_rating(values.get(k))
        if rating:
            break
    dist = distribution_from_values(values)
    dist_total = distribution_total(dist)
    analyst_count = dist_total
    if analyst_count is None:
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
        return FetchedTV(
            symbol=symbol,
            market="US",
            coverage_status="covered",
            rating=rating,
            analyst_count=analyst_count,
            avg_target_price=avg_target,
            source=source,
            exchange=exchange,
            raw=values,
            **dist,
        )
    return None

'''
    if "def distribution_from_values" not in text:
        text = regex_replace_once(
            text,
            r"def candidate_from_values\(symbol: str, values: Dict\[str, Any\], source: str, exchange: Optional\[str\] = None\) -> Optional\[FetchedTV\]:.*?def load_fixture",
            candidate_block + "def load_fixture",
            "candidate_from_values distribution",
        )

    # Fixture support for distribution fields.
    if 'strong_buy_count=safe_int(row.get("strong_buy_count"))' not in text:
        text = replace_once(
            text,
            'out[f"US:{symbol}"] = FetchedTV(symbol, "US", "covered", rating, analyst_count, avg_target, "fixture", row.get("exchange"), row)',
            'out[f"US:{symbol}"] = FetchedTV(symbol, "US", "covered", rating, analyst_count, avg_target, "fixture", row.get("exchange"), row, strong_buy_count=safe_int(row.get("strong_buy_count")), buy_count=safe_int(row.get("buy_count")), hold_count=safe_int(row.get("hold_count")), sell_count=safe_int(row.get("sell_count")), strong_sell_count=safe_int(row.get("strong_sell_count")))',
            "fixture distribution fields",
        )

    # Forecast page fallback: keep TradingView-only, but attempt the same keys.
    if '"analyst_rating_strong_buy": _regex_json_value' not in text:
        text = replace_once(
            text,
            '"target_price_average": _regex_json_value(text, ["target_price_average", "price_target_average", "average_target_price", "avg_target_price"]), } cand = candidate_from_values',
            '"target_price_average": _regex_json_value(text, ["target_price_average", "price_target_average", "average_target_price", "avg_target_price"]), "analyst_rating_strong_buy": _regex_json_value(text, ["analyst_rating_strong_buy", "strong_buy", "strongBuy"]), "analyst_rating_buy": _regex_json_value(text, ["analyst_rating_buy", "buy"]), "analyst_rating_hold": _regex_json_value(text, ["analyst_rating_hold", "analyst_rating_neutral", "hold", "neutral"]), "analyst_rating_sell": _regex_json_value(text, ["analyst_rating_sell", "sell"]), "analyst_rating_strong_sell": _regex_json_value(text, ["analyst_rating_strong_sell", "strong_sell", "strongSell"]), } cand = candidate_from_values',
            "forecast page distribution fields",
        )

    tv_snapshot_to_dict = r'''def tv_snapshot_to_dict(s: TVSnapshot) -> Dict[str, Any]:
    return {
        "symbol": s.symbol,
        "market": s.market,
        "coverage_status": s.coverage_status,
        "rating": s.rating,
        "analyst_count": s.analyst_count,
        "avg_target_price": s.avg_target_price,
        "strong_buy_count": getattr(s, "strong_buy_count", None),
        "buy_count": getattr(s, "buy_count", None),
        "hold_count": getattr(s, "hold_count", None),
        "sell_count": getattr(s, "sell_count", None),
        "strong_sell_count": getattr(s, "strong_sell_count", None),
        "updated_at": s.updated_at,
        "source": s.source,
        "reason": s.reason,
    }

'''
    if '"strong_buy_count": getattr(s, "strong_buy_count", None)' not in text:
        text = regex_replace_once(
            text,
            r"def tv_snapshot_to_dict\(s: TVSnapshot\) -> Dict\[str, Any\]:.*?def diff_fields",
            tv_snapshot_to_dict + "def diff_fields",
            "tv_snapshot_to_dict distribution",
        )

    text = replace_once(
        text,
        '("avg_target_price", old.avg_target_price, new.avg_target_price), ]',
        '("avg_target_price", old.avg_target_price, new.avg_target_price), ("strong_buy_count", getattr(old, "strong_buy_count", None), new.strong_buy_count), ("buy_count", getattr(old, "buy_count", None), new.buy_count), ("hold_count", getattr(old, "hold_count", None), new.hold_count), ("sell_count", getattr(old, "sell_count", None), new.sell_count), ("strong_sell_count", getattr(old, "strong_sell_count", None), new.strong_sell_count), ]',
        "diff_fields distribution checks",
    )

    # Candidate report display.
    if "分布：{new.get('strong_buy_count'" not in text:
        text = replace_once(
            text,
            'lines.append(f"- 新：{new.get(\'coverage_status\')} / {new.get(\'rating\')} / {new.get(\'analyst_count\')}人 / {new.get(\'avg_target_price\')}") lines.append(f"- 取引所候補：{c.get(\'exchange\') or \'未取得\'}")',
            'lines.append(f"- 新：{new.get(\'coverage_status\')} / {new.get(\'rating\')} / {new.get(\'analyst_count\')}人 / {new.get(\'avg_target_price\')}") lines.append(f"- 分布：{new.get(\'strong_buy_count\') if new.get(\'strong_buy_count\') is not None else \'未取得\'} / {new.get(\'buy_count\') if new.get(\'buy_count\') is not None else \'未取得\'} / {new.get(\'hold_count\') if new.get(\'hold_count\') is not None else \'未取得\'} / {new.get(\'sell_count\') if new.get(\'sell_count\') is not None else \'未取得\'} / {new.get(\'strong_sell_count\') if new.get(\'strong_sell_count\') is not None else \'未取得\'}") lines.append(f"- 取引所候補：{c.get(\'exchange\') or \'未取得\'}")',
            "candidate report distribution display",
        )

    if "分布:" not in text.split("## 値は同じ・確認済み", 1)[-1]:
        text = replace_once(
            text,
            'lines.append(f"- {c[\'key\']}：{new.get(\'rating\')} / {new.get(\'analyst_count\')}人 / {new.get(\'avg_target_price\')}")',
            'lines.append(f"- {c[\'key\']}：{new.get(\'rating\')} / {new.get(\'analyst_count\')}人 / {new.get(\'avg_target_price\')} / 分布:{new.get(\'strong_buy_count\') if new.get(\'strong_buy_count\') is not None else \'未取得\'}/{new.get(\'buy_count\') if new.get(\'buy_count\') is not None else \'未取得\'}/{new.get(\'hold_count\') if new.get(\'hold_count\') is not None else \'未取得\'}/{new.get(\'sell_count\') if new.get(\'sell_count\') is not None else \'未取得\'}/{new.get(\'strong_sell_count\') if new.get(\'strong_sell_count\') is not None else \'未取得\'}")',
            "unchanged report distribution display",
        )

    write(path, text)


def patch_us_report(path: Path) -> None:
    text = read(path)
    text = replace_once(
        text,
        'tv_upside, write_error_report, write_report, )',
        'tv_upside, tv_distribution_label, write_error_report, write_report, )',
        f"{path.name} import tv_distribution_label",
    )
    if '"tv_distribution": tv_distribution_label(tv) if tv else "未取得"' not in text:
        text = replace_once(
            text,
            '"tv_analyst_count": tv.analyst_count if tv else None, "tv_avg_target_price": tv.avg_target_price if tv else None,',
            '"tv_analyst_count": tv.analyst_count if tv else None, "tv_distribution": tv_distribution_label(tv) if tv else "未取得", "tv_avg_target_price": tv.avg_target_price if tv else None,',
            f"{path.name} row distribution",
        )
    text = replace_once(
        text,
        'f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}", f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\') if cov == \'covered\' else na}",',
        'f"- アナリスト人数：{ac}人" if ac is not None else f"- アナリスト人数：{na}", f"- アナリスト分布：{r.get(\'tv_distribution\') if cov == \'covered\' else na}", f"- 平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), \'US\') if cov == \'covered\' else na}",',
        f"{path.name} display distribution",
    )
    write(path, text)


def patch_buy_alert() -> None:
    path = SCRIPTS / "cis_buy_alert.py"
    text = read(path)
    text = replace_once(
        text,
        'tv_upside, write_error_report, write_report, )',
        'tv_upside, tv_distribution_label, write_error_report, write_report, )',
        "buy_alert import tv_distribution_label",
    )
    if '"tv_distribution": tv_distribution_label(tv) if tv else "未取得"' not in text:
        text = replace_once(
            text,
            '"tv_analyst_count": tv.analyst_count if tv else None, "tv_avg_target_price": tv.avg_target_price if tv else None,',
            '"tv_analyst_count": tv.analyst_count if tv else None, "tv_distribution": tv_distribution_label(tv) if tv else "未取得", "tv_avg_target_price": tv.avg_target_price if tv else None,',
            "buy_alert row distribution",
        )
    text = replace_once(
        text,
        'f"- TVアナリスト人数：{r.get(\'tv_analyst_count\') if r.get(\'tv_analyst_count\') is not None else \'なし\'}", f"- TV平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), market)}",',
        'f"- TVアナリスト人数：{r.get(\'tv_analyst_count\') if r.get(\'tv_analyst_count\') is not None else \'なし\'}", f"- TVアナリスト分布：{r.get(\'tv_distribution\') if r.get(\'tv_distribution\') else \'未取得\'}", f"- TV平均目標株価：{fmt_price(r.get(\'tv_avg_target_price\'), market)}",',
        "buy_alert display distribution",
    )
    write(path, text)


def main() -> int:
    patch_core()
    patch_master_update()
    patch_tv_monthly_refresh()
    patch_us_report(SCRIPTS / "cis_daily_us.py")
    patch_us_report(SCRIPTS / "cis_weekly_performance.py")
    patch_buy_alert()
    print("TV distribution patch applied. TradingView-only logic; no substitute data providers added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
