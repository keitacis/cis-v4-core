# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/09 17:03 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-09T17:03:35.094488+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-09T10:32:29.843188+09:00
- expected_price_dates：{'US': '2026-09-08'}
- row_dates：['2026-09-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:32:07Z / updated=2026-09-09T01:32:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T00:17:37Z / updated=2026-09-09T00:18:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:23:39Z / updated=2026-09-08T01:24:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T00:26:38Z / updated=2026-09-08T00:27:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-05T01:24:27Z / updated=2026-09-05T01:24:59Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-09T13:51:59.758964+09:00
- expected_price_dates：{'US': '2026-09-08'}
- row_dates：['2026-09-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:16:38Z / updated=2026-09-09T01:17:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:14:03Z / updated=2026-09-08T01:14:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-08T22:49:40.590709+09:00
- expected_price_dates：{'JP': '2026-09-09'}
- row_dates：['2026-09-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T13:49:17Z / updated=2026-09-08T13:49:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T13:02:04Z / updated=2026-09-08T13:02:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T15:11:56Z / updated=2026-09-07T15:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T14:24:39Z / updated=2026-09-07T14:25:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T13:44:05Z / updated=2026-09-04T13:44:37Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-09T13:51:59.758964+09:00
- expected_price_dates：{'JP': '2026-09-09'}
- row_dates：['2026-09-09']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T04:51:35Z / updated=2026-09-09T04:52:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-09T01:16:38Z / updated=2026-09-09T01:17:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T04:49:01Z / updated=2026-09-08T04:49:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-08T01:14:03Z / updated=2026-09-08T01:14:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z
