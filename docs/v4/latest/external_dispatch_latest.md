# CIS 外部起動確認 R11.2

生成日時：2026-09-25T10:25:23.890095+09:00
mode：auto
source：cron-job.org-morning
status：ok
planned_steps：1

## auto判定

- ⚠️ 米国株日次：再生成対象 / reason=row_dates_lt_expected / dates=['2026-09-23', '2026-09-24'] / expected=2026-09-24
- ✅ 買い場アラート（米国価格）：最新扱い / dates=['2026-09-24']
- 日本株日次：対象時間外
- 買い場アラート（日本価格）：対象時間外

## 実行ステップ

1. ✅ `scripts/cis_v4/cis_daily_us.py` exit=0
   - duration：8.944s

## 役割

このレポートは、GitHub scheduleに頼らず外部スケジューラからworkflow_dispatchされた実行記録です。
CIS本体の表示は、各レポートとHomeの更新日時を優先して確認してください。
