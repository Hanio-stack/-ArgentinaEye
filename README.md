# ArgentinaEye 🇦🇷

自分専用のアルゼンチン投資・学習モニター。

毎朝、ミレイ改革・マクロ・Vaca Muerta・電力市場・大口資本の動きを確認し、**VIST / PAM / CEPU / TGS** を題材に「企業がどう成長し、株価がどう評価されるか」を勉強するための軽量PWAです。

## 設計原則

1. **一次情報優先** — INDEC / BCRA / Argentina.gob.ar / Secretaría de Energía / CAMMESA / 企業IRを優先。
2. **無料・自動・壊れにくい** — APIキーを極力使わず、GitHub Actions + 静的PWAで運用。
3. **ニュースアプリにしない** — 「何が変わったか」「投資仮説にプラスかマイナスか」を最初に出す。
4. **AI依存を最小化** — 数値スコアは説明可能なルールベース。
5. **欠損を隠さない** — 更新失敗や古いデータを推測で埋めず、`stale` / `unavailable` と表示。
6. **初心者でも読める** — 専門用語には「何を見る数字か」の注釈を付ける。
7. **勉強が主目的** — 事業テーマ・株価評価・リスクを分離し、「買い推奨スコア」を作らない。

## 4銘柄

- **VIST** — 「掘る」。Vaca Muertaの原油・ガス生産。
- **PAM** — 「総合」。石油・ガス、発電、インフラ。
- **CEPU** — 「作る」。発電・電力市場正常化。
- **TGS** — 「運ぶ」。ガス輸送・処理インフラ。

## v0.5 — Live valuation + scenario lab

- 4銘柄の**株価 / 時価総額 / EV / PER / Forward PER / EV・EBITDA / P・FCF / Debt・EBITDA / 52週騰落**を毎朝更新
- 市場データ取得失敗時は前回値を保持し `stale` 表示
- 事業テーマ・スコアとバリュエーションを完全に分離
- 各倍率に「何を見る数字か」の初心者向け注釈
- VIST / PAM / CEPU / TGS すべてに2028年 **Bear / Base / Bull** 学習モデル
- シナリオ前提（EBITDA、評価倍率、純負債）を画面に明示
- PWAオフラインキャッシュに valuation snapshot を追加
- バリュエーション取得・シナリオ計算の自動テストを追加

### Valuation data boundary

標準化された日次の価格・倍率比較には StockAnalysis.com（基礎データ: S&P Global Market Intelligence）を利用します。これは一次情報ではないため、**決算や事業判断の最終確認は企業IR/SEC等の一次資料**を優先します。取得に失敗した場合は古い値を「最新」と偽装せず `stale` にします。

Bear / Base / Bull はアナリスト目標株価ではありません。`EBITDA × EV/EBITDA − 純負債` という簡易モデルを学ぶための明示的な仮定です。

## NISA / 国内証券会社（2026-09-03確認）

| 銘柄 | SBI証券 | 松井証券 | NISA枠 |
|---|---|---|---|
| VIST | 取扱あり | 取扱あり | 成長投資枠 |
| PAM | 取扱あり | 取扱あり | 成長投資枠 |
| CEPU | 取扱あり | 取扱あり | 成長投資枠 |
| TGS | 取扱あり | 取扱あり | 成長投資枠 |

米国株は基本1株単位。実際の発注時は証券会社の注文画面でNISA表示・取扱状況を最終確認します。

## 監視対象

- ミレイ支持率 / 2027年再選リスク
- インフレ率
- BCRA外貨準備
- 財政収支
- Vaca Muerta生産量
- RIGI承認投資額
- 電力市場改革・電力需要
- Peter Thiel / Harold Hamm / Chevron / Mercuria / Eni / XRG 等の資本移動
- VIST / PAM / CEPU / TGS の企業ニュース
- 4銘柄のバリュエーション

## Architecture

**静的PWA + Pythonデータ収集 + GitHub Actions**。DBも有料APIも不要です。

毎朝06:15 JSTを目安に以下を更新します。

1. `scripts/update.py` — アルゼンチン中核指標
2. `scripts/augment_stocks.py` — 4社スコア・企業ニュース
3. `scripts/update_valuation.py` — 価格・倍率・シナリオ再計算

## Local preview

```bash
python -m http.server 8080 -d public
```

## Status

v0.5: live valuation + scenario lab. テーマ、値段、リスク、NISA実行条件を1画面で学べる状態。