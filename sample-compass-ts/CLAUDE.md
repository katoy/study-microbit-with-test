# CLAUDE.md - TypeScript Compass Project Guide

このファイルは AI アシスタント（Claude、Copilot など）が sample-compass-ts プロジェクトで作業する際の指南書です。

## プロジェクト概要

**目的**: micro:bit 用 TypeScript 方位磁石アプリケーション

**特徴**:
- 型安全な実装（TypeScript）
- Compass クラスで方位磁石の機能を実装
- 方位角（0-359度）から8方位（N, NE, E, SE, S, SW, W, NW）への変換
- キャリブレーション機能
- Jest による単体テスト + E2E テスト

## ディレクトリ構造

```
sample-compass-ts/
├── src/
│   └── compass.ts           # Main implementation
├── test/
│   ├── compass.test.ts      # Unit tests (42 tests)
│   └── compass.e2e.test.ts  # E2E tests (23 tests)
├── jest.config.js           # Jest configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # npm dependencies & scripts
├── README.md
└── .tool-versions           # Node version management
```

## テスト実行方法

### 全テスト（ユニット + E2E）
```bash
cd sample-compass-ts
npm test
```

### ユニットテストのみ
```bash
cd sample-compass-ts
npm run test:unit
```

### E2E テストのみ
```bash
cd sample-compass-ts
npm run test:e2e
```

### Watch モード（ファイル変更時に自動再実行）
```bash
cd sample-compass-ts
npm run test:watch
```

### カバレッジ付き実行
```bash
cd sample-compass-ts
npm run test:coverage
```

### ビルド
```bash
cd sample-compass-ts
npm run build
```

## コード規約

### ファイル命名規則
- 実装ファイル: `camelCase.ts` または `snake_case.ts`
- テストファイル: `*.test.ts` または `*.spec.ts`
- E2E テスト: `*.e2e.test.ts`

### TypeScript スタイル
- 厳密な型定義を使用
- インターフェースで構造を定義
- docstring は JSDoc 形式

```typescript
/**
 * コンパスの状態を管理するインターフェース
 */
export interface CompassState {
  heading: number;
  direction: Direction;
  isCalibrated: boolean;
}

/**
 * 現在の方角を取得する
 * @returns 方角（N, NE, E, SE, S, SW, W, NW）
 */
public getDirection(): Direction {
  return this.headingToDirection(this.heading);
}
```

### 方位の型定義
```typescript
export type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';
```

## 重要なクラス・インターフェース

### `Direction` 型
```typescript
type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';
```

### `CompassState` インターフェース
```typescript
interface CompassState {
  heading: number;        // 0-359 度
  direction: Direction;   // 8方位
  isCalibrated: boolean;  // キャリブレーション状態
}
```

### `Compass` クラス

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `constructor()` | 初期化 | なし |
| `calibrate()` | キャリブレーション実行 | void |
| `getHeading()` | 現在の方位角を取得 | number |
| `setHeading(heading: number)` | 方位角を設定（テスト用） | void |
| `getDirection()` | 現在の方角を取得 | Direction |
| `getIsCalibrated()` | キャリブレーション状態を取得 | boolean |
| `getState()` | 現在の状態をスナップショット | CompassState |
| `static headingToDirection(heading)` | 方位角を方角に変換 | Direction |

### 方位計算ロジック
```
0°: N (北)
45°: NE (北東)
90°: E (東)
135°: SE (南東)
180°: S (南)
225°: SW (南西)
270°: W (西)
315°: NW (北西)
```

境界値：
- N: 337.5° 以上 または 22.5° 未満
- NE: 22.5° 以上 67.5° 未満
- 以降 45° ごとに区切る

## よくある作業

### 新しいテストを追加する

**ユニットテスト**:
```typescript
// test/compass.test.ts に追加
describe('Compass', () => {
  test('should handle new feature', () => {
    // arrange
    const compass = new Compass();
    compass.calibrate();
    compass.setHeading(90);

    // act
    const direction = compass.getDirection();

    // assert
    expect(direction).toBe('E');
  });
});
```

**E2E テスト**:
```typescript
// test/compass.e2e.test.ts の describe ブロックに追加
it('should handle new scenario', () => {
  compass.calibrate();
  compass.setHeading(45);
  
  expect(compass.getDirection()).toBe('NE');
  expect(compass.getHeading()).toBe(45);
});
```

### 新機能を追加する

1. テストを先に書く（TDD）:
   ```typescript
   test('should implement new method', () => {
     const compass = new Compass();
     const result = compass.newMethod();
     expect(result).toBe(expectedValue);
   });
   ```

2. テストが失敗することを確認:
   ```bash
   npm test -- --testNamePattern="new method"
   ```

3. 実装を追加 (src/compass.ts):
   ```typescript
   public newMethod(): ReturnType {
     /**
      * 新しいメソッドの説明
      */
     return calculatedValue;
   }
   ```

4. テストが成功することを確認:
   ```bash
   npm test -- --testNamePattern="new method"
   ```

5. ビルドでコンパイルエラーがないか確認:
   ```bash
   npm run build
   ```

6. リファクタリング（必要に応じて）

## テスト戦略

### ユニットテスト (test/compass.test.ts)
- **42 個のテスト**
- 各メソッドの単体テスト
- 型安全性の確認
- エラーハンドリング

