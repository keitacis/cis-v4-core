# CIS TradingView Probe v2 safe

生成日時：2026/07/06 01:33 JST

## 目的

TradingView取得失敗の原因を、GitHub Actions上で非破壊診断します。`tv_snapshot.json` は変更しません。

## ステータス

- status: ok
- generated_at_jst: 2026-07-06T01:33:57.283689+09:00
- symbols_tested: ['AVAV', 'PYPL', 'META', 'EWY', 'AEM', 'NOW', 'QCOM', 'ZETA']
- best_tv_symbols: ['NASDAQ:AVAV', 'NASDAQ:PYPL', 'NASDAQ:META', 'AMEX:EWY', 'NYSE:AEM', 'NYSE:NOW', 'NASDAQ:QCOM', 'NYSE:ZETA']
- baseline_success_symbols: 8
- candidate_fields_tested: 19
- valid_candidate_fields_union: ['analyst_rating', 'analyst_rating_count', 'analyst_rating_strong_buy', 'analyst_rating_buy', 'analyst_rating_hold', 'analyst_rating_neutral', 'analyst_rating_sell', 'analyst_rating_strong_sell', 'number_of_analysts', 'target_price_average', 'target_price_high', 'target_price_low', 'target_price_median', 'price_target_mean', 'price_target_average', 'price_target_high', 'price_target_low', 'recommendation_mark', 'recommendation_mean']
- non_null_fields_union: ['name', 'description', 'close', 'currency', 'price_target_average', 'price_target_high', 'price_target_low', 'recommendation_mark']
- forecast_rows: 20
- note: Diagnostic only. tv_snapshot.json is not modified.

## Baseline scanner access

