# CIS v4 Core upsilon-tv-refresh-guard-homefix-autoschedule notes

この版では homefix をベースに、CIS本番運用向けの自動実行cronを有効化した。

## 有効化した自動実行

- Daily US: JST 火〜土 07:15（UTC 月〜金 22:15）
- Buy Alert: JST 月〜金 08:00（UTC 日〜木 23:00）
- Daily JP: JST 月〜金 16:10（UTC 月〜金 07:10）
- Weekly Performance: JST 土曜 18:30（UTC 土曜 09:30）
- Home: JST 毎日 06:00（UTC 前日21:00）

Monthly Maintenance と TV Monthly Refresh の月次自動実行は既存仕様を維持した。

## TV候補反映後の再生成

Apply TV Monthly Candidate 後に、Buy Alertに加えて Daily US と Weekly Performance の再生成も試行する。
Daily US / Weekly は価格取得タイミングやyfinance側事情で失敗する可能性があるため、TV候補反映自体の必須成功条件には含めない。Home側のstale判定で状態を確認する。

## 注意

GitHub ActionsのcronはUTC基準。JSTの時刻に合わせるため、各workflow内のcronはUTC換算で設定している。
