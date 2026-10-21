# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/21 17:28 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-21T17:28:13.523346+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-21T11:02:45.969280+09:00
- expected_price_dates：{'US': '2026-10-20'}
- row_dates：['2026-10-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T02:02:18Z / updated=2026-10-21T02:02:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T00:38:59Z / updated=2026-10-21T00:39:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T02:04:58Z / updated=2026-10-20T02:05:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:05:45Z / updated=2026-10-20T01:06:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-17T01:32:45Z / updated=2026-10-17T01:33:17Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-21T14:00:05.950896+09:00
- expected_price_dates：{'US': '2026-10-20'}
- row_dates：['2026-10-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T04:59:29Z / updated=2026-10-21T05:00:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T01:40:09Z / updated=2026-10-21T01:40:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T05:00:00Z / updated=2026-10-20T05:00:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:53:14Z / updated=2026-10-20T01:53:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-10-20T23:27:48.608106+09:00
- expected_price_dates：{'JP': '2026-10-21'}
- row_dates：['2026-10-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T14:27:24Z / updated=2026-10-20T14:27:54Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T13:48:51Z / updated=2026-10-20T13:49:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T16:36:42Z / updated=2026-10-19T16:42:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T15:50:03Z / updated=2026-10-19T16:15:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-16T14:11:45Z / updated=2026-10-16T14:12:15Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-21T14:00:05.950896+09:00
- expected_price_dates：{'JP': '2026-10-21'}
- row_dates：['2026-10-21']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T04:59:29Z / updated=2026-10-21T05:00:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T01:40:09Z / updated=2026-10-21T01:40:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T05:00:00Z / updated=2026-10-20T05:00:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T01:53:14Z / updated=2026-10-20T01:53:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-19T04:52:40Z / updated=2026-10-19T04:53:21Z