### AVAV
- best: NASDAQ:AVAV
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "AVAV",
  "description": "AeroVironment, Inc.",
  "close": 190.89,
  "currency": "USD"
}
```
### PYPL
- best: NASDAQ:PYPL
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "PYPL",
  "description": "PayPal Holdings, Inc.",
  "close": 45.47,
  "currency": "USD"
}
```
### META
- best: NASDAQ:META
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "META",
  "description": "Meta Platforms Inc Class A",
  "close": 582.9,
  "currency": "USD"
}
```
### EWY
- best: AMEX:EWY
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "EWY",
  "description": "iShares MSCI South Korea ETF",
  "close": 180.14,
  "currency": "USD"
}
```
### AEM
- best: NYSE:AEM
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "AEM",
  "description": "Agnico Eagle Mines Limited",
  "close": 153.86,
  "currency": "USD"
}
```
### NOW
- best: NYSE:NOW
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "NOW",
  "description": "ServiceNow, Inc.",
  "close": 106.32,
  "currency": "USD"
}
```
### QCOM
- best: NASDAQ:QCOM
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "QCOM",
  "description": "QUALCOMM Incorporated",
  "close": 176.25,
  "currency": "USD"
}
```
### ZETA
- best: NYSE:ZETA
- HTTP: 200
- fields: name, description, close, currency
```json
{
  "name": "ZETA",
  "description": "Zeta Global Holdings Corp. Class A",
  "close": 20.7,
  "currency": "USD"
}
```

## Candidate field probe

### NASDAQ:AVAV
- valid fields: analyst_rating, analyst_rating_count, analyst_rating_strong_buy, analyst_rating_buy, analyst_rating_hold, analyst_rating_neutral, analyst_rating_sell, analyst_rating_strong_sell, number_of_analysts, target_price_average, target_price_high, target_price_low, target_price_median, price_target_mean, price_target_average, price_target_high, price_target_low, recommendation_mark, recommendation_mean
- combined HTTP: 200 / なし
```json
{
  "name": "AVAV",
  "description": "AeroVironment, Inc.",
  "close": 190.89,
  "currency": "USD",
  "price_target_average": 241.470588,
  "price_target_high": 361,
  "price_target_low": 166,
  "recommendation_mark": 1.131579
}
```
### NASDAQ:PYPL
- valid fields: analyst_rating, analyst_rating_count, analyst_rating_strong_buy, analyst_rating_buy, analyst_rating_hold, analyst_rating_neutral, analyst_rating_sell, analyst_rating_strong_sell, number_of_analysts, target_price_average, target_price_high, target_price_low, target_price_median, price_target_mean, price_target_average, price_target_high, price_target_low, recommendation_mark, recommendation_mean
- combined HTTP: 200 / なし
```json
{
  "name": "PYPL",
  "description": "PayPal Holdings, Inc.",
  "close": 45.47,
  "currency": "USD",
  "price_target_average": 47.112903,
  "price_target_high": 63,
  "price_target_low": 32,
  "recommendation_mark": 1.934783
}
```
### NASDAQ:META
- valid fields: analyst_rating, analyst_rating_count, analyst_rating_strong_buy, analyst_rating_buy, analyst_rating_hold, analyst_rating_neutral, analyst_rating_sell, analyst_rating_strong_sell, number_of_analysts, target_price_average, target_price_high, target_price_low, target_price_median, price_target_mean, price_target_average, price_target_high, price_target_low, recommendation_mark, recommendation_mean
- combined HTTP: 200 / なし
```json
{
  "name": "META",
  "description": "Meta Platforms Inc Class A",
  "close": 582.9,
  "currency": "USD",
  "price_target_average": 820.996334,
  "price_target_high": 1015,
  "price_target_low": 697.467353,
  "recommendation_mark": 1.130435
}
```
### AMEX:EWY
- valid fields: analyst_rating, analyst_rating_count, analyst_rating_strong_buy, analyst_rating_buy, analyst_rating_hold, analyst_rating_neutral, analyst_rating_sell, analyst_rating_strong_sell, number_of_analysts, target_price_average, target_price_high, target_price_low, target_price_median, price_target_mean, price_target_average, price_target_high, price_target_low, recommendation_mark, recommendation_mean
- combined HTTP: 200 / なし
```json
{
  "name": "EWY",
  "description": "iShares MSCI South Korea ETF",
  "close": 180.14,
  "currency": "USD"
}
```
### NYSE:AEM
- valid fields: analyst_rating, analyst_rating_count, analyst_rating_strong_buy, analyst_rating_buy, analyst_rating_hold, analyst_rating_neutral, analyst_rating_sell, analyst_rating_strong_sell, number_of_analysts, target_price_average, target_price_high, target_price_low, target_price_median, price_target_mean, price_target_average, price_target_high, price_target_low, recommendation_mark, recommendation_mean
- combined HTTP: 200 / なし
```json
{
  "name": "AEM",
  "description": "Agnico Eagle Mines Limited",
  "close": 153.86,
  "currency": "USD",
  "price_target_average": 250.6115209984,
  "price_target_high": 306.26554201839997,
  "price_target_low": 169.91705476159999,
  "recommendation_mark": 1.326087
}
```

## Forecast page probe

### https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast/
- HTTP: 200
- Error: なし
- Title: AVAV Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 269291
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="Sx0hRMkRFXqfnrjb4+BDXw==">window.initData = {};</script><title>AVAV Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 19 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-AVAV/financials-income-statement/\">AeroVironment, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy AeroVironment, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AVAV shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&#
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> window.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See AeroVironment, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/AVAV/forecast/
- HTTP: 200
- Error: なし
- Title: AVAV Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 269291
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="Sx0hRMkRFXqfnrjb4+BDXw==">window.initData = {};</script><title>AVAV Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 19 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-AVAV/financials-income-statement/\">AeroVironment, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy AeroVironment, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AVAV shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&#
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> window.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See AeroVironment, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: AVAV Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 269291
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="Sx0hRMkRFXqfnrjb4+BDXw==">window.initData = {};</script><title>AVAV Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 19 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-AVAV/financials-income-statement/\">AeroVironment, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy AeroVironment, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AVAV shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&#
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> window.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See AeroVironment, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/AVAV/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: AVAV Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 269291
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="Sx0hRMkRFXqfnrjb4+BDXw==">window.initData = {};</script><title>AVAV Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 19 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-AVAV/financials-income-statement/\">AeroVironment, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy AeroVironment, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AVAV shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&#
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> window.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See AeroVironment, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-AVAV/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast/
- HTTP: 200
- Error: なし
- Title: PYPL Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 282174
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="LISU1k7ozD0VVglJgHWXEA==">window.initData = {};</script><title>PYPL Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 46 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> a href=\"/symbols/NASDAQ-PYPL/financials-income-statement/\">PayPal Holdings, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy PayPal Holdings, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, PYPL shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> ndow.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See PayPal Holdings, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/PYPL/forecast/
- HTTP: 200
- Error: なし
- Title: PYPL Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 282174
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="LISU1k7ozD0VVglJgHWXEA==">window.initData = {};</script><title>PYPL Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 46 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> a href=\"/symbols/NASDAQ-PYPL/financials-income-statement/\">PayPal Holdings, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy PayPal Holdings, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, PYPL shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> ndow.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See PayPal Holdings, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: PYPL Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 282174
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="LISU1k7ozD0VVglJgHWXEA==">window.initData = {};</script><title>PYPL Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 46 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> a href=\"/symbols/NASDAQ-PYPL/financials-income-statement/\">PayPal Holdings, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy PayPal Holdings, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, PYPL shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> ndow.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See PayPal Holdings, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/PYPL/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: PYPL Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 282174
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="LISU1k7ozD0VVglJgHWXEA==">window.initData = {};</script><title>PYPL Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 46 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> a href=\"/symbols/NASDAQ-PYPL/financials-income-statement/\">PayPal Holdings, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy PayPal Holdings, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, PYPL shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> ndow.PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See PayPal Holdings, Inc. stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-PYPL/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NASDAQ-META/forecast/
- HTTP: 200
- Error: なし
- Title: META Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 285364
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="tR5jPJu0UePsGauZduL5fg==">window.initData = {};</script><title>META Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 69 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-META/financials-income-statement/\">Meta Platforms, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy Meta Platforms, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, META shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Meta Platforms Inc Class A stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-META/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/META/forecast/
- HTTP: 200
- Error: なし
- Title: META Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 285364
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="tR5jPJu0UePsGauZduL5fg==">window.initData = {};</script><title>META Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 69 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-META/financials-income-statement/\">Meta Platforms, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy Meta Platforms, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, META shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Meta Platforms Inc Class A stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-META/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NASDAQ-META/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: META Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 285364
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="tR5jPJu0UePsGauZduL5fg==">window.initData = {};</script><title>META Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 69 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-META/financials-income-statement/\">Meta Platforms, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy Meta Platforms, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, META shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Meta Platforms Inc Class A stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-META/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/META/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: META Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 285364
> ce-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="tR5jPJu0UePsGauZduL5fg==">window.initData = {};</script><title>META Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 69 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> <a href=\"/symbols/NASDAQ-META/financials-income-statement/\">Meta Platforms, Inc. financial statements</a>." } }, { "@type": "Question", "name": "How to buy Meta Platforms, Inc. stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, META shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a broker&
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Meta Platforms Inc Class A stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/NASDAQ-META/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico">
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/AMEX-EWY/forecast/
- HTTP: 404
- Error: HTTPError 404
- Title: Page not found — TradingView
- Length: 1200
### https://www.tradingview.com/symbols/EWY/forecast/
- HTTP: 404
- Error: HTTPError 404
- Title: Page not found — TradingView
- Length: 1200
### https://www.tradingview.com/symbols/AMEX-EWY/forecast-price-target/
- HTTP: 404
- Error: HTTPError 404
- Title: Page not found — TradingView
- Length: 1200
### https://www.tradingview.com/symbols/EWY/forecast-price-target/
- HTTP: 404
- Error: HTTPError 404
- Title: Page not found — TradingView
- Length: 1200
### https://www.tradingview.com/symbols/NYSE-AEM/forecast/
- HTTP: 200
- Error: なし
- Title: AEM Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 275261
> ice-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="wcZW9EvcVxlRu0YLu27gZw==">window.initData = {};</script><title>AEM Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 23 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> href=\"/symbols/NYSE-AEM/financials-income-statement/\">Agnico Eagle Mines Limited financial statements</a>." } }, { "@type": "Question", "name": "How to buy Agnico Eagle Mines Limited stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AEM shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a br
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Agnico Eagle Mines Limited stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/TSX-AEM/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico"> <me
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/AEM/forecast/
- HTTP: 200
- Error: なし
- Title: AEM Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 275261
> ice-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="wcZW9EvcVxlRu0YLu27gZw==">window.initData = {};</script><title>AEM Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 23 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> href=\"/symbols/NYSE-AEM/financials-income-statement/\">Agnico Eagle Mines Limited financial statements</a>." } }, { "@type": "Question", "name": "How to buy Agnico Eagle Mines Limited stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AEM shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a br
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Agnico Eagle Mines Limited stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/TSX-AEM/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico"> <me
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/NYSE-AEM/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: AEM Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 275261
> ice-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="wcZW9EvcVxlRu0YLu27gZw==">window.initData = {};</script><title>AEM Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 23 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> href=\"/symbols/NYSE-AEM/financials-income-statement/\">Agnico Eagle Mines Limited financial statements</a>." } }, { "@type": "Question", "name": "How to buy Agnico Eagle Mines Limited stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AEM shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a br
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Agnico Eagle Mines Limited stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/TSX-AEM/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico"> <me
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
### https://www.tradingview.com/symbols/AEM/forecast-price-target/
- HTTP: 200
- Error: なし
- Title: AEM Forecast — Price Target — Prediction for 2027 — TradingView
- Length: 275261
> ice-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"> <script nonce="wcZW9EvcVxlRu0YLu27gZw==">window.initData = {};</script><title>AEM Forecast — Price Target — Prediction for 2027 — TradingView</title> <!-- { block promo_footer_css_bundle } --> <!-- { render_css_bundle('promo_footer') } --> <link crossorigin="anonymous" href="https://static.tradingview.com/static/bundles/16110.2f7475fb52f92b7f0159.css" rel="stylesheet" type="text/css"/> <!-- { endblock promo_footer_cs
> oC1LJH7"><div class="wrap-moC1LJH7"></div></div></div><div class="container-J7p_MdH4 analysisRating-PiYrtFUm"><div class="sectionHeader-gwBNukaA"><h3 class="sectionTitle-gwBNukaA">Analyst rating</h3><div><div class="sectionSubtitle-gwBNukaA">Based on 23 analysts giving stock ratings in the past 3 months.</div></div></div><div class="emptyBlock-J7p_MdH4"></div></div></div><div class="financialsSection-PiYrtFUm"><div class="content-fVoYyyYN"><div class="heading-GQWAi9kx heading-fVoYyyYN"><h3 class="title-GQWAi9
> udy all the available data, e.g. company's financials, related news, and its technical analysis.","filter":null},{"text":"So {symbol_instrument_name} technincal analysis shows the strong buy rating today,","filter":{"operator":"and","operands":[{"expression":{"left":{"name":"recommend_signal","source":"django_seo","value":null,"origin_field_name":null,"symbol":null},"operation":"equals","right":"strong-buy"}}]}},{"text":"So {symbol_instrument_name} technincal analysis shows the buy rating today,","filter"
> href=\"/symbols/NYSE-AEM/financials-income-statement/\">Agnico Eagle Mines Limited financial statements</a>." } }, { "@type": "Question", "name": "How to buy Agnico Eagle Mines Limited stocks?", "acceptedAnswer": { "@type": "Answer", "text": "Like other stocks, AEM shares are traded on stock exchanges, e.g. Nasdaq, Nyse, Euronext, and the easiest way to buy them is through an online stock broker. To do this, you need to open an account and follow a br
> n(e){e[e.Info=0]="Info",e[e.Normal=1]="Normal",e[e.Debug=2]="Debug",e[e.Error=3]="Error"}(k||(k={}));const b="undefined"!=typeof window&&Number(window.TELEMETRY_WS_ERROR_LOGS_THRESHOLD)||0;var C;!function(e){e[e.PingInterval=1e4]="PingInterval",e[e.MaxPingsCount=10]="MaxPingsCount",e[e.MaxRedirects=20]="MaxRedirects",e[e.MaxReconnects=20]="MaxReconnects"}(C||(C={}));class T{constructor(e,t={}){this._queueStack=[],this._logsQueue=[],this._telemetryObjectsQueue=[],this._reconnectCount=0,this._redirect
> ix-automatico":1.0,"braintree_transaction_source":1.0,"vertex-tax":1.0,"vertex-tax-fix":1.0,"receipt_in_emails":1.0,"adwords-analytics":1.0,"cm360-analytics":1.0,"disable_mobile_upsell_ios":1.0,"disable_mobile_upsell_android":1.0,"required_agreement_for_rt":1.0,"check_market_data_limits":1.0,"force_to_complete_data":1.0,"force_to_upgrade_to_expert":1.0,"send_tradevan_invoice":1.0,"show_pepe_animation":1.0,"send_next_payment_info_receipt":1.0,"screener-alerts-read-only":1.0,"screener_bond_restriction
> PINE_URL || "https://pine-facade.tradingview.com/pine-facade";</script> <meta name="description" content="See Agnico Eagle Mines Limited stock price prediction for 1 year made by analysts and compare it to price changes over time to develop a better trading strategy." /> <link rel="canonical" href="https://www.tradingview.com/symbols/TSX-AEM/forecast-price-target/" /> <meta name="robots" content="index, follow" /> <link rel="icon" href="https://static.tradingview.com/static/images/favicon.ico"> <me
> ons":1.0,"spark_category_translations":1.0,"spark_tags_translations":1.0,"pro_plan_initial_refunds_disabled":1.0,"previous_monoproduct_purchases_refunds_enabled":1.0,"enable_ideas_recommendations":1.0,"enable_ideas_recommendations_feed":1.0,"fail_on_duplicate_payment_methods_for_trial":1.0,"ethoca_alert_notification_webhook":1.0,"hide_suspicious_users_ideas":1.0,"disable_publish_strategy_range_based_chart":1.0,"restrict_simultaneous_requests":1.0,"login_from_new_device_email":1.0,"ssr_worker_nowait":1.0,"brok
