# CIS v4 TV Monthly No Coverage Patch R9

## 目的

KITT / OPTX を `no_coverage` 登録したあとも、TradingView月次自動確認で「TV取得失敗2件」として残る問題を修正する。

## 原因

Daily / Buy Alert / Weekly 側では `no_coverage` が反映されているが、`scripts/cis_v4/cis_tv_monthly_refresh.py` が、保存済みの `no_coverage` / `not_applicable` を月次取得対象から除外していなかった。
そのため KITT / OPTX を引き続きTradingView取得失敗として数えていた。

## 修正内容

- `data/tv_snapshot.json` で `no_coverage` または `not_applicable` 登録済みの米国株は、TV Monthly Refreshでは再取得しない。
- それらを `failed` に入れず、`unchanged` 扱いにする。
- 月次レポートの方針文に「保存済み対象外は月次取得失敗に数えない」を追加する。
- `.github/workflows/*` は書き換えない。R7のようなworkflow権限エラーを避ける。

## 投入後の確認手順

1. `CIS v4 TV Monthly No Coverage Patch R9` を実行する。
2. 緑成功を確認する。
3. `CIS v4 TV Monthly Refresh` を実行する。
4. 緑成功を確認する。
5. `CIS v4 Home` を実行する。
6. CISホームで「TradingView月次自動確認：TV取得失敗2件」が消えたか確認する。

## 触らないもの

- KITT / OPTX は監視リストから削除しない。
- Daily US / Daily JP / Buy Alert / Weekly は再実行不要。
- Apply TV Monthly Candidate は実行しない。
- R7 / R8 Core は再実行しない。
