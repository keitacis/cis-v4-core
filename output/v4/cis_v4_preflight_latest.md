# CIS v4 Preflight

生成日時：2026/07/05 21:08 JST

総合判定：✅ 構成OK（まだ運用開始前。次は初期マスター投入/手動確認）

このPreflightは破壊的変更を行いません。既存CISを上書きせず、v4投入前の衝突・不足・root dataマスターのv4互換性を確認します。

## 重要

- このOKは『ファイル構成とroot dataの形式がv4で読める』という意味です。
- まだCIS運用開始ではありません。BUYZONEとTradingViewの初期投入、各レポートの手動確認が必要です。

## 次にやること

- root dataマスターはv4厳格検査OKです。次に `CIS v4 Master Init Template` を手動実行してください。
- BUYZONE/TradingViewの不足を確認し、`CIS v4 Master Update` で初期投入してください。
- その後、日次US/日次JP/週間/買い場を手動実行し、`docs/v4/index.html` を確認します。

## スクリプト

- ✅ scripts/cis_v4/cis_core.py
- ✅ scripts/cis_v4/cis_daily_us.py
- ✅ scripts/cis_v4/cis_daily_jp.py
- ✅ scripts/cis_v4/cis_buy_alert.py
- ✅ scripts/cis_v4/cis_weekly_performance.py
- ✅ scripts/cis_v4/cis_home.py
- ✅ scripts/cis_v4/cis_watchlist_update.py
- ✅ scripts/cis_v4/cis_master_update.py
- ✅ scripts/cis_v4/cis_monthly_maintenance.py
- ✅ scripts/cis_v4/cis_master_init_template.py
- ✅ scripts/cis_v4/cis_v4_preflight.py
- ✅ scripts/cis_v4/cis_v4_apply_seed.py

## Workflow

- ✅ .github/workflows/cis_v4_preflight.yml
- ✅ .github/workflows/cis_v4_apply_seed.yml
- ✅ .github/workflows/cis_v4_daily_us.yml
- ✅ .github/workflows/cis_v4_daily_jp.yml
- ✅ .github/workflows/cis_v4_buy_alert.yml
- ✅ .github/workflows/cis_v4_weekly_performance.yml
- ✅ .github/workflows/cis_v4_home.yml
- ✅ .github/workflows/cis_v4_watchlist_update.yml
- ✅ .github/workflows/cis_v4_master_update.yml
- ✅ .github/workflows/cis_v4_monthly_maintenance.yml
- ✅ .github/workflows/cis_v4_master_init_template.yml
- ✅ 既知の旧Workflow同名衝突なし

## seed退避データ

- ✅ data/v4_seed/company_master.csv: v4厳格検査OK / count=73
- ✅ data/v4_seed/watchlist_master.csv: v4厳格検査OK / count=73
- ✅ data/v4_seed/tv_snapshot.json: v4厳格検査OK / count=0
- ✅ data/v4_seed/buyzone_master.json: v4厳格検査OK / count=0
- ✅ data/v4_seed/cis_settings.json: v4厳格検査OK / count=12
- ✅ data/v4_seed/watchlist_history.json: 厳格JSON確認OK / count=0
- ✅ data/v4_seed/master_update_history.json: 厳格JSON確認OK / count=0
- ✅ data/v4_seed watchlist/company整合性: OK

## root dataマスター v4厳格検査

- ✅ data/company_master.csv: v4厳格検査OK / count=73
- ✅ data/watchlist_master.csv: v4厳格検査OK / count=73
- ✅ data/tv_snapshot.json: v4厳格検査OK / count=0
- ✅ data/buyzone_master.json: v4厳格検査OK / count=0
- ✅ data/cis_settings.json: v4厳格検査OK / count=12
- ✅ data/watchlist_history.json: 厳格JSON確認OK / count=0
- ✅ data/master_update_history.json: 厳格JSON確認OK / count=0
- ✅ root watchlist/company整合性: OK

## 安全メモ

- v4 Workflowは `cis_v4_` 接頭辞付きで、旧Workflowと並走できる前提です。
- 初回確認が終わるまで、v4の自動scheduleは有効化しません。
- PreflightでNGが出たroot dataを、seedで無条件上書きしないでください。
