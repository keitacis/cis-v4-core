# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/12 19:38 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / 生成日が当日ではない：2026-10-10 / JP価格日付が想定2026-10-12より古い：['2026-10-09']
- ⚠️ 買い場アラート（日本価格）：再生成対象 / JP価格日付が想定2026-10-12より古い：['2026-10-09']

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=partial / generated=2026-10-12T19:37:46.247949+09:00 / dates=['2026-10-09']
- 買い場アラート（日本価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-10-12T19:38:01.972567+09:00 / dates=['2026-10-09']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-12T19:38:02.517228+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-10T11:45:39.455493+09:00
- expected_price_dates：{'US': '2026-10-09'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-10T02:45:16Z / updated=2026-10-10T02:45:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-10T01:45:49Z / updated=2026-10-10T01:46:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T03:04:10Z / updated=2026-10-09T03:04:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:12:51Z / updated=2026-10-09T02:13:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:56:04Z / updated=2026-10-08T02:56:40Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-12T15:09:52.088046+09:00
- expected_price_dates：{'US': '2026-10-09'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T06:09:19Z / updated=2026-10-12T06:09:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T02:28:01Z / updated=2026-10-12T02:28:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:58:03Z / updated=2026-10-09T02:58:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-10T01:31:22.423246+09:00
- expected_price_dates：{'JP': '2026-10-12'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T16:31:00Z / updated=2026-10-09T16:31:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T15:31:52Z / updated=2026-10-09T15:32:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T16:53:45Z / updated=2026-10-08T16:54:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T15:49:31Z / updated=2026-10-08T15:50:03Z
  - event=schedule / status=completed / conclusion=failure / started=2026-10-07T16:52:29Z / updated=2026-10-07T16:53:12Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-12T15:09:52.088046+09:00
- expected_price_dates：{'JP': '2026-10-12'}
- row_dates：['2026-10-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T06:09:19Z / updated=2026-10-12T06:09:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T02:28:01Z / updated=2026-10-12T02:28:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T06:19:16Z / updated=2026-10-09T06:19:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-09T02:58:03Z / updated=2026-10-09T02:58:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z
