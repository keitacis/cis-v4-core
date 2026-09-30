# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/30 18:34 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-30T18:34:56.014480+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-30T11:23:40.753133+09:00
- expected_price_dates：{'US': '2026-09-29'}
- row_dates：['2026-09-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:23:15Z / updated=2026-09-30T02:23:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T01:18:44Z / updated=2026-09-30T01:19:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:44:04Z / updated=2026-09-29T02:44:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:00:31Z / updated=2026-09-29T02:00:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-26T01:59:15Z / updated=2026-09-26T01:59:48Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-30T14:42:23.456383+09:00
- expected_price_dates：{'US': '2026-09-29'}
- row_dates：['2026-09-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:35:28Z / updated=2026-09-29T02:35:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T05:33:39Z / updated=2026-09-28T05:34:13Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-30T18:25:33.240780+09:00
- expected_price_dates：{'JP': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T16:05:47Z / updated=2026-09-29T16:06:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T15:02:42Z / updated=2026-09-29T15:03:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T17:47:28Z / updated=2026-09-28T17:48:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T16:58:20Z / updated=2026-09-28T16:58:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T14:42:53Z / updated=2026-09-25T14:43:18Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-30T14:42:23.456383+09:00
- expected_price_dates：{'JP': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:35:28Z / updated=2026-09-29T02:35:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T05:33:39Z / updated=2026-09-28T05:34:13Z
