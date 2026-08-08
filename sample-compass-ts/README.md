# sample-compass-ts

micro:bit 用の TypeScript 実装による方位磁石アプリケーション

## Table of Contents

- [機能](#機能)
- [技術スタック](#技術スタック)
- [インストール](#インストール)
- [ビルド](#ビルド)
- [HEX ファイル生成](#hex-ファイル生成)
- [テスト](#テスト)
- [使用例](#使用例)
- [プロジェクト構成](#プロジェクト構成)
- [ファイル一覧](#ファイル一覧)
- [CI/CD](#cicd)
- [テストカバレッジ](#テストカバレッジ)
- [API リファレンス](#api-リファレンス)
- [npm Scripts リファレンス](#npm-scripts-リファレンス)
- [Cleanup](#cleanup)
- [トラブルシューティング](#トラブルシューティング)
- [ライセンス](#ライセンス)
- [参考リンク](#参考リンク)

## 機能

- 🧭 **型安全な方位磁石クラス**: TypeScript の型定義を活用した堅牢な実装
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- 🔄 **キャリブレーション管理**: キャリブレーション状態を管理
- ✅ **包括的なテスト**: Jest による 65 テストケース（ユニット 42 + E2E 23）
- 📦 **HEX ファイル生成**: micro:bit 転送用の HEX ファイルを自動生成

## 技術スタック

- **言語**: TypeScript 5.2+
- **テストフレームワーク**: Jest 29+
- **ノードバージョン**: 20.x（推奨）

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/sample-compass-ts.git
cd sample-compass-ts

# 依存パッケージをインストール
npm install
```

## ビルド

```bash
# TypeScript をコンパイル
npm run build

# dist/ ディレクトリに JavaScript が生成されます
ls -l dist/
```

## HEX ファイル生成

micro:bit に転送可能な HEX ファイルを生成できます。

```bash
# HEX ファイルを生成
npm run build:hex

# 生成されたファイルを確認
ls -lh dist/hex/compass.hex
```

生成された HEX ファイルは `dist/hex/compass.hex` に保存されます。

詳細は [HEX_BUILD_GUIDE.md](../HEX_BUILD_GUIDE.md) を参照してください。

## テスト

```bash
# すべてのテストを実行
npm test

# ユニットテストのみ
npm run test:unit

# E2E テストのみ
npm run test:e2e

# テストカバレッジを表示
npm run test:coverage

# ウォッチモードでテストを実行
npm run test:watch
```

## 使用例

```typescript
import { Compass } from './src/compass';

const compass = new Compass();
compass.calibrate();

compass.setHeading(90);
console.log(compass.getDirection()); // 出力: 'E'

const state = compass.getState();
console.log(state); // { heading: 90, direction: 'E', isCalibrated: true }
```

## プロジェクト構成

```
sample-compass-ts/
├── src/
│   └── compass.ts              # メインの Compass クラス
├── test/
│   ├── compass.test.ts         # ユニットテスト（42 個）
│   └── compass.e2e.test.ts     # E2E テスト（23 個）
├── scripts/
│   └── generate-hex.js         # HEX ファイル生成スクリプト
├── dist/                       # コンパイル済み JavaScript
│   ├── compass.js
│   ├── compass.d.ts            # 型定義
│   └── hex/                    # 生成された HEX ファイル
├── coverage/                   # テストカバレッジレポート
├── package.json                # npm プロジェクト設定
├── tsconfig.json               # TypeScript コンパイラ設定
├── jest.config.js              # Jest テストランナー設定
├── .tool-versions              # Node バージョン管理
├── CLAUDE.md                   # AI 開発ガイド
└── README.md                   # このファイル
```

## ファイル一覧

### ソースコード

| ファイル | 説明 | 行数 |
|---------|------|------|
| `src/compass.ts` | Compass クラス、インターフェース、型定義 | ~100 |

### テスト

| ファイル | 説明 | テスト数 |
|---------|------|---------|
| `test/compass.test.ts` | ユニットテスト | 42 |
| `test/compass.e2e.test.ts` | E2E テスト | 23 |

### ビルド・スクリプト

| ファイル | 説明 |
|---------|------|
| `scripts/generate-hex.js` | HEX ファイル生成スクリプト |
| `jest.config.js` | Jest テストランナー設定 |
| `tsconfig.json` | TypeScript コンパイラ設定 |
| `package.json` | npm プロジェクト設定 |

### 設定ファイル

| ファイル | 説明 |
|---------|------|
| `.gitignore` | Git 除外設定 |
| `.tool-versions` | Node.js バージョン管理（asdf） |

### ドキュメント

| ファイル | 説明 |
|---------|------|
| `README.md` | このファイル |
| `CLAUDE.md` | AI 開発ガイド |

### ディレクトリ

| ディレクトリ | 説明 | .gitignore |
|-----------|------|-----------|
| `dist/` | ビルド出力ディレクトリ | ✅ 除外 |
| `dist/hex/` | 生成された HEX ファイル | ✅ 除外 |
| `coverage/` | テストカバレッジレポート | ✅ 除外 |

## CI/CD

GitHub Actions で自動的に以下が実行されます:

- ✅ TypeScript のコンパイル
- ✅ Jest でのユニットテスト（42 テストケース）
- ✅ E2E テスト（23 テストケース）
- ✅ テストカバレッジの計測
- ✅ 複数のノードバージョン（20.x）で検証

詳細は `.github/workflows/typescript-tests.yml` を参照してください。

## テストカバレッジ

目標: **100%** のコードカバレッジ

- Compass クラスの全メソッド
- 全 8 方位のテスト
- 境界値とエッジケースのテスト
- エラーハンドリングのテスト
- パフォーマンステスト（10000 回実行）

テストカバレッジレポート：

```bash
npm run test:coverage
# coverage/lcov-report/index.html をブラウザで開く
```

## API リファレンス

### `Compass` クラス

#### メソッド

- `calibrate(): void` - コンパスをキャリブレーション
- `getHeading(): number` - 方位角を取得（0-359 度）
- `setHeading(heading: number): void` - 方位角を設定（テスト用）
- `getDirection(): Direction` - 方角を取得
- `getIsCalibrated(): boolean` - キャリブレーション状態を取得
- `getState(): CompassState` - 現在の状態を取得
- `static headingToDirection(heading: number): Direction` - 方位角を方角に変換

#### 型

```typescript
type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

interface CompassState {
  heading: number;
  direction: Direction;
  isCalibrated: boolean;
}
```

## npm Scripts リファレンス

| コマンド | 説明 |
|---------|------|
| `npm run build` | TypeScript をコンパイル |
| `npm run build:hex` | HEX ファイルを生成 |
| `npm test` | 全テスト実行 |
| `npm run test:unit` | ユニットテストのみ |
| `npm run test:e2e` | E2E テストのみ |
| `npm run test:coverage` | カバレッジレポート付き |
| `npm run test:watch` | ウォッチモード |
| `npm run clean` | ビルド成果物を削除 |

## Cleanup

中間ファイルやキャッシュを削除：

```bash
# プロジェクト全体から実行
../scripts/clean.sh sample-compass-ts

# またはルートディレクトリから
./scripts/clean.sh sample-compass-ts
```

削除されるファイル：
- `node_modules/`, `package-lock.json/`
- `dist/`, `build/`
- `coverage/`, `.jest-cache/`

## トラブルシューティング

### npm install が失敗する

```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript コンパイルエラー

```bash
npm run build
# または
npx tsc --noEmit
```

### テストが検出されない

```bash
# jest.config.js の testMatch パターンを確認
ls -la test/*.test.ts
```

### HEX ファイルが生成されない

```bash
# ビルドが成功しているか確認
npm run build
# HEX スクリプトを実行
npm run build:hex
```

## ライセンス

**MIT License**

このプロジェクトは MIT ライセンスの下で公開されています。
自由に使用、変更、配布できます。

## 参考リンク

- [Jest Documentation](https://jestjs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript JSDoc Reference](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)
- [micro:bit TypeScript API](https://makecode.microbit.org/)
- [Intel HEX Format](https://en.wikipedia.org/wiki/Intel_HEX)

## 貢献

プルリクエストを歓迎します！テストカバレッジを保つようお願いします。
