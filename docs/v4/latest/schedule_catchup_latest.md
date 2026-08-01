# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/01 18:17 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定対象外曜日：weekday=5）
- 日本株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=5）
- 買い場アラート（日本価格）：判定対象外/判定前（判定対象外曜日：weekday=5）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-01T18:17:13.417281+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-08-01T16:53:04.863865+09:00
- expected_price_dates：{'US': '2026-07-31'}
- row_dates：['2026-07-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-01T07:51:03Z / updated=2026-08-01T07:53:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-01T07:37:10Z / updated=2026-08-01T07:37:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:00:41Z / updated=2026-07-31T10:01:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T08:20:35Z / updated=2026-07-31T08:21:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T07:57:34Z / updated=2026-07-30T07:58:17Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-31T19:12:55.996584+09:00
- expected_price_dates：{'US': '2026-07-31'}
- row_dates：['2026-07-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:12:24Z / updated=2026-07-31T10:13:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T09:50:41Z / updated=2026-07-31T09:51:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T09:44:59Z / updated=2026-07-30T09:45:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T07:56:35Z / updated=2026-07-30T07:57:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T10:16:43Z / updated=2026-07-29T10:17:14Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-08-01T01:18:10.037490+09:00
- expected_price_dates：{'JP': '2026-07-31'}
- row_dates：['2026-07-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T16:17:39Z / updated=2026-07-31T16:18:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T16:09:01Z / updated=2026-07-31T16:09:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T16:01:19Z / updated=2026-07-30T16:01:49Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T15:34:53Z / updated=2026-07-30T15:35:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T15:58:25Z / updated=2026-07-29T15:59:02Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-31T19:12:55.996584+09:00
- expected_price_dates：{'JP': '2026-07-31'}
- row_dates：['2026-07-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:12:24Z / updated=2026-07-31T10:13:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T09:50:41Z / updated=2026-07-31T09:51:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T09:44:59Z / updated=2026-07-30T09:45:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T07:56:35Z / updated=2026-07-30T07:57:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T10:16:43Z / updated=2026-07-29T10:17:14Z
