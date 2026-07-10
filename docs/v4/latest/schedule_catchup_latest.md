# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/10 21:16 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-10T21:16:34.167782+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-10T19:39:50.203053+09:00
- expected_price_dates：{'US': '2026-07-09'}
- row_dates：['2026-07-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:39:28Z / updated=2026-07-10T10:39:54Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:30:46Z / updated=2026-07-10T10:31:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:41:18Z / updated=2026-07-09T10:46:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:36:05Z / updated=2026-07-09T10:36:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T08:01:04Z / updated=2026-07-08T08:01:29Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-10T20:30:23.449323+09:00
- expected_price_dates：{'US': '2026-07-09'}
- row_dates：['2026-07-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T11:29:49Z / updated=2026-07-10T11:30:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:38:01Z / updated=2026-07-10T10:38:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T11:30:58Z / updated=2026-07-09T11:31:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:40:30Z / updated=2026-07-09T10:41:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T09:33:59Z / updated=2026-07-08T09:34:33Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-07-10T18:25:33.245191+09:00
- expected_price_dates：{'JP': '2026-07-10'}
- row_dates：['2026-07-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T17:28:20Z / updated=2026-07-09T17:28:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T17:25:03Z / updated=2026-07-09T17:25:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T16:14:38Z / updated=2026-07-08T16:15:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T16:08:50Z / updated=2026-07-08T16:09:16Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-07T12:50:36Z / updated=2026-07-07T12:51:14Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-10T20:30:23.449323+09:00
- expected_price_dates：{'JP': '2026-07-10'}
- row_dates：['2026-07-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T11:29:49Z / updated=2026-07-10T11:30:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:38:01Z / updated=2026-07-10T10:38:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T11:30:58Z / updated=2026-07-09T11:31:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:40:30Z / updated=2026-07-09T10:41:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T09:33:59Z / updated=2026-07-08T09:34:33Z
