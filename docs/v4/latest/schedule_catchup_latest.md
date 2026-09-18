# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/18 23:20 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-18T23:20:11.763348+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-18T10:30:30.166392+09:00
- expected_price_dates：{'US': '2026-09-17'}
- row_dates：['2026-09-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:30:07Z / updated=2026-09-18T01:30:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T00:22:58Z / updated=2026-09-18T00:23:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:41:52Z / updated=2026-09-17T01:42:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T00:34:37Z / updated=2026-09-17T00:35:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T01:39:46Z / updated=2026-09-16T01:40:28Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-18T13:52:54.688887+09:00
- expected_price_dates：{'US': '2026-09-17'}
- row_dates：['2026-09-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:18:40Z / updated=2026-09-18T01:19:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-18T22:47:32.203665+09:00
- expected_price_dates：{'JP': '2026-09-18'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T13:47:06Z / updated=2026-09-18T13:47:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T13:07:21Z / updated=2026-09-18T13:08:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T14:25:11Z / updated=2026-09-17T14:25:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T13:44:32Z / updated=2026-09-17T13:44:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T14:20:14Z / updated=2026-09-16T14:20:48Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-18T13:52:54.688887+09:00
- expected_price_dates：{'JP': '2026-09-18'}
- row_dates：['2026-09-18']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T04:52:29Z / updated=2026-09-18T04:52:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-18T01:18:40Z / updated=2026-09-18T01:19:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z
