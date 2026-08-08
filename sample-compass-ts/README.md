# sample-compass-ts

micro:bit 用の TypeScript 実装による方位磁石アプリケーション

## 機能

- 🧭 **型安全な方位磁石クラス**: TypeScript の型定義を活用した堅牢な実装
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- 🔄 **キャリブレーション管理**: キャリブレーション状態を管理
- ✅ **包括的なテスト**: Jest による 33+ テストケース

## 技術スタック

- **言語**: TypeScript 5.2+
- **テストフレームワーク**: Jest 29+
- **ノードバージョン**: 16+

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
npm run build
```

コンパイル済みの JavaScript ファイルが `dist/` ディレクトリに生成されます。

## テスト

```bash
# すべてのテストを実行
npm test

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

## micro:bit での使用方法

このコードをビルドして生成された JavaScript を micro:bit の MakeCode または MicroPython エディタで使用できます。

1. `npm run build` でビルド
2. `dist/compass.js` を micro:bit エディタにコピー
3. micro:bit に転送

## プロジェクト構成

```
sample-compass-ts/
├── src/
│   └── compass.ts              # メインの Compass クラス
├── test/
│   └── compass.test.ts         # Jest テストスイート
├── dist/                       # コンパイル済み JavaScript
├── coverage/                   # テストカバレッジレポート
├── package.json                # npm プロジェクト設定
├── tsconfig.json               # TypeScript コンパイラ設定
├── jest.config.js              # Jest テストランナー設定
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions ワークフロー
└── README.md
```

## CI/CD

GitHub Actions で自動的に以下が実行されます:

- ✅ TypeScript のコンパイル
- ✅ Jest でのユニットテスト（33+ テストケース）
- ✅ テストカバレッジの計測
- ✅ 複数のノードバージョン（16.x, 18.x, 20.x）で検証

## テストカバレッジ

目標: **100%** のコードカバレッジ

- Compass クラスの全メソッド
- 全 8 方位のテスト
- 境界値とエッジケースのテスト
- エラーハンドリングのテスト

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

## ライセンス

MIT

## 貢献

プルリクエストを歓迎します！テストカバレッジを保つようお願いします。
