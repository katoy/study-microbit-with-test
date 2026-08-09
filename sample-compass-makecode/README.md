# sample-compass-makecode: MakeCode/PXT版

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

- [`main.ts`](./main.ts) — ボタンイベントと表示ループ
- [`compass.ts`](./compass.ts) — 状態、実機API、8方位変換
- [`test.ts`](./test.ts) — PXTシミュレーター内テスト
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
