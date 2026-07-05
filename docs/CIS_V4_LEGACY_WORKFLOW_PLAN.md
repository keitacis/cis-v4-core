# CIS v4 Core｜旧Workflow停止・移行手順

CIS v4 Coreは、既存CISをいきなり削除しない。まず `cis_v4_*.yml` を手動実行で確認し、問題ないことを見てから旧Workflowの自動scheduleだけ止める。

## 1. 新しく使うv4 Workflow

v4のWorkflow名は、既存CISとの同名衝突を避けるため、すべて `cis_v4_` で始める。

- `cis_v4_preflight.yml`：既存CISとの衝突・root data互換性チェック
- `cis_v4_apply_seed.yml`：seedから不足root dataだけを安全作成
- `cis_v4_home.yml`：iPhoneホーム生成
- `cis_v4_daily_us.yml`：米国株日次騰落
- `cis_v4_daily_jp.yml`：日本株日次騰落
- `cis_v4_buy_alert.yml`：買い場アラート
- `cis_v4_weekly_performance.yml`：週間騰落
- `cis_v4_watchlist_update.yml`：監視リスト更新
- `cis_v4_master_init_template.yml`：初期マスター投入テンプレート生成
- `cis_v4_master_update.yml`：TradingView・買い場基準更新
- `cis_v4_monthly_maintenance.yml`：月次メンテナンス

## 2. 旧Workflowの扱い

| 旧Workflowの種類 | 例 | 方針 |
|---|---|---|
| 旧dashboard / Pages系 | dashboard系、pages系、旧home系 | v4ホーム確認後にschedule停止 |
| 旧米国株日次 | daily_us系、us_market系 | v4 `cis_v4_daily_us.yml` 確認後にschedule停止 |
| 旧日本株日次 | daily_jp系、jp_market系 | v4 `cis_v4_daily_jp.yml` 確認後にschedule停止 |
| 旧買い場アラート | buy_alert系、buy_zone系 | v4 `cis_v4_buy_alert.yml` 確認後にschedule停止 |
| 旧週間騰落 | weekly系、weekly_performance系 | v4 `cis_v4_weekly_performance.yml` 確認後にschedule停止 |
| watchlist_repair | watchlist_repair.yml | 初期移行完了までは残す。v4安定後に停止候補 |

## 3. 安全な移行順

### Phase A：v4投入直後

1. 旧Workflowはまだ触らない。
2. `CIS v4 Preflight` を手動実行する。
3. `docs/v4/latest/cis_v4_preflight_latest.html` を確認する。
4. root dataマスターが未作成または一部不足の場合のみ、`CIS v4 Apply Seed` を `missing_only` で実行する。
5. `docs/v4/index.html` を開き、CIS v4ホームが表示されることを確認する。
6. `CIS v4 Master Init Template` を手動実行する。
7. `docs/v4/latest/master_init_template_latest.html` を開き、BUYZONE/TVの不足一覧を見る。

### Phase B：初期マスター投入

1. `master_init_template_ready_commands.txt` に旧CSVから変換できたBUYZONE候補があれば、価格を確認してから `CIS v4 Master Update` に貼る。
2. `master_init_template_buyzone_blank.txt` は、打診・本命・強く買いたい価格を手入力してから使う。空欄のまま貼らない。
3. `master_init_template_tv_blank.txt` は、TradingViewのレーティング・アナリスト人数・平均目標株価を確認してから使う。
4. ETFやアナリスト予想が存在しない銘柄は `no_coverage` / `not_applicable` として明示する。
5. `CIS v4 Master Update` 実行後、`master_update_latest.html` と `monthly_maintenance_latest.html` を確認する。

### Phase C：v4手動実行テスト

1. `cis_v4_daily_us.yml` を手動実行し、米国株日次が出るか確認する。
2. `cis_v4_daily_jp.yml` を手動実行し、日本株日次が出るか確認する。
3. `cis_v4_weekly_performance.yml` を手動実行し、週間騰落が出るか確認する。
4. `cis_v4_buy_alert.yml` を手動実行し、買い場アラートが出るか確認する。
5. `cis_v4_home.yml` を再実行し、ホームの各カードが `✅` / `⚠️` / `休場` / `❌` で正しく表示されるか確認する。

### Phase D：旧Workflowのschedule停止

v4の各レポートが確認できたら、旧Workflowを削除せず、まずscheduleだけ止める。

止め方：

