# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/16 09:13 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-16T09:13:47.874092+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-16T07:25:38.895189+09:00
- expected_price_dates：{'US': '2026-07-15'}
- row_dates：['2026-07-15']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T07:26:46Z / updated=2026-07-15T07:27:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T06:33:29Z / updated=2026-07-15T06:33:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:22:12Z / updated=2026-07-14T07:22:49Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T06:30:10Z / updated=2026-07-14T06:30:42Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-11T07:21:03Z / updated=2026-07-11T07:21:35Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-16T08:25:50.971907+09:00
- expected_price_dates：{'US': '2026-07-15'}
- row_dates：['2026-07-15']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T07:31:23Z / updated=2026-07-15T07:32:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T07:24:42Z / updated=2026-07-15T07:25:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:26:43Z / updated=2026-07-14T07:27:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:20:41Z / updated=2026-07-14T07:21:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T11:44:50Z / updated=2026-07-13T11:45:21Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-07-16T00:11:35.167227+09:00
- expected_price_dates：{'JP': '2026-07-15'}
- row_dates：['2026-07-15']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T15:11:03Z / updated=2026-07-15T15:11:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T12:58:57Z / updated=2026-07-15T12:59:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T15:10:16Z / updated=2026-07-14T15:10:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T12:51:37Z / updated=2026-07-14T12:52:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T17:25:35Z / updated=2026-07-13T17:26:04Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-16T08:25:50.971907+09:00
- expected_price_dates：{'JP': '2026-07-15'}
- row_dates：['2026-07-15']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T07:31:23Z / updated=2026-07-15T07:32:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T07:24:42Z / updated=2026-07-15T07:25:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:26:43Z / updated=2026-07-14T07:27:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:20:41Z / updated=2026-07-14T07:21:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T11:44:50Z / updated=2026-07-13T11:45:21Z
