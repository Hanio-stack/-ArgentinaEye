# ArgentinaEye 🇦🇷

自分専用のアルゼンチン投資モニター。

毎朝、ミレイ改革・マクロ・Vaca Muerta・電力市場・大口資本の動きを1画面で確認し、**VIST / PAM / CEPU / TGS** の投資テーマが前進しているかを判断するための軽量PWAです。

## 設計原則

1. **一次情報優先** — INDEC / BCRA / Argentina.gob.ar / Secretaría de Energía / CAMMESA / 企業IRを優先。
2. **無料・自動・壊れにくい** — APIキーを極力使わず、GitHub Actions + 静的PWAで運用。
3. **ニュースアプリにしない** — 「何が変わったか」「投資仮説にプラスかマイナスか」を最初に出す。
4. **AI依存を最小化** — 数値スコアは説明可能なルールベース。AI要約は将来の任意機能。
5. **欠損を隠さない** — 更新失敗や古いデータを推測で埋めず、`stale` / `unavailable` と表示。
6. **初心者でも読める** — 専門用語には「何を見る数字か」「上がると誰に効くか」の注釈を付ける。
7. **個人利用前提** — 認証・マルチユーザー・DBをMVPでは持たない。

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
- 4銘柄の投資テーマへの影響

## 4銘柄の役割

- **VIST** — 「掘る」。Vaca Muertaの原油・ガス生産への直接ベット。
- **PAM** — 「総合」。石油・ガス、発電、インフラを広く持つ総合エネルギー。
- **CEPU** — 「作る」。発電・電力市場正常化へのベット。
- **TGS** — 「運ぶ」。ガス輸送・処理インフラ。Vaca Muerta全体の流通量増加へのベット。

## v0.3 — Four-stock watch + Beginner guide

- Argentina / VIST / PAM / CEPU / TGS のルールベーススコア
- VIST / PAM / CEPU / TGS のニュース監視
- 各銘柄に「何の会社」「追い風」「逆風」の初心者向け注釈
- 中核指標カードを初心者向けの言葉に変更
- 用語ミニ辞典を追加
- スコアは**事業テーマの健康度であり、株価の割安・割高や買い推奨ではない**ことを明示

## v0.2 — Phase 2 + Web

- iPhone向け縦長1画面ダッシュボード / PWA
- 毎朝06:15 JSTを目安にGitHub Actionsで自動更新
- Big Money / 政策ニュース監視
- 履歴JSON・ソース健全性・部分障害フォールバック
- **INDEC CPI** 公式データ自動取得
- **BCRA外貨準備** 公式API自動取得
- **財政収支** Ministerio de Economía 公式ページ自動取得
- **Vaca Muerta原油生産** Secretaría de Energía 公式発表自動取得
- **RIGI承認投資額** Ministerio de Economía 公式情報自動取得
- **CAMMESA電力需要** 公開APIを優先し、取得できない場合は公式月次レポートへフォールバック
- GitHub Pages向け自動デプロイワークフロー
- PRごとの公式ソース・ライブスモークテスト

## Data boundary

ミレイ支持率は政府公式統計ではないため、公式経済データとは分離して世論調査・報道モニターとして扱います。RIGIは公式累計スナップショットを基準にし、新しい公式累計発表が見つかったときに更新します。CAMMESAのライブ需要APIが取得できない場合、数値を推測せず最新公式月次レポートの存在だけを表示します。

企業ニュースはGoogle News RSSを発見用に使い、見出しだけをダッシュボードへ表示します。企業スコアには株価・PER・EV/EBITDAなどのバリュエーションをまだ含めません。

## Architecture

**静的PWA + Pythonデータ収集 + GitHub Actions**。DBも有料APIも不要です。

詳細:
- `docs/ARCHITECTURE.md`
- `docs/DATA_SOURCES.md`
- `docs/SCORING.md`
- `docs/ROADMAP.md`
- `docs/RUNNING.md`

## Local preview

```bash
python -m http.server 8080 -d public
```

## Status

v0.3: four-stock thesis monitoring + beginner-friendly UI.
