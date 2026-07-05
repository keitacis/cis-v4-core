# CIS v4 Core upsilon-tv-refresh-guard-homefix

## 目的

upsilon-tv-refresh-guard の最終UX補強版。

TV月次自動確認で変更候補が出たあと、CIS v4 Apply TV Monthly Candidate で候補を反映しても、CIS Homeの要確認欄に「TV変更候補N件」が残り続ける問題を修正した。

## 修正内容

- `cis_home.py` に `mark_tv_monthly_candidate_applied()` を追加。
- `tv_monthly_refresh_status_latest.json.generated_at_jst` と `apply_tv_monthly_candidate_status_latest.json.candidate_generated_at_jst` が一致し、Apply側が `ok` の場合、その月次確認のTV変更候補は反映済みと判定する。
- 反映済みの変更候補はHomeの要確認から除外する。
- 取得失敗が残っている場合は、変更候補は消し、取得失敗件数だけを要確認に残す。
- Homeカードには「TV変更候補N件は反映済みです」という補足を表示する。
- 最終ZIPから `data/backups` を除外。

## 運用イメージ

1. CIS v4 TV Monthly Refresh が月1で候補生成。
2. Homeに変更候補・取得失敗が表示される。
3. iPhoneから CIS v4 Apply TV Monthly Candidate を実行。
4. 反映成功後、Home上の変更候補警告は消える。
5. 取得失敗がある場合だけ要確認に残る。
