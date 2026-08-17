# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/08/17 12:57 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-08-17T12:57:18.814068+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-08-15T08:58:58.813352+09:00
- expected_price_dates：{'US': '2026-08-14'}
- row_dates：['2026-08-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T23:58:32Z / updated=2026-08-14T23:59:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T22:42:03Z / updated=2026-08-14T22:42:31Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T00:42:44Z / updated=2026-08-14T00:43:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T23:04:14Z / updated=2026-08-13T23:04:49Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T00:43:22Z / updated=2026-08-13T00:43:59Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-08-17T10:57:53.927276+09:00
- expected_price_dates：{'US': '2026-08-14'}
- row_dates：['2026-08-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-17T01:57:28Z / updated=2026-08-17T01:57:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-16T23:36:36Z / updated=2026-08-16T23:37:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T03:01:55Z / updated=2026-08-14T03:02:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T00:01:00Z / updated=2026-08-14T00:01:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T03:02:29Z / updated=2026-08-13T03:03:02Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-08-14T19:36:10.760015+09:00
- expected_price_dates：{'JP': '2026-08-14'}
- row_dates：['2026-08-14']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T10:35:50Z / updated=2026-08-14T10:36:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T09:38:46Z / updated=2026-08-14T09:39:16Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T10:40:18Z / updated=2026-08-13T10:40:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T09:43:29Z / updated=2026-08-13T09:44:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-12T10:39:07Z / updated=2026-08-12T10:39:42Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-08-17T10:57:53.927276+09:00
- expected_price_dates：{'JP': '2026-08-14'}
- row_dates：['2026-08-17']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-08-17T01:57:28Z / updated=2026-08-17T01:57:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-16T23:36:36Z / updated=2026-08-16T23:37:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T03:01:55Z / updated=2026-08-14T03:02:39Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-14T00:01:00Z / updated=2026-08-14T00:01:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-08-13T03:02:29Z / updated=2026-08-13T03:03:02Z
