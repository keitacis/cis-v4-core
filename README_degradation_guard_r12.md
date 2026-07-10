# CIS v4 R12.2 劣化上書き防止パッチ

R12.2 は、R12.1 の GitHub Actions 実行時エラーを修正した版です。

## R12.1 の失敗原因

R12.1 のパッチスクリプトは `re.subn(pattern, R12_CORE_CODE, ...)` で `cis_core.py` の `write_report()` を差し替える構造でした。
差し替え後のコード文字列内に `\d{4}-\d{2}-\d{2}` が含まれていたため、Python の正規表現置換処理が replacement 側の `\d` を不正なエスケープとして解釈し、`re.error: bad escape \d` で停止しました。

R12.2 では `re.subn(pattern, lambda _m: R12_CORE_CODE, ...)` に変更し、replacement 側のバックスラッシュを正規表現エスケープとして解釈させないようにしています。

## 目的

- 夜中・早朝の価格ソース遅延で、正常だった `daily_jp_latest` などが価格未更新レポートに劣化上書きされるのを防ぐ。
- 既存の正常レポート本文と JSON は保持する。
- ただし、ステータスは `partial` にして Home の要確認に表示する。
- 上書きしなかった悪い結果は `<stem>_degraded_attempt_latest.*` に退避する。

## 対象

- `daily_jp`
- `daily_us`
- `buy_alert`

## 期待されるiPhone表示

日本株で夜中に古い価格データが返った場合、`価格未更新 日本株騰落` に本文まで上書きされず、日本株カードは `一部注意` として「劣化上書き防止」が表示されます。夕方に正常価格が取得できれば通常の `更新済み` に戻ります。

## 適用後の確認

1. `CIS v4 Degradation Guard Patch R12.2` を手動実行。
2. 緑成功を確認。
3. 必要なら `CIS v4 Home` を1回実行。
4. 翌朝、夜中の価格未更新で daily_jp latest 本文が劣化上書きされていないか確認。

## 注意

R12.1 の失敗は、パッチスクリプトが `cis_core.py` を書き換える前に停止したものです。したがって、CIS本体の `cis_core.py` / `cis_home.py` はR12.1で壊れていない想定です。
R12.1 workflow は再実行しないでください。R12.2 workflow を使ってください。
