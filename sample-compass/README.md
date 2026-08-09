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
- `-1` 応答時の再校正要求
- 完全な操作フローを模したモック統合テスト
- HEXの構文、チェックサム、V1/V2 Universal HEX構造

PC上のテストでは [`conftest.py`](./conftest.py) が `microbit` APIをモックします。実機の磁気センサーや校正精度を検査するものではありません。

カバレッジ品質ゲート:

```bash
uv run pytest --cov=compass --cov-report=term-missing --cov-fail-under=100
```

## MicroPython版の動作

1. 起動時に校正する
2. 校正済みなら8方位と角度をLEDへスクロール表示する
3. Aボタンで再校正する
4. 未校正なら `CAL` を表示する

主なAPI:

- `Compass.calibrate()` — 実機コンパスを校正する
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
- `-1` を受けた後に `CAL` が表示される流れを図にする
- MicroPython版とMakeCode Python版で、校正イベントの書き方を比較する

## ライセンス

[MIT License](../LICENSE)
