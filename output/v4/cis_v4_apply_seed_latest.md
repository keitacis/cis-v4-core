# CIS v4 Apply Seed

生成日時：2026/07/05 21:06 JST

総合判定：ok

## 事前検査

- data/v4_seed/company_master.csv: OK / count=73
- data/v4_seed/watchlist_master.csv: OK / count=73
- data/v4_seed/tv_snapshot.json: OK / count=0
- data/v4_seed/buyzone_master.json: OK / count=0
- data/v4_seed/cis_settings.json: OK / count=12
- data/v4_seed/watchlist_history.json: OK / count=0
- data/v4_seed/master_update_history.json: OK / count=0
- watchlist/company整合性: OK
- staged data/company_master.csv: OK / count=73
- staged data/watchlist_master.csv: OK / count=73
- staged data/tv_snapshot.json: OK / count=0
- staged data/buyzone_master.json: OK / count=0
- staged data/cis_settings.json: OK / count=12
- staged data/watchlist_history.json: OK / count=0
- staged data/master_update_history.json: OK / count=0
- watchlist/company整合性: OK

## 実行内容

- コピー: data/v4_seed/watchlist_master.csv → data/watchlist_master.csv
- コピー: data/v4_seed/company_master.csv → data/company_master.csv
- コピー: data/v4_seed/buyzone_master.json → data/buyzone_master.json
- コピー: data/v4_seed/tv_snapshot.json → data/tv_snapshot.json
- コピー: data/v4_seed/cis_settings.json → data/cis_settings.json
- コピー: data/v4_seed/watchlist_history.json → data/watchlist_history.json
- コピー: data/v4_seed/master_update_history.json → data/master_update_history.json

## 注意

- 既存root dataを不用意に上書きしないための安全Workflowです。
- 既存ファイルがある場合は原則停止します。
- missing_onlyでも、既存rootとseedを合わせたstaged dataがv4厳格検査NGなら何もコピーしません。
- 上書きはバックアップ後のみ、明示確認文字列が必要です。
