# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/07 09:31 JST

## 判定サマリー

- ⚠️ 米国株日次騰落：再生成対象 / 生成日が当日ではない：2026-10-06 / US価格日付が想定2026-10-06より古い：['2026-10-05']
- 買い場アラート（米国価格）：判定対象外/判定前（判定前：JST 10:00 以降に確認）
- 日本株日次騰落：判定対象外/判定前（判定前：JST 19:00 以降に確認）
- 買い場アラート（日本価格）：判定対象外/判定前（判定前：JST 19:00 以降に確認）

## 実行結果

- 米国株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_daily_us.py`
  - after：status=partial / generated=2026-10-07T09:31:17.228536+09:00 / dates=['2026-10-05']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-07T09:31:19.169829+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-06T12:20:12.704833+09:00
- expected_price_dates：{'US': '2026-10-06'}
- row_dates：['2026-10-05']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T03:19:45Z / updated=2026-10-06T03:20:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T02:19:36Z / updated=2026-10-06T02:20:13Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-03T02:19:11Z / updated=2026-10-03T02:19:36Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-03T01:12:55Z / updated=2026-10-03T01:13:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T02:34:36Z / updated=2026-10-02T02:35:09Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-06T15:31:38.670418+09:00
- expected_price_dates：{'US': '2026-10-06'}
- row_dates：['2026-10-05']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T06:31:01Z / updated=2026-10-06T06:31:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T03:04:59Z / updated=2026-10-06T03:05:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T05:52:20Z / updated=2026-10-05T05:52:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T02:03:11Z / updated=2026-10-05T02:03:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T05:50:54Z / updated=2026-10-02T05:51:30Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-07T01:14:13.258321+09:00
- expected_price_dates：{'JP': '2026-10-06'}
- row_dates：['2026-10-06']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T16:13:50Z / updated=2026-10-06T16:14:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T15:24:49Z / updated=2026-10-06T15:25:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T18:48:06Z / updated=2026-10-05T18:48:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T17:21:34Z / updated=2026-10-05T17:22:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T15:57:02Z / updated=2026-10-02T15:57:35Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-06T15:31:38.670418+09:00
- expected_price_dates：{'JP': '2026-10-06'}
- row_dates：['2026-10-06']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T06:31:01Z / updated=2026-10-06T06:31:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T03:04:59Z / updated=2026-10-06T03:05:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T05:52:20Z / updated=2026-10-05T05:52:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T02:03:11Z / updated=2026-10-05T02:03:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T05:50:54Z / updated=2026-10-02T05:51:30Z
