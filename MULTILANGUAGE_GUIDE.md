# micro:bit 方位磁石を3つの環境で学ぶ

このガイドは、同じ方位判定仕様をMakeCode、Python、TypeScriptで比較する自習教材です。コードを丸ごと書き換えるのではなく、既存テストを読み、境界値を1件追加し、実装との対応を確認します。

## 共通仕様

micro:bitのコンパスは北を0度として0〜359度を返します。本教材は45度幅で8方位へ変換します。

| 方位 | 範囲 |
|---|---|
| N | 337.5度以上、または22.5度未満 |
| NE | 22.5度以上67.5度未満 |
| E | 67.5度以上112.5度未満 |
| SE | 112.5度以上157.5度未満 |
| S | 157.5度以上202.5度未満 |
| SW | 202.5度以上247.5度未満 |
| W | 247.5度以上292.5度未満 |
| NW | 292.5度以上337.5度未満 |

0度付近では範囲が360度をまたぎます。`heading < 22.5 || heading >= 337.5` と書くのが重要です。

## 1. MakeCode: 目で動きをつかむ

対象: [`sample-compass-makecode`](./sample-compass-makecode/)

MakeCode版は実機APIを直接使います。

```typescript
const heading = input.compassHeading();
```

`input.acceleration(Dimension.X)` と `Y` は傾き・加速度であり、磁北の方位角ではありません。方位磁石教材では `input.compassHeading()` を使います。

主な流れは次のとおりです。

1. ボタンAのイベントで `Compass.calibrate()` を呼ぶ
2. `basic.forever` で `Compass.getDirection()` を繰り返す
3. LEDへ方位を表示する
4. 自動テストでは `setHeadingForTest()` で実機入力を置き換える

```bash
npm --prefix sample-compass-makecode test
```

`pxt test` のコンパイル検査と、PXTシミュレーター内の境界値テストが実行されます。

### ミニ課題

[`sample-compass-makecode/test.ts`](./sample-compass-makecode/test.ts) で、`337.5` が `N` になるテストを探してください。次に、その直前の値が `NW` になる理由を範囲表で説明します。

## 2. Python: ハードウェアをモックしてテストする

対象: [`sample-compass`](./sample-compass/)

このディレクトリには目的の異なる2種類のPythonがあります。

| ファイル | API | 用途 |
|---|---|---|
| `compass.py` | `from microbit import ...` | MicroPython実機、PC上のpytest |
| `compass_makecode.py` | `input`、`basic` などのグローバルAPI | MakeCode Python、ブロック相互変換 |

MicroPython版では実機の値を次で取得します。

```python
value = compass.heading()
```

PCには `microbit` モジュールがないため、[`conftest.py`](./sample-compass/conftest.py) がテスト中だけモックを提供します。方位変換は `_heading_to_direction()` に分離され、センサーなしで境界値を高速に検査できます。

```bash
cd sample-compass
uv sync
uv run pytest
```

### ミニ課題

1. `test_heading_to_direction_boundaries` を読む
2. `337.4` と `337.5` の期待値を追加する
3. テストを実行し、北の折り返し条件を確認する

実機で `-1` が返った場合、`get_heading()` は最後の有効値を保持し、校正状態を `False` に戻します。`display_direction()` は未校正なら `CAL` を表示します。

## 3. TypeScript: 型と入力検証を学ぶ

対象: [`sample-compass-ts`](./sample-compass-ts/)

この実装はNode.js上で動く純粋な学習モデルで、MakeCode APIを呼びません。`Direction` は8つの文字列だけを許し、方位角が有限かつ0以上360未満であることを検査します。

```typescript
export type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';
```

未校正で `getDirection()` や `getState()` を呼ぶと例外になります。Python版の「`CAL`を表示する」方針との違いは、どちらが正解というより、利用者へ失敗をどう伝えるかという設計判断です。

```bash
cd sample-compass-ts
npm ci
npm run build
npm test
```

### ミニ課題

`NaN`、`Infinity`、`-1`、`360` のテストを探し、「型がnumberでも実行時検証が必要な理由」を説明します。

## 4. 3環境を比較する

| 観点 | MakeCode | MicroPython | Node TypeScript |
|---|---|---|---|
| 実機API | `input.compassHeading()` | `compass.heading()` | なし |
| 主な入力方法 | 実機／PXTテストモード | 実機／pytestモック | メソッドで値を設定 |
| 未校正の表現 | `CAL` | LEDに`CAL` | 例外 |
| 強み | ブロックと実機イベント | 短いコードとpytest | 型・純粋ロジック・入力検証 |
| 注意 | Static Python/PXTの制約 | PCではモックが必要 | そのまま実機HEXにはならない |

## 5. 完全な品質ゲート

リポジトリのルートへ戻って実行します。

```bash
npm run test:all
npm run lint
npm run build:hex
```

ブロック変換まで確かめる場合は、ネットワーク接続のある環境で次を実行します。

```bash
npm run verify:blocks
```

このコマンドは変換エラー、グレーブロック、Blocklyワークスペース欠落を失敗として扱います。

## 振り返り

- センサー取得と方位変換を分けると、どのテストが簡単になったか
- `22.5` のような境界値に、なぜ通常値より高い価値があるか
- モックテスト、PXTシミュレーター、実機テストはそれぞれ何を保証しないか
- 同じ仕様でも、`CAL` と例外のどちらを選ぶかは利用場面でどう変わるか
