# CIS v4 Price Freshness + Buy Alert UX Patch R8 Core

R8 Core is a safe split from R7 after GitHub Actions rejected workflow-file updates.

This workflow applies only files that GitHub Actions can commit with normal `contents: write` permission:

- scripts/cis_v4/cis_core.py
- scripts/cis_v4/cis_home.py
- scripts/cis_v4/cis_daily_us.py
- scripts/cis_v4/cis_daily_jp.py
- scripts/cis_v4/cis_buy_alert.py
- scripts/cis_v4/cis_weekly_performance.py
- data/cis_settings.json

It intentionally does **not** modify `.github/workflows/*`.
Workflow cron changes must be committed separately by the user through GitHub Desktop.

Use this instead of R7 for the automated patch workflow.
