# CIS TradingView月次自動確認

生成日時：2026/07/06 16:49 JST

## これは何をするレポートか

- 月1でTradingView候補値を自動確認し、保存済み tv_snapshot.json と比較します。
- このレポート自体は tv_snapshot.json を直接書き換えません。
- rating + analyst_count + 平均目標株価が揃った銘柄だけ、反映用コマンドを自動生成します。
- 分布は取れた場合だけ反映コマンドに含めます。取れなくても、rating・人数・平均目標株価が揃っていれば候補化します。

## ステータス

- 米国株監視リスト：48件
- 自動取得成功：25件
- 値の変更候補：25件
- 値は同じ・確認済み：0件
- 取得失敗・手動確認候補：23件

## 取得経路サマリー

- source: TradingView scanner + TradingView forecast page analyst_count：25件
- analyst_count経路: forecast_page_text：25件
- 分布あり：0件
- 分布なし：25件

## iPhone用・反映導線

### 推奨：コピーなしで反映する

- GitHub Actions → `CIS v4 Apply TV Monthly Candidate` → `Run workflow` を押してください。
- このWorkflowは、この月次確認で取得できた銘柄だけをMaster Updateに渡します。
- 取得失敗銘柄は反映対象外なので、既存値は維持されます。

### 手動で貼る場合

iPhoneでは、まず分割版を使うのが安全です。

#### 全成功取得分・iPhone分割1行版

- [tv_monthly_refresh_apply_iphone_part_01_1line.txt](tv_monthly_refresh_apply_iphone_part_01_1line.txt)
- [tv_monthly_refresh_apply_iphone_part_02_1line.txt](tv_monthly_refresh_apply_iphone_part_02_1line.txt)

#### 変更ありだけ・iPhone分割1行版

- [tv_monthly_refresh_changed_only_iphone_part_01_1line.txt](tv_monthly_refresh_changed_only_iphone_part_01_1line.txt)
- [tv_monthly_refresh_changed_only_iphone_part_02_1line.txt](tv_monthly_refresh_changed_only_iphone_part_02_1line.txt)

#### PC向け・全件

- [全成功取得分・1行版](tv_monthly_refresh_apply_commands_iphone_1line.txt)
- [変更ありだけ・1行版](tv_monthly_refresh_changed_only_commands_iphone_1line.txt)
- [全成功取得分・改行版](tv_monthly_refresh_apply_commands.txt)
- [変更ありだけ・改行版](tv_monthly_refresh_changed_only_commands.txt)
- [候補manifest](tv_monthly_refresh_candidate_manifest.json)

## 値の変更候補

### US:AVAV AeroVironment

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 19人 / 241.470588
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.131579 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast/
- 差分：新規取得

### US:AXON Axon Enterprise

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 23人 / 676.882353
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.173913 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-AXON/forecast/
- 差分：新規取得

### US:AUR Aurora Innovation

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 14人 / 11.144545
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.464286 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-AUR/forecast/
- 差分：新規取得

### US:TMDX TransMedics Group

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 11人 / 117.333333
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.318182 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-TMDX/forecast/
- 差分：新規取得

### US:NOW ServiceNow

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 50人 / 140.380952
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.16 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-NOW/forecast/
- 差分：新規取得

### US:RDW Redwire

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 8人 / 15.714286
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.4375 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-RDW/forecast/
- 差分：新規取得

### US:TRMB Trimble

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 16人 / 84.083333
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.15625 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-TRMB/forecast/
- 差分：新規取得

### US:VEEV Veeva Systems

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 29人 / 241.434783
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.431034 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-VEEV/forecast/
- 差分：新規取得

### US:PYPL PayPal

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Buy / 46人 / 47.112903
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.934783 → Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast/
- 差分：新規取得

### US:TEM Tempus AI

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Buy / 20人 / 66.0625
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.55 → Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-TEM/forecast/
- 差分：新規取得

### US:FICO Fair Isaac

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 25人 / 1501.65
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.48 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-FICO/forecast/
- 差分：新規取得

### US:AAOI Applied Optoelectronics

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Buy / 8人 / 172.75
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.5625 → Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-AAOI/forecast/
- 差分：新規取得

### US:OUST Ouster

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 8人 / 47.285714
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.25 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-OUST/forecast/
- 差分：新規取得

### US:APH Amphenol

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 24人 / 184.611111
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.270833 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-APH/forecast/
- 差分：新規取得

### US:ASPI ASP Isotopes

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 3人 / 13.0
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-ASPI/forecast/
- 差分：新規取得

### US:NBIS Nebius Group

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 17人 / 257.785714
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.470588 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-NBIS/forecast/
- 差分：新規取得

### US:ISRG Intuitive Surgical

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 35人 / 573.444444
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.414286 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-ISRG/forecast/
- 差分：新規取得

### US:SPGI S&P Global

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 29人 / 501.235852
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.12069 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-SPGI/forecast/
- 差分：新規取得

### US:MELI MercadoLibre

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 25人 / 2235.409091
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.2 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-MELI/forecast/
- 差分：新規取得

### US:TMO Thermo Fisher Scientific

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 31人 / 595.208333
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.290323 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-TMO/forecast/
- 差分：新規取得

### US:META Meta Platforms

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 69人 / 820.996334
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.130435 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-META/forecast/
- 差分：新規取得

### US:IONQ IonQ

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 14人 / 71.318182
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NYSE
- recommendation_mark(raw)：1.321429 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NYSE-IONQ/forecast/
- 差分：新規取得

### US:RGTI Rigetti Computing

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 13人 / 31.0
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.346154 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-RGTI/forecast/
- 差分：新規取得

### US:SDGR Schrodinger

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Strong Buy / 8人 / 20.875
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.25 → Strong Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-SDGR/forecast/
- 差分：新規取得

### US:RXRX Recursion Pharmaceuticals

- 旧：未設定 / 未設定 / 未設定人 / 未設定
- 新：covered / Buy / 8人 / 6.642857
- 取得経路：TradingView scanner + TradingView forecast page analyst_count / 人数はforecast本文補完 / 分布なし
- 取引所候補：NASDAQ
- recommendation_mark(raw)：1.625 → Buy
- 平均目標株価フィールド：price_target_average
- analyst_count補完URL：https://www.tradingview.com/symbols/NASDAQ-RXRX/forecast/
- 差分：新規取得

## 値は同じ・確認済み

なし

## 取得失敗・手動確認候補

取得失敗銘柄は候補コマンドから除外しています。既存の tv_snapshot.json は守られます。

- US:EWY：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 404 / NYSEARCA: forecast HTTPError 404 / BATS: forecast HTTPError 404 / OTC: forecast HTTPError 404 / 不足:rating,avg_target_price,analyst_count
- US:QCOM：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:HSAI：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:PL：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:V：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:VRTX：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:DIS：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:KVYO：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:DKNG：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:CRSP：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:BEAM：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:ETN：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:MSTR：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:POET：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:KITT：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:AXTI：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:COHR：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:ANET：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:DDOG：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:SNOW：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:OPTX：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:AEM：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
- US:ZETA：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403 / 不足:rating,avg_target_price,analyst_count
