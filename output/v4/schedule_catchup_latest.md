# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/06 19:05 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ✅ 日本株日次騰落：最新扱い
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-06T19:05:52.742384+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-06T12:20:12.704833+09:00
- expected_price_dates：{'US': '2026-10-05'}
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
- expected_price_dates：{'US': '2026-10-05'}
- row_dates：['2026-10-05']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T06:31:01Z / updated=2026-10-06T06:31:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T03:04:59Z / updated=2026-10-06T03:05:43Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T05:52:20Z / updated=2026-10-05T05:52:56Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T02:03:11Z / updated=2026-10-05T02:03:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T05:50:54Z / updated=2026-10-02T05:51:30Z

### 日本株日次騰落

- status_before：ok
- generated_at_before：2026-10-06T18:25:32.241263+09:00
- expected_price_dates：{'JP': '2026-10-06'}
- row_dates：['2026-10-06']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T18:48:06Z / updated=2026-10-05T18:48:33Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T17:21:34Z / updated=2026-10-05T17:22:07Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T15:57:02Z / updated=2026-10-02T15:57:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-02T14:56:25Z / updated=2026-10-02T14:56:52Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-01T16:40:13Z / updated=2026-10-01T16:41:15Z

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
