# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/07/08 13:50 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.15/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-07-08T13:50:45.248631+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：ok
- generated_at_before：2026-07-08T13:44:44.199635+09:00
- expected_price_dates：{'US': '2026-07-07'}
- row_dates：['2026-07-07']
- recent_workflow_runs_available：True
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-07T12:49:05Z / updated=2026-07-07T12:49:38Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-07T10:37:02Z / updated=2026-07-07T10:37:29Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-06T12:17:15Z / updated=2026-07-06T12:17:44Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-06T08:00:36Z / updated=2026-07-06T08:02:06Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-05T13:41:54Z / updated=2026-07-05T13:42:21Z

### 買い場アラート（米国価格）

- status_before：ok
- generated_at_before：2026-07-08T13:44:52.729784+09:00
- expected_price_dates：{'US': '2026-07-07'}
- row_dates：['2026-07-07']
- recent_workflow_runs_available：True
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-07T12:51:43Z / updated=2026-07-07T12:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-07T10:39:17Z / updated=2026-07-07T10:39:47Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-06T13:01:52Z / updated=2026-07-06T13:02:32Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-06T12:24:58Z / updated=2026-07-06T12:25:28Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-05T14:16:36Z / updated=2026-07-05T14:17:12Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-07-07T21:51:08.357420+09:00
- expected_price_dates：{'JP': '2026-07-07'}
- row_dates：['2026-07-07']
- recent_workflow_runs_available：True
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-07T12:50:36Z / updated=2026-07-07T12:51:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-06T17:30:31Z / updated=2026-07-06T17:30:57Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-05T14:14:47Z / updated=2026-07-05T14:15:17Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-05T13:43:39Z / updated=2026-07-05T13:44:08Z

### 買い場アラート（日本価格）

- status_before：ok
- generated_at_before：2026-07-08T13:44:52.729784+09:00
- expected_price_dates：{'JP': '2026-07-07'}
- row_dates：['2026-07-08']
- recent_workflow_runs_available：True
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-07T12:51:43Z / updated=2026-07-07T12:52:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-07T10:39:17Z / updated=2026-07-07T10:39:47Z
  - event=schedule / status=completed / conclusion=success / started=2026-07-06T13:01:52Z / updated=2026-07-06T13:02:32Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-06T12:24:58Z / updated=2026-07-06T12:25:28Z
  - event=workflow_dispatch / status=completed / conclusion=success / started=2026-07-05T14:16:36Z / updated=2026-07-05T14:17:12Z
