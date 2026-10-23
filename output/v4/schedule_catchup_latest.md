# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/23 14:56 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-23T14:56:33.156744+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-23T10:58:00.574850+09:00
- expected_price_dates：{'US': '2026-10-22'}
- row_dates：['2026-10-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T01:57:26Z / updated=2026-10-23T01:58:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T00:41:51Z / updated=2026-10-23T00:42:26Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T01:51:33Z / updated=2026-10-22T01:52:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T00:41:49Z / updated=2026-10-22T00:42:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T02:02:18Z / updated=2026-10-21T02:02:52Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-23T14:02:32.745266+09:00
- expected_price_dates：{'US': '2026-10-22'}
- row_dates：['2026-10-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T05:01:59Z / updated=2026-10-23T05:02:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T01:35:37Z / updated=2026-10-23T01:36:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T05:01:30Z / updated=2026-10-22T05:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T01:35:08Z / updated=2026-10-22T01:35:47Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T04:59:29Z / updated=2026-10-21T05:00:10Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-10-22T23:38:01.539024+09:00
- expected_price_dates：{'JP': '2026-10-22'}
- row_dates：['2026-10-22']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T14:37:32Z / updated=2026-10-22T14:47:24Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T14:02:51Z / updated=2026-10-22T14:06:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T14:37:44Z / updated=2026-10-21T14:38:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T14:04:40Z / updated=2026-10-21T14:05:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-20T14:27:24Z / updated=2026-10-20T14:27:54Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-23T14:02:32.745266+09:00
- expected_price_dates：{'JP': '2026-10-22'}
- row_dates：['2026-10-23']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T05:01:59Z / updated=2026-10-23T05:02:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-23T01:35:37Z / updated=2026-10-23T01:36:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T05:01:30Z / updated=2026-10-22T05:02:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-22T01:35:08Z / updated=2026-10-22T01:35:47Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-21T04:59:29Z / updated=2026-10-21T05:00:10Z
