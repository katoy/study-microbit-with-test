# CLAUDE.md - TypeScript Compass Project Guide

このファイルは AI アシスタント（Claude、Copilot など）が sample-compass-ts プロジェクトで作業する際のプロジェクト固有ガイドです。

**プロジェクト全体のガイドは `../CLAUDE.md` を参照してください。**  
**AIアシスタント連携（カスタムスキル同期）については、ルートにある [`../sync-ai-skills.sh`](file:///Users/katoy/github/study-microbit-with-test/sync-ai-skills.sh) をご利用ください。**

## プロジェクト概要

**目的**: micro:bit 用 TypeScript 方位磁石アプリケーション

**特徴**:
- 型安全な TypeScript 実装
- 方位角（0-359度）から8方位への変換
- キャリブレーション機能
- テスト: JestによるユニットテストとNode.js上の統合テスト

## ディレクトリ構造

```
sample-compass-ts/
├── src/
│   └── compass.ts           # Main implementation
├── test/
│   ├── compass.test.ts      # Unit tests
│   └── compass.integration.test.ts # Integration tests
├── jest.config.js           # Jest configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # npm dependencies & scripts
├── CLAUDE.md                # このファイル
├── README.md
└── .tool-versions           # Node version management (22.23.2)
```

## テスト実行方法

### 全テスト（ユニット + 統合）
```bash
npm test
```

### ユニットテストのみ
```bash
npm run test:unit
```

### 統合テストのみ
```bash
npm run test:integration
```

### Watch モード（ファイル変更時に自動再実行）
```bash
npm run test:watch
```

### 特定のテストのみ実行
```bash
# テスト名パターンで実行
npm test -- --testNamePattern="direction detection"

# ファイルで実行
npm test test/compass.test.ts

# キーワードマッチ
npm test -- -t "should handle"
```

### カバレッジ付き実行
```bash
npm run test:coverage
# coverage/index.html をブラウザで開く
```

### ビルド
```bash
npm run build
```

## TypeScript コード規約

### ファイル命名規則
- 実装ファイル: `camelCase.ts` または `snake_case.ts`
- テストファイル: `*.test.ts` または `*.spec.ts`
- 統合テスト: `*.integration.test.ts`

### TypeScript スタイル
- **厳密な型定義を使用**
- **インターフェースで構造を定義**
- **JSDoc 形式の docstring**
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

### `Compass` クラスのメソッド

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `calibrate()` | キャリブレーション実行 | void |
| `getHeading()` | 現在の方位角を取得 | number |
| `setHeading(heading)` | 方位角を設定（テスト用） | void |
| `getDirection()` | 現在の方角を取得 | Direction |
| `getIsCalibrated()` | キャリブレーション状態を取得 | boolean |
| `getState()` | 現在の状態をスナップショット | CompassState |
| `static headingToDirection(heading)` | 方位角を方角に変換 | Direction |

## テスト戦略

### ユニットテスト (test/compass.test.ts) - 47個
- 各メソッドの単体テスト
- 型安全性の確認
- エラーハンドリング
- 8方位すべての判定
- 境界値テスト（22.5°, 67.5° など）

### 統合テスト (test/compass.integration.test.ts)
- 完全なワークフロー
- 8方位全体の判定
- 境界値での正確な遷移
- ラップアラウンド（359° → 0°）
- 連続回転シミュレーション
- 複数インスタンスの独立動作
- 無効な入力の拒否
- パフォーマンステスト（10000回実行）

## よくある作業

### 新しいテストを追加する

**ユニットテスト**:
```typescript
// test/compass.test.ts に追加
describe('Compass', () => {
  test('should handle new feature', () => {
    const compass = new Compass();
    compass.calibrate();
    compass.setHeading(90);
    expect(compass.getDirection()).toBe('E');
  });
});
```

**統合テスト**:
```typescript
// test/compass.integration.test.ts の describe ブロックに追加
it('should handle new scenario', () => {
  compass.calibrate();
  compass.setHeading(45);
  expect(compass.getDirection()).toBe('NE');
});
```

### 新機能を追加する（TDD）

1. テストを先に書く
2. テスト実行（失敗）
3. 実装を追加（src/compass.ts）
4. テスト実行（成功）
5. ビルド確認
6. 必要に応じてリファクタリング

```bash
# テスト実行
npm test -- --testNamePattern="new feature"

# 実装追加後
npm test -- --testNamePattern="new feature"

# ビルド確認
npm run build
```

## Git Hooks 連携

### Pre-commit Hook
コミット前に自動実行：
```bash
npm test
```

### Pre-push Hook
プッシュ前に全テスト実行

詳細は `../.husky/` を参照。

## トラブルシューティング

### npm dependencies のエラー
```bash
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

### カバレッジレポートが表示されない
```bash
npm run test:coverage
# coverage/lcov-report/index.html をブラウザで開く
```

### 特定のテストだけを実行したい
```bash
# テスト名パターンで実行
npm test -- --testNamePattern="direction detection"

# ファイルで実行
npm test test/compass.test.ts

# 統合テストのみ
npm run test:integration

# ユニットテストのみ
npm run test:unit
```

### Watch モードで開発する
```bash
npm run test:watch
# ファイル保存時に自動的にテスト実行
# q キーで終了
```

## 環境設定

### 必須ツール
- Node.js 22.x（LTS）
- npm

### 初期セットアップ
```bash
npm install
npm run build
npm test
```

### Node バージョン管理（asdf）
```bash
asdf install nodejs 22.23.2
asdf local nodejs 22.23.2
node --version  # v22.23.2 であることを確認
```

## npm Scripts 一覧

| コマンド | 説明 |
|---------|------|
| `npm run build` | TypeScript をコンパイル |
| `npm test` | 全テスト実行（ユニット + 統合） |
| `npm run test:watch` | Watch モード |
| `npm run test:coverage` | カバレッジ付き実行 |
| `npm run test:unit` | ユニットテストのみ |
| `npm run test:integration` | 統合テストのみ |
| `npm run clean` | ビルド成果物を削除 |

## CI/CD

### GitHub Actions
`.github/workflows/typescript-tests.yml` で自動実行：
- Node 22.x でテスト
- push と PR トリガー
- TypeScript ビルド確認
- Jest でユニット + 統合テスト
- カバレッジレポートを codecov に送信

### ローカルテスト
```bash
# すべてのテストを実行
npm test -- --coverage
```

## 方位計算ロジック

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

### 境界値
- N: 337.5° 以上 または 22.5° 未満
- NE: 22.5° 以上 67.5° 未満
- 以降 45° ごとに区切る

## 外部リソース

- [Jest Documentation](https://jestjs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript JSDoc Reference](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)
- [micro:bit TypeScript API](https://makecode.microbit.org/)
