# CIS 初期マスター投入テンプレート

生成日時：2026/07/07 21:45 JST

## 目的

このページは、買い場基準とTradingViewスナップショットの初期投入漏れを防ぐための確認用です。
この処理はマスターを更新しません。更新するには、下のコマンドを `CIS v4 Master Update` に貼ります。

## サマリー

- active銘柄：73
- 米国株active銘柄：48
- 買い場基準未設定：0
- 買い場基準不正：0
- 旧buy-zone CSVから変換候補あり：0
- TradingView未設定/要区分入力：1

## iPhone用・分割コピー

長すぎる貼り付け事故を避けるため、10〜15銘柄単位の分割txtを先に出します。iPhoneでは基本こちらを1つずつ開いて使います。

### TradingView 分割

月1回の確認用です。毎日自動取得するのではなく、ここで更新したスナップショットを各レポートで再利用します。

- 改行 part 01: [開く](master_init_tv_blank_part_01.txt) / 1行版: [開く](master_init_tv_blank_semicolon_part_01.txt)

## PC向け・全件コピー

PCや長文貼り付けに慣れている場合はこちらを使えます。iPhoneでは分割txtの方が安全です。

- [旧CSVから変換できたBUYZONEコマンド・全件](master_init_template_ready_commands.txt)
- [手入力が必要なBUYZONEテンプレート・全件](master_init_template_buyzone_blank.txt)
- [TradingView更新テンプレート・全件](master_init_template_tv_blank.txt)

## TradingView更新テンプレート

TradingViewにアナリスト予想がある銘柄はレーティング・人数・平均目標株価を入れます。ETFやカバレッジなし銘柄は、未取得ではなく `not_applicable` / `no_coverage` と明示します。

```text
TV US OPTX|Strong Buy/Buy/Neutral/Sell|人数|平均目標株価|TradingView YYYY/MM/DD  または  TV US OPTX|no_coverage|TradingViewにアナリスト予想なし  または  TV US OPTX|not_applicable|ETF等のため対象外
```
