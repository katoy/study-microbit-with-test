# sample-compass-ts

micro:bit 用の TypeScript 実装による方位磁石アプリケーション

## Table of Contents

- [機能](#機能)
- [技術スタック](#技術スタック)
- [インストール](#インストール)
- [ビルド](#ビルド)
- [実機用 HEX](#実機用-hex)
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
- ✅ **包括的なテスト**: Jest によるユニットテストと統合テスト

## 技術スタック

- **言語**: TypeScript 5.2+
- **テストフレームワーク**: Jest 29+
- **ノードバージョン**: 22.x（推奨）

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

## 実機用 HEX

このディレクトリはNode.js上で方位ロジックを学習・テストするための通常のTypeScript実装です。
MakeCode/PXTのターゲット情報を持たないため、ここからmicro:bit用HEXは生成しません。

```bash
cd ../sample-compass-makecode
npm run build:hex
```

実機向けTypeScriptは `sample-compass-makecode` を使用してください。生成物は
`sample-compass-makecode/built/binary.hex` です。

詳細は [HEX_BUILD_GUIDE.md](../HEX_BUILD_GUIDE.md) を参照してください。

## テスト

```bash
# すべてのテストを実行
npm test

# ユニットテストのみ
npm run test:unit

# 統合テストのみ
npm run test:integration

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
│   ├── compass.test.ts         # ユニットテスト（47 個）
│   └── compass.integration.test.ts # Node.js上の統合テスト
├── dist/                       # コンパイル済み JavaScript
│   ├── compass.js
│   ├── compass.d.ts            # 型定義
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
| `test/compass.test.ts` | ユニットテスト | 47 |
| `test/compass.integration.test.ts` | Node.js上の統合テスト | 25 |

### ビルド・スクリプト

| ファイル | 説明 |
|---------|------|
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
| `coverage/` | テストカバレッジレポート | ✅ 除外 |

## CI/CD

GitHub Actions で自動的に以下が実行されます:

- ✅ TypeScript のコンパイル
- ✅ Jest でのユニットテスト（47 テストケース）
- ✅ Node.js上の統合テスト
- ✅ テストカバレッジの計測
- ✅ Node.js 22.x で検証

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
| `npm test` | 全テスト実行 |
| `npm run test:unit` | ユニットテストのみ |
| `npm run test:integration` | 統合テストのみ |
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

削除されるファイル（Git追跡中のパスは保持されます）：
- `node_modules/`
- `dist/`, `build/`
- `coverage/`, `.jest-cache/`, `.nyc_output/`, `.cache/`

`package-lock.json` は削除されません。

## トラブルシューティング

### npm install が失敗する

```bash
npm ci
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

### 実機用 HEX が必要

```bash
cd ../sample-compass-makecode
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
