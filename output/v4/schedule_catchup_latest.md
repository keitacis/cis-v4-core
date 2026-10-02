# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/02 09:37 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-02T09:37:10.506445+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-02T07:25:30.458366+09:00
- expected_price_dates：{'US': '2026-10-01'}
- row_dates：['2026-10-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:25:38Z / updated=2026-10-01T02:26:05Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T01:18:28Z / updated=2026-10-01T01:18:59Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:23:15Z / updated=2026-09-30T02:23:45Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T01:18:44Z / updated=2026-09-30T01:19:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T02:44:04Z / updated=2026-09-29T02:44:33Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-02T08:25:39.154323+09:00
- expected_price_dates：{'US': '2026-10-01'}
- row_dates：['2026-10-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T06:07:35Z / updated=2026-10-01T06:08:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:11:57Z / updated=2026-10-01T02:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-02T01:41:10.857294+09:00
- expected_price_dates：{'JP': '2026-10-01'}
- row_dates：['2026-10-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T16:40:13Z / updated=2026-10-01T16:41:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T15:37:34Z / updated=2026-10-01T15:38:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T16:03:19Z / updated=2026-09-30T16:03:46Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T15:13:50Z / updated=2026-09-30T15:14:19Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T16:05:47Z / updated=2026-09-29T16:06:12Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-02T08:25:39.154323+09:00
- expected_price_dates：{'JP': '2026-10-01'}
- row_dates：['2026-10-01']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T06:07:35Z / updated=2026-10-01T06:08:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:11:57Z / updated=2026-10-01T02:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T02:09:57Z / updated=2026-09-30T02:10:25Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-29T05:51:38Z / updated=2026-09-29T05:52:20Z
