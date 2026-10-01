# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/01 09:26 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-01T09:26:26.659524+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-01T07:25:32.522906+09:00
- expected_price_dates：{'US': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:23:15Z / updated=2026-09-30T02:23:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T01:18:44Z / updated=2026-09-30T01:19:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:44:04Z / updated=2026-09-29T02:44:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:00:31Z / updated=2026-09-29T02:00:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-26T01:59:15Z / updated=2026-09-26T01:59:48Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-01T08:25:33.625003+09:00
- expected_price_dates：{'US': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:35:28Z / updated=2026-09-29T02:35:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T05:33:39Z / updated=2026-09-28T05:34:13Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-01T01:03:40.472136+09:00
- expected_price_dates：{'JP': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T16:03:19Z / updated=2026-09-30T16:03:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T15:13:50Z / updated=2026-09-30T15:14:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T16:05:47Z / updated=2026-09-29T16:06:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T15:02:42Z / updated=2026-09-29T15:03:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T17:47:28Z / updated=2026-09-28T17:48:32Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-01T08:25:33.625003+09:00
- expected_price_dates：{'JP': '2026-09-30'}
- row_dates：['2026-09-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:35:28Z / updated=2026-09-29T02:35:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-28T05:33:39Z / updated=2026-09-28T05:34:13Z
