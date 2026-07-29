# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/29 20:37 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-29T20:37:13.187270+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-29T18:48:12.051006+09:00
- expected_price_dates：{'US': '2026-07-28'}
- row_dates：['2026-07-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T09:47:35Z / updated=2026-07-29T09:48:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T08:07:27Z / updated=2026-07-29T08:08:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T09:42:57Z / updated=2026-07-28T09:43:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T07:59:01Z / updated=2026-07-28T07:59:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-25T07:32:26Z / updated=2026-07-25T07:33:05Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-29T19:17:09.023143+09:00
- expected_price_dates：{'US': '2026-07-28'}
- row_dates：['2026-07-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T10:16:43Z / updated=2026-07-29T10:17:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T08:11:41Z / updated=2026-07-29T08:12:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T10:13:00Z / updated=2026-07-28T10:13:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T08:07:21Z / updated=2026-07-28T08:08:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T12:42:52Z / updated=2026-07-27T12:43:26Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-07-29T18:25:36.162250+09:00
- expected_price_dates：{'JP': '2026-07-29'}
- row_dates：['2026-07-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T16:19:31Z / updated=2026-07-28T16:20:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T16:15:45Z / updated=2026-07-28T16:16:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T17:05:07Z / updated=2026-07-27T17:05:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T16:39:05Z / updated=2026-07-27T16:39:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-24T15:17:19Z / updated=2026-07-24T15:17:57Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-29T19:17:09.023143+09:00
- expected_price_dates：{'JP': '2026-07-29'}
- row_dates：['2026-07-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T10:16:43Z / updated=2026-07-29T10:17:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-29T08:11:41Z / updated=2026-07-29T08:12:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T10:13:00Z / updated=2026-07-28T10:13:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-28T08:07:21Z / updated=2026-07-28T08:08:04Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-27T12:42:52Z / updated=2026-07-27T12:43:26Z
