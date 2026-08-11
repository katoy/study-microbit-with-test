# sample-compass-ts: Node.js TypeScript版

[![TypeScript Tests](https://github.com/katoy/study-microbit-with-test/actions/workflows/typescript-tests.yml/badge.svg)](https://github.com/katoy/study-microbit-with-test/actions/workflows/typescript-tests.yml)

> **📚 参照**: プロジェクト全体については [`../README.md`](../README.md) を、開発ガイドについては [`CLAUDE.md`](./CLAUDE.md) を参照してください。

方位磁石の状態と8方位変換を、ハードウェアから切り離して学ぶTypeScript教材です。MakeCodeプログラムではないため、このディレクトリからmicro:bit用HEXは生成しません。

## 学習テーマ

- 8候補だけを許す文字列union型 `Direction`
- `CompassState` による状態の表現
- 未校正時の例外
- `NaN`、`Infinity`、範囲外を防ぐ実行時検証
- Jestによる境界値、状態遷移、統合テスト
- 100% カバレッジによる品質基準

## セットアップ

```bash
# プロジェクト依存関係のインストール
npm ci

# ビルド確認
npm run build

# テスト実行
npm test
```

## よく使うコマンド

| コマンド | 説明 |
|---|---|
| `npm run build` | TypeScript をコンパイル |
| `npm test` | 全テスト実行（ユニット + 統合）|
| `npm run test:unit` | ユニットテストのみ |
| `npm run test:integration` | 統合テストのみ |
| `npm run test:coverage` | カバレッジレポート（100% 要件チェック）|
| `npm run test:watch` | ファイル変更時に自動再実行 |
| `npm run clean` | ビルド成果物を削除 |

## 操作デモ

### テスト実行による動作確認

Node.js 上でテストを実行し、コンパスの動作を確認できます：

```bash
# 全テスト実行
npm test

# Watch モードで開発
npm run test:watch

# 特定のテストのみ実行
npm test -- --testNamePattern="direction detection"
```

**検証内容**:
- ✅ 8 方位の判定（N, NE, E, SE, S, SW, W, NW）
- ✅ 境界値での正確な判定（22.5°, 67.5° など）
- ✅ キャリブレーション状態の管理
- ✅ エラーハンドリング（NaN, 範囲外、負数）

**テスト実行例**:
```bash
$ npm test

PASS  test/compass.test.ts (1.2 s)
PASS  test/compass.integration.test.ts (0.8 s)

Tests:       74 passed, 74 total
Snapshots:   0 total
Time:        2.00 s

Coverage summary:
  Statements   : 100% ( 62/62 )
  Branches     : 100% ( 48/48 )
  Functions    : 100% ( 8/8 )
  Lines        : 100% ( 62/62 )
```

---

## API リファレンス

```typescript
const compass = new Compass();
compass.calibrate();
compass.setHeading(90);

console.log(compass.getDirection());  // 'E'
console.log(compass.getState());      // { heading: 90, direction: 'E', isCalibrated: true }
```

### 主要メソッド

| メソッド | 説明 | 戻り値 |
|---|---|---|
| `calibrate()` | 校正済み状態へ移す | void |
| `getHeading()` | 現在の方位角を取得（校正済みの場合） | number |
| `setHeading(heading)` | 方位角を設定（テスト用） | void |
| `getDirection()` | 8方位を取得（校正済みの場合） | Direction |
| `getIsCalibrated()` | 校正状態を取得 | boolean |
| `getState()` | 現在の状態をスナップショット | CompassState |
| `static headingToDirection(heading)` | 方位角を方角に変換（静的） | Direction |

### 型定義

```typescript
type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

interface CompassState {
  heading: number;        // 0-359度
  direction: Direction;   // 8方位
  isCalibrated: boolean;  // 校正済みフラグ
}
```

## テスト戦略

### ユニットテスト (test/compass.test.ts)
- 各メソッドの単体テスト
- 型安全性の確認
- エラーハンドリング（NaN、無限大、範囲外）
- 8方位すべての判定
- **境界値テスト**（22.5°、67.5°、337.5° など）

**例: 境界値テスト**
```typescript
test('should detect N at boundary 0°', () => {
  compass.calibrate();
  compass.setHeading(0);
  expect(compass.getDirection()).toBe('N');
});

test('should detect N at boundary 359°', () => {
  compass.calibrate();
  compass.setHeading(359);
  expect(compass.getDirection()).toBe('N');
});
```

### 統合テスト (test/compass.integration.test.ts)
- 完全なワークフロー（校正 → 回転 → 方向判定）
- 8方位全体を連続的に判定
- 境界値での正確な遷移
- 複数インスタンスの独立動作
- 無効な入力の拒否

**カバレッジ要件: 全メトリクス 100%**
- Branches (分岐): 100%
- Functions (関数): 100%
- Lines (行): 100%
- Statements (文): 100%

## テストカバレッジ

### 📊 カバレッジ結果: **100%** ✅

```
------------|---------|----------|---------|---------|-------------------
File        | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
------------|---------|----------|---------|---------|-------------------
All files   |     100 |      100 |     100 |     100 |                   
 compass.ts |     100 |      100 |     100 |     100 |                   
------------|---------|----------|---------|---------|-------------------

Test Suites: 2 passed, 2 total
Tests:       74 passed, 74 total
Snapshots:   0 total
Time:        1.64 s, estimated 2 s
```

**達成状況**:
- ✅ **Statements**: 100% - すべてのコード行を実行
- ✅ **Branches**: 100% - すべての条件分岐をカバー
- ✅ **Functions**: 100% - すべての関数を呼び出し
- ✅ **Lines**: 100% - すべての行をカバー

### カバレッジ測定方法

```bash
# コンソール出力で結果確認
npm run test:coverage

# HTML レポート生成
npm run test:coverage
# coverage/lcov-report/index.html をブラウザで開く
```

### テスト構成（74 テスト）

**ユニットテスト** (test/compass.test.ts):
- 8 方位の判定テスト (22.5°, 45°, 90° など各方位の複数境界値)
- エラーハンドリング (NaN, Infinity, 負数, 範囲外)
- キャリブレーション状態の管理
- 方位変換の静的メソッド検証

**統合テスト** (test/compass.integration.test.ts):
- 完全なワークフロー（校正 → 回転 → 判定）
- 8 方位全体の連続判定
- 境界値での正確な遷移
- 複数インスタンスの独立動作
- 連続更新後の一貫性確認

## CI/CD 統合

### GitHub Actions
`.github/workflows/typescript-tests.yml` で自動実行：
- Node.js 22.23.2 環境をセットアップ
- `npm ci` で依存関係をインストール
- `npm run build` で TypeScript をコンパイル
- `npm test` で全テストを実行
- **100% カバレッジを確認**
- codecov へカバレッジレポートをアップロード

### ローカルテスト
```bash
# 全テスト実行
npm test

# カバレッジレポート生成
npm run test:coverage
# coverage/lcov-report/index.html をブラウザで開く
```

## トラブルシューティング

### npm dependencies のエラー
```bash
rm -rf node_modules package-lock.json
npm install
npm test
```

### TypeScript コンパイルエラー
```bash
npm run build
# または
npx tsc --noEmit
```

### テストが 100% カバレッジを満たさない
```bash
npm run test:coverage
# coverage/lcov-report/index.html で未カバー部分を確認
```

### 特定のテストだけを実行したい
```bash
# テスト名パターンで実行
npm test -- --testNamePattern="direction detection"

# ファイルで実行
npm test test/compass.test.ts

# キーワードマッチ
npm test -- -t "should handle"
```

### Watch モードで開発する
```bash
npm run test:watch
# ファイル保存時に自動的にテスト実行
# q キーで終了
```

## ドキュメント

- [`CLAUDE.md`](./CLAUDE.md) - AI アシスタント向けの詳細ガイド（テスト戦略・デバッグ方法）
- [`../compass_spec.md`](../compass_spec.md) - 共通アプリケーション仕様
- [`../CLAUDE.md`](../CLAUDE.md) - プロジェクト全体のガイド
- [Jest Documentation](https://jestjs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 学習課題

- **16 方位** へ拡張し、11.25 度の境界テストを設計する
- **キャリブレーション状態の永続化** を実装（localStorage など）
- **複数の磁場環境** をシミュレート（オフセット値の設定）
- **統計的な外れ値検出** を実装（不安定な磁場計測値をフィルタリング）

未校正で状態を読むと `Compass not calibrated` 例外になります。Python版の `CAL` 表示と比較し、ライブラリAPIと対話型UIでエラー通知がどう違うか考える教材です。

## 実機へ移すには

この実装は `input.compassHeading()` を含まない純粋なNode.jsコードです。micro:bitへ転送する場合は [`../sample-compass-makecode`](../sample-compass-makecode/) を使い、同じ境界仕様をMakeCode APIへ接続します。

## 学習課題

- `Compass.headingToDirection(337.5)` のテストを探す
- TypeScriptの `number` 型だけでは `NaN` を防げない理由を説明する
- 未校正を例外ではなく結果型で表す設計を比較する
- **16 方位**へ拡張し、文字列 union 型と 11.25 度の境界テストを更新する
- 方位角の配列へ**移動平均**を適用し、359 度と 1 度を円環として扱う
- 加速度を引数に追加する**傾き補正**関数を、実機から独立した純粋関数として設計する
- 記録済みデータへ外れ値を加え、**磁気干渉**を検出するテストを作る

## ライセンス

[MIT License](../LICENSE)
