# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/20 19:38 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-20T19:38:44.337326+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-08-20T08:57:50.721180+09:00
- expected_price_dates：{'US': '2026-08-19'}
- row_dates：['2026-08-19']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T23:57:21Z / updated=2026-08-19T23:57:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T22:43:56Z / updated=2026-08-19T22:44:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T23:57:27Z / updated=2026-08-18T23:57:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T22:42:54Z / updated=2026-08-18T22:43:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-17T23:57:29Z / updated=2026-08-17T23:58:08Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-08-20T10:55:08.709187+09:00
- expected_price_dates：{'US': '2026-08-19'}
- row_dates：['2026-08-19']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-20T01:54:40Z / updated=2026-08-20T01:55:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T23:40:41Z / updated=2026-08-19T23:41:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T01:55:33Z / updated=2026-08-19T01:56:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T23:40:08Z / updated=2026-08-18T23:40:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T01:53:37Z / updated=2026-08-18T01:54:19Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-08-20T19:03:51.930532+09:00
- expected_price_dates：{'JP': '2026-08-20'}
- row_dates：['2026-08-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-20T10:03:27Z / updated=2026-08-20T10:03:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-20T09:07:46Z / updated=2026-08-20T09:08:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T10:01:36Z / updated=2026-08-19T10:02:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T09:06:59Z / updated=2026-08-19T09:07:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T10:00:50Z / updated=2026-08-18T10:01:17Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-08-20T10:55:08.709187+09:00
- expected_price_dates：{'JP': '2026-08-20'}
- row_dates：['2026-08-20']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-20T01:54:40Z / updated=2026-08-20T01:55:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T23:40:41Z / updated=2026-08-19T23:41:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-19T01:55:33Z / updated=2026-08-19T01:56:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T23:40:08Z / updated=2026-08-18T23:40:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-18T01:53:37Z / updated=2026-08-18T01:54:19Z
