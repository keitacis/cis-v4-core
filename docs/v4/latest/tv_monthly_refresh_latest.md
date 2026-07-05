# CIS TradingView月次自動確認

生成日時：2026/07/05 21:26 JST

## これは何をするレポートか

- 月1でTradingView候補値を自動確認し、保存済み tv_snapshot.json と比較します。
- このレポート自体は tv_snapshot.json を直接書き換えません。
- 取得できた銘柄だけ、反映用コマンドを自動生成します。取得失敗銘柄の既存値は守ります。
- iPhoneでは、問題なさそうなら GitHub Actions の `CIS v4 Apply TV Monthly Candidate` を実行すると、コピー作業なしで候補を反映できます。

## ステータス

- 米国株監視リスト：48件
- 自動取得成功：0件
- 値の変更候補：0件
- 値は同じ・確認済み：0件
- 取得失敗・手動確認候補：48件

## iPhone用・反映導線

反映できる自動取得結果がありません。

## 値の変更候補

変更候補なし

## 値は同じ・確認済み

なし

## 取得失敗・手動確認候補

取得失敗銘柄は候補コマンドから除外しています。既存の tv_snapshot.json は守られます。

- US:AVAV：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:AXON：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:AUR：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:TMDX：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:NOW：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:RDW：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:TRMB：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:VEEV：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:PYPL：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:TEM：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:FICO：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 404 / BATS: forecast fields not found / OTC: HTTPError 404
- US:AAOI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:OUST：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:APH：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:ASPI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:NBIS：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:EWY：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:ISRG：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:SPGI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:MELI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:TMO：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:META：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:IONQ：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:RGTI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:SDGR：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:RXRX：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:QCOM：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:HSAI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:PL：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:V：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:VRTX：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:DIS：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:KVYO：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:DKNG：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:CRSP：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:BEAM：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:ETN：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:MSTR：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:POET：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:KITT：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:AXTI：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:COHR：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:ANET：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:DDOG：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:SNOW：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:OPTX：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:AEM：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
- US:ZETA：required analyst fields not found / required analyst fields not found / required analyst fields not found / NYSEARCA: HTTPError 403 / BATS: HTTPError 403 / OTC: HTTPError 403
