# CIS 監視リスト追加・変更テンプレート

生成日時：2026/07/05 21:06 JST

## 目的

監視リストの追加・停止・再開・説明修正を、iPhoneからでもミスなく行うためのページです。
このページはテンプレート作成だけで、監視リスト自体は変更しません。変更は `CIS v4 Watchlist Update` にコマンドを貼って実行します。

## 最短手順

1. このページのtxtを開いて、必要なコマンドをコピーします。
2. GitHub Actions > `CIS v4 Watchlist Update` を開きます。
3. `commands` に貼って実行します。
4. Homeの `監視リスト更新` と `初期マスター投入テンプレート` を確認します。
5. 新規追加銘柄は、必要に応じて `CIS v4 Master Update` でBUYZONE/TVも投入します。

## 基本コマンド

- `ADD US CRDO`：最低限の追加。名前はティッカーで仮登録。あとからUPDATE可能。
- `ADD US CRDO|Credo Technology|高速接続チップ|ai_datacenter`：説明つきで追加。
- `ADD JP 6758|ソニーグループ|ゲーム・半導体・エンタメ|大型成長`：日本株追加。
- `UPDATE US CRDO|Credo Technology|高速接続チップ|ai_datacenter`：既存銘柄の説明修正。active状態は変えません。
- `STOP US CRDO|理由`：監視停止。完全削除ではなくinactive化。
- `RESUME US CRDO|理由`：監視再開。

## サマリー

- 全登録：73件
- active：73件（US 48件 / JP 25件）
- inactive：0件（US 0件 / JP 0件）

## iPhone用txt

- [追加・変更の例](watchlist_add_examples.txt)
- [空の追加テンプレート](watchlist_quick_add_blank.txt)
- [active銘柄一覧](watchlist_active_list.txt)
- [inactive銘柄一覧](watchlist_inactive_list.txt)

### US停止テンプレート

- [part 01](watchlist_stop_us_part_01.txt)
- [part 02](watchlist_stop_us_part_02.txt)
- [part 03](watchlist_stop_us_part_03.txt)

### JP停止テンプレート

- [part 01](watchlist_stop_jp_part_01.txt)
- [part 02](watchlist_stop_jp_part_02.txt)

### US説明修正テンプレート

- [part 01](watchlist_update_us_part_01.txt)
- [part 02](watchlist_update_us_part_02.txt)
- [part 03](watchlist_update_us_part_03.txt)
- [part 04](watchlist_update_us_part_04.txt)

### JP説明修正テンプレート

- [part 01](watchlist_update_jp_part_01.txt)
- [part 02](watchlist_update_jp_part_02.txt)

## 注意

- 新規追加後、BUYZONEやTradingViewが未設定の銘柄は `初期マスター投入テンプレート` に出ます。
- STOPはデータを消さず、active=falseにします。再開はRESUMEで戻せます。
- 1回の入力内で同じ銘柄を複数回指定すると安全停止します。
- 区切りは半角 `|` でも全角 `｜` でも使えます。
