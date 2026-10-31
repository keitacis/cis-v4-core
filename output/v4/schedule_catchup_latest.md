# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/31 09:35 JST

## 判定サマリー

- ⚠️ 米国株日次騰落：再生成対象 / 生成日が当日ではない：2026-10-30 / US価格日付が想定2026-10-30より古い：['2026-10-29']
- 買い場アラート（米国価格）：判定対象外/判定前（判定対象外曜日：weekday=5）
- 日本株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=5）
- 買い場アラート（日本価格）：判定対象外/判定前（判定対象外曜日：weekday=5）

## 実行結果

- 米国株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_daily_us.py`
  - after：status=partial / generated=2026-10-31T09:35:30.473287+09:00 / dates=['2026-10-29']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-31T09:35:32.551698+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-30T11:57:46.186268+09:00
- expected_price_dates：{'US': '2026-10-30'}
- row_dates：['2026-10-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:57:18Z / updated=2026-10-30T02:57:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T01:58:36Z / updated=2026-10-30T01:59:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:52:13Z / updated=2026-10-29T02:52:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T01:49:34Z / updated=2026-10-29T01:50:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:34:25Z / updated=2026-10-28T02:35:02Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-30T15:00:25.520949+09:00
- expected_price_dates：{'US': '2026-10-30'}
- row_dates：['2026-10-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T05:59:54Z / updated=2026-10-30T06:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:39:22Z / updated=2026-10-30T02:40:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-31T01:11:30.573223+09:00
- expected_price_dates：{'JP': '2026-10-30'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T16:11:06Z / updated=2026-10-30T16:11:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T15:16:45Z / updated=2026-10-30T15:17:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T16:23:05Z / updated=2026-10-29T16:23:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T15:29:38Z / updated=2026-10-29T15:30:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T16:14:29Z / updated=2026-10-28T16:14:58Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-30T15:00:25.520949+09:00
- expected_price_dates：{'JP': '2026-10-30'}
- row_dates：['2026-10-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T05:59:54Z / updated=2026-10-30T06:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:39:22Z / updated=2026-10-30T02:40:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
