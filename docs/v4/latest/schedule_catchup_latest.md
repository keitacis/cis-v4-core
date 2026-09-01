# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/01 23:43 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-01T23:43:54.275057+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-01T11:03:38.149046+09:00
- expected_price_dates：{'US': '2026-08-31'}
- row_dates：['2026-08-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T02:03:05Z / updated=2026-09-01T02:03:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T01:18:27Z / updated=2026-09-01T01:18:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-29T04:19:21Z / updated=2026-08-29T04:19:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-29T03:43:45Z / updated=2026-08-29T03:44:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T07:04:12Z / updated=2026-08-28T07:04:44Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-01T14:19:35.547063+09:00
- expected_price_dates：{'US': '2026-08-31'}
- row_dates：['2026-08-31']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T05:18:52Z / updated=2026-09-01T05:19:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T01:51:02Z / updated=2026-09-01T01:51:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T05:45:44Z / updated=2026-08-31T05:46:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T01:23:28Z / updated=2026-08-31T01:24:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-01T23:16:36.404758+09:00
- expected_price_dates：{'JP': '2026-09-01'}
- row_dates：['2026-09-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T14:16:13Z / updated=2026-09-01T14:16:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T13:39:22Z / updated=2026-09-01T13:39:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T17:12:24Z / updated=2026-08-31T17:12:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T16:20:39Z / updated=2026-08-31T16:21:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T20:58:15Z / updated=2026-08-28T20:58:49Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-01T14:19:35.547063+09:00
- expected_price_dates：{'JP': '2026-09-01'}
- row_dates：['2026-09-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T05:18:52Z / updated=2026-09-01T05:19:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T01:51:02Z / updated=2026-09-01T01:51:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T05:45:44Z / updated=2026-08-31T05:46:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-31T01:23:28Z / updated=2026-08-31T01:24:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-28T11:30:54Z / updated=2026-08-28T11:31:31Z
