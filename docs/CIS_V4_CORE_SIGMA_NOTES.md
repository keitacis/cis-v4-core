# CIS v4 Core sigma notes

sigma is based on omega and focuses on iPhone-first watchlist operations.

## Added
- `scripts/cis_v4/cis_watchlist_template.py`
  - Generates an iPhone guide and short txt files for ADD / UPDATE / STOP / RESUME commands.
  - Generates active/inactive list txt files and split STOP/RESUME/UPDATE templates.
- `.github/workflows/cis_v4_watchlist_template.yml`
  - Manual workflow to regenerate the watchlist template page.
- Home card for `監視リスト追加・変更テンプレート`.

## Improved
- `cis_watchlist_update.py`
  - `ADD US TICKER` and `ADD JP 1234` are now valid minimal commands.
  - `UPDATE` command added for name/description/theme changes without changing active state.
  - Watchlist, company master, and watchlist history are replaced transactionally.
- `cis_v4_preflight.yml`
  - Rebuilds CIS Home after Preflight so the Home card reflects the latest result.
- `cis_v4_apply_seed.yml` and `cis_v4_watchlist_update.yml`
  - Rebuild the watchlist template before rebuilding Home.

## Preserved
- psi/omega seed safety, staged validation, Master Update transaction safety, and iPhone Home UX improvements.
