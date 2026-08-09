# sample-compass-makecode

micro:bit 用の方位磁石アプリケーション（MakeCode/PXT 版）

> [!NOTE]  
> AIアシスタント（Antigravity, Claude, Copilot, Cursor）の環境設定や、プロジェクト共通のカスタムスキル同期方法については、ルートの [`../README.md`](file:///Users/katoy/github/study-microbit-with-test/README.md#aiアシスタント連携) を参照してください。

## Table of Contents

- [機能](#機能)
- [操作方法](#操作方法)
- [MakeCode エディターで開く](#makecode-エディターで開く)
- [ローカルでビルド・テスト](#ローカルでビルドテスト)
- [ファイル構成](#ファイル構成)
- [API リファレンス](#api-リファレンス)
- [テストについて](#テストについて)
- [Cleanup](#cleanup)
- [CI/CD](#cicd)
- [トラブルシューティング](#トラブルシューティング)
- [ライセンス](#ライセンス)
- [参考資料](#参考資料)

## 機能

- 🧭 **方位磁石機能**: micro:bit の内蔵コンパスを活用
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- ⚙️ **キャリブレーション**: ボタン A でコンパスをキャリブレーション
- 🧪 **実行テスト**: PXT 内蔵シミュレーターで方位判定テストを実行
- ✅ **GitHub Actions CI/CD**: 自動ビルドとテスト

## 操作方法

- **ボタン A**: コンパスをキャリブレーション（キャリブレーション完了後、"OK" が表示されます）
- **ボタン B**: 現在のコンパス状態を確認（度数と方角を表示）
- **LED ディスプレイ**: 北・東・南・西で矢印を表示、その他の方向は文字で表示

## MakeCode Web エディターとの相互インポート/エクスポート

本プロジェクトは、Web上の [MakeCode for micro:bit](https://makecode.microbit.org) エディターとローカル開発環境の間で双方向にインポート/エクスポートすることができます。用途に合わせて最適な方法を利用してください。

### 🔄 方法 1：GitHub 連携による双方向インポート (推奨)
GitHub を経由することで、Webエディターで編集したブロックコードとローカル環境をシームレスに同期できます。

1. **ローカルから GitHub へプッシュ**:
   プロジェクトをあなた自身の GitHub リポジトリにプッシュします。
2. **Web エディターへインポート**:
   - [MakeCode for micro:bit](https://makecode.microbit.org) を開きます。
   - 「インポート」 ➔ 「GitHub からリポジトリをインポートする」を選択します。
   - あなたのリポジトリ URL を入力してインポートします。
3. **Webでの編集とローカルへの反映**:
   - インポートが成功すると、Webエディターの左下に「GitHub」マーク（コミットツール）が表示されます。
   - Webエディター上でブロックを変更後、この GitHub マークからコミット＆プッシュを実行できます。
   - ローカル側では `git pull` を実行するだけで、Webでの変更（ブロックとコード）が瞬時に反映されます。

### 📂 方法 2：HEX ファイルを用いた簡易インポート/エクスポート
GitHub を使わずに、生成された書き込み用 HEX ファイルを介してコードを復元できます。PXT が出力する HEX ファイルにはソースコード自体が内包されているためです。

* **ローカル ➔ Web エディター (エクスポート)**:
  - ローカルでビルドした HEX ファイル (`sample-compass-makecode/built/binary.hex`) を、MakeCode Web エディターの画面に直接**ドラッグ＆ドロップ**します。
  - プロジェクトが瞬時に復元され、ブロックまたは JavaScript/Python としてWeb上で編集できます。
* **Web エディター ➔ ローカル (インポート)**:
  - Web エディターの「ダウンロード」ボタンを押して HEX ファイルを保存します。
  - Web エディターの右上の「エクスポート」からプロジェクトを zip ファイルとしてダウンロードし、ローカルに展開して `main.ts` や `compass.ts` を上書き更新できます。

### 🌐 方法 3：PXT ローカルサーバーを使ったリアルタイム連携
ローカルのテキストエディタ（VS Code等）でコードを書きながら、Webエディターのシミュレータやブロック自動生成をリアルタイムで同期させることができます。

1. **ローカルサーバーの起動**:
   ```bash
   npm run serve
   ```
2. **ブラウザで確認**:
   - コマンドを実行すると、ローカルの開発用 Web エディターが自動的にブラウザで起動します (`http://localhost:3232/` 等)。
3. **リアルタイム同期**:
   - ローカルの `compass.ts` や `main.ts` を VS Code 等で編集して保存します。
   - 保存を検知すると、ブラウザ上の MakeCode エディターおよびシミュレータが**自動リロードされ、ブロックも自動更新**されます。

## ローカルでビルド・テスト

### 必要なツール
- Node.js 22+

### インストール

```bash
npm ci
```

### ビルド

```bash
npm run build
```

### テスト実行

#### コンパイル・シミュレーターテスト

```bash
npm test
```

このコマンドはランナー自身の判定テスト、`pxt test` のコンパイル確認、PXT 内蔵シミュレーターでの28件の方位判定を順に実行します。1件でも失敗した場合や結果が出力されなかった場合は非ゼロ終了します。

### デバッグ用シミュレーター実行

```bash
npm run serve
```

開発サーバーが表示するURLをブラウザで開いて手動確認します。この操作は自動テストには含まれません。

自動テストの保証範囲は [SIMULATOR_TEST_GUIDE.md](./SIMULATOR_TEST_GUIDE.md)、CIでの実行範囲は [GITHUB_ACTIONS_TESTS.md](./GITHUB_ACTIONS_TESTS.md) を参照してください。

## ファイル構成

```
sample-compass-makecode/
├── pxt.json                 # MakeCode プロジェクト設定
├── main.ts                  # メインプログラム
├── compass.ts               # コンパス機能の実装
├── test.ts                  # テストコード
├── simulator-test-runner.cjs # PXT シミュレーターテストランナー
├── simulator-test-runner.test.cjs # ランナーの判定テスト
├── configure-pxt.cjs        # ローカル PXT CLI 設定
├── tsconfig.json            # TypeScript コンパイラ設定
├── SIMULATOR_TEST_GUIDE.md  # 自動シミュレーターテストの範囲
├── GITHUB_ACTIONS_TESTS.md  # CIでのテスト範囲
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

- **8 方位テスト**: 各方位（北、北東、東...）の判定確認
- **境界値テスト**: 方位の境界値での正確な判定確認

テストは製品プログラムの起動時には実行されません。`npm test` がテスト専用の一時 MakeCode プロジェクトを作り、テスト結果を検証した後に削除します。

## Cleanup

中間ファイルやキャッシュを削除：

```bash
# プロジェクト全体から実行
../scripts/clean.sh sample-compass-makecode

# またはルートディレクトリから
./scripts/clean.sh sample-compass-makecode
```

削除されるファイル（Git追跡中のパスは保持されます）：
- `built/` - MakeCode ビルド出力
- `node_modules/`, `pxt_modules/` - Node.js / PXT 依存関係
- `.pxt/` - PXT キャッシュ
- `coverage/`, `.jest-cache/`, `.nyc_output/`, `.cache/` - テスト・ツールキャッシュ

`package-lock.json` は削除されません。

## CI/CD

GitHub Actions で以下が自動実行されます：

- ✅ `npm ci` で固定済みの依存関係をインストール
- ✅ `pxt test` で TypeScript をコンパイル
- ✅ `pxt run` で28件のテストを実行し、失敗時は CI を停止

## トラブルシューティング

### コンパスが反応しない
- ボタン A でキャリブレーションを実行してください
- micro:bit をゆっくり回転させてキャリブレーションを完了させてください

### 方角が不正確
- キャリブレーションを再度実行してください
- 電子機器や磁場から遠い場所でテストしてください

### ビルドエラー
```bash
npm run install-deps
npx pxt clean
npm run build
```

## ライセンス

MIT

## 参考資料

- [MakeCode for micro:bit 公式サイト](https://makecode.microbit.org)
- [micro:bit Python API](https://microbit-micropython.readthedocs.io)
- [PXT ドキュメント](https://makecode.com/docs)
