# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/09 19:23 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / JP価格日付が想定2026-10-09より古い：['2026-10-08']
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=ok / generated=2026-10-09T19:23:00.352330+09:00 / dates=['2026-10-09']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-09T19:23:00.749462+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-09T12:04:38.816321+09:00
- expected_price_dates：{'US': '2026-10-08'}
- row_dates：['2026-10-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T03:04:10Z / updated=2026-10-09T03:04:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:12:51Z / updated=2026-10-09T02:13:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:56:04Z / updated=2026-10-08T02:56:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T01:58:45Z / updated=2026-10-08T01:59:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T02:41:20Z / updated=2026-10-07T02:41:57Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-09T15:19:45.539174+09:00
- expected_price_dates：{'US': '2026-10-08'}
- row_dates：['2026-10-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:58:03Z / updated=2026-10-09T02:58:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:43:28Z / updated=2026-10-08T02:44:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T06:09:52Z / updated=2026-10-07T06:10:35Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-09T01:54:12.673391+09:00
- expected_price_dates：{'JP': '2026-10-09'}
- row_dates：['2026-10-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T16:53:45Z / updated=2026-10-08T16:54:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T15:49:31Z / updated=2026-10-08T15:50:03Z
  - event=schedule / status=completed / conclusion=failure / started=2026-10-07T16:52:29Z / updated=2026-10-07T16:53:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T15:43:54Z / updated=2026-10-07T15:44:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T16:13:50Z / updated=2026-10-06T16:14:17Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-09T15:19:45.539174+09:00
- expected_price_dates：{'JP': '2026-10-09'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:58:03Z / updated=2026-10-09T02:58:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:43:28Z / updated=2026-10-08T02:44:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T06:09:52Z / updated=2026-10-07T06:10:35Z
