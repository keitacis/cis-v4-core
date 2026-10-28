# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/28 18:31 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-28T18:31:48.839758+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-28T11:34:56.525335+09:00
- expected_price_dates：{'US': '2026-10-27'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:34:25Z / updated=2026-10-28T02:35:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T01:25:18Z / updated=2026-10-28T01:25:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T02:25:06Z / updated=2026-10-27T02:25:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T01:29:37Z / updated=2026-10-27T01:30:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-24T01:58:18Z / updated=2026-10-24T01:58:47Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-28T14:55:01.562026+09:00
- expected_price_dates：{'US': '2026-10-27'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:21:44Z / updated=2026-10-28T02:22:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T05:15:42Z / updated=2026-10-27T05:16:27Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T02:08:14Z / updated=2026-10-27T02:08:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-26T04:58:01Z / updated=2026-10-26T04:58:42Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-28T00:31:10.767195+09:00
- expected_price_dates：{'JP': '2026-10-28'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T15:30:46Z / updated=2026-10-27T15:31:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T14:52:09Z / updated=2026-10-27T14:52:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-26T16:17:00Z / updated=2026-10-26T16:17:32Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-26T15:25:31Z / updated=2026-10-26T15:26:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T14:23:32Z / updated=2026-10-23T14:23:58Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-28T14:55:01.562026+09:00
- expected_price_dates：{'JP': '2026-10-28'}
- row_dates：['2026-10-28']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:21:44Z / updated=2026-10-28T02:22:21Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T05:15:42Z / updated=2026-10-27T05:16:27Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T02:08:14Z / updated=2026-10-27T02:08:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-26T04:58:01Z / updated=2026-10-26T04:58:42Z
