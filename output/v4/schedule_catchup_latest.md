# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/23 23:52 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / JP価格日付が想定2026-09-23より古い：['2026-09-18']
- ⚠️ 買い場アラート（日本価格）：再生成対象 / JP価格日付が想定2026-09-23より古い：['2026-09-18']

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=partial / generated=2026-09-23T23:52:33.542035+09:00 / dates=['2026-09-18']
- 買い場アラート（日本価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-09-23T23:52:44.586575+09:00 / dates=['2026-09-18']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-23T23:52:45.028998+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-23T10:48:02.398638+09:00
- expected_price_dates：{'US': '2026-09-22'}
- row_dates：['2026-09-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T01:47:38Z / updated=2026-09-23T01:48:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T00:37:17Z / updated=2026-09-23T00:37:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:52:44Z / updated=2026-09-22T01:53:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T00:52:18Z / updated=2026-09-22T00:52:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-19T01:36:40Z / updated=2026-09-19T01:37:09Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-23T20:25:38.526742+09:00
- expected_price_dates：{'US': '2026-09-22'}
- row_dates：['2026-09-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T04:52:40Z / updated=2026-09-23T04:53:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T01:31:58Z / updated=2026-09-23T01:32:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T05:07:57Z / updated=2026-09-22T05:08:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:37:28Z / updated=2026-09-22T01:37:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T05:06:46Z / updated=2026-09-21T05:07:24Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-09-23T23:24:26.539171+09:00
- expected_price_dates：{'JP': '2026-09-23'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=failure / started=2026-09-23T14:24:01Z / updated=2026-09-23T14:24:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T13:49:17Z / updated=2026-09-23T13:49:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T14:09:30Z / updated=2026-09-22T14:09:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T13:37:53Z / updated=2026-09-22T13:38:27Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T15:59:35Z / updated=2026-09-21T16:00:02Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-23T20:25:38.526742+09:00
- expected_price_dates：{'JP': '2026-09-23'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T04:52:40Z / updated=2026-09-23T04:53:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T01:31:58Z / updated=2026-09-23T01:32:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T05:07:57Z / updated=2026-09-22T05:08:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T01:37:28Z / updated=2026-09-22T01:37:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-21T05:06:46Z / updated=2026-09-21T05:07:24Z
