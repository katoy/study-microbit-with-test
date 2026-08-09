# sample-compass

micro:bit 用のシンプルな方位磁石アプリケーション（Python 実装）

> [!NOTE]  
> AIアシスタント（Antigravity, Claude, Copilot, Cursor）の環境設定や、プロジェクト共通のカスタムスキル同期方法については、ルートの [`../README.md`](file:///Users/katoy/github/study-microbit-with-test/README.md#aiアシスタント連携) を参照してください。

## Table of Contents

- [機能](#機能)
- [インストール](#インストール)
- [使用方法](#使用方法)
- [テスト](#テスト)
- [HEX ファイル生成](#hex-ファイル生成)
- [プロジェクト構成](#プロジェクト構成)
- [ファイル一覧](#ファイル一覧)
- [API リファレンス](#api-リファレンス)
- [CI/CD](#cicd)
- [テストカバレッジ](#テストカバレッジ)
- [ライセンス](#ライセンス)
- [参考リンク](#参考リンク)

## 機能

- 🧭 **方位角検出**: 0-359 度の方位角を取得
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- 🔄 **キャリブレーション**: ボタンA でコンパスをキャリブレーション
- 📦 **HEX ファイル生成**: uflash でV1/V2対応のUniversal Hexを生成

## インストール

### 開発環境セットアップ

```bash
cd sample-compass
uv sync
```

### micro:bit へのデプロイ

HEX ファイルを生成して転送する方法：

```bash
# HEX ファイルを生成
uv run python build_hex.py

# 生成されたファイルを確認
ls -l dist/hex/compass.hex

# uflash でデバイスに転送（uflash インストール済みの場合）
uflash compass.py
```

### Python 実行環境の差異とデプロイ方法

本教材では、micro:bit における Python の2つの主要な実行環境に対応しています。用途に合わせてファイルを選択してください。

| 特徴 | MicroPython (`compass.py`) | MakeCode Python (`compass_makecode.py`) |
| :--- | :--- | :--- |
| **用途** | 実機への直接書き込み・ローカル単体テスト | MakeCode エディタでのブロック相互変換・シミュレータ |
| **ライブラリ** | `from microbit import *` を明示的インポート | インポート不要（グローバルAPI） |
| **言語仕様** | 標準の Python 3 に近い (クラスや try-except をサポート) | 静的型付けの TypeScript にトランスパイルされる制限版 |
| **ブロック変換**| 不可 | **可能**（Pythonコードとビジュアルブロックの相互変換） |
| **書き込み方法** | `uflash` CLI 等で直接 HEX 転送 | Web エディタ経由で HEX をダウンロードして転送 |

#### 1. 標準の MicroPython を使用する場合
`compass.py` を実機に転送するか、`uflash` で書き込みます：
```bash
# uflash でデバイスに転送
uflash compass.py
```

#### 2. MakeCode Editor (Pythonモード) を使用する場合
1. [MakeCode Editor](https://makecode.microbit.org/) を開く
2. **Python** モードに切り替える
3. [`compass_makecode.py`](file:///Users/katoy/github/study-microbit-with-test/sample-compass/compass_makecode.py) の内容をコピー＆ペースト
4. 「ブロック」ボタンを押すと、自動的にビジュアルブロックに変換されます
5. **Download** をクリックして micro:bit に書き込みます

### エッジケースとエラーハンドリング

本プログラムでは、以下の組み込み開発特有のエッジケースに対応しています。

1. **未キャリブレーション（校正）状態のハンドリング**:
   - 初期状態のまま方位表示（`display_direction()`）を呼び出すと、方位ではなく `"CAL"` という警告文字がスクロール表示され、ボタンAによるキャリブレーションを促します。
2. **センサー異常値（負の値など）のハンドリング**:
   - センサー取得時に `-1` などの無効値が返ってきた場合、キャリブレーション状態を自動で未完了（`False`）に戻し、再校正が必要なことを示します。

## 使用方法

1. micro:bit 上で実行すると、LED ディスプレイに現在の方向と角度が表示されます
2. ボタンA を押すとコンパスをキャリブレーションします

## テスト

### ユニットテスト

```bash
uv run pytest test_compass.py -v
```

### 統合テスト

```bash
uv run pytest test_compass_integration.py -v
```

micro:bit APIをモック化したプロセス内テストです。実機のセンサーやUSB転送までは検証しません。

### 全テスト実行

```bash
uv run pytest -v
```

### テストカバレッジ

```bash
uv run pytest --cov=compass --cov-report=html
# htmlcov/index.html をブラウザで開く
```

## HEX ファイル生成

### 生成コマンド

```bash
uv run python build_hex.py
```

### 出力ファイル

生成されたファイルは `dist/hex/compass.hex` に保存されます。

```bash
ls -lh dist/hex/
```

### uflash

`uflash==2.0.0` はプロジェクト依存関係に固定されています。通常は次のセットアップだけで導入されます：

```bash
uv sync
```

コンパイラが利用できない場合や出力が不正な場合、ビルドは失敗し、代替のダミーHEXは生成しません。

## プロジェクト構成

```
sample-compass/
├── compass.py               # メイン実装（方位磁石ロジック）
├── test_compass.py          # ユニットテスト（17 個）
├── test_build_hex.py        # HEX生成テスト（4 個）
├── test_compass_integration.py # モック環境での統合テスト
├── build_hex.py             # HEX ファイル生成スクリプト
├── conftest.py              # pytest 設定
├── pyproject.toml           # uv プロジェクト設定
├── .gitignore               # Git 除外設定
├── .tool-versions           # Python バージョン管理
├── CLAUDE.md                # AI 開発ガイド
└── README.md                # このファイル
```

## ファイル一覧

### ソースコード

| ファイル | 説明 | 行数 |
|---------|------|------|
| `compass.py` | Compass クラスと関連関数 | ~50 |
| `conftest.py` | pytest 設定・フィクスチャ | ~20 |

### テスト

| ファイル | 説明 | テスト数 |
|---------|------|---------|
| `test_compass.py` | ユニットテスト | 17 |
| `test_build_hex.py` | HEX生成テスト | 4 |
| `test_compass_integration.py` | モック環境での統合テスト | 13 |

### ビルド・設定

| ファイル | 説明 |
|---------|------|
| `build_hex.py` | HEX ファイル生成スクリプト |
| `.gitignore` | Git 除外設定 |
| `.tool-versions` | Python バージョン管理（asdf） |

### ドキュメント

| ファイル | 説明 |
|---------|------|
| `README.md` | このファイル |
| `CLAUDE.md` | AI 開発ガイド |

### ディレクトリ

| ディレクトリ | 説明 | .gitignore |
|-----------|------|-----------|
| `dist/` | ビルド出力ディレクトリ | ✅ 除外 |
| `dist/hex/` | 生成された HEX ファイル | ✅ 除外 |

## API リファレンス

### `Compass` クラス

#### メソッド

- `calibrate()` - コンパスをキャリブレーション
- `get_heading()` - 方位角を取得（0-359 度）
- `get_direction()` - 方角を取得（N, NE, E, SE, S, SW, W, NW）
- `display_direction()` - 現在の方角と方位角を LED ディスプレイにスクロール表示
- `_heading_to_direction(heading)` - 方位角を方角に変換する内部ヘルパー

#### 使用例

```python
from compass import Compass

compass_app = Compass()
compass_app.calibrate()

print(compass_app.get_heading())
print(compass_app.get_direction())
compass_app.display_direction()
```

## CI/CD

GitHub Actions で自動的に以下が実行されます:

- ✅ pytest でのユニットテスト（Python 3.11）
- ✅ モック環境での統合テスト
- ✅ テストカバレッジの計測
- ✅ Codecov へのアップロード

詳細は `.github/workflows/python-tests.yml` を参照してください。

## テストカバレッジ

目標: **100%** のコードカバレッジ

- Compass クラスの全メソッド
- 全 8 方位のテスト
- 境界値とエッジケースのテスト
- エラーハンドリングのテスト

カバレッジレポート確認：

```bash
uv run pytest --cov=compass --cov-report=html
# htmlcov/index.html をブラウザで開く
```

## Cleanup

中間ファイルやキャッシュを削除：

```bash
# プロジェクト全体から実行
../scripts/clean.sh sample-compass

# またはルートディレクトリから
./scripts/clean.sh sample-compass
```

削除されるファイル（Git追跡中のパスは保持されます）：
- `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.coverage`, `coverage.xml`, `htmlcov/`
- `.venv/`, `.egg-info/`
- `dist/`, `build/`

`uv.lock` は削除されません。

## ライセンス

**MIT License**

このプロジェクトは MIT ライセンスの下で公開されています。
自由に使用、変更、配布できます。

## 参考リンク

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [uflash GitHub](https://github.com/ntoll/uflash)
