# CIS v4 Schedule Reliability Patch R10.4

目的：GitHub Actions の `schedule` が期待時刻に発火しない場合でも、CISの「毎日見る」レポートが古いまま緑表示される問題を防ぐ。

## 追加するもの

- `.github/workflows/cis_v4_schedule_reliability_patch_r10.yml`
  - 手動実行用。`cis_home.py` にR10の鮮度ガードを入れる。
- `.github/workflows/cis_v4_schedule_catchup_r10.yml`
  - 自動更新取りこぼし確認・復旧用。
  - 10:05 / 12:05 JSTは月〜土、19:05 / 20:05 JSTは月〜金に確認。
- `scripts/cis_v4/cis_schedule_catchup_r10.py`
  - `daily_us` / `buy_alert` / `daily_jp` の生成日・価格日付を検査し、古ければ再生成する。GITHUB_TOKENが使える場合は、対象workflowの直近実行履歴も保存する。
- `scripts/cis_v4/patch_schedule_reliability_r10.py`
  - `cis_home.py` に「Homeだけ新しいが本体が古い」状態を検知する処理を追加する。

## 重要な設計

- R10は「GitHubのscheduleが不安定だから諦める」ではなく、取りこぼしをログ化し、自動復旧する。
- Homeは、Home自身の更新日時だけで緑判定しない。
- Daily US / Buy Alert / Daily JP の本体生成日時と価格日付を見て、古ければHomeで要確認に出す。

## 導入後の確認順

1. ZIPをリポジトリ直下へ展開・コピーしてcommit/push。
2. Actionsで `CIS v4 Schedule Reliability Patch R10` を手動実行。
3. 緑成功後、`CIS v4 Schedule Catchup R10` を手動実行。
4. Homeを確認し、古いDaily US / Buy Alertが緑のままにならないことを確認。

## 触らないもの

- R7 / R8 / R9の再実行は不要。
- Daily US / Buy Alert / Daily JP の既存workflowは直接壊さない。


## R10.4での精査反映

- 米国株日次の火〜土運用に合わせ、朝のcatch-upは月〜土へ拡張。
- 日本株の土日誤判定を避けるため、各タスクに判定曜日を設定。
- `actions: read` を付与し、可能な範囲でGitHub Actionsの直近実行履歴をレポートへ保存。
- 復旧成功時はHomeの要確認に残し続けないよう、catch-up自体のstatusは成功なら `ok` にする。


## R10.4での追加精査反映

- `workflow_run` で `CIS v4 Home` 完了後にも catch-up を起動し、Homeだけが走った場合でも後追い復旧できるようにした。
- 当日生成済みの `market_closed` / `price_stale` は正常な休場・価格遅延シグナルとして扱い、同じ日に無限再生成しない。
- Homeの鮮度ガードは `ok` / `partial` のみを上書き対象にし、`休場` や `価格未更新` の既存表示を壊さない。


## R10.4での追加精査反映

- `buy_alert` は米国価格と日本価格を1つのレポートで扱うため、朝に米国側で `price_stale` が出ても、夕方の日本株側catch-upを抑制しないようにした。
- `market_closed` / `price_stale` を終端扱いするのは、そのタスク自身の判定時刻以降に生成されたレポートだけに限定した。
- ZIPはリポジトリ直下へコピーしやすいよう、`.github` / `scripts` / README がルートに出る構成とする。


## R10.4での追加精査反映

- `cis_home.py` のimportやITEMS周辺の整形差分に強くするため、patcherをより堅牢化。
- R10.3の運用ロジックは維持し、投入時のマーカー不一致による赤リスクを下げた。
- iPhone Homeでの見え方はR10.3と同じく、古いDaily/Buy Alert/JPを要確認に出す。
