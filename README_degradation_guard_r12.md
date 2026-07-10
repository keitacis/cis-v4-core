# CIS v4 Degradation Guard R12.3

R12.3 は、Daily JP / Daily US / Buy Alert の `latest` を、後続の劣化実行で壊さないための保護パッチです。

## 背景

R11 により外部スケジューラからの起動は改善されましたが、夜間・早朝など価格ソースが古いデータしか返さない時間帯に Daily JP が再生成され、正常だった `daily_jp_latest` が `price_stale` レポートで上書きされる問題が残りました。

## 方針

`write_report()` は CIS v4 のレポート出力の共通出口です。ここで次の条件を満たす場合、本文・JSONの劣化上書きを止めます。

- 対象 stem が `daily_jp` / `daily_us` / `buy_alert`
- 新しい実行結果が `price_stale`
- 既存 latest status が `ok` または `partial`

この場合、正常な latest 本文・JSONは保持し、悪い取得結果は `*_degraded_attempt_latest.*` に退避します。元の status だけは `partial` として更新し、Home の要確認で保護作動を見えるようにします。

## R12.1 / R12.2 からの修正

- R12.1: `re.subn()` の置換文字列内 `\d` が `bad escape` で失敗。
- R12.2: 正規表現置換は直したが、現行 `cis_core.py` が圧縮気味の1行実装だったため、想定パターンで `write_report()` を見つけられず失敗。
- R12.3: 正規表現ではなく、`def write_report(` から `def write_error_report(` までの範囲を文字列境界で置換する方式に変更。

## 注意

このパッチは、すでに劣化上書き済みのレポートを即座に復元するものではありません。夕方などに正常レポートが作られた後、次回以降の劣化上書きを防ぎます。
