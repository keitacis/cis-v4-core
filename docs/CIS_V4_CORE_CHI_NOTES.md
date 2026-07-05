# CIS v4 Core chi 補強メモ

phiの主修正（seed厳格検査後にApply Seedする）は維持しつつ、根幹部向けに以下を補強。

## 補強内容

1. `missing_only` の混在防止
   - seed単体の検査に加え、既存root dataとseed不足分を合わせた `staged data` を一時領域で検査。
   - staged dataがNGなら、root dataには何もコピーしない。

2. 履歴JSON検査の厳格化
   - `watchlist_history.json` / `master_update_history.json` は `items:list` だけでなく、各itemがobjectか確認。
   - 月次メンテナンス、Master Update、Watchlist Updateも履歴item object検査を使う。

3. watchlist/companyクロス整合性
   - watchlist_master.csv の各銘柄が company_master.csv に存在するか確認。
   - company_master側の余分な候補は将来候補として許容し、件数のみ表示。

4. Home可視化
   - CIS v4 Homeに `CIS v4 Preflight` と `CIS v4 Apply Seed` カードを追加。
   - error / partial / stale はホーム上部の「要確認」に表示。

5. コピー処理の安全化
   - ファイルコピーは一時ファイル経由で `os.replace`。
   - missing_onlyの途中失敗時は、その回にコピーした不足ファイルを削除。
   - overwrite_after_backupの途中失敗時は、可能な範囲でバックアップから復元。

## 実行確認

- 正常seed → Apply Seed ok → Preflight ok。
- 壊れたroot watchlist + missing_only → staged検査でerror、追加コピーなし。
- 正常root watchlistのみ + missing_only → staged検査OK、不足6ファイルのみコピー、partial。
- 履歴JSON itemsに文字列/数値 → Preflight / Apply Seedでerror。
- company_masterが空でwatchlistあり → watchlist/company整合性NGでerror。
- HomeにPreflight / Apply Seedカードと要確認表示が出ることを確認。
