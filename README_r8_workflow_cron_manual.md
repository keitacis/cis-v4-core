# CIS v4 R8 Workflow Cron Manual Files

These three files are the workflow cron part of the R7/R8 fix.
They must be committed by the user through GitHub Desktop because GitHub Actions bot cannot update `.github/workflows/*`.

Replace the existing files in `.github/workflows/` with these files, then commit and push.

Schedules after replacement:

- Daily US: 07:15 JST + 08:45 JST backup
- Daily JP: 17:40 JST + 18:40 JST backup
- Buy Alert: 08:20 JST + 09:20 JST backup
