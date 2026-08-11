# sample-compass: Python版

[![Integration Tests](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml/badge.svg?branch=main)](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml)

> **📚 参照**: プロジェクト全体については [`../README.md`](../README.md) を、開発ガイドについては [`CLAUDE.md`](./CLAUDE.md) を参照してください。

micro:bit 方位磁石の **Python 教材**です。MakeCode ブロックに変換できる **Static Python** を扱っています。

## 目次

- [概要](#概要)
- [セットアップ](#セットアップ)
- [操作デモ](#操作デモ)
  - [シミュレータ画面の実演動画](#シミュレータ画面の実演動画)
  - [実際のシミュレータで確認](#実際のシミュレータで確認)
  - [ビデオ記録の制御](#ビデオ記録の制御)
- [LED 表示パターン](#led-表示パターン)
- [テスト実行](#テスト実行)
  - [全テスト（推奨）](#全テスト推奨)
  - [ユニットテスト（高速）](#ユニットテスト高速)
  - [シミュレーターテスト（完全検証）](#シミュレーターテスト完全検証)
  - [構文チェック（最高速）](#構文チェック最高速)
- [MakeCode で実行](#makecode-で実行)
- [カバレッジ詳細](#カバレッジ詳細)
- [トラブルシューティング](#トラブルシューティング)
- [学習課題](#学習課題)

---

## 概要

**目的**: Python 3.12.8 で MakeCode 互換の方位磁石アプリケーションを実装・テスト

**実装**:
| ファイル | 環境 | API | ブロック変換 |
|---------|------|-----|----------|
| [`compass_makecode.py`](./src/compass_makecode.py) | MakeCode Python | `input.compass_heading()` | ✅ 対応 |

**テスト戦略（3 層）**:

1. **ユニットテスト** (`test/test_coverage.py`, 43 テスト)
   - 方向判定ロジックの完全検証
   - 8 方位の境界値テスト（22.5°, 67.5° など）
   - エラーハンドリング（負数、NaN、範囲外）
   - 実行時間: < 1 秒

2. **シミュレーターテスト** (`test/test_simulator.py`, 1 テスト)
   - MakeCode Web 上での統合動作検証
   - 実際の LED マトリックス表示パターン確認
   - ブロック変換後の動作確認
   - 実行時間: 30～40 秒（ネットワーク依存）

3. **カバレッジ**: **100% 保証** ✅

詳細は [`CLAUDE.md`](./CLAUDE.md) を参照。

---

## セットアップ

```bash
# プロジェクト依存関係のインストール
cd sample-compass
uv sync

# ブラウザ自動化ツールのセットアップ（初回のみ）
uv run playwright install chromium
```

**環境要件**:
- Python 3.12.8
- uv (Python パッケージマネージャー)
- Playwright (ブラウザ自動化)
- ffmpeg（ビデオ→GIF 変換用、オプション）

---

## 操作デモ

### シミュレータ画面の実演動画

![Simulator Screencast](./screenshots/simulator-demo.gif)

上の GIF は、ブラウザで実際に動作するシミュレータをスクリーンキャストしたものです。

**デモで確認できる動作**:
- ✅ コンパスプログラムの実行
- ✅ 8 方位の自動判定
- ✅ LED マトリックスへの矢印表示
- ✅ ボタン操作によるキャリブレーション

### 実際のシミュレータで確認

#### ブラウザウィンドウを表示して実行

```bash
PLAYWRIGHT_HEADLESS=0 uv run pytest test/test_simulator.py -v -s
```

- ✅ ブラウザウィンドウが自動で開く
- ✅ MakeCode シミュレータの動作をリアルタイムで確認
- ✅ 実行時間: 30～40 秒

#### バックグラウンドで実行

```bash
uv run pytest test/test_simulator.py -v -s
```

- ✅ ブラウザウィンドウなし（ヘッドレスモード）
- ✅ テスト結果をコンソール出力
- ✅ 実行時間: 30～40 秒

**検証項目**:

| 検証項目 | 詳細 |
|---------|------|
| 📍 コード実行 | compass_makecode.py をシミュレータで実行 |
| 📐 方向判定 | 0°～315° の各方向を正確に判定 |
| 🔴 LED 表示 | 5×5 LED マトリックスに 8 方向の矢印を表示 |
| 🔧 キャリブレーション | ボタン A で校正開始、校正完了後に方向を表示 |
| 📹 動画記録 | テスト実行をビデオ→GIF で保存（制御可能） |

### ビデオ記録の制御

デフォルトではビデオは記録されません。ビデオを記録したい場合：

```bash
# ビデオを記録して GIF を生成
RECORD_VIDEO=1 uv run pytest test/test_simulator.py -v -s
```

生成された `screenshots/simulator-demo.gif` で、実際のシミュレータ動作を確認できます。

**ビデオ記録オプション**:

| 環境変数 | 値 | 動作 | 実行時間 |
|---------|-----|------|---------|
| `RECORD_VIDEO` | `0` (デフォルト) | ビデオなし | 30～40 秒 |
| `RECORD_VIDEO` | `1` | ビデオ記録＋GIF 生成 | 40～50 秒 |

---

## LED 表示パターン

micro:bit の 5×5 LED マトリックスに、現在の方位を示す 8 方向の矢印を表示します。

### 方向別 LED パターン

各角度で表示される矢印（MakeCode シミュレーター実際のキャプチャ）：

| 角度 | 方向 | 矢印 | LED パターン（シミュレーター） | ArrowNames 定数 |
|------|------|------|------|------------|
| **0°** | **北（N）** | **↑** | ![North](./screenshots/led_000_north.png) | `ArrowNames.NORTH` |
| **45°** | **北東（NE）** | **↗** | ![Northeast](./screenshots/led_045_northeast.png) | `ArrowNames.NORTH_EAST` |
| **90°** | **東（E）** | **→** | ![East](./screenshots/led_090_east.png) | `ArrowNames.EAST` |
| **135°** | **南東（SE）** | **↘** | ![Southeast](./screenshots/led_135_southeast.png) | `ArrowNames.SOUTH_EAST` |
| **180°** | **南（S）** | **↓** | ![South](./screenshots/led_180_south.png) | `ArrowNames.SOUTH` |
| **225°** | **南西（SW）** | **↙** | ![Southwest](./screenshots/led_225_southwest.png) | `ArrowNames.SOUTH_WEST` |
| **270°** | **西（W）** | **←** | ![West](./screenshots/led_270_west.png) | `ArrowNames.WEST` |
| **315°** | **北西（NW）** | **↖** | ![Northwest](./screenshots/led_315_northwest.png) | `ArrowNames.NORTH_WEST` |

**実装での使用例**:
```python
if direction == "N":
    basic.show_arrow(ArrowNames.NORTH)  # 北向き矢印を表示
```

### キャリブレーションフロー

1. **初回起動時**: LED マトリックスに **「CAL」** メッセージを表示
2. **ボタン A 押下**: キャリブレーション開始（LED が回転パターンで表示）
3. **校正完了**: ボタン A を押して検出した現在の方向を表示

---

## テスト実行

### 全テスト（推奨）

```bash
uv run pytest test/ -v --cov=compass_makecode --cov-report=term-missing
```

**実行内容**:
- ✅ ユニットテスト (43 テスト) - 0.1 秒
- ✅ シミュレーターテスト (1 テスト) - 30～40 秒
- ✅ カバレッジ検証 - 100% 必須

**期待される結果**:

```
================================ tests coverage ================================
Name                      Stmts   Miss  Cover
---------------------------------------------------------------------------
src/compass_makecode.py      62      0   100%
---------------------------------------------------------------------------
============================== 44 passed in 32.55s ==============================
```

### ユニットテスト（高速）

```bash
uv run pytest test/test_coverage.py -v
```

**テスト内容**:
- 8 方位の境界値テスト (30 テスト)
- エラーハンドリング (負数、NaN、範囲外)
- 関数テスト (キャリブレーション、ボタン、ループ)

**実行時間**: < 1 秒

### シミュレーターテスト（完全検証）

```bash
# ヘッドレスモード（バックグラウンド）
uv run pytest test/test_simulator.py -v -s

# ブラウザ表示モード
PLAYWRIGHT_HEADLESS=0 uv run pytest test/test_simulator.py -v -s

# ビデオ記録ありで実行
RECORD_VIDEO=1 uv run pytest test/test_simulator.py -v -s
```

**テスト内容**:
- MakeCode Web 上での実行
- 45° ステップでの回転テスト (0°, 45°, 90°, ..., 315°)
- 各角度での LED パターン検証
- ボタン操作と方向判定の確認

**実行時間**: 30～40 秒（ネットワーク依存）

### 構文チェック（最高速）

```bash
uv run python -m py_compile src/compass_makecode.py
```

- MakeCode への変換前のバリデーション
- Pre-commit hook で自動実行
- 実行時間: < 0.1 秒

### カバレッジレポート（HTML）

```bash
uv run pytest test/ -v --cov=compass_makecode --cov-report=html
open htmlcov/index.html
```

ブラウザで詳細なカバレッジレポートを確認できます。

---

## MakeCode で実行

実機の micro:bit で実行するには：

1. <https://makecode.microbit.org/> で新規プロジェクト作成
2. **Python へ切り替え**
3. [`src/compass_makecode.py`](./src/compass_makecode.py) の内容をコピーペースト
4. **ブロックへ切り替え**（Static Python がブロックに自動変換される）
5. **シミュレーター**または**実機**で動作確認
6. **HEX ダウンロード** → micro:bit に書き込み

---

## カバレッジ詳細

### 📊 カバレッジ結果: 100% ✅

```
================================ tests coverage ================================
Name                      Stmts   Miss  Cover
---------------------------------------------------------------------------
src/compass_makecode.py      62      0   100%
---------------------------------------------------------------------------
TOTAL                        62      0   100%
============================== 44 passed in 32.55s ==============================
```

### 達成内容

✅ **すべての関数をカバー**
- `calibrate_compass()` - キャリブレーション実行
- `get_direction_string(heading)` - 方向判定
- `on_button_pressed_a()` - ボタン操作
- `on_forever()` - メインループ

✅ **すべての条件分岐をカバー**
- 8 方位の判定ロジック（30 テスト）
- エラーハンドリング（負数、NaN、範囲外）
- 校正状態の分岐

✅ **すべての実行パスをカバー**
- 44 テストケース（43 ユニット + 1 シミュレーター）

### 計測コマンド

```bash
# コンソール出力
uv run pytest test/ -v --cov=compass_makecode --cov-report=term-missing

# HTML レポート
uv run pytest test/ -v --cov=compass_makecode --cov-report=html

# JSON レポート（CI 統合用）
uv run pytest test/ --cov=compass_makecode --cov-report=json
```

### 100% 未満になった場合

```bash
# 未カバーの行を確認
uv run pytest test/ -v --cov=compass_makecode --cov-report=term-missing

# HTML レポートで詳細確認
uv run pytest test/ -v --cov=compass_makecode --cov-report=html
open htmlcov/index.html

# 特定のテストのみ実行
uv run pytest test/test_coverage.py::TestGetDirectionString -v
```

---

## よく使うコマンド

| コマンド | 説明 |
|---------|------|
| `uv sync` | 依存関係をインストール |
| `uv run pytest test/ -v` | 全テスト実行 |
| `uv run pytest test/test_coverage.py -v` | ユニットテストのみ |
| `uv run pytest test/test_simulator.py -v -s` | シミュレーターテスト |
| `uv run python -m py_compile src/compass_makecode.py` | 構文チェック |
| `uv run ruff check src/` | Lint チェック |
| `uv run ruff format src/` | コード自動整形 |

---

## トラブルシューティング

### `uv sync` が失敗する

```bash
# キャッシュをクリア
rm -rf .venv

# 再度同期
uv sync
```

### Playwright インストール失敗

```bash
uv run playwright install chromium
```

### テストがタイムアウトする

ネットワーク遅延の可能性があります。タイムアウト時間を延長：

```bash
uv run pytest test/test_simulator.py -v --timeout=60
```

### シミュレーターに接続できない

MakeCode Web のサーバーが一時的に不安定な可能性があります。

- しばらく待ってから再実行
- ネットワーク接続を確認

### カバレッジが 100% 未満

```bash
# 未カバーの行を確認
uv run pytest test/ -v --cov=compass_makecode --cov-report=term-missing

# HTML レポートで詳細確認
open htmlcov/index.html
```

### ビデオ記録が生成されない

```bash
# ffmpeg が インストール済みか確認
which ffmpeg

# インストール（必要に応じて）
brew install ffmpeg
```

---

## 学習課題

コンパスプログラムを改善・拡張するための学習課題：

1. **16 方位へ拡張**
   - 11.25° の境界値テストを設計する
   - NNE (北北東), ENE (東北東) などを追加

2. **追加テストケースの設計**
   - シミュレーターテストに複数のシナリオを追加
   - キャリブレーションの再実行テスト

3. **エラーハンドリング改善**
   - 磁気センサー利用不可時の処理
   - 異常値（999°, -999°）への対応

4. **移動平均フィルター**
   - 複数回の方位角から平均を求める
   - 359° と 1° の境界を工夫する

5. **傾き補正**
   - 加速度センサーとの組み合わせ
   - 傾いた状態での精度向上

6. **磁気干渉検出**
   - 実機を金属に近づけて揺らぎを記録
   - 干渉検出アルゴリズムの設計

---

## ドキュメント

- [`CLAUDE.md`](./CLAUDE.md) - AI アシスタント向けの詳細ガイド（テスト戦略・デバッグ）
- [`../compass_spec.md`](../compass_spec.md) - 共通アプリケーション仕様
- [`../CLAUDE.md`](../CLAUDE.md) - プロジェクト全体のガイド
- [`../HEX_BUILD_GUIDE.md`](../HEX_BUILD_GUIDE.md) - HEX ファイル生成手順

---

## ライセンス

[MIT License](../LICENSE)
