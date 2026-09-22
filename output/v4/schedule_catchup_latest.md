# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/22 23:40 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / JP価格日付が想定2026-09-22より古い：['2026-09-18']
- ⚠️ 買い場アラート（日本価格）：再生成対象 / JP価格日付が想定2026-09-22より古い：['2026-09-18']

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=partial / generated=2026-09-22T23:39:49.354999+09:00 / dates=['2026-09-18']
- 買い場アラート（日本価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-09-22T23:40:03.117363+09:00 / dates=['2026-09-18']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-22T23:40:03.625338+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-22T10:53:11.548817+09:00
- expected_price_dates：{'US': '2026-09-21'}
- row_dates：['2026-09-21']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:52:44Z / updated=2026-09-22T01:53:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T00:52:18Z / updated=2026-09-22T00:52:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-19T01:36:40Z / updated=2026-09-19T01:37:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-19T00:22:50Z / updated=2026-09-19T00:23:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:30:07Z / updated=2026-09-18T01:30:34Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-22T20:25:50.677913+09:00
- expected_price_dates：{'US': '2026-09-21'}
- row_dates：['2026-09-21']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T05:07:57Z / updated=2026-09-22T05:08:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:37:28Z / updated=2026-09-22T01:37:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T05:06:46Z / updated=2026-09-21T05:07:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T01:11:12Z / updated=2026-09-21T01:11:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-09-22T23:09:53.504678+09:00
- expected_price_dates：{'JP': '2026-09-22'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T14:09:30Z / updated=2026-09-22T14:09:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T13:37:53Z / updated=2026-09-22T13:38:27Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T15:59:35Z / updated=2026-09-21T16:00:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T15:17:53Z / updated=2026-09-21T15:18:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T13:47:06Z / updated=2026-09-18T13:47:38Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-22T20:25:50.677913+09:00
- expected_price_dates：{'JP': '2026-09-22'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T05:07:57Z / updated=2026-09-22T05:08:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:37:28Z / updated=2026-09-22T01:37:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T05:06:46Z / updated=2026-09-21T05:07:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T01:11:12Z / updated=2026-09-21T01:11:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z
