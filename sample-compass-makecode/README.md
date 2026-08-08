# sample-compass-makecode

micro:bit 用の方位磁石アプリケーション（MakeCode/PXT 版）

## 機能

- 🧭 **方位磁石機能**: micro:bit の内蔵コンパスを活用
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- ⚙️ **キャリブレーション**: ボタン A でコンパスをキャリブレーション
- 🧪 **組み込みテスト**: シリアルコンソールでテスト実行可能
- ✅ **GitHub Actions CI/CD**: 自動ビルドとテスト

## 操作方法

- **ボタン A**: コンパスをキャリブレーション（キャリブレーション完了後、"OK" が表示されます）
- **ボタン B**: 現在のコンパス状態を確認（度数と方角を表示）
- **LED ディスプレイ**: 北・東・南・西で矢印を表示、その他の方向は文字で表示

## MakeCode エディターで開く

[MakeCode for micro:bit](https://makecode.microbit.org) でこのプロジェクトを開きます：

1. MakeCode エディターを開く
2. 「ファイル」→「インポート」→「GitHub から」を選択
3. リポジトリ URL を入力（`https://github.com/YOUR_USERNAME/sample-compass-makecode`）
4. HEX ファイルをダウンロードして micro:bit に転送

## ローカルでビルド・テスト

### 必要なツール
- Node.js 14+
- `pxt` CLI

### インストール

```bash
npm install -g pxt
```

### ビルド

```bash
pxt install
pxt build
```

### テスト実行

#### ユニットテスト（MakeCode テスト）

```bash
pxt test
```

テスト結果がシリアルコンソールに出力されます。

#### E2E テスト（pxt serve + Puppeteer）

基本的な E2E テストを実行：

```bash
npm install
npm run e2e
```

より詳細な E2E テストを実行（UI要素・コンソール・ネットワーク監視）：

```bash
npm install
npm run e2e:advanced
```

**E2E テストの内容:**
- ✅ ページ読み込み確認
- ✅ シミュレーター UI 表示確認
- ✅ JavaScript エラー監視
- ✅ コンソール出力確認
- ✅ ボタン要素検出
- ✅ ネットワークリクエスト監視
- 📸 スクリーンショット自動取得

**注意:** E2E テストを実行するには Node.js 14+ と Puppeteer がインストールされている必要があります。

### デバッグ用シミュレーター実行

```bash
pxt serve
```

ブラウザで http://localhost:3232 を開くとシミュレーターが起動します。

## ファイル構成

```
sample-compass-makecode/
├── pxt.json                 # MakeCode プロジェクト設定
├── main.ts                  # メインプログラム
├── compass.ts               # コンパス機能の実装
├── test.ts                  # テストコード
├── tsconfig.json            # TypeScript コンパイラ設定
├── .github/workflows/
│   └── test.yml             # GitHub Actions ワークフロー
├── built/                   # コンパイル出力
├── pxt_modules/             # MakeCode 標準パッケージ
├── README.md                # このファイル
└── .gitignore
```

## API リファレンス

### Compass 名前空間

#### `calibrate()`
コンパスをキャリブレーションします。
```blocks
Compass.calibrate()
```

#### `getHeading()`
現在の方位角を取得します（0-359 度）。
```blocks
let heading = Compass.getHeading()
```

#### `getDirection()`
現在の方角を取得します（N/NE/E/SE/S/SW/W/NW）。
```blocks
let direction = Compass.getDirection()
```

#### `isCalibrated()`
コンパスがキャリブレーション済みかどうかを取得します。
```blocks
let calibrated = Compass.isCalibrated()
```

#### `headingToDirection(heading)`
指定の方位角から方角文字列に変換します。
```blocks
let direction = Compass.headingToDirection(90)
```

#### `showState()`
現在のコンパス状態（度数と方角）を表示します。
```blocks
Compass.showState()
```

## テストについて

このプロジェクトには組み込みテストスイートが含まれています：

- **初期化テスト**: 初期状態の確認
- **8 方位テスト**: 各方位（北、北東、東...）の判定確認
- **境界値テスト**: 方位の境界値での正確な判定確認

テストは自動で起動時に実行され、シリアルコンソールに結果が出力されます。

## CI/CD

GitHub Actions で以下が自動実行されます：

- ✅ `pxt install` で依存関係をインストール
- ✅ `pxt build` で TypeScript をコンパイル
- ✅ `pxt test` でテストを実行
- ✅ ビルド成功時に HEX ファイルをアーティファクトにアップロード

## トラブルシューティング

### コンパスが反応しない
- ボタン A でキャリブレーションを実行してください
- micro:bit をゆっくり回転させてキャリブレーションを完了させてください

### 方角が不正確
- キャリブレーションを再度実行してください
- 電子機器や磁場から遠い場所でテストしてください

### ビルドエラー
```bash
pxt install
pxt clean
pxt build
```

## ライセンス

MIT

## 参考資料

- [MakeCode for micro:bit 公式サイト](https://makecode.microbit.org)
- [micro:bit Python API](https://microbit-micropython.readthedocs.io)
- [PXT ドキュメント](https://makecode.com/docs)
