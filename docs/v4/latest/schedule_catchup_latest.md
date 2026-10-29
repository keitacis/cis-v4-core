# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/29 15:57 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-29T15:57:01.574769+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-29T11:52:44.824231+09:00
- expected_price_dates：{'US': '2026-10-28'}
- row_dates：['2026-10-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:52:13Z / updated=2026-10-29T02:52:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T01:49:34Z / updated=2026-10-29T01:50:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:34:25Z / updated=2026-10-28T02:35:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T01:25:18Z / updated=2026-10-28T01:25:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T02:25:06Z / updated=2026-10-27T02:25:41Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-29T14:59:31.894313+09:00
- expected_price_dates：{'US': '2026-10-28'}
- row_dates：['2026-10-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:21:44Z / updated=2026-10-28T02:22:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T05:15:42Z / updated=2026-10-27T05:16:27Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-29T01:14:50.830574+09:00
- expected_price_dates：{'JP': '2026-10-29'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T16:14:29Z / updated=2026-10-28T16:14:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T15:23:37Z / updated=2026-10-28T15:24:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T15:30:46Z / updated=2026-10-27T15:31:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T14:52:09Z / updated=2026-10-27T14:52:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-26T16:17:00Z / updated=2026-10-26T16:17:32Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-29T14:59:31.894313+09:00
- expected_price_dates：{'JP': '2026-10-29'}
- row_dates：['2026-10-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:21:44Z / updated=2026-10-28T02:22:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T05:15:42Z / updated=2026-10-27T05:16:27Z
