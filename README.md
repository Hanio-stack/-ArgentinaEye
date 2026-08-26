# ArgentinaEye 🇦🇷

自分専用のアルゼンチン投資モニター。

毎朝、ミレイ改革・マクロ・Vaca Muerta・電力市場・大口資本の動きを1画面で確認し、VIST / CEPU の投資テーマが前進しているかを判断するための軽量PWAです。

## 設計原則

1. **一次情報優先** — INDEC / BCRA / Argentina.gob.ar / Secretaría de Energía / CAMMESA / 企業IRを優先。
2. **無料・自動・壊れにくい** — APIキーを極力使わず、GitHub Actions + 静的PWAで運用。
3. **ニュースアプリにしない** — 「何が変わったか」「投資仮説にプラスかマイナスか」を最初に出す。
4. **AI依存を最小化** — 数値スコアは説明可能なルールベース。AI要約は将来の任意機能。
5. **欠損を隠さない** — 更新失敗や古いデータを推測で埋めず、`stale` / `unavailable` と表示。
6. **個人利用前提** — 認証・マルチユーザー・DBをMVPでは持たない。

## 監視対象

- ミレイ支持率 / 2027年再選リスク
- インフレ率
- BCRA外貨準備
- 財政収支
- Vaca Muerta生産量
- RIGI承認投資額
- 電力市場改革・電力需要
- Peter Thiel / Harold Hamm / Chevron / Mercuria / Eni / XRG 等の資本移動
- VIST / CEPU の投資テーマへの影響

## MVP

- iPhone向け縦長1画面ダッシュボード
- 毎朝自動更新
- 指標カード + 前回差分 + 更新日 + ソース
- Big Moneyニュース監視
- Argentina / VIST / CEPU のルールベーススコア
- データ取得失敗時のフォールバック
- 履歴JSON蓄積
- PWAとしてホーム画面追加可能

## Architecture

MVPは **静的PWA + Pythonデータ収集 + GitHub Actions**。
DBも有料APIも不要です。

詳細:
- `docs/ARCHITECTURE.md`
- `docs/DATA_SOURCES.md`
- `docs/SCORING.md`
- `docs/ROADMAP.md`

## Status

Design complete → MVP implementation in progress.
