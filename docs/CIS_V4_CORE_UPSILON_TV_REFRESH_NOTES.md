# CIS v4 Core upsilon-tv-refresh notes

upsilonをベースに、TradingView月次確認の手作業を減らす補強版。

## 追加

- `scripts/cis_v4/cis_tv_monthly_refresh.py`
  - activeな米国株監視リストを対象にTradingView候補値を月次取得。
  - 保存済み `data/tv_snapshot.json` と比較。
  - 本番masterは直接書き換えず、候補レポートとMaster Update用コマンドを生成。
  - 取得失敗銘柄は候補から除外し、既存TVスナップショットを守る。
  - GitHub Actionsのネットワーク・TradingView構造変更に備え、失敗時も明示レポートを残す。

- `.github/workflows/cis_v4_tv_monthly_refresh.yml`
  - JST毎月1日09:20に自動実行。
  - TV候補取得、Master Init Template、Monthly Maintenance、Homeを再生成。

- `.github/workflows/cis_v4_apply_tv_monthly_candidate.yml`
  - iPhoneからコピーなしで月次TV候補を反映するWorkflow。
  - `apply_all_success`：取得成功分を全反映し、更新日も刷新。
  - `changed_only`：値が変わった候補だけ反映。
  - Master Update経由で反映するため、TV/BUYZONE/履歴のトランザクション安全性を継承。

## Home補強

- Homeに「TradingView月次自動確認」カードを追加。
- 変更候補や取得失敗がある場合、Home要確認に件数表示。
- TV更新後、Daily US / Weekly / Buy Alertが古い場合はstale表示。

## iPhone導線

- 月次確認レポートに、コピーなし反映の案内を表示。
- 手動運用用に以下も生成。
  - 全成功取得分の改行版txt
  - 全成功取得分の1行セミコロン版txt
  - 変更ありだけの改行版txt
  - 変更ありだけの1行セミコロン版txt
  - 15銘柄単位の分割txt

## 注意

TradingViewからの取得は候補生成であり、取得失敗やTradingView側仕様変更を想定する。本番 `tv_snapshot.json` は自動確認Workflowだけでは変更しない。反映は `CIS v4 Apply TV Monthly Candidate` または `CIS v4 Master Update` 経由で行う。
