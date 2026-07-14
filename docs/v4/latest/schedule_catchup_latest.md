# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/14 16:30 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-14T16:30:02.009033+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-14T16:22:43.825702+09:00
- expected_price_dates：{'US': '2026-07-13'}
- row_dates：['2026-07-13']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:22:12Z / updated=2026-07-14T07:22:49Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T06:30:10Z / updated=2026-07-14T06:30:42Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-11T07:21:03Z / updated=2026-07-11T07:21:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-11T06:30:09Z / updated=2026-07-11T06:32:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:39:28Z / updated=2026-07-10T10:39:54Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-14T16:27:15.613571+09:00
- expected_price_dates：{'US': '2026-07-13'}
- row_dates：['2026-07-13']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:26:43Z / updated=2026-07-14T07:27:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:20:41Z / updated=2026-07-14T07:21:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T11:44:50Z / updated=2026-07-13T11:45:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T10:43:51Z / updated=2026-07-13T10:44:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T11:29:49Z / updated=2026-07-10T11:30:28Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-07-14T02:26:00.343039+09:00
- expected_price_dates：{'JP': '2026-07-14'}
- row_dates：['2026-07-13']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T17:25:35Z / updated=2026-07-13T17:26:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T17:01:49Z / updated=2026-07-13T17:02:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T17:04:30Z / updated=2026-07-10T17:04:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T16:37:17Z / updated=2026-07-10T16:37:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T17:28:20Z / updated=2026-07-09T17:28:51Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-14T16:27:15.613571+09:00
- expected_price_dates：{'JP': '2026-07-14'}
- row_dates：['2026-07-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:26:43Z / updated=2026-07-14T07:27:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-14T07:20:41Z / updated=2026-07-14T07:21:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T11:44:50Z / updated=2026-07-13T11:45:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-13T10:43:51Z / updated=2026-07-13T10:44:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T11:29:49Z / updated=2026-07-10T11:30:28Z
