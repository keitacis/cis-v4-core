# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/15 17:11 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-15T17:11:23.287329+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-15T10:51:08.694211+09:00
- expected_price_dates：{'US': '2026-10-14'}
- row_dates：['2026-10-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T01:50:38Z / updated=2026-10-15T01:51:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T00:33:07Z / updated=2026-10-15T00:33:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T02:09:23Z / updated=2026-10-14T02:10:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T01:14:52Z / updated=2026-10-14T01:15:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T03:52:53Z / updated=2026-10-13T03:53:28Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-15T13:51:46.315187+09:00
- expected_price_dates：{'US': '2026-10-14'}
- row_dates：['2026-10-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T04:51:11Z / updated=2026-10-15T04:51:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T01:32:05Z / updated=2026-10-15T01:32:42Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T05:02:22Z / updated=2026-10-14T05:03:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T01:57:31Z / updated=2026-10-14T01:58:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T06:52:59Z / updated=2026-10-13T06:53:34Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-10-14T23:38:45.753267+09:00
- expected_price_dates：{'JP': '2026-10-15'}
- row_dates：['2026-10-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T14:38:22Z / updated=2026-10-14T14:38:50Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T13:58:52Z / updated=2026-10-14T13:59:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T17:06:11Z / updated=2026-10-13T17:06:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T16:22:26Z / updated=2026-10-13T16:23:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-12T19:16:38Z / updated=2026-10-12T19:17:11Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-15T13:51:46.315187+09:00
- expected_price_dates：{'JP': '2026-10-15'}
- row_dates：['2026-10-15']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T04:51:11Z / updated=2026-10-15T04:51:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-15T01:32:05Z / updated=2026-10-15T01:32:42Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T05:02:22Z / updated=2026-10-14T05:03:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-14T01:57:31Z / updated=2026-10-14T01:58:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-13T06:52:59Z / updated=2026-10-13T06:53:34Z
