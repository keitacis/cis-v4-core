# CIS 自動更新取りこぼし確認 R10.4

生成日時：2026/10/08 19:24 JST

## 判定サマリー

- ✅ 米国株日次騰落：最新扱い
- ✅ 買い場アラート（米国価格）：最新扱い
- ⚠️ 日本株日次騰落：再生成対象 / JP価格日付が想定2026-10-08より古い：['2026-10-07']
- ✅ 買い場アラート（日本価格）：最新扱い

## 実行結果

- 日本株日次騰落：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_daily_jp.py`
  - after：status=ok / generated=2026-10-08T19:24:49.918851+09:00 / dates=['2026-10-08']
- CISホーム再生成：exit=0 / `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python scripts/cis_v4/cis_home.py`
  - after：status=ok / generated=2026-10-08T19:24:50.321803+09:00 / dates=[]

## 詳細

### 米国株日次騰落

- status_before：partial
- generated_at_before：2026-10-08T11:56:35.683939+09:00
- expected_price_dates：{'US': '2026-10-07'}
- row_dates：['2026-10-07']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:56:04Z / updated=2026-10-08T02:56:40Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T01:58:45Z / updated=2026-10-08T01:59:14Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T02:41:20Z / updated=2026-10-07T02:41:57Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T01:35:08Z / updated=2026-10-07T01:36:08Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T03:19:45Z / updated=2026-10-06T03:20:17Z

### 買い場アラート（米国価格）

- status_before：partial
- generated_at_before：2026-10-08T15:17:49.041829+09:00
- expected_price_dates：{'US': '2026-10-07'}
- row_dates：['2026-10-07']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:43:28Z / updated=2026-10-08T02:44:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T06:09:52Z / updated=2026-10-07T06:10:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T02:27:04Z / updated=2026-10-07T02:27:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T06:31:01Z / updated=2026-10-06T06:31:44Z

### 日本株日次騰落

- status_before：partial
- generated_at_before：2026-10-08T00:44:17.249348+09:00
- expected_price_dates：{'JP': '2026-10-08'}
- row_dates：['2026-10-07']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=failure / started=2026-10-07T16:52:29Z / updated=2026-10-07T16:53:12Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T15:43:54Z / updated=2026-10-07T15:44:22Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T16:13:50Z / updated=2026-10-06T16:14:17Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T15:24:49Z / updated=2026-10-06T15:25:20Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-05T18:48:06Z / updated=2026-10-05T18:48:33Z

### 買い場アラート（日本価格）

- status_before：partial
- generated_at_before：2026-10-08T15:17:49.041829+09:00
- expected_price_dates：{'JP': '2026-10-08'}
- row_dates：['2026-10-08']
- recent_workflow_runs_available：True
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T06:17:17Z / updated=2026-10-08T06:17:55Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-08T02:43:28Z / updated=2026-10-08T02:44:10Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T06:09:52Z / updated=2026-10-07T06:10:35Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-07T02:27:04Z / updated=2026-10-07T02:27:44Z
  - event=schedule / status=completed / conclusion=success / started=2026-10-06T06:31:01Z / updated=2026-10-06T06:31:44Z
