# micro:bit 方位磁石を3つの環境で学ぶ

このガイドは、同じ方位判定仕様を MakeCode、Python、TypeScript で比較する自習教材です。既存テストを読み、境界値を 1 件追加した後、入力検証や発展機能まで段階的に扱います。

## 共通仕様

MicroPython の `compass.heading()` は北を 0 度として 0〜360 度を返し、未校正なら校正シーケンスを開始します。本教材の方位変換関数は有限な 0 度以上 360 度未満を入力仕様とし、実機 API の 360 度は 0 度へ正規化してから 45 度幅の 8 方位へ変換します。

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

1. 起動時に `CAL` と操作案内を表示する
2. ボタン A のイベントで `Compass.calibrate()` を呼ぶ
3. ボタン B で現在の方位と角度を確認する
4. `basic.forever` で LED の方位表示を更新する
5. 自動テストでは `setHeadingForTest()` で実機入力を置き換える

```bash
npm --prefix sample-compass-makecode test
```

`pxt test` のコンパイル検査と、PXTシミュレーター内の境界値テストが実行されます。

### ミニ課題

[`sample-compass-makecode/test/test.ts`](./sample-compass-makecode/test/test.ts) で、`337.5` が `N` になるテストを探してください。次に、その直前の値が `NW` になる理由を範囲表で説明します。

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

PCには `microbit` モジュールがないため、`conftest.py` がテスト中だけモックを提供します。方位変換は `_heading_to_direction()` に分離され、センサーなしで境界値を高速に検査できます。

```bash
cd sample-compass
uv sync
uv run pytest
```

### ミニ課題

1. `test_heading_to_direction_boundaries` を読む
2. `337.4` と `337.5` の期待値を追加する
3. テストを実行し、北の折り返し条件を確認する

公式 API に `-1` を返す規約はありません。`get_heading()` が範囲外の値でも最後の有効値を保つ処理は、「仕様上はあり得ない値が来ても壊れないか」を考える防御的プログラミングの練習です。校正状態は自前のフラグではなく `compass.is_calibrated()` から取得します。

MicroPython 版の操作も MakeCode 版と同じく、起動時の案内、A ボタンで校正、B ボタンで状態確認、ループで LED 矢印を表示する流れです。`display.scroll()` 中の押下を取りこぼさないよう、ボタンは `was_pressed()` で確認します。

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
| 操作フロー | 起動案内 → A で校正 → B で確認 → LED 矢印更新 | 起動案内 → A で校正 → B で確認 → LED 矢印更新 | コンソールで状態を確認 |
| 入力検証 | 範囲外と `NaN` は `ERR` | 範囲外と `NaN` は `ValueError` | 範囲外・`NaN`・`Infinity` は例外 |
| 強み | ブロックと実機イベント | 短いコードとpytest | 型・純粋ロジック・入力検証 |
| 注意 | Static Python/PXTの制約 | PCではモックが必要 | そのまま実機HEXにはならない |

エラーの伝え方だけは実行環境に合わせています。MakeCode はブロック UI を停止させない `ERR`、Python と Node TypeScript は呼び出し側が処理できる例外です。有効な入力範囲は 3 実装で同じです。

### ミニ課題: カバレッジ 100% でも仕様差を見逃す

1. 無効入力のテストを読む前に、`-5`、`400`、`NaN` の期待結果を 3 実装について予想する
2. 各実装のテストと変換関数を確認し、予想との差を記録する
3. 無効入力の assertion がなくても、既存の正常系入力だけで各分岐行を通れば行カバレッジ 100% になり得る理由を説明する

カバレッジは「実行された行」を測りますが、「必要な入力仕様をすべて assertion したか」は測りません。そのため、カバレッジ 100% でもバグゼロとは限りません。

さらに、Python の品質ゲートは `--cov=compass` で `compass.py` だけを測ります。MakeCode Web 貼り付け用の `compass_makecode.py` は対象外なので、表示された 100% は Python ファイルすべての網羅率ではありません。

## 発展課題

境界値を 1 件追加した後は、次の順に仕様、テスト、実装を広げます。

1. **16 方位** — 22.5 度幅へ拡張し、11.25 度ごとの境界値を先にテストする
2. **移動平均による平滑化** — 359 度と 1 度を単純平均すると 180 度になる問題も含め、円環上の平均を考える
3. **傾き補正** — 加速度センサーの値を入力に加え、水平でない場合の方位補正を設計する
4. **磁気干渉の観察** — 実機を安全な金属や磁石へ少しずつ近づけ、値の揺れと校正への影響を記録する

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

このコマンドは変換エラー、グレーブロック、Blocklyワークスペース欠落を失敗として扱い、ブロック表示対応HEXを `sample-compass/dist/hex/blocks.hex` と `sample-compass-makecode/built/blocks.hex` に生成します。

## 振り返り

- センサー取得と方位変換を分けると、どのテストが簡単になったか
- `22.5` のような境界値に、なぜ通常値より高い価値があるか
- モックテスト、PXTシミュレーター、実機テストはそれぞれ何を保証しないか
- 同じ仕様でも、`CAL` と例外のどちらを選ぶかは利用場面でどう変わるか
- カバレッジ 100% でも、未検証入力や対象外ファイルの不具合を見逃すのはなぜか
- 16 方位、平滑化、傾き補正、磁気干渉のうち、次にどの仮説をテストしたいか
