# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/22 19:54 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-22T19:54:39.904148+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-22T17:00:19.612136+09:00
- expected_price_dates：{'US': '2026-07-21'}
- row_dates：['2026-07-21']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T07:59:53Z / updated=2026-07-22T08:00:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T07:43:15Z / updated=2026-07-22T07:44:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T07:59:37Z / updated=2026-07-21T08:00:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T07:42:54Z / updated=2026-07-21T07:43:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-18T06:32:54Z / updated=2026-07-18T06:33:38Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-22T18:38:57.652511+09:00
- expected_price_dates：{'US': '2026-07-21'}
- row_dates：['2026-07-21']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T09:38:08Z / updated=2026-07-22T09:39:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T07:57:49Z / updated=2026-07-22T07:58:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T09:40:34Z / updated=2026-07-21T09:41:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T07:57:48Z / updated=2026-07-21T07:58:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T11:24:17Z / updated=2026-07-20T11:25:04Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-07-22T18:25:48.090096+09:00
- expected_price_dates：{'JP': '2026-07-22'}
- row_dates：['2026-07-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T15:27:12Z / updated=2026-07-21T15:27:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T13:06:38Z / updated=2026-07-21T13:07:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T16:04:34Z / updated=2026-07-20T16:05:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T15:32:01Z / updated=2026-07-20T15:32:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-17T14:59:29Z / updated=2026-07-17T14:59:58Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-22T18:38:57.652511+09:00
- expected_price_dates：{'JP': '2026-07-22'}
- row_dates：['2026-07-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T09:38:08Z / updated=2026-07-22T09:39:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-22T07:57:49Z / updated=2026-07-22T07:58:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T09:40:34Z / updated=2026-07-21T09:41:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-21T07:57:48Z / updated=2026-07-21T07:58:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-20T11:24:17Z / updated=2026-07-20T11:25:04Z
