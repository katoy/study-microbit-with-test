# sample-compass: Python版

micro:bit方位磁石のPython教材です。MakeCodeのブロックへ変換できるStatic Pythonを扱っています。

## ファイル構成

| ファイル | 実行環境 | センサーAPI | ブロック変換 |
|---|---|---|---|
| [`compass_makecode.py`](./src/compass_makecode.py) | MakeCode Python | `input.compass_heading()` | 対応 |

MakeCode版は、ブロックで表現できるイベント、関数、条件分岐を使います。

## MakeCode Pythonを使う

1. <https://makecode.microbit.org/> で新規プロジェクトを作る
2. Pythonへ切り替える
3. [`compass_makecode.py`](./src/compass_makecode.py) の内容を貼り付ける
4. ブロックへ切り替える
5. 変換エラーやグレーブロックがないことを確認する

リポジトリのルートでは、この操作をPlaywrightで検査できます。

```bash
npm run verify:blocks
```

ブロック表示対応HEXは `dist/hex/blocks.hex` に生成されます。ネットワーク接続が必要です。

また、本ディレクトリ（`sample-compass`）内では、Playwright（Python版）を用いて MakeCode Web シミュレーター上での方位磁石の動作チェックを行う統合テストを実行できます。

### シミュレーター動作テストの実行方法

このテストは、ヘッドレスブラウザ上で MakeCode エディタを操作して `compass_makecode.py` を流し込み、45度ずつ回転させたときの LED 表示パターンを検証します。

1. 依存ライブラリとブラウザのセットアップ（初回のみ）:
   ```bash
   uv sync
   uv run playwright install chromium
   ```

2. テストの実行:
   ```bash
   uv run pytest test/test_simulator.py -v -s
   ```

テストが成功すると、シミュレーターの実行結果のスクリーンショットが `../dist/rotation-test-py.png` に保存されます。

## 学習課題

- **16 方位**へ拡張し、11.25 度の境界テストを設計する
- 複数回の方位角から**移動平均**を求め、359 度と 1 度の扱いを工夫する
- 加速度センサーを組み合わせた**傾き補正**の入力を設計する
- 実機を安全な金属へ近づけ、方位角の揺れという**磁気干渉**を記録する

## ライセンス

[MIT License](../LICENSE)
