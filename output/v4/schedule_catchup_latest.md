# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/31 15:56 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-31T15:56:38.642845+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-08-29T13:19:46.277483+09:00
- expected_price_dates：{'US': '2026-08-28'}
- row_dates：['2026-08-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-29T04:19:21Z / updated=2026-08-29T04:19:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-29T03:43:45Z / updated=2026-08-29T03:44:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T07:04:12Z / updated=2026-08-28T07:04:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:09:00Z / updated=2026-08-28T06:09:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T05:02:16Z / updated=2026-08-27T05:02:48Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-08-31T14:46:18.448887+09:00
- expected_price_dates：{'US': '2026-08-28'}
- row_dates：['2026-08-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T05:45:44Z / updated=2026-08-31T05:46:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T01:23:28Z / updated=2026-08-31T01:24:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:56:53Z / updated=2026-08-28T06:57:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T09:58:35Z / updated=2026-08-27T09:59:23Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-08-29T05:58:42.533596+09:00
- expected_price_dates：{'JP': '2026-08-31'}
- row_dates：['2026-08-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T20:58:15Z / updated=2026-08-28T20:58:49Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T20:20:21Z / updated=2026-08-28T20:20:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T19:57:38Z / updated=2026-08-27T19:58:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T19:14:07Z / updated=2026-08-27T19:14:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T10:09:40Z / updated=2026-08-26T10:10:07Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-08-31T14:46:18.448887+09:00
- expected_price_dates：{'JP': '2026-08-31'}
- row_dates：['2026-08-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T05:45:44Z / updated=2026-08-31T05:46:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T01:23:28Z / updated=2026-08-31T01:24:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:56:53Z / updated=2026-08-28T06:57:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T09:58:35Z / updated=2026-08-27T09:59:23Z
