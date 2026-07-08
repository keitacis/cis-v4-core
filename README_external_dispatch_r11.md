# CIS v4 External Dispatch R11.2

## 目的

GitHub Actions の `schedule` が予定どおり発火しない場合に備え、外部スケジューラから `workflow_dispatch` API で CIS を起動する入口を追加する。

R11.2はGitHub cronを増やすパッチではない。外部から手動実行相当の `workflow_dispatch` を投げるためのラッパーである。

## R11.1からの変更

- 現行 `cis_core.write_report()` との引数互換を修正。
- `latest_date` が空の行を誤って最新扱いしないよう鮮度判定を強化。
- GitHub Actionsランナー開始が遅れてもno-opになりにくいよう、auto判定時間帯を広げた。
- no-op autoではdocs/Homeを更新しない。不要なcommitを増やさない。

## 追加ファイル

- `.github/workflows/cis_v4_external_dispatch_r11.yml`
- `scripts/cis_v4/cis_external_dispatch_r11.py`
- `README_external_dispatch_r11.md`

## workflow_dispatch input

`mode`:

- `auto`：JST時刻とレポート鮮度を見て必要分だけ実行。外部スケジューラ本番用の推奨。
- `us_morning`：米国株日次 → 買い場アラート → Home
- `us_retry`：米国株日次 → Home
- `buy_alert_morning`：買い場アラート → Home
- `jp_evening`：日本株日次 → 買い場アラート → Home
- `jp_retry`：日本株日次 → Home
- `catchup`：R10 catchup → Home

`source`:

- `manual`
- `cron-job.org`
- 任意の外部起動元ラベル

## 外部API呼び出し先

POST

`https://api.github.com/repos/keitacis/cis-v4-core/actions/workflows/cis_v4_external_dispatch_r11.yml/dispatches`

Headers:

- `Accept: application/vnd.github+json`
- `Authorization: Bearer <GitHub Fine-grained PAT>`
- `X-GitHub-Api-Version: 2026-03-10`
- `Content-Type: application/json`

Body例:

```json
{"ref":"main","inputs":{"mode":"auto","source":"cron-job.org-auto"}}
```

## 推奨外部スケジュール JST：手間を減らす構成

まずは外部ジョブ2本だけで始める。

### 1. Morning Auto

- 月〜土
- 07:25 / 08:25 / 09:25 / 10:25 JST
- Body: `{"ref":"main","inputs":{"mode":"auto","source":"cron-job.org-morning"}}`

R11.2 autoが内部で判定すること：

- 火〜土 07〜13時：米国株日次が古ければ再生成
- 月〜金 08〜13時：買い場アラートの米国価格が古ければ再生成

### 2. Evening Auto

- 月〜金
- 18:25 / 19:25 / 20:25 JST
- Body: `{"ref":"main","inputs":{"mode":"auto","source":"cron-job.org-evening"}}`

R11.2 autoが内部で判定すること：

- 月〜金 18〜22時：日本株日次が古ければ再生成
- 月〜金 18〜22時：買い場アラートの日本価格が古ければ再生成

## より細かく分ける場合

外部ジョブを増やしてよいなら、以下の明示modeも使える。

- 火〜土 07:20：`us_morning`
- 火〜土 08:55：`us_retry`
- 月〜金 09:25：`buy_alert_morning`
- 月〜金 17:50：`jp_evening`
- 月〜金 18:55：`jp_retry`
- 月〜金 19:15：`catchup`

ただし、ユーザー操作を減らす目的では、まずは `auto` 2本構成を推奨する。

## 注意

- GitHub tokenはチャットやスクショに絶対に貼らない。
- Fine-grained PATは対象リポジトリを `keitacis/cis-v4-core` のみに限定する。
- 権限は `Actions: Read and write` を最小限として使う。
- 期限は短め、まずは90日程度を推奨する。
- cron-job.org側の成功は「GitHubがworkflow_dispatchを受け付けた」ことを意味する。CIS更新完了はCISホームまたはGitHub Actionsで確認する。
