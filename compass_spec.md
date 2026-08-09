# 方位磁石アプリケーション共通仕様 (Compass Application Specification)

このドキュメントは、Python / TypeScript / MakeCode のすべての実装における方位磁石アプリケーションの共通動作仕様を定義します。

## 1. キャリブレーション（校正）仕様

* **初期状態**: `is_calibrated` (校正済みフラグ) = `false`
* **校正処理 (`calibrate`)**:
  1. 画面表示をクリア（`clearScreen`）。
  2. 画面にひし形（矢印）LEDパターンを描画。
     ```
     . . # . .
     . # # # .
     # # # # #
     . # # # .
     . . # . .
     ```
  3. ハードウェアの校正API（`input.calibrateCompass()`）を実行。
  4. 画面表示をクリア（`clearScreen`）。
  5. 画面に `"OK"` をスクロール表示。
  6. 校正済みフラグを `true` に更新。

## 2. 8方位判定ロジック

方位角（度数: `heading`）から文字列による方位（`Direction`）への変換仕様：

* **無効な入力**: `heading` が `NaN`, `< 0`, または `>= 360` の場合は `"ERR"` を返す。
* **各方位の判定範囲 (45度幅)**:
  * `heading < 22.5` または `heading >= 337.5`: `"N"` (北)
  * `heading < 67.5`: `"NE"` (北東)
  * `heading < 112.5`: `"E"` (東)
  * `heading < 157.5`: `"SE"` (南東)
  * `heading < 202.5`: `"S"` (南)
  * `heading < 247.5`: `"SW"` (南西)
  * `heading < 292.5`: `"W"` (西)
  * 上記以外（`< 337.5`）: `"NW"` (北西)

## 3. UI / UX 動作仕様

### 3.1. 起動時
1. 画面に `"COMPASS"` をスクロール表示。
2. 画面に `"A:LOG"` をスクロール表示。

### 3.2. ボタン A 押下時
* **校正未完了時 (`!is_calibrated`)**: 上記の「校正処理」を実行する。
* **校正完了時 (`is_calibrated`)**: 
  1. 現在の方位角（度数）と方向を取得。
  2. 以下のフォーマットでシリアル出力（`console.log`）にログを出力する：
     `Time: {running_time}ms, Heading: {heading}, Dir: {direction}`

### 3.3. メインループ（`forever`）
* **校正未完了時 (`!is_calibrated`)**: 
  1. 画面に `"CAL"` をスクロール表示.
  2. `1000ms` 待機（ポーズ）。
* **校正完了時 (`is_calibrated`)**:
  1. 現在の方位角を取得。
  2. 方位角が `< 0` (エラー値) の場合、画面に `"ERR"` をスクロール表示し、`1000ms` 待機。
  3. 正常値の場合、対応する組み込み矢印（`basic.showArrow`）を表示し、`500ms` 待機。
     * N: `NORTH`, NE: `NORTH_EAST`, E: `EAST`, SE: `SOUTH_EAST`, S: `SOUTH`, SW: `SOUTH_WEST`, W: `WEST`, NW: `NORTH_WEST`
