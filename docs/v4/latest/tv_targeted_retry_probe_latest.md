# CIS TradingView Targeted Retry Probe

生成日時: 2026-07-06T18:33:47.536889+09:00

## これは何をするレポートか

- Monthly Refreshで失敗した銘柄のうち、大型・中型など取りこぼしが疑われる銘柄をTradingViewだけで再診断します。
- このレポートは診断専用です。tv_snapshot.json、Master、Apply、Daily、Weekly、Buy Alert、Homeは変更しません。

## ステータス

- target_mode: priority_failed
- 元JSON失敗件数: 23
- 再診断対象: 16

## 分類サマリー

- 追加取得可能候補: 9件
- 部分データあり: 7件

## 銘柄別

### 1. DIS Walt Disney

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.21875
- price_target_average: 130.444444
- number_of_analysts: None
- forecast analyst count matches: [27, 32]
- forecast title: DIS Forecast — Price Target — Prediction for 2027 — TradingView

### 2. V Visa

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.158537
- price_target_average: 401.794118
- number_of_analysts: None
- forecast analyst count matches: [34, 41]
- forecast title: V Forecast — Price Target — Prediction for 2027 — TradingView

### 3. VRTX Vertex Pharmaceuticals

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NASDAQ / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.263889
- price_target_average: 553.642857
- number_of_analysts: None
- forecast analyst count matches: [28, 36]
- forecast title: VRTX Forecast — Price Target — Prediction for 2027 — TradingView

### 4. ANET Arista Networks

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.0625
- price_target_average: 190.295162
- number_of_analysts: None
- forecast analyst count matches: [25, 32]
- forecast title: ANET Forecast — Price Target — Prediction for 2027 — TradingView

### 5. DDOG Datadog

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NASDAQ / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.2
- price_target_average: 244.774139
- number_of_analysts: None
- forecast analyst count matches: [44, 50]
- forecast title: DDOG Forecast — Price Target — Prediction for 2027 — TradingView

### 6. SNOW Snowflake

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.211538
- price_target_average: 298.159091
- number_of_analysts: None
- forecast analyst count matches: [44, 52]
- forecast title: SNOW Forecast — Price Target — Prediction for 2027 — TradingView

### 7. QCOM Qualcomm

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NASDAQ / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.7875
- price_target_average: 224.433333
- number_of_analysts: None
- forecast analyst count matches: [30, 40]
- forecast title: QCOM Forecast — Price Target — Prediction for 2027 — TradingView

### 8. ETN Eaton

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.303571
- price_target_average: 469.409091
- number_of_analysts: None
- forecast analyst count matches: [22, 28]
- forecast title: ETN Forecast — Price Target — Prediction for 2027 — TradingView

### 9. AEM Agnico Eagle Mines

- 判定: 追加取得可能候補
- 推奨アクション: Monthly Refresh v3で取り込み候補。v2で落ちた原因を確認してから本体修正。
- best_exchange: NYSE / score: 17
- scanner confirmed HTTP: 200
- forecast HTTP: 200
- recommendation_mark: 1.295455
- price_target_average: 250.21235997539998
- number_of_analysts: None
- forecast analyst count matches: [19, 23]
- forecast title: AEM Forecast — Price Target — Prediction for 2027 — TradingView

### 10. COHR Coherent

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NYSE / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.326923
- price_target_average: 390.998124
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 11. CRSP CRISPR Therapeutics

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NASDAQ / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.442308
- price_target_average: 81.095238
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 12. DKNG DraftKings

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NASDAQ / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.280488
- price_target_average: 34.163889
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 13. BEAM Beam Therapeutics

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NASDAQ / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.147059
- price_target_average: 49.866667
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 14. MSTR MicroStrategy

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NASDAQ / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.157895
- price_target_average: 309.866667
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 15. ZETA Zeta Global

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NYSE / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.125
- price_target_average: 28.678571
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again

### 16. PL Planet Labs

- 判定: 部分データあり
- 推奨アクション: 片方だけ取れている。no_coverage固定は禁止。v3で部分取得扱いを検討。
- best_exchange: NYSE / score: 13
- scanner confirmed HTTP: 200
- forecast HTTP: 403
- recommendation_mark: 1.454545
- price_target_average: 41.1
- number_of_analysts: None
- forecast analyst count matches: []
- forecast title: None
- forecast error: HTTPError 403: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Request blocked.
We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again
