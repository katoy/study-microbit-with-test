# sample-compass-makecode: MakeCode/PXT版

> **📚 参照**: プロジェクト全体については [`../README.md`](../README.md) をご覧ください。詳細な開発ガイドは本ディレクトリの `.vscode/CLAUDE.md` を参照。

MakeCodeのブロック、TypeScript、シミュレーター、実機HEXをつなぐ方位磁石教材です。

## 動作

- Aボタン: コンパス校正
- Bボタン: 方位と角度を表示
- forever: 現在の8方位をLED表示
- 未校正: `CAL`
- センサー異常: `ERR`

実機の方位角は `input.compassHeading()` から取得します。加速度APIは使用しません。

## セットアップとテスト

```bash
npm ci
npm test
```

`npm test` は次を順に実行します。

1. シミュレーターテスト結果パーサーのNodeテスト
2. `pxt test` によるコンパイル検査
3. PXTシミュレーターでの8方位、境界値、校正状態テスト

テストでは、ブロックに表示されない `Compass.calibrateForTest()` と `Compass.setHeadingForTest()` が実機センサーを置き換えます。PXT シミュレーターの成功は、実機の磁気センサー精度を保証しません。

## テストカバレッジ

### 📊 テスト結果: **35/35 成功** ✅

```
test:runner      (Node.js テスト)           4/4 成功
test:compile     (PXT コンパイル検査)        成功
test:simulator   (PXT シミュレーター)        35/35 成功

================================ テスト項目 ================================

8 方位判定テスト (24 テスト):
✓ 北（N）: 0°, 359°, 22.5°, 45°, 357°
✓ 北東（NE）: 22.5°, 45°, 67.5°
✓ 東（E）: 67.5°, 90°, 112°
✓ 南東（SE）: 112.5°, 135°, 157°
✓ 南（S）: 157.5°, 180°, 202°
✓ 南西（SW）: 202.5°, 225°, 247°
✓ 西（W）: 247.5°, 270°, 292°
✓ 北西（NW）: 292.5°, 315°, 337°

境界値テスト (4 テスト):
✓ 22.4° → N（22.5° 境界未満）
✓ 67.4° → NE（67.5° 境界未満）
✓ 202.4° → S（202.5° 境界未満）
✓ 337.4° → NW（337.5° 境界未満）

エラーハンドリング (3 テスト):
✓ -5° → ERR（負数）
✓ 400° → ERR（範囲外）
✓ NaN → ERR（特殊値）

キャリブレーション / 状態テスト (4 テスト):
✓ 初期状態: isCalibrated() == false
✓ 未校正時の getDirection() == CAL
✓ 校正後: isCalibrated() == true
✓ 校正後のデフォルト状態（heading = 0） == N

実行時間: 約 50 秒（PXT シミュレーター含む）
================================
```

### テストカバレッジの特性

MakeCode/PXT では従来のコードカバレッジ（行、分岐、関数）を測定しません。代わりに：

- **ブロック変換検証**: TypeScript がブロックへ正しく変換されるか確認
- **シミュレーター実行検証**: 変換後のブロックが PXT シミュレーター上で正常に動作するか確認
- **仕様カバレッジ**: 8 方位、境界値、エラー処理などの仕様要件をカバー

### カバレッジの確認方法

```bash
# テスト実行と結果確認
npm test

# 詳細なテストログを表示
npm run test:simulator

# 実行時間を確認
npm test 2>&1 | tail -20
```

## ビルド

```bash
npm run build
```

生成先は `built/binary.hex` です。USB接続したmicro:bitドライブへコピーし、実機で校正と表示を確認します。

ローカルMakeCodeエディター:

```bash
npm run serve
```

## MakeCode Webとの相互利用

### HEXを使う（推奨）

1. `npm run build` を実行
2. <https://makecode.microbit.org/> を開く
3. `built/binary.hex` を画面へドラッグ＆ドロップ

### GitHub連携の注意

このプロジェクトはモノレポのサブディレクトリにあり、リポジトリルートには `pxt.json` がありません。モノレポのGitHub URLをMakeCodeへ直接インポートすると、このPXTプロジェクトとして認識されません。

GitHub連携を使う場合は、`sample-compass-makecode` の内容を専用リポジトリのルートへ置き、そのリポジトリをMakeCodeからインポートしてください。ローカルとの確認だけならHEXまたは `npm run serve` が簡単です。

## ブロックAPI

`compass.ts` の `//% block` 注釈により、次の関数が「コンパス」カテゴリへ表示されます。

- コンパスをキャリブレーション
- コンパスの度数 (度)
- コンパスの方角
- コンパスはキャリブレーション済み
- 方位角 $heading 度の方角
- コンパス状態を表示

`calibrateForTest()` と `setHeadingForTest()` は自動テスト専用で、ブロックには公開しません。方位変換へ範囲外や `NaN` を渡した場合は、ブロック UI を停止させず `ERR` を返します。

## ブロック変換を検証する

ルートで実行します。

```bash
npm run verify:blocks
```

PlaywrightがMakeCode WebでTypeScriptをブロックへ切り替え、変換エラー、グレーブロック、ワークスペース欠落を検査します。ブロック表示対応HEXは `built/blocks.hex` に生成され、通常のPXTビルドが生成する `built/binary.hex` を上書きしません。ネットワーク接続が必要です。

## ファイル

- [`main.ts`](./src/main.ts) — ボタンイベントと表示ループ
- [`compass.ts`](./src/compass.ts) — 状態、実機API、8方位変換
- [`test.ts`](./test/test.ts) — PXTシミュレーター内テスト
- [`simulator-test-runner.cjs`](./simulator-test-runner.cjs) — シミュレーター起動と結果検査
- [`pxt.json`](./pxt.json) — MakeCodeプロジェクト定義

## 学習課題

- `337.4` と `337.5` の境界テストを比較する
- **16 方位**へ拡張し、11.25 度ごとのブロック条件を設計する
- 方位角の履歴から**移動平均**を計算し、LED 表示の揺れを減らす
- 加速度ブロックを組み合わせ、実機を傾けた場合の**傾き補正**を試す
- 実機を安全な金属へ近づけ、表示変化という**磁気干渉**を観察して記録する

## ライセンス

[MIT License](../LICENSE)
