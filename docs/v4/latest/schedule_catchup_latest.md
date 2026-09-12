# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/12 16:51 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定対象外曜日：weekday=5）
- 日本株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=5）
- 買い場アラート（日本価格）：判定対象外/判定前（判定対象外曜日：weekday=5）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-12T16:51:14.817602+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-12T10:33:26.990628+09:00
- expected_price_dates：{'US': '2026-09-11'}
- row_dates：['2026-09-11']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-12T01:33:08Z / updated=2026-09-12T01:33:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-12T00:20:16Z / updated=2026-09-12T00:20:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T01:28:20Z / updated=2026-09-11T01:29:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T00:12:36Z / updated=2026-09-11T00:13:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:27:31Z / updated=2026-09-10T01:28:00Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-11T13:50:16.131936+09:00
- expected_price_dates：{'US': '2026-09-11'}
- row_dates：['2026-09-10']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T04:49:39Z / updated=2026-09-11T04:50:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T01:10:02Z / updated=2026-09-11T01:11:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T04:53:08Z / updated=2026-09-10T04:53:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:08:25Z / updated=2026-09-10T01:08:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-11T22:47:56.621000+09:00
- expected_price_dates：{'JP': '2026-09-11'}
- row_dates：['2026-09-11']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T13:47:31Z / updated=2026-09-11T13:48:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T12:59:06Z / updated=2026-09-11T12:59:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T13:46:20Z / updated=2026-09-10T13:46:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T13:05:07Z / updated=2026-09-10T13:05:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T13:52:07Z / updated=2026-09-09T13:52:41Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-11T13:50:16.131936+09:00
- expected_price_dates：{'JP': '2026-09-11'}
- row_dates：['2026-09-11']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T04:49:39Z / updated=2026-09-11T04:50:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-11T01:10:02Z / updated=2026-09-11T01:11:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T04:53:08Z / updated=2026-09-10T04:53:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-10T01:08:25Z / updated=2026-09-10T01:08:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z
