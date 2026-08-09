# sample-compass-ts: Node.js TypeScript版

方位磁石の状態と8方位変換を、ハードウェアから切り離して学ぶTypeScript教材です。MakeCodeプログラムではないため、このディレクトリからmicro:bit用HEXは生成しません。

## 学習テーマ

- 8候補だけを許す文字列union型 `Direction`
- `CompassState` による状態の表現
- 未校正時の例外
- `NaN`、`Infinity`、範囲外を防ぐ実行時検証
- Jestによる境界値、状態遷移、統合テスト

## セットアップ

リポジトリをcloneした後、モノレポ内で実行します。

```bash
cd sample-compass-ts
npm ci
```

## コマンド

| コマンド | 内容 |
|---|---|
| `npm run build` | TypeScriptをコンパイル |
| `npm test` | すべてのJestテスト |
| `npm run test:unit` | ユニットテスト |
| `npm run test:integration` | 統合テスト |
| `npm run test:coverage` | カバレッジ100%を検査 |
| `npm run test:watch` | 編集中の再実行 |

## API

```typescript
const compass = new Compass();
compass.calibrate();
compass.setHeading(90);

console.log(compass.getDirection()); // E
console.log(compass.getState());
```

- `calibrate()` — 校正済み状態へ移す
- `setHeading(heading)` — 0以上360未満の有限値を設定する
- `getHeading()` — 校正済みなら現在値を返す
- `getDirection()` — 校正済みなら8方位を返す
- `getState()` — heading、direction、isCalibratedを返す
- `Compass.headingToDirection(heading)` — 状態を持たない変換

未校正で状態を読むと `Compass not calibrated` 例外になります。Python版の `CAL` 表示と比較し、ライブラリAPIと対話型UIでエラー通知がどう違うか考える教材です。

## 実機へ移すには

この実装は `input.compassHeading()` を含まない純粋なNode.jsコードです。micro:bitへ転送する場合は [`../sample-compass-makecode`](../sample-compass-makecode/) を使い、同じ境界仕様をMakeCode APIへ接続します。

## 学習課題

- `Compass.headingToDirection(337.5)` のテストを探す
- TypeScriptの `number` 型だけでは `NaN` を防げない理由を説明する
- 未校正を例外ではなく結果型で表す設計を比較する

## ライセンス

[MIT License](../LICENSE)
