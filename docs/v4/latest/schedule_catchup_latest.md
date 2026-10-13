# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/13 16:37 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-13T16:37:39.772742+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-13T12:53:23.318621+09:00
- expected_price_dates：{'US': '2026-10-12'}
- row_dates：['2026-10-12']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T03:52:53Z / updated=2026-10-13T03:53:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T03:03:39Z / updated=2026-10-13T03:04:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-10T02:45:16Z / updated=2026-10-10T02:45:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-10T01:45:49Z / updated=2026-10-10T01:46:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T03:04:10Z / updated=2026-10-09T03:04:45Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-13T15:53:30.593095+09:00
- expected_price_dates：{'US': '2026-10-12'}
- row_dates：['2026-10-12']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T06:52:59Z / updated=2026-10-13T06:53:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T03:36:37Z / updated=2026-10-13T03:37:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T06:09:19Z / updated=2026-10-12T06:09:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T02:28:01Z / updated=2026-10-12T02:28:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-13T04:17:05.129008+09:00
- expected_price_dates：{'JP': '2026-10-13'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T19:16:38Z / updated=2026-10-12T19:17:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T18:09:59Z / updated=2026-10-12T18:10:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T16:31:00Z / updated=2026-10-09T16:31:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T15:31:52Z / updated=2026-10-09T15:32:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T16:53:45Z / updated=2026-10-08T16:54:19Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-13T15:53:30.593095+09:00
- expected_price_dates：{'JP': '2026-10-13'}
- row_dates：['2026-10-13']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T06:52:59Z / updated=2026-10-13T06:53:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T03:36:37Z / updated=2026-10-13T03:37:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T06:09:19Z / updated=2026-10-12T06:09:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T02:28:01Z / updated=2026-10-12T02:28:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z
