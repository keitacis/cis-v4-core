# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/05 08:53 JST

## 判定サマリー

- 米国株日次騰落：判定対象外/判定前（判定対象外曜日：weekday=0）
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-05T08:53:49.968533+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-03T11:19:31.600109+09:00
- expected_price_dates：{'US': '2026-10-02'}
- row_dates：['2026-10-02']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-03T02:19:11Z / updated=2026-10-03T02:19:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-03T01:12:55Z / updated=2026-10-03T01:13:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T02:34:36Z / updated=2026-10-02T02:35:09Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T01:41:56Z / updated=2026-10-02T01:42:27Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:25:38Z / updated=2026-10-01T02:26:05Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-05T08:25:41.266091+09:00
- expected_price_dates：{'US': '2026-10-02'}
- row_dates：['2026-10-02']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T05:50:54Z / updated=2026-10-02T05:51:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T02:18:29Z / updated=2026-10-02T02:19:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T06:07:35Z / updated=2026-10-01T06:08:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:11:57Z / updated=2026-10-01T02:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-03T00:57:28.765496+09:00
- expected_price_dates：{'JP': '2026-10-02'}
- row_dates：['2026-10-02']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T15:57:02Z / updated=2026-10-02T15:57:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T14:56:25Z / updated=2026-10-02T14:56:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T16:40:13Z / updated=2026-10-01T16:41:15Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T15:37:34Z / updated=2026-10-01T15:38:03Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T16:03:19Z / updated=2026-09-30T16:03:46Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-05T08:25:41.266091+09:00
- expected_price_dates：{'JP': '2026-10-02'}
- row_dates：['2026-10-02']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T05:50:54Z / updated=2026-10-02T05:51:30Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T02:18:29Z / updated=2026-10-02T02:19:11Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T06:07:35Z / updated=2026-10-01T06:08:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T02:11:57Z / updated=2026-10-01T02:12:29Z
  - event=schedule / status=completed / conclusion=success / started=2026-09-30T05:41:48Z / updated=2026-09-30T05:42:29Z
