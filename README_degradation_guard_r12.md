# CIS v4 Degradation Guard R12.3

R12.3 applied.

- Protected stems: `daily_jp`, `daily_us`, `buy_alert`
- Guard condition: incoming report status is `price_stale` and existing latest status is `ok` or `partial`
- Behavior: retain latest Markdown/HTML/JSON, update status to `partial`, and save the rejected stale run as `*_degraded_attempt_latest.*`

This patch intentionally replaces the current `write_report()` implementation by locating the text range from `def write_report(` to `def write_error_report(`. This avoids brittle regex matching against the current compact formatting of `cis_core.py`.
