# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/26 19:42 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-26T19:42:26.449387+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-08-26T08:58:52.485031+09:00
- expected_price_dates：{'US': '2026-08-25'}
- row_dates：['2026-08-25']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T23:58:26Z / updated=2026-08-25T23:58:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T22:47:14Z / updated=2026-08-25T22:47:47Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T23:57:11Z / updated=2026-08-24T23:57:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T22:46:11Z / updated=2026-08-24T22:46:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-21T23:58:10Z / updated=2026-08-21T23:58:38Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-08-26T11:02:03.646042+09:00
- expected_price_dates：{'US': '2026-08-25'}
- row_dates：['2026-08-25']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T02:01:33Z / updated=2026-08-26T02:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T23:41:30Z / updated=2026-08-25T23:41:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T01:55:44Z / updated=2026-08-25T01:56:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T23:39:44Z / updated=2026-08-24T23:40:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T02:00:10Z / updated=2026-08-24T02:00:49Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-08-26T19:10:02.387289+09:00
- expected_price_dates：{'JP': '2026-08-26'}
- row_dates：['2026-08-26']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T10:09:40Z / updated=2026-08-26T10:10:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T09:21:28Z / updated=2026-08-26T09:22:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T10:03:31Z / updated=2026-08-25T10:04:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T09:16:55Z / updated=2026-08-25T09:17:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T10:19:56Z / updated=2026-08-24T10:20:25Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-08-26T11:02:03.646042+09:00
- expected_price_dates：{'JP': '2026-08-26'}
- row_dates：['2026-08-26']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-26T02:01:33Z / updated=2026-08-26T02:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T23:41:30Z / updated=2026-08-25T23:41:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-25T01:55:44Z / updated=2026-08-25T01:56:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T23:39:44Z / updated=2026-08-24T23:40:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-24T02:00:10Z / updated=2026-08-24T02:00:49Z
