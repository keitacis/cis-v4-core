# CIS v4 Core upsilon-tv-refresh-hotfix

TradingView月次確認の候補ファイル安全化hotfix。

- TV月次確認開始時に古い候補txt/manifestを削除。
- TV月次確認エラー時にも候補txtを残さず、manifestをerror化。
- 反映候補manifestを生成し、候補txtのsha256・件数・生成時刻を保存。
- Apply TV Monthly Candidate側で最新status/manifest/hash/件数を検査してからMaster Updateへ渡す。
- 古い候補txtや編集済み候補txtは反映不可。
- TV月次確認レポートにiPhone用分割txtリンクを表示。
- Apply後のBuy Alert再生成失敗もWorkflow失敗条件に含める。
