# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/20 21:03 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / JP価格日付が想定2026-07-20より古い：['2026-07-17']
- ⚠️ 買い場アラート（日本価格）：再生成対象 / JP価格日付が想定2026-07-20より古い：['2026-07-17']

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=partial / generated=2026-07-20T21:03:47.470664+09:00 / dates=['2026-07-17']
- 買い場アラート（日本価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-07-20T21:03:55.860107+09:00 / dates=['2026-07-17']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-20T21:03:56.416490+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-18T15:33:31.835846+09:00
- expected_price_dates：{'US': '2026-07-17'}
- row_dates：['2026-07-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-18T06:32:54Z / updated=2026-07-18T06:33:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-18T06:15:52Z / updated=2026-07-18T06:18:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T07:33:28Z / updated=2026-07-17T07:33:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T06:32:18Z / updated=2026-07-17T06:32:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-16T07:36:53Z / updated=2026-07-16T07:37:23Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-07-20T20:30:57.421996+09:00
- expected_price_dates：{'US': '2026-07-17'}
- row_dates：['2026-07-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T11:24:17Z / updated=2026-07-20T11:25:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T10:27:15Z / updated=2026-07-20T10:27:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T07:36:07Z / updated=2026-07-17T07:37:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T07:30:48Z / updated=2026-07-17T07:31:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-16T07:48:49Z / updated=2026-07-16T07:49:55Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-07-20T20:30:35.096717+09:00
- expected_price_dates：{'JP': '2026-07-20'}
- row_dates：['2026-07-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T14:59:29Z / updated=2026-07-17T14:59:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T12:45:46Z / updated=2026-07-17T12:46:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-16T15:21:24Z / updated=2026-07-16T15:21:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-16T15:18:22Z / updated=2026-07-16T15:18:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-15T15:11:03Z / updated=2026-07-15T15:11:40Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-07-20T20:30:57.421996+09:00
- expected_price_dates：{'JP': '2026-07-20'}
- row_dates：['2026-07-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T11:24:17Z / updated=2026-07-20T11:25:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T10:27:15Z / updated=2026-07-20T10:27:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T07:36:07Z / updated=2026-07-17T07:37:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T07:30:48Z / updated=2026-07-17T07:31:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-16T07:48:49Z / updated=2026-07-16T07:49:55Z
