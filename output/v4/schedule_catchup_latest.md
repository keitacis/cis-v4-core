# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/25 17:44 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-25T17:44:07.892429+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-25T10:54:47.753121+09:00
- expected_price_dates：{'US': '2026-09-24'}
- row_dates：['2026-09-24']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T01:54:27Z / updated=2026-09-25T01:54:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T00:34:25Z / updated=2026-09-25T00:34:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T01:38:42Z / updated=2026-09-24T01:39:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T00:31:33Z / updated=2026-09-24T00:32:02Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T01:47:38Z / updated=2026-09-23T01:48:07Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-25T14:05:52.272345+09:00
- expected_price_dates：{'US': '2026-09-24'}
- row_dates：['2026-09-24']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T05:05:15Z / updated=2026-09-25T05:05:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T01:35:39Z / updated=2026-09-25T01:36:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T05:01:44Z / updated=2026-09-24T05:02:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T01:28:16Z / updated=2026-09-24T01:28:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T04:52:40Z / updated=2026-09-23T04:53:12Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-24T23:23:16.779658+09:00
- expected_price_dates：{'JP': '2026-09-25'}
- row_dates：['2026-09-24']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T14:22:50Z / updated=2026-09-24T14:23:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T13:44:29Z / updated=2026-09-24T13:44:53Z
  - event=schedule / status=completed / conclusion=failure / started=2026-09-23T14:24:01Z / updated=2026-09-23T14:24:37Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T13:49:17Z / updated=2026-09-23T13:49:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-22T14:09:30Z / updated=2026-09-22T14:09:59Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-25T14:05:52.272345+09:00
- expected_price_dates：{'JP': '2026-09-25'}
- row_dates：['2026-09-25']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T05:05:15Z / updated=2026-09-25T05:05:58Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-25T01:35:39Z / updated=2026-09-25T01:36:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T05:01:44Z / updated=2026-09-24T05:02:23Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-24T01:28:16Z / updated=2026-09-24T01:28:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-23T04:52:40Z / updated=2026-09-23T04:53:12Z
