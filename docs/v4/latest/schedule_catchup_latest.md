# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/20 09:10 JST

## 判定サマリー

- ⚠️ 米国株日次騰落：再生成対象 / 生成日が当日ではない：2026-10-17 / US価格日付が想定2026-10-19より古い：['2026-10-16']
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- 米国株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_daily_us.py`
  - after：status=partial / generated=2026-10-20T09:10:36.807240+09:00 / dates=['2026-10-16']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-20T09:10:39.022745+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-17T14:30:38.180986+09:00
- expected_price_dates：{'US': '2026-10-19'}
- row_dates：['2026-10-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-17T01:32:45Z / updated=2026-10-17T01:33:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-17T00:31:03Z / updated=2026-10-17T00:31:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T01:39:14Z / updated=2026-10-16T01:39:42Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T00:25:48Z / updated=2026-10-16T00:26:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T01:50:38Z / updated=2026-10-15T01:51:14Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-19T13:53:16.122837+09:00
- expected_price_dates：{'US': '2026-10-19'}
- row_dates：['2026-10-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T01:20:33Z / updated=2026-10-19T01:21:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T04:41:54Z / updated=2026-10-16T04:42:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T01:27:08Z / updated=2026-10-16T01:27:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T04:51:11Z / updated=2026-10-15T04:51:51Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-20T01:37:06.230799+09:00
- expected_price_dates：{'JP': '2026-10-19'}
- row_dates：['2026-10-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T16:36:42Z / updated=2026-10-19T16:42:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T15:50:03Z / updated=2026-10-19T16:15:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T14:11:45Z / updated=2026-10-16T14:12:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T13:29:28Z / updated=2026-10-16T13:29:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T14:22:26Z / updated=2026-10-15T14:22:57Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-19T13:53:16.122837+09:00
- expected_price_dates：{'JP': '2026-10-19'}
- row_dates：['2026-10-19']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T01:20:33Z / updated=2026-10-19T01:21:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T04:41:54Z / updated=2026-10-16T04:42:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T01:27:08Z / updated=2026-10-16T01:27:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T04:51:11Z / updated=2026-10-15T04:51:51Z
