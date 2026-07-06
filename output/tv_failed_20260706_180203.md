# CIS TradingView失敗23件 抽出レポート

生成日時：2026/07/06 18:02 JST

## これは何をするレポートか

- Monthly Refreshで取得失敗・手動確認になった銘柄だけを抽出します。
- 診断専用です。tv_snapshot.json、Master、Apply、Daily/Weekly/Buy Alertは変更しません。
- 残件を「追加取得」「対象外」「カバレッジなし」に分けるための材料です。

## ステータス

- 元JSON：`docs/v4/latest/tv_monthly_refresh_latest.json`
- 失敗抽出件数：23件

## 判定候補サマリー

- ETF/対象外候補：1件
- カバレッジなし候補：22件

## HTTPエラーサマリー

- なし

## 不足項目サマリー

- rating：23件
- avg_target_price：23件
- analyst_count：23件

## 取得失敗・手動確認候補

### 1. US:EWY 

- 判定候補：ETF/対象外候補
- 次の見方：ETFやファンド系はTradingViewの個別株アナリスト予想対象外の可能性があります。
- 不足項目：`rating, avg_target_price, analyst_count`
- 試した取引所：`AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 404 / NYSEARCA: forecast HTTPError 404 / BATS: forecast HTTPError 404 / OTC: forecast HTTPError 404
- forecast errors：なし

### 2. US:AEM 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 3. US:ANET 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 4. US:AXTI 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 5. US:BEAM 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 6. US:COHR 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 7. US:CRSP 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 8. US:DDOG 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 9. US:DIS 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 10. US:DKNG 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 11. US:ETN 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 12. US:HSAI 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 13. US:KITT 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`rating, avg_target_price, analyst_count`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 14. US:KVYO 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 15. US:MSTR 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 16. US:OPTX 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`rating, avg_target_price, analyst_count`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 17. US:PL 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 18. US:POET 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 19. US:QCOM 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 20. US:SNOW 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 21. US:V 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 22. US:VRTX 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NASDAQ, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

### 23. US:ZETA 

- 判定候補：カバレッジなし候補
- 次の見方：scannerでrating・人数・平均目標株価が揃いません。実質カバレッジなしの可能性があります。
- 不足項目：`analyst_count, rating, avg_target_price`
- 試した取引所：`NYSE, AMEX, NYSEARCA, BATS, OTC`
- 理由：scanner fields missing analyst_count / scanner fields missing analyst_count / scanner fields missing rating,analyst_count / scanner fields missing avg_target_price,analyst_count / scanner fields missing rating,avg_target_price,analyst_count / AMEX: forecast HTTPError 403 / NYSEARCA: forecast HTTPError 403 / BATS: forecast HTTPError 403 / OTC: forecast HTTPError 403
- forecast errors：なし

