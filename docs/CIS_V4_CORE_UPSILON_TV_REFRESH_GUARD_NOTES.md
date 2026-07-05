# CIS v4 Core upsilon-tv-refresh-guard notes

この版は `upsilon-tv-refresh-hotfix` の安全補強版です。

## 主修正

- `scripts/cis_v4/cis_apply_tv_monthly_candidate.py` を追加。
- TradingView月次候補の反映前に、以下を1本のPython内で連続検査する。
  - 最新statusの存在
  - statusが `ok` / `partial` であること
  - candidate manifestの存在
  - manifestが `ok` / `partial` であること
  - statusとmanifestの `generated_at_jst` 一致
  - 候補ファイルがmanifestに登録されていること
  - 候補ファイルのsha256一致
  - コマンド件数一致
  - 候補の有効期限が45日以内であること
- 検査に1つでも失敗した場合はMaster Updateを実行しない。
- `.github/workflows/cis_v4_apply_tv_monthly_candidate.yml` は専用Pythonを呼ぶだけに変更し、Workflow step分離による「検査失敗後に反映stepが走る」事故を防止。
- Homeに `TradingView月次候補反映` カードを追加。

## 運用方針

TradingView値は毎回取得しない。月1の `CIS v4 TV Monthly Refresh` で候補を作り、`CIS v4 Apply TV Monthly Candidate` で安全検査後にMaster Update経由で反映する。

## 重要

TradingView月次確認がerrorの場合、古い候補や改ざん候補は反映不可。忙しい時期のiPhoneワンタップ運用でも、候補ファイルの整合性を確認してから反映する。
