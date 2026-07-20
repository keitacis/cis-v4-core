# CIS 外部起動確認 R11.2

生成日時：2026-07-20T20:25:24.008814+09:00
mode：auto
source：cron-job.org-evening
status：ok
planned_steps：2

## auto判定

- 米国株日次：対象時間外
- 買い場アラート（米国価格）：対象時間外
- ⚠️ 日本株日次：再生成対象 / reason=row_dates_lt_expected / dates=['2026-07-17'] / expected=2026-07-20
- ⚠️ 買い場アラート（日本価格）：再生成対象 / reason=row_dates_lt_expected / dates=['2026-07-17'] / expected=2026-07-20

## 実行ステップ

1. ✅ `scripts/cis_v4/cis_daily_jp.py` exit=0
   - duration：9.755s
2. ✅ `scripts/cis_v4/cis_buy_alert.py` exit=0
   - duration：19.736s

## 役割

このレポートは、GitHub scheduleに頼らず外部スケジューラからworkflow_dispatchされた実行記録です。
CIS本体の表示は、各レポートとHomeの更新日時を優先して確認してください。
