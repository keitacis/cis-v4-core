# CIS v4 Core 初回投入・移行計画

このパッケージは、既存CISをいきなり上書きしないための安全投入版です。

## 重要方針

- v4 Workflowはすべて `.github/workflows/cis_v4_*.yml` にします。
- 旧Workflowは最初に削除しません。
- v4レポートは初期確認中 `docs/v4/` と `output/v4/` に出します。
- 既存の `docs/latest/` や `docs/index.html` は初回投入では触りません。
- seedデータは `data/v4_seed/` に置き、`data/watchlist_master.csv` などのroot masterを直接上書きしません。
- 初回確認中のiPhoneホームは `docs/v4/index.html` です。

## 初回投入後の確認順

1. `CIS v4 Preflight` を手動実行する。
2. `docs/v4/latest/cis_v4_preflight_latest.html` を確認する。
3. Preflightでroot dataが未作成なら、`CIS v4 Apply Seed` を `missing_only` で実行する。
4. Preflightでroot dataが一部不足なら、`CIS v4 Apply Seed` を `missing_only` で実行して不足ファイルだけ作成し、既存ファイルは上書きしない。
5. Preflightでroot dataがv4非互換なら、Apply Seedで上書きせず、該当ファイルを修正またはバックアップ方針を決める。
6. `CIS v4 Master Init Template` を手動実行し、BUYZONE/TVの不足を確認する。
7. `CIS v4 Master Update` でTradingViewと買い場基準を初期投入する。
8. `CIS v4 Daily US`、`CIS v4 Daily JP`、`CIS v4 Weekly Performance`、`CIS v4 Buy Alert` を手動実行する。
9. `docs/v4/index.html` をiPhoneで確認する。
10. 問題なければ旧Workflowのscheduleを止める。
11. 最後にv4 Workflowのscheduleを有効化する。

## Preflightの判定別アクション

### ✅ OK

root dataはv4厳格検査OKです。`CIS v4 Master Init Template` に進みます。

### ⚠️ 要確認：root data未作成

`CIS v4 Apply Seed` を `missing_only` で実行します。seedからroot dataを作成したあと、Preflightを再実行します。

### ⚠️ 要確認：root data一部不足

`CIS v4 Apply Seed` の `missing_only` で不足ファイルだけ作成します。既存ファイルは上書きされません。完了後にPreflightを再実行します。

### ❌ エラー：root data非互換

Apply Seedでいきなり上書きしません。Preflightのエラー対象ファイルを見て、既存データを修正するか、バックアップ後にseedへ置換するかを決めます。

## Apply Seedの挙動

`missing_only` は既存root dataを上書きしません。不足ファイルだけコピーします。

既存ファイルがある場合、Workflowは赤く終わる場合があります。これは処理失敗ではなく、**既存ファイルを保護したための停止表示**です。レポート内の「実行内容」を確認してください。

`overwrite_after_backup` は、明示確認文字列を入力した場合だけ使います。既存ファイルをバックアップしてからseedで置き換えます。

## 注意

`data/v4_seed/` は初期seedの保管場所です。ここを編集してもv4本番レポートには反映されません。本番データは `data/watchlist_master.csv`、`data/company_master.csv`、`data/buyzone_master.json`、`data/tv_snapshot.json` です。

## 自動scheduleについて

初回投入版では、主要Workflowは `workflow_dispatch` のみです。自動実行は、v4手動確認が終わってから有効化します。
