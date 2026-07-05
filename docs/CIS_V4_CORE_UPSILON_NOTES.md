# CIS v4 Core upsilon notes

Based on tau. Focus: buy-alert practicality, TradingView snapshot reuse, monthly review workflow, and iPhone stale visibility.

## Changes

- Buy Alert now loads `tv_snapshot.json` and shows TradingView status for US equities.
- Buy Alert now shows daily change and daily percentage.
- Buy Alert sorting now prioritizes buy-zone state, then closest-to-main-buy-zone for waiting symbols.
- CIS Home now marks dependent reports as stale when Master Update or Watchlist Update is newer than the report.
  - Master Update newer than Buy Alert -> Buy Alert stale.
  - Watchlist Update newer than Daily/Weekly/Buy Alert -> those reports stale.
- Monthly Maintenance is scheduled monthly at JST 09:00 on the 1st and rebuilds Master Init Template before the monthly report.
- Master Init Template now also writes one-line semicolon chunk files for iPhone GitHub Actions input.

## TradingView policy

TradingView analyst data is not fetched daily. It is stored as a monthly snapshot in `data/tv_snapshot.json`, reused by Daily US, Weekly Performance, and Buy Alert. Monthly Maintenance automatically identifies stale/missing snapshot rows and regenerates update templates. Actual analyst values are updated through `CIS v4 Master Update`; the report records before/after diffs.
