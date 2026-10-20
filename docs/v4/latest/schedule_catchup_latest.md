# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/20 17:25 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-20T17:25:00.876673+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-20T11:05:18.650640+09:00
- expected_price_dates：{'US': '2026-10-19'}
- row_dates：['2026-10-19']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T02:04:58Z / updated=2026-10-20T02:05:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:05:45Z / updated=2026-10-20T01:06:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-17T01:32:45Z / updated=2026-10-17T01:33:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-17T00:31:03Z / updated=2026-10-17T00:31:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T01:39:14Z / updated=2026-10-16T01:39:42Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-20T14:00:31.892660+09:00
- expected_price_dates：{'US': '2026-10-19'}
- row_dates：['2026-10-19']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T05:00:00Z / updated=2026-10-20T05:00:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:53:14Z / updated=2026-10-20T01:53:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T01:20:33Z / updated=2026-10-19T01:21:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T04:41:54Z / updated=2026-10-16T04:42:30Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-20T01:37:06.230799+09:00
- expected_price_dates：{'JP': '2026-10-20'}
- row_dates：['2026-10-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T16:36:42Z / updated=2026-10-19T16:42:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T15:50:03Z / updated=2026-10-19T16:15:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T14:11:45Z / updated=2026-10-16T14:12:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T13:29:28Z / updated=2026-10-16T13:29:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T14:22:26Z / updated=2026-10-15T14:22:57Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-20T14:00:31.892660+09:00
- expected_price_dates：{'JP': '2026-10-20'}
- row_dates：['2026-10-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T05:00:00Z / updated=2026-10-20T05:00:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:53:14Z / updated=2026-10-20T01:53:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T01:20:33Z / updated=2026-10-19T01:21:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T04:41:54Z / updated=2026-10-16T04:42:30Z
