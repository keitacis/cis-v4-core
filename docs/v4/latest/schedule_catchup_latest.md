# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/10 23:56 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-10T23:56:53.627330+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-10T10:27:56.347035+09:00
- expected_price_dates：{'US': '2026-09-09'}
- row_dates：['2026-09-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:27:31Z / updated=2026-09-10T01:28:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T00:16:42Z / updated=2026-09-10T00:17:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:32:07Z / updated=2026-09-09T01:32:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T00:17:37Z / updated=2026-09-09T00:18:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:23:39Z / updated=2026-09-08T01:24:15Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-10T13:53:40.832133+09:00
- expected_price_dates：{'US': '2026-09-09'}
- row_dates：['2026-09-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T04:53:08Z / updated=2026-09-10T04:53:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:08:25Z / updated=2026-09-10T01:08:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:16:38Z / updated=2026-09-09T01:17:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-10T22:46:49.708069+09:00
- expected_price_dates：{'JP': '2026-09-10'}
- row_dates：['2026-09-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T13:46:20Z / updated=2026-09-10T13:46:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T13:05:07Z / updated=2026-09-10T13:05:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T13:52:07Z / updated=2026-09-09T13:52:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T13:07:10Z / updated=2026-09-09T13:07:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T13:49:17Z / updated=2026-09-08T13:49:46Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-10T13:53:40.832133+09:00
- expected_price_dates：{'JP': '2026-09-10'}
- row_dates：['2026-09-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T04:53:08Z / updated=2026-09-10T04:53:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:08:25Z / updated=2026-09-10T01:08:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:16:38Z / updated=2026-09-09T01:17:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z