1. `.github/workflows/旧ファイル名.yml` を開く。
2. `on:` の下にある `schedule:` ブロックだけコメントアウト、または削除する。
3. `workflow_dispatch:` は残してよい。手動再実行できる保険になる。
4. Commitする。

## 4. 失敗したときに見る場所

| 失敗内容 | 見る場所 |
|---|---|
| Preflightが失敗 | `docs/v4/latest/cis_v4_preflight_latest.html`、`docs/v4/latest/cis_v4_preflight_status_latest.json` |
| Apply Seedが保護停止 | `docs/v4/latest/cis_v4_apply_seed_latest.md`、`docs/v4/latest/cis_v4_apply_seed_status_latest.json` |
| ホームが出ない | `docs/v4/index.html`、`docs/v4/latest/index_status_latest.json` |
| 米国株日次が失敗 | `docs/v4/latest/daily_us_latest.html`、`docs/v4/latest/daily_us_status_latest.json` |
| 日本株日次が失敗 | `docs/v4/latest/daily_jp_latest.html`、`docs/v4/latest/daily_jp_status_latest.json` |
| 買い場アラートが失敗 | `docs/v4/latest/buy_alert_latest.html`、`docs/v4/latest/buy_alert_status_latest.json` |
| TV/BUYZONE更新が失敗 | `docs/v4/latest/master_update_latest.html` |
| 初期投入テンプレートが見にくい | `.txt` ファイルを直接開く |

## 5. 削除タイミング

旧Workflowは、v4を1〜2週間使って問題がないことを確認してから削除する。最初はschedule停止までに留める。

## 6. v4自動scheduleの有効化

CIS v4 Core 初回投入版では、主要Workflowをあえて `workflow_dispatch` のみで入れる。理由は、`buyzone_master.json` と `tv_snapshot.json` の初期投入前に自動実行され、CISホームが最初からエラーだらけに見える事故を避けるため。

手動実行で以下を確認してから、自動scheduleを有効化する。

1. `CIS v4 Master Init Template` が成功している。
2. `CIS v4 Master Update` でBUYZONEとTVの初期投入が終わっている。
3. `CIS v4 Daily US`、`CIS v4 Daily JP`、`CIS v4 Weekly Performance`、`CIS v4 Buy Alert` を手動実行している。
4. `CIS v4 Home` で各カードが想定どおり表示されている。

有効化するcronの目安：

```yaml
# cis_v4_daily_us.yml
schedule:
  - cron: '15 22 * * 1-5'  # JST 07:15

# cis_v4_daily_jp.yml
schedule:
  - cron: '10 7 * * 1-5'  # JST 16:10

# cis_v4_buy_alert.yml
schedule:
  - cron: '0 23 * * 0-4'  # JST 月〜金 08:00

# cis_v4_weekly_performance.yml
schedule:
  - cron: '30 9 * * 6'  # JST 土曜18:30

# cis_v4_monthly_maintenance.yml
schedule:
  - cron: '0 0 1 * *'  # JST 毎月1日09:00

# cis_v4_home.yml
schedule:
  - cron: '0 21 * * *'  # JST 06:00
```

## 7. schedule有効化時の差し替え用 `on:` ブロック

自動化を有効にするときは、各v4 Workflowの冒頭にある `on:` ブロックを、該当する全文に差し替える。`permissions:` より上だけを触る。

### cis_v4_daily_us.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '15 22 * * 1-5'  # JST 07:15
```

### cis_v4_daily_jp.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '10 7 * * 1-5'  # JST 16:10
```

### cis_v4_buy_alert.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 23 * * 0-4'  # JST 月〜金 08:00
```

### cis_v4_weekly_performance.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '30 9 * * 6'  # JST 土曜18:30
```

### cis_v4_monthly_maintenance.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 1 * *'  # JST 毎月1日09:00
```

### cis_v4_home.yml

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 21 * * *'  # JST 06:00
```

注意：初期マスター投入が終わるまでは、この差し替えは行わない。

## 8. rho以降の安全投入版での変更

- v4 Workflowは `cis_v4_*.yml` 名にし、旧Workflowと同名にしない。
- 初回確認中の出力先は `docs/v4/` と `output/v4/`。
- seedデータは `data/v4_seed/` に退避し、root dataマスターは直接上書きしない。
- 最初に `CIS v4 Preflight` を実行して、既存CISとの衝突とdataマスター状態を確認する。
