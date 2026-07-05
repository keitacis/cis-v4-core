#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate iPhone-friendly watchlist add/change templates.

This script does not change data.  It creates short txt files and a guide page
so the user can update the watchlist from GitHub Actions without hand-typing
long or fragile commands on an iPhone.
"""
from __future__ import annotations

import sys
from typing import Dict, List

from cis_core import (
    DOCS_LATEST_DIR,
    OUTPUT_DIR,
    load_watchlist,
    now_jst,
    timestamp_jst,
    write_error_report,
    write_report,
    write_text,
)

STEM = "watchlist_template"
TITLE = "CIS 監視リスト追加・変更テンプレート"


def chunked(values: List[str], size: int = 20) -> List[List[str]]:
    return [values[i:i + size] for i in range(0, len(values), size)]


def write_chunk_files(prefix: str, values: List[str], size: int = 20) -> List[str]:
    links: List[str] = []
    for base_dir in [OUTPUT_DIR, DOCS_LATEST_DIR]:
        for old in base_dir.glob(f"{prefix}_part_*.txt"):
            try:
                old.unlink()
            except Exception:
                pass
        for idx, part in enumerate(chunked(values, size), start=1):
            name = f"{prefix}_part_{idx:02d}.txt"
            write_text(base_dir / name, "\n".join(part) + ("\n" if part else ""))
            if base_dir == DOCS_LATEST_DIR:
                links.append(name)
    return links


def write_both_txt(name: str, lines: List[str]) -> None:
    text = "\n".join(lines) + ("\n" if lines else "")
    for base_dir in [OUTPUT_DIR, DOCS_LATEST_DIR]:
        write_text(base_dir / name, text)


def main() -> int:
    try:
        items = load_watchlist(active_only=False)
        active = [x for x in items if x.active]
        inactive = [x for x in items if not x.active]
        active_us = [x for x in active if x.market == "US"]
        active_jp = [x for x in active if x.market == "JP"]
        inactive_us = [x for x in inactive if x.market == "US"]
        inactive_jp = [x for x in inactive if x.market == "JP"]

        add_examples = [
            "# いちばん簡単：名前や説明は後から整える",
            "ADD US CRDO",
            "ADD JP 7203",
            "",
            "# 名前・説明・テーマまで入れる",
            "ADD US CRDO|Credo Technology|高速接続チップ/CPO関連|ai_datacenter",
            "ADD JP 6758|ソニーグループ|ゲーム・半導体・エンタメ|大型成長",
            "",
            "# 既存銘柄の名前・説明・テーマを直す。active状態は変えない",
            "UPDATE US CRDO|Credo Technology|高速接続チップ/CPO関連|ai_datacenter",
            "",
            "# 監視から外す。完全削除ではなくinactive化",
            "STOP US CRDO|監視優先度を下げる",
            "",
            "# inactive銘柄を再開",
            "RESUME US CRDO|監視再開",
        ]
        quick_add_blank = [
            "ADD US ティッカー",
            "ADD US ティッカー|会社名|説明|テーマ",
            "ADD JP 4桁コード",
            "ADD JP 4桁コード|会社名|説明|テーマ",
        ]
        active_list = [f"{x.market}:{x.symbol}\t{x.name}\tactive\t{x.category}" for x in active]
        inactive_list = [f"{x.market}:{x.symbol}\t{x.name}\tinactive\t{x.category}" for x in inactive]
        stop_us = [f"STOP US {x.symbol}|監視停止" for x in active_us]
        stop_jp = [f"STOP JP {x.symbol}|監視停止" for x in active_jp]
        resume_us = [f"RESUME US {x.symbol}|監視再開" for x in inactive_us]
        resume_jp = [f"RESUME JP {x.symbol}|監視再開" for x in inactive_jp]
        update_us = [f"UPDATE US {x.symbol}|{x.name}|{x.description or x.notes}|{x.category}" for x in active_us]
        update_jp = [f"UPDATE JP {x.symbol}|{x.name}|{x.description or x.notes}|{x.category}" for x in active_jp]

        write_both_txt("watchlist_add_examples.txt", add_examples)
        write_both_txt("watchlist_quick_add_blank.txt", quick_add_blank)
        write_both_txt("watchlist_active_list.txt", active_list)
        write_both_txt("watchlist_inactive_list.txt", inactive_list)
        stop_us_links = write_chunk_files("watchlist_stop_us", stop_us, 20)
        stop_jp_links = write_chunk_files("watchlist_stop_jp", stop_jp, 20)
        resume_us_links = write_chunk_files("watchlist_resume_us", resume_us, 20)
        resume_jp_links = write_chunk_files("watchlist_resume_jp", resume_jp, 20)
        update_us_links = write_chunk_files("watchlist_update_us", update_us, 15)
        update_jp_links = write_chunk_files("watchlist_update_jp", update_jp, 15)

        status = {
            "status": "ok",
            "generated_at_jst": timestamp_jst(),
            "total_count": len(items),
            "active_count": len(active),
            "inactive_count": len(inactive),
            "active_us_count": len(active_us),
            "active_jp_count": len(active_jp),
        }

        lines: List[str] = [
            f"# {TITLE}",
            "",
            f"生成日時：{now_jst().strftime('%Y/%m/%d %H:%M JST')}",
            "",
            "## 目的",
            "",
            "監視リストの追加・停止・再開・説明修正を、iPhoneからでもミスなく行うためのページです。",
            "このページはテンプレート作成だけで、監視リスト自体は変更しません。変更は `CIS v4 Watchlist Update` にコマンドを貼って実行します。",
            "",
            "## 最短手順",
            "",
            "1. このページのtxtを開いて、必要なコマンドをコピーします。",
            "2. GitHub Actions > `CIS v4 Watchlist Update` を開きます。",
            "3. `commands` に貼って実行します。",
            "4. Homeの `監視リスト更新` と `初期マスター投入テンプレート` を確認します。",
            "5. 新規追加銘柄は、必要に応じて `CIS v4 Master Update` でBUYZONE/TVも投入します。",
            "",
            "## 基本コマンド",
            "",
            "- `ADD US CRDO`：最低限の追加。名前はティッカーで仮登録。あとからUPDATE可能。",
            "- `ADD US CRDO|Credo Technology|高速接続チップ|ai_datacenter`：説明つきで追加。",
            "- `ADD JP 6758|ソニーグループ|ゲーム・半導体・エンタメ|大型成長`：日本株追加。",
            "- `UPDATE US CRDO|Credo Technology|高速接続チップ|ai_datacenter`：既存銘柄の説明修正。active状態は変えません。",
            "- `STOP US CRDO|理由`：監視停止。完全削除ではなくinactive化。",
            "- `RESUME US CRDO|理由`：監視再開。",
            "",
            "## サマリー",
            "",
            f"- 全登録：{len(items)}件",
            f"- active：{len(active)}件（US {len(active_us)}件 / JP {len(active_jp)}件）",
            f"- inactive：{len(inactive)}件（US {len(inactive_us)}件 / JP {len(inactive_jp)}件）",
            "",
            "## iPhone用txt",
            "",
            "- [追加・変更の例](watchlist_add_examples.txt)",
            "- [空の追加テンプレート](watchlist_quick_add_blank.txt)",
            "- [active銘柄一覧](watchlist_active_list.txt)",
            "- [inactive銘柄一覧](watchlist_inactive_list.txt)",
            "",
        ]
        if stop_us_links:
            lines += ["### US停止テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(stop_us_links)] + [""]
        if stop_jp_links:
            lines += ["### JP停止テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(stop_jp_links)] + [""]
        if resume_us_links:
            lines += ["### US再開テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(resume_us_links)] + [""]
        if resume_jp_links:
            lines += ["### JP再開テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(resume_jp_links)] + [""]
        if update_us_links:
            lines += ["### US説明修正テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(update_us_links)] + [""]
        if update_jp_links:
            lines += ["### JP説明修正テンプレート", ""] + [f"- [part {i+1:02d}]({name})" for i, name in enumerate(update_jp_links)] + [""]

        lines += [
            "## 注意",
            "",
            "- 新規追加後、BUYZONEやTradingViewが未設定の銘柄は `初期マスター投入テンプレート` に出ます。",
            "- STOPはデータを消さず、active=falseにします。再開はRESUMEで戻せます。",
            "- 1回の入力内で同じ銘柄を複数回指定すると安全停止します。",
            "- 区切りは半角 `|` でも全角 `｜` でも使えます。",
            "",
        ]

        payload = {"status": status, "active": active_list, "inactive": inactive_list}
        write_report(STEM, "\n".join(lines), payload, status)
        return 0
    except Exception as e:
        write_error_report(STEM, TITLE, f"{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
