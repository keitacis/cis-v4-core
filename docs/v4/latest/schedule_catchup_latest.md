# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/30 18:53 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-30T18:53:07.062083+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-30T11:57:46.186268+09:00
- expected_price_dates：{'US': '2026-10-29'}
- row_dates：['2026-10-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:57:18Z / updated=2026-10-30T02:57:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T01:58:36Z / updated=2026-10-30T01:59:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:52:13Z / updated=2026-10-29T02:52:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T01:49:34Z / updated=2026-10-29T01:50:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T02:34:25Z / updated=2026-10-28T02:35:02Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-30T15:00:25.520949+09:00
- expected_price_dates：{'US': '2026-10-29'}
- row_dates：['2026-10-29']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T05:59:54Z / updated=2026-10-30T06:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:39:22Z / updated=2026-10-30T02:40:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-30T01:23:29.253360+09:00
- expected_price_dates：{'JP': '2026-10-30'}
- row_dates：['2026-10-27']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T16:23:05Z / updated=2026-10-29T16:23:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T15:29:38Z / updated=2026-10-29T15:30:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T16:14:29Z / updated=2026-10-28T16:14:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T15:23:37Z / updated=2026-10-28T15:24:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-27T15:30:46Z / updated=2026-10-27T15:31:17Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-30T15:00:25.520949+09:00
- expected_price_dates：{'JP': '2026-10-30'}
- row_dates：['2026-10-30']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T05:59:54Z / updated=2026-10-30T06:00:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-30T02:39:22Z / updated=2026-10-30T02:40:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T05:59:00Z / updated=2026-10-29T05:59:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-29T02:28:50Z / updated=2026-10-29T02:29:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-28T05:54:32Z / updated=2026-10-28T05:55:06Z
