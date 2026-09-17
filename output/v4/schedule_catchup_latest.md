# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/17 15:01 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-17T15:01:49.505912+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-17T10:42:16.201865+09:00
- expected_price_dates：{'US': '2026-09-16'}
- row_dates：['2026-09-15', '2026-09-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:41:52Z / updated=2026-09-17T01:42:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T00:34:37Z / updated=2026-09-17T00:35:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T01:39:46Z / updated=2026-09-16T01:40:28Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T00:24:38Z / updated=2026-09-16T00:25:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-15T01:53:33Z / updated=2026-09-15T01:53:59Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-17T14:00:25.603074+09:00
- expected_price_dates：{'US': '2026-09-16'}
- row_dates：['2026-09-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T01:28:04Z / updated=2026-09-16T01:28:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-15T05:01:43Z / updated=2026-09-15T05:02:19Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-16T23:20:41.303349+09:00
- expected_price_dates：{'JP': '2026-09-17'}
- row_dates：['2026-09-16']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T14:20:14Z / updated=2026-09-16T14:20:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T13:41:49Z / updated=2026-09-16T13:42:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-15T14:25:53Z / updated=2026-09-15T14:26:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-15T13:50:08Z / updated=2026-09-15T13:50:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-14T15:58:32Z / updated=2026-09-14T15:59:04Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-17T14:00:25.603074+09:00
- expected_price_dates：{'JP': '2026-09-17'}
- row_dates：['2026-09-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T04:59:57Z / updated=2026-09-17T05:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-17T01:29:40Z / updated=2026-09-17T01:30:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T04:56:51Z / updated=2026-09-16T04:57:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-16T01:28:04Z / updated=2026-09-16T01:28:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-15T05:01:43Z / updated=2026-09-15T05:02:19Z
