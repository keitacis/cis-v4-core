# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/28 21:40 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-28T21:40:30.639035+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-08-28T16:04:39.307175+09:00
- expected_price_dates：{'US': '2026-08-27'}
- row_dates：['2026-08-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T07:04:12Z / updated=2026-08-28T07:04:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:09:00Z / updated=2026-08-28T06:09:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T05:02:16Z / updated=2026-08-27T05:02:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T03:20:30Z / updated=2026-08-27T03:21:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T23:58:26Z / updated=2026-08-25T23:58:58Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-08-28T20:31:25.542720+09:00
- expected_price_dates：{'US': '2026-08-27'}
- row_dates：['2026-08-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:56:53Z / updated=2026-08-28T06:57:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T09:58:35Z / updated=2026-08-27T09:59:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T04:32:29Z / updated=2026-08-27T04:33:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T02:01:33Z / updated=2026-08-26T02:02:08Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-08-28T18:25:34.767781+09:00
- expected_price_dates：{'JP': '2026-08-28'}
- row_dates：['2026-08-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T19:57:38Z / updated=2026-08-27T19:58:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T19:14:07Z / updated=2026-08-27T19:14:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T10:09:40Z / updated=2026-08-26T10:10:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T09:21:28Z / updated=2026-08-26T09:22:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T10:03:31Z / updated=2026-08-25T10:04:03Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-08-28T20:31:25.542720+09:00
- expected_price_dates：{'JP': '2026-08-28'}
- row_dates：['2026-08-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T06:56:53Z / updated=2026-08-28T06:57:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T09:58:35Z / updated=2026-08-27T09:59:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-27T04:32:29Z / updated=2026-08-27T04:33:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T02:01:33Z / updated=2026-08-26T02:02:08Z
