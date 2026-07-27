# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/27 21:45 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-27T21:45:23.181889+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-07-25T16:32:59.229562+09:00
- expected_price_dates：{'US': '2026-07-24'}
- row_dates：['2026-07-23', '2026-07-24']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-25T07:32:26Z / updated=2026-07-25T07:33:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-25T06:34:47Z / updated=2026-07-25T06:37:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T07:59:15Z / updated=2026-07-24T07:59:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T07:42:06Z / updated=2026-07-24T07:42:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-23T08:03:47Z / updated=2026-07-23T08:04:28Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-27T21:43:22.605232+09:00
- expected_price_dates：{'US': '2026-07-24'}
- row_dates：['2026-07-24']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T12:42:52Z / updated=2026-07-27T12:43:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T11:57:01Z / updated=2026-07-27T11:57:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T09:14:39Z / updated=2026-07-24T09:15:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T07:57:36Z / updated=2026-07-24T07:58:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-23T09:31:59Z / updated=2026-07-23T09:32:45Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-07-27T18:25:30.243837+09:00
- expected_price_dates：{'JP': '2026-07-27'}
- row_dates：['2026-07-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T15:17:19Z / updated=2026-07-24T15:17:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T15:12:11Z / updated=2026-07-24T15:12:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-23T16:05:14Z / updated=2026-07-23T16:06:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-23T15:45:32Z / updated=2026-07-23T15:46:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T15:23:13Z / updated=2026-07-22T15:23:51Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-27T21:43:22.605232+09:00
- expected_price_dates：{'JP': '2026-07-27'}
- row_dates：['2026-07-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T12:42:52Z / updated=2026-07-27T12:43:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T11:57:01Z / updated=2026-07-27T11:57:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T09:14:39Z / updated=2026-07-24T09:15:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T07:57:36Z / updated=2026-07-24T07:58:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-23T09:31:59Z / updated=2026-07-23T09:32:45Z
