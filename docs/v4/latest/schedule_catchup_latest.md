# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/11 09:14 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定対象外曜日：weekday=5）
- 日本株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=5）
- 買い場アラート（日本価格）：判定対象外/判定前（判定対象外曜日：weekday=5）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-11T09:14:09.683149+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-11T07:25:28.753670+09:00
- expected_price_dates：{'US': '2026-07-10'}
- row_dates：['2026-07-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:39:28Z / updated=2026-07-10T10:39:54Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:30:46Z / updated=2026-07-10T10:31:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:41:18Z / updated=2026-07-09T10:46:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:36:05Z / updated=2026-07-09T10:36:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T08:01:04Z / updated=2026-07-08T08:01:29Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-10T20:30:23.449323+09:00
- expected_price_dates：{'US': '2026-07-10'}
- row_dates：['2026-07-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T11:29:49Z / updated=2026-07-10T11:30:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T10:38:01Z / updated=2026-07-10T10:38:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T11:30:58Z / updated=2026-07-09T11:31:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T10:40:30Z / updated=2026-07-09T10:41:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T09:33:59Z / updated=2026-07-08T09:34:33Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-07-11T02:04:53.131354+09:00
- expected_price_dates：{'JP': '2026-07-10'}
- row_dates：['2026-07-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T17:04:30Z / updated=2026-07-10T17:04:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-10T16:37:17Z / updated=2026-07-10T16:37:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T17:28:20Z / updated=2026-07-09T17:28:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-09T17:25:03Z / updated=2026-07-09T17:25:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-08T16:14:38Z / updated=2026-07-08T16:15:03Z

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
