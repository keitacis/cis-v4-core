# CIS v4 Core omega notes

psiをベースに、iPhone運用とユーザー導線を補強した版。

## 主な補強

- CIS Homeの未生成カードから404になる「開く」リンクを削除。未生成は「まだ実行されていません」と表示。
- CIS Homeの表示時刻を `YYYY/MM/DD HH:mm JST` に統一。
- `master_init_template` のpartial理由をHomeの要確認欄に件数表示。
- Master Update後に `cis_master_init_template.py` を再生成してからHomeを作成。古いpartial警告が残らないようにした。
- Watchlist Update後にも `cis_master_init_template.py` を再生成。銘柄追加・削除後の不足TV/BUYZONEをHomeに反映。
- Apply Seedのpartial時見出しを「エラー」ではなく「保護停止」に変更。
- Master Init TemplateにiPhone用の分割txtを追加。10〜15銘柄単位でコピーしやすくした。
- 各レポートHTMLに「CISホームへ戻る」リンクを追加。

## 継承

psiで修正したMaster Updateの3ファイル同時反映、Apply Seedのstaged検査、履歴JSON厳格化、watchlist/company整合性検査は継承。
