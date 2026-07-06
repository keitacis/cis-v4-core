# CIS 初期マスター投入テンプレート

生成日時：2026/07/06 21:02 JST

## 目的

このページは、買い場基準とTradingViewスナップショットの初期投入漏れを防ぐための確認用です。
この処理はマスターを更新しません。更新するには、下のコマンドを `CIS v4 Master Update` に貼ります。

## サマリー

- active銘柄：73
- 米国株active銘柄：48
- 買い場基準未設定：0
- 買い場基準不正：0
- 旧buy-zone CSVから変換候補あり：0
- TradingView未設定/要区分入力：23

## iPhone用・分割コピー

長すぎる貼り付け事故を避けるため、10〜15銘柄単位の分割txtを先に出します。iPhoneでは基本こちらを1つずつ開いて使います。

### TradingView 分割

月1回の確認用です。毎日自動取得するのではなく、ここで更新したスナップショットを各レポートで再利用します。

- 改行 part 01: [開く](master_init_tv_blank_part_01.txt) / 1行版: [開く](master_init_tv_blank_semicolon_part_01.txt)
- 改行 part 02: [開く](master_init_tv_blank_part_02.txt) / 1行版: [開く](master_init_tv_blank_semicolon_part_02.txt)

## PC向け・全件コピー

PCや長文貼り付けに慣れている場合はこちらを使えます。iPhoneでは分割txtの方が安全です。

- [旧CSVから変換できたBUYZONEコマンド・全件](master_init_template_ready_commands.txt)
- [手入力が必要なBUYZONEテンプレート・全件](master_init_template_buyzone_blank.txt)
- [TradingView更新テンプレート・全件](master_init_template_tv_blank.txt)

## TradingView更新テンプレート

TradingViewにアナリスト予想がある銘柄はレーティング・人数・平均目標株価を入れます。ETFやカバレッジなし銘柄は、未取得ではなく `not_applicable` / `no_coverage` と明示します。

```text
TV US EWY|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US EWY|no_coverage|TradingViewにアナリスト予想なし  または  TV US EWY|not_applicable|ETF等のため対象外
TV US QCOM|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US QCOM|no_coverage|TradingViewにアナリスト予想なし  または  TV US QCOM|not_applicable|ETF等のため対象外
TV US HSAI|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US HSAI|no_coverage|TradingViewにアナリスト予想なし  または  TV US HSAI|not_applicable|ETF等のため対象外
TV US PL|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US PL|no_coverage|TradingViewにアナリスト予想なし  または  TV US PL|not_applicable|ETF等のため対象外
TV US V|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US V|no_coverage|TradingViewにアナリスト予想なし  または  TV US V|not_applicable|ETF等のため対象外
TV US VRTX|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US VRTX|no_coverage|TradingViewにアナリスト予想なし  または  TV US VRTX|not_applicable|ETF等のため対象外
TV US DIS|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US DIS|no_coverage|TradingViewにアナリスト予想なし  または  TV US DIS|not_applicable|ETF等のため対象外
TV US KVYO|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US KVYO|no_coverage|TradingViewにアナリスト予想なし  または  TV US KVYO|not_applicable|ETF等のため対象外
TV US DKNG|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US DKNG|no_coverage|TradingViewにアナリスト予想なし  または  TV US DKNG|not_applicable|ETF等のため対象外
TV US CRSP|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US CRSP|no_coverage|TradingViewにアナリスト予想なし  または  TV US CRSP|not_applicable|ETF等のため対象外
TV US BEAM|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US BEAM|no_coverage|TradingViewにアナリスト予想なし  または  TV US BEAM|not_applicable|ETF等のため対象外
TV US ETN|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US ETN|no_coverage|TradingViewにアナリスト予想なし  または  TV US ETN|not_applicable|ETF等のため対象外
TV US MSTR|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US MSTR|no_coverage|TradingViewにアナリスト予想なし  または  TV US MSTR|not_applicable|ETF等のため対象外
TV US POET|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US POET|no_coverage|TradingViewにアナリスト予想なし  または  TV US POET|not_applicable|ETF等のため対象外
TV US KITT|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US KITT|no_coverage|TradingViewにアナリスト予想なし  または  TV US KITT|not_applicable|ETF等のため対象外
TV US AXTI|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US AXTI|no_coverage|TradingViewにアナリスト予想なし  または  TV US AXTI|not_applicable|ETF等のため対象外
TV US COHR|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US COHR|no_coverage|TradingViewにアナリスト予想なし  または  TV US COHR|not_applicable|ETF等のため対象外
TV US ANET|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US ANET|no_coverage|TradingViewにアナリスト予想なし  または  TV US ANET|not_applicable|ETF等のため対象外
TV US DDOG|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US DDOG|no_coverage|TradingViewにアナリスト予想なし  または  TV US DDOG|not_applicable|ETF等のため対象外
TV US SNOW|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US SNOW|no_coverage|TradingViewにアナリスト予想なし  または  TV US SNOW|not_applicable|ETF等のため対象外
TV US OPTX|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US OPTX|no_coverage|TradingViewにアナリスト予想なし  または  TV US OPTX|not_applicable|ETF等のため対象外
TV US AEM|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US AEM|no_coverage|TradingViewにアナリスト予想なし  または  TV US AEM|not_applicable|ETF等のため対象外
TV US ZETA|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US ZETA|no_coverage|TradingViewにアナリスト予想なし  または  TV US ZETA|not_applicable|ETF等のため対象外
```
