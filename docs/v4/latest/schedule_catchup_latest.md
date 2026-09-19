# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/19 14:43 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定対象外曜日：weekday=5）
- 日本株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=5）
- 買い場アラート（日本価格）：判定対象外/判定前（判定対象外曜日：weekday=5）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-19T14:43:48.661471+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-19T10:37:03.112742+09:00
- expected_price_dates：{'US': '2026-09-18'}
- row_dates：['2026-09-17', '2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-19T01:36:40Z / updated=2026-09-19T01:37:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-19T00:22:50Z / updated=2026-09-19T00:23:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:30:07Z / updated=2026-09-18T01:30:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T00:22:58Z / updated=2026-09-18T00:23:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:41:52Z / updated=2026-09-17T01:42:24Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-18T13:52:54.688887+09:00
- expected_price_dates：{'US': '2026-09-18'}
- row_dates：['2026-09-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:18:40Z / updated=2026-09-18T01:19:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-18T22:47:32.203665+09:00
- expected_price_dates：{'JP': '2026-09-18'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T13:47:06Z / updated=2026-09-18T13:47:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T13:07:21Z / updated=2026-09-18T13:08:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T14:25:11Z / updated=2026-09-17T14:25:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T13:44:32Z / updated=2026-09-17T13:44:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T14:20:14Z / updated=2026-09-16T14:20:48Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-18T13:52:54.688887+09:00
- expected_price_dates：{'JP': '2026-09-18'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:18:40Z / updated=2026-09-18T01:19:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z
