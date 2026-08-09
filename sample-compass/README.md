# sample-compass: Python版

micro:bit方位磁石のPython教材です。実機用MicroPythonと、MakeCodeのブロックへ変換できるStatic Pythonを意図的に分けています。

## 2種類のPython

| ファイル | 実行環境 | センサーAPI | ブロック変換 |
|---|---|---|---|
| [`compass.py`](./compass.py) | MicroPython | `compass.heading()` | 非対応 |
| [`compass_makecode.py`](./compass_makecode.py) | MakeCode Python | `input.compass_heading()` | 対応 |

MicroPython版にはクラスと例外処理があります。MakeCode版は、ブロックで表現できるイベント、関数、条件分岐を使います。MakeCodeへ `compass.py` を貼り付けないでください。

## セットアップとテスト

```bash
uv sync
uv run pytest
```

テストは次を扱います。

- 8方位と22.5度刻みの境界値
- 未校正表示 `CAL`
- センサー例外時の最後の有効値
- 仕様上はあり得ない範囲外入力を想定する防御的プログラミング
- 実機 API の境界から入力するモック統合テスト
- HEXの構文、チェックサム、V1/V2 Universal HEX構造

PC 上のテストでは [`conftest.py`](./conftest.py) が `microbit` API をモックします。ユニットテストは主に純粋な `_heading_to_direction()`、統合テストは `compass.heading()` の戻り値を API 境界で設定した操作フローを担当します。アプリ内部の `heading` を直接書き換えないため、役割の違いを比較できます。実機の磁気センサーや校正精度を検査するものではありません。

カバレッジ品質ゲート:

```bash
uv run pytest --cov=compass --cov-report=term-missing --cov-fail-under=100
```

## MicroPython版の動作

1. 起動時に `CAL` と A／B ボタンの操作案内を表示する
2. A ボタンで校正する
3. B ボタンで 8 方位と角度をスクロール表示する
4. 校正済みならループで LED 矢印を表示し、未校正なら `CAL` を表示する

`display.scroll()` は表示中に処理を待つため、ボタンは押下を記録する `was_pressed()` で確認します。校正状態は自前のフラグを持たず、実機 API の `compass.is_calibrated()` を情報源にします。

MicroPython の `compass.heading()` は 0〜360 度を返し、未校正なら校正シーケンスを開始します。公式 API に `-1` を返す規約はありません。本実装が範囲外の値で前回値を保つのは、仕様上はあり得ない入力にも備える防御的プログラミングの練習です。

主なAPI:

- `Compass.calibrate()` — 実機コンパスを校正する
- `Compass.is_calibrated()` — 実機 API から校正状態を取得する
- `Compass.get_heading()` — 直近の有効な方位角を返す
- `Compass.get_direction()` — 8方位へ変換する
- `Compass.display_direction()` — LEDへ状態を表示する
- `Compass._heading_to_direction(heading)` — センサー非依存の変換ロジック

## Universal HEXを作る

```bash
uv run python build_hex.py
```

生成先は `dist/hex/compass.hex` です。ビルド後にIntel HEXの長さとチェックサムを検査し、micro:bit V1（target `0x9900`）とV2（target `0x9903`）の両方にファームウェアブロックがあることを確認します。不完全な出力は削除して失敗します。

HEXをUSB接続したmicro:bitドライブへコピーし、実機で校正と方位表示を確認してください。

## MakeCode Pythonを使う

1. <https://makecode.microbit.org/> で新規プロジェクトを作る
2. Pythonへ切り替える
3. [`compass_makecode.py`](./compass_makecode.py) の内容を貼り付ける
4. ブロックへ切り替える
5. 変換エラーやグレーブロックがないことを確認する

リポジトリのルートでは、この操作をPlaywrightで検査できます。

```bash
npm run verify:blocks
```

ブロック表示対応HEXは `dist/hex/blocks.hex` に生成されます。ネットワーク接続が必要です。

## 学習課題

- `337.4` と `337.5` の期待値をテストに追加する
- 公式範囲外の `-1` をあえて与え、前回値を保つ防御処理の利点と限界を説明する
- MicroPython版とMakeCode Python版で、校正イベントの書き方を比較する
- **16 方位**へ拡張し、11.25 度の境界テストを先に書く
- 複数回の方位角から**移動平均**を求め、359 度と 1 度の扱いを工夫する
- 加速度センサーを組み合わせた**傾き補正**の入力と期待値を設計する
- 実機を安全な金属へ近づけ、方位角の揺れという**磁気干渉**を記録する

## ライセンス

[MIT License](../LICENSE)
