# sample-compass

micro:bit 用のシンプルな方位磁石アプリケーション（Python 実装）

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
- 📦 **HEX ファイル生成**: micro:bit 転送用の HEX ファイルを自動生成

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

または MakeCode Editor で手動転送：

1. [MakeCode Editor](https://makecode.microbit.org/) を開く
2. Python モードに切り替え
3. `compass.py` の内容をコピー＆ペースト
4. Download をクリック

## 使用方法

1. micro:bit 上で実行すると、LED ディスプレイに現在の方向と角度が表示されます
2. ボタンA を押すとコンパスをキャリブレーションします

## テスト

### ユニットテスト

```bash
uv run pytest test_compass.py -v
```

### E2E テスト

```bash
uv run pytest e2e_test_compass.py -v
```

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

### オプション：uflash のインストール

より正式な HEX ファイルを生成するには uflash をインストール：

```bash
uv pip install uflash
```

その後、スクリプトが uflash を自動検出して使用します。

## プロジェクト構成

```
sample-compass/
├── compass.py               # メイン実装（方位磁石ロジック）
├── test_compass.py          # ユニットテスト（13 個）
├── e2e_test_compass.py      # E2E テスト（12 個）
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
| `test_compass.py` | ユニットテスト | 13 |
| `e2e_test_compass.py` | E2E テスト | 12 |

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
- `set_heading(heading)` - 方位角を設定（テスト用）
- `get_direction()` - 方角を取得（N, NE, E, SE, S, SW, W, NW）
- `get_calibrated()` - キャリブレーション状態を取得
- `get_state()` - 現在の状態を取得
- `_heading_to_direction(heading)` - 方位角を方角に変換

#### 使用例

```python
from compass import Compass

compass = Compass()
compass.calibrate()
compass.set_heading(90)

print(compass.get_direction())  # 'E'
print(compass.get_heading())    # 90
print(compass.get_state())      # {'heading': 90, 'direction': 'E', 'calibrated': True}
```

## CI/CD

GitHub Actions で自動的に以下が実行されます:

- ✅ pytest でのユニットテスト（Python 3.11）
- ✅ E2E テスト
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

削除されるファイル：
- `__pycache__/`, `.pytest_cache/`, `.coverage/`, `htmlcov/`
- `.venv/`, `.egg-info/`
- `dist/`, `build/`
- `uv.lock`

## ライセンス

**MIT License**

このプロジェクトは MIT ライセンスの下で公開されています。
自由に使用、変更、配布できます。

## 参考リンク

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [uflash GitHub](https://github.com/ntoll/uflash)