テストカバレッジ:
- `constructor()`: 初期化状態の確認
- `calibrate()`: キャリブレーション状態の更新
- `getHeading()`: 方位角の取得
- `setHeading()`: 方位角の設定と検証
- `getDirection()`: 8方位すべてについて検証
- `getIsCalibrated()`: キャリブレーション状態の確認
- `getState()`: 状態スナップショット
- 静的メソッド: `headingToDirection()`
- 境界値: 22.5°, 67.5°, 112.5°, 157.5°, 202.5°, 247.5°, 292.5°, 337.5°
- エラーハンドリング: 無効な方位角

### E2E テスト (test/compass.e2e.test.ts)
- **23 個の統合テスト**
- 実際のユースケースに基づいたシナリオテスト
- ワークフロー全体の検証
- パフォーマンステスト

テストシナリオ:
1. 初期化と基本的なヘッディング確認
2. キャリブレーションと状態保持
3. ヘッディング更新と方角変更
4. 8方位全体の方向検出
5. 各境界条件での判定
6. ラップアラウンド（359° → 0°）
7. 連続ヘッディング更新（360°回転）
8. 連続クエリの一貫性
9. 複数インスタンスの独立動作
10. 無効な入力の拒否
11. キャリブレーション状態の永続性
12. 完全な状態スナップショット
13. パフォーマンス（10000回の高速実行）
14. 1000回のクエリ一貫性確認
15. 包括的なワークフロー検証

## よくある問題とトラブルシューティング

### npm dependencies のエラー
```bash
cd sample-compass-ts
rm -rf node_modules package-lock.json
npm install
npm test
```

### TypeScript のコンパイルエラー
```bash
# ビルドして詳細なエラーを確認
npm run build

# または tsc で直接実行
npx tsc --noEmit
```

### テストが検出されない
```bash
# jest.config.js の testMatch パターンを確認
# *.test.ts または *.spec.ts である必要があります
ls -la test/*.test.ts
```

### カバレッジレポートが生成されない
```bash
npm run test:coverage
# coverage/ ディレクトリが生成される
# coverage/index.html をブラウザで開く
```

### 特定のテストだけを実行したい
```bash
# テスト名パターンで実行
npm test -- --testNamePattern="direction detection"

# ファイルで実行
npm test test/compass.test.ts

# E2E テストのみ
npm run test:e2e

# ユニットテストのみ
npm run test:unit
```

### Watch モードで開発する
```bash
npm run test:watch
# ファイル保存時に自動的にテスト実行
# q キーで終了
```

## Git Hooks との連携

### Pre-commit Hook
コミット前に自動的に以下が実行されます：
```bash
npm test
```

### Pre-push Hook
プッシュ前に全テストが実行されます：
```bash
npm test
```

## GitHub Actions での実行

`.github/workflows/typescript-tests.yml` で自動実行：
- Node 20.x（最新 LTS）
- push と PR トリガー
- TypeScript ビルド確認
- Jest でユニット + E2E テスト
- カバレッジレポートを codecov に送信

## 推奨される変更ワークフロー

1. ブランチを作成:
   ```bash
   git checkout -b feature/add-new-direction
   ```

2. 新しいテストを書く:
   ```bash
   # test/compass.test.ts または test/compass.e2e.test.ts に追加
   ```

3. テストが失敗することを確認:
   ```bash
   npm test
   ```

4. 実装を追加 (src/compass.ts):
   ```typescript
   public newMethod(): Type {
     // 実装
   }
   ```

5. すべてのテストが成功することを確認:
   ```bash
   npm test
   ```

6. ビルドでコンパイルエラーがないか確認:
   ```bash
   npm run build
   ```

7. コミット（hooks が自動実行）:
   ```bash
   git commit -m "Add new feature"
   ```

8. プッシュ（hooks が全テスト実行）:
   ```bash
   git push origin feature/add-new-direction
   ```

9. PR を作成（GitHub Actions が自動実行）

## 開発環境セットアップ

### 必須ツール
- Node.js 20.x（最新 LTS）
- npm

### 初期セットアップ
```bash
cd sample-compass-ts
npm install
npm run build
npm test
```

### Node バージョン管理（asdf）
```bash
asdf install nodejs 20.x.x
asdf local nodejs 20.x.x
node --version  # v20.x.x であることを確認
```

## ファイル構成

### src/compass.ts
- `Direction` 型定義
- `CompassState` インターフェース
- `Compass` クラス実装
- `main()` 関数（エントリーポイント）

### test/compass.test.ts
- ユニットテスト（42個）
- 各メソッド・各境界値のテスト

### test/compass.e2e.test.ts
- E2E テスト（23個）
- 統合シナリオテスト
- パフォーマンステスト

## 外部リソース

- [Jest Documentation](https://jestjs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript JSDoc Reference](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)
- [micro:bit TypeScript API](https://makecode.microbit.org/)

## npm Scripts 一覧

| コマンド | 説明 |
|---------|------|
| `npm run build` | TypeScript をコンパイル |
| `npm test` | 全テスト実行（ユニット + E2E） |
| `npm run test:watch` | Watch モード |
| `npm run test:coverage` | カバレッジ付き実行 |
| `npm run test:unit` | ユニットテストのみ |
| `npm run test:e2e` | E2E テストのみ |
| `npm run clean` | ビルド成果物を削除 |

## 質問や改善提案

このファイルは継続的に改善されています。
プロジェクトのベストプラクティスを発見したら、このファイルを更新してください。
