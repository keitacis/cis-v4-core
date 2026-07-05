# CIS v4 Core psi notes

chi精査で見つかった `cis_master_update.py` の根幹不具合を修正した候補版。

## 修正内容

- `hist_items` 未定義による Master Update 失敗を修正。
- `master_update_history.json` を厳格に読み込み、`items` の各要素が object であることを確認。
- TV / BUYZONE / master_update_history の3ファイルを、メモリ上で全更新内容を確定してから一時ファイルへ書き出し、再読込検査後に反映する方式へ変更。
- `os.replace()` 途中失敗時は、既に置換済みのmasterをバックアップから復元するベストエフォート・ロールバックを追加。
- エラー終了なのに `tv_snapshot.json` と `buyzone_master.json` だけ反映され履歴が残らない、というchiのトランザクション破綻を解消。

## ローカル確認済み

- 正常seed → Apply Seed ok → Master Update ok。
- TV / BUYZONE正常更新で、`tv_snapshot.json`、`buyzone_master.json`、`master_update_history.json` が揃って反映されることを確認。
- 1件でも不正な更新命令がある場合、3 masterは変更されないことを確認。
- 既存 `tv_snapshot.json` が壊れている場合、3 masterは変更されないことを確認。
- 既存 `master_update_history.json` の `items` にobject以外がある場合、3 masterは変更されないことを確認。
- `os.replace()` 途中失敗を擬似発生させ、置換済みmasterがバックアップから復元されることを確認。
- 全Python構文チェックOK。
- 全GitHub Actions YAML構文チェックOK。

## 未検証

- GitHub Actions本番環境でのcommit/push。
- yfinanceなど外部ネットワーク取得。
