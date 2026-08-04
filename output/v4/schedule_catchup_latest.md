# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/04 20:36 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ⚠️ 買い場アラート（米国価格）：再生成対象 / US価格日付が想定2026-08-03より古い：['2026-07-31']
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- 買い場アラート（米国価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-08-04T20:36:50.012185+09:00 / dates=['2026-07-31']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-04T20:36:50.901012+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-08-04T18:50:09.107259+09:00
- expected_price_dates：{'US': '2026-08-03'}
- row_dates：['2026-08-03']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T09:49:45Z / updated=2026-08-04T09:50:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T08:01:02Z / updated=2026-08-04T08:01:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-01T07:51:03Z / updated=2026-08-01T07:53:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-01T07:37:10Z / updated=2026-08-01T07:37:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:00:41Z / updated=2026-07-31T10:01:10Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-08-04T20:02:00.504396+09:00
- expected_price_dates：{'US': '2026-08-03'}
- row_dates：['2026-07-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T10:18:32Z / updated=2026-08-04T10:19:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T08:10:15Z / updated=2026-08-04T08:10:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T12:43:00Z / updated=2026-08-03T12:43:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T12:01:35Z / updated=2026-08-03T12:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:12:24Z / updated=2026-07-31T10:13:01Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-08-04T18:25:32.830601+09:00
- expected_price_dates：{'JP': '2026-08-04'}
- row_dates：['2026-08-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T17:21:26Z / updated=2026-08-03T17:21:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T17:01:20Z / updated=2026-08-03T17:01:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T16:17:39Z / updated=2026-07-31T16:18:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T16:09:01Z / updated=2026-07-31T16:09:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-30T16:01:19Z / updated=2026-07-30T16:01:49Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-08-04T20:36:50.012185+09:00
- expected_price_dates：{'JP': '2026-08-04'}
- row_dates：['2026-08-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T10:18:32Z / updated=2026-08-04T10:19:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-04T08:10:15Z / updated=2026-08-04T08:10:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T12:43:00Z / updated=2026-08-03T12:43:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-03T12:01:35Z / updated=2026-08-03T12:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-31T10:12:24Z / updated=2026-07-31T10:13:01Z
