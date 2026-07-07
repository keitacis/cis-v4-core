# CIS v4 Price Freshness + Buy Alert UX Patch R7

R7はR6の内容を維持しつつ、精査で見つかった表示ノイズをさらに削る版です。

- 価格鮮度ガードをDaily US / Daily JP / Buy Alert / Weeklyへ適用
- 全件価格未更新時は通常ランキング・買い場カードを非表示
- 一部価格未更新時は古い価格の銘柄をランキング対象外へ分離
- 「休場」と「価格未更新」を分離
- Daily US / Daily JP / Buy Alertのcronを終値反映後＋予備実行へ変更
- data/cis_settings.jsonとcis_core.pyの時刻メタデータをcronに同期
- Buy Alertを買い場接近銘柄中心の表示へ変更
- TradingView区分・アナリスト分布・基準理由・長いTV更新表示を非表示
- no_coverage / not_applicable銘柄では、アナリスト人数・目標株価・乖離率に「カバレッジなし」を繰り返さず、TradingViewは1行表示に圧縮
- no_coverage / not_applicableはTradingView鮮度注意に数えない

R1〜R6は使わないでください。
