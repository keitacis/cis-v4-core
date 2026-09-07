# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/07 14:57 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-07T14:57:48.344723+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-05T10:24:54.833848+09:00
- expected_price_dates：{'US': '2026-09-04'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-05T01:24:27Z / updated=2026-09-05T01:24:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-05T00:08:05Z / updated=2026-09-05T00:08:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:21:37Z / updated=2026-09-04T01:22:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T00:07:55Z / updated=2026-09-04T00:08:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T01:26:46Z / updated=2026-09-03T01:27:18Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-07T13:53:48.484923+09:00
- expected_price_dates：{'US': '2026-09-04'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T01:04:28Z / updated=2026-09-07T01:04:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:02:16Z / updated=2026-09-04T01:02:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T04:40:12Z / updated=2026-09-03T04:40:41Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-04T22:44:32.601751+09:00
- expected_price_dates：{'JP': '2026-09-04'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T13:44:05Z / updated=2026-09-04T13:44:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T12:53:38Z / updated=2026-09-04T12:54:06Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T13:50:07Z / updated=2026-09-03T13:50:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T12:58:34Z / updated=2026-09-03T12:59:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T13:50:22Z / updated=2026-09-02T13:50:48Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-07T13:53:48.484923+09:00
- expected_price_dates：{'JP': '2026-09-04'}
- row_dates：['2026-09-07']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T04:53:21Z / updated=2026-09-07T04:53:53Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-07T01:04:28Z / updated=2026-09-07T01:04:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:02:16Z / updated=2026-09-04T01:02:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T04:40:12Z / updated=2026-09-03T04:40:41Z
