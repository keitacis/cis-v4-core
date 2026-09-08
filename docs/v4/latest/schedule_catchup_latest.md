# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/08 23:22 JST

## 判定サマリー

- ⚠️ 米国株日次騰落：再生成対象 / US価格日付が想定2026-09-07より古い：['2026-09-04']
- ⚠️ 買い場アラート（米国価格）：再生成対象 / US価格日付が想定2026-09-07より古い：['2026-09-04']
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- 米国株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_daily_us.py`
  - after：status=partial / generated=2026-09-08T23:22:22.754539+09:00 / dates=['2026-09-08']
- 買い場アラート（米国価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-09-08T23:22:30.974600+09:00 / dates=['2026-09-08']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-08T23:22:32.093561+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-08T17:00:01.525770+09:00
- expected_price_dates：{'US': '2026-09-07'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:23:39Z / updated=2026-09-08T01:24:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T00:26:38Z / updated=2026-09-08T00:27:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-05T01:24:27Z / updated=2026-09-05T01:24:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-05T00:08:05Z / updated=2026-09-05T00:08:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:21:37Z / updated=2026-09-04T01:22:12Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-08T17:00:08.212255+09:00
- expected_price_dates：{'US': '2026-09-07'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:14:03Z / updated=2026-09-08T01:14:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T01:04:28Z / updated=2026-09-07T01:04:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-08T22:49:40.590709+09:00
- expected_price_dates：{'JP': '2026-09-08'}
- row_dates：['2026-09-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T13:49:17Z / updated=2026-09-08T13:49:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T13:02:04Z / updated=2026-09-08T13:02:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T15:11:56Z / updated=2026-09-07T15:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T14:24:39Z / updated=2026-09-07T14:25:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T13:44:05Z / updated=2026-09-04T13:44:37Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-08T23:22:30.974600+09:00
- expected_price_dates：{'JP': '2026-09-08'}
- row_dates：['2026-09-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:14:03Z / updated=2026-09-08T01:14:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T01:04:28Z / updated=2026-09-07T01:04:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z
