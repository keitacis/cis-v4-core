# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/09/04 14:45 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ⚠️ 買い場アラート（米国価格）：再生成対象 / US価格日付が想定2026-09-03より古い：['2026-09-02']
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- 買い場アラート（米国価格）：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_buy_alert.py`
  - after：status=partial / generated=2026-09-04T14:45:24.271562+09:00 / dates=['2026-09-03']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-09-04T14:45:25.517599+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-09-04T10:25:39.815911+09:00
- expected_price_dates：{'US': '2026-09-03'}
- row_dates：['2026-09-02', '2026-09-03']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:21:37Z / updated=2026-09-04T01:22:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T00:07:55Z / updated=2026-09-04T00:08:34Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T01:26:46Z / updated=2026-09-03T01:27:18Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T00:18:33Z / updated=2026-09-03T00:19:00Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T01:24:08Z / updated=2026-09-02T01:24:36Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-09-04T13:42:59.771204+09:00
- expected_price_dates：{'US': '2026-09-03'}
- row_dates：['2026-09-02']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:02:16Z / updated=2026-09-04T01:02:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T04:40:12Z / updated=2026-09-03T04:40:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T01:09:32Z / updated=2026-09-03T01:10:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T04:44:26Z / updated=2026-09-02T04:44:57Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-09-03T22:50:38.031946+09:00
- expected_price_dates：{'JP': '2026-09-03'}
- row_dates：['2026-09-03']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T13:50:07Z / updated=2026-09-03T13:50:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T12:58:34Z / updated=2026-09-03T12:59:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T13:50:22Z / updated=2026-09-02T13:50:48Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T12:56:13Z / updated=2026-09-02T12:56:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-01T14:16:13Z / updated=2026-09-01T14:16:41Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-09-04T14:45:24.271562+09:00
- expected_price_dates：{'JP': '2026-09-03'}
- row_dates：['2026-09-04']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T04:42:23Z / updated=2026-09-04T04:43:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-04T01:02:16Z / updated=2026-09-04T01:02:51Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T04:40:12Z / updated=2026-09-03T04:40:41Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-03T01:09:32Z / updated=2026-09-03T01:10:01Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-02T04:44:26Z / updated=2026-09-02T04:44:57Z
