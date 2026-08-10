# CLAUDE.md - Python Compass Project Guide

このファイルは AI アシスタントが sample-compass プロジェクトで作業する際のガイドです。

**プロジェクト全体のガイドは `../CLAUDE.md` を参照してください。**  
**共通のアプリケーション仕様については、ルートディレクトリの [`../compass_spec.md`](../compass_spec.md) を参照してください。**

## プロジェクト概要

**目的**: micro:bit 用 Python 方位磁石アプリケーション（MakeCode 互換）

**特徴**:
- MakeCode のブロックエディターに変換可能な Static Python 実装
- Python 3.12.8 でのコンパイルチェック
- Playwright ベースのシミュレーターテスト
- GitHub Actions による CI/CD 統合

## ディレクトリ構造

```
sample-compass/
├── src/
│   └── compass_makecode.py  # MakeCode Python（メイン実装）
├── test/
│   └── test_simulator.py    # Playwright シミュレーターテスト
├── pyproject.toml           # uv プロジェクト設定・pytest 設定
├── CLAUDE.md                # このファイル
└── README.md
```

**注:** `.tool-versions` はルートディレクトリで一元管理されています。詳細は [`../.tool-versions`](../.tool-versions) を参照してください。

## テスト戦略

このプロジェクトは **3層のテスト戦略** を採用しています：

### 層1: 静的コンパイルチェック（Pre-commit Hook）
**目的**: Python 構文エラーを即座に検出
```bash
uv run python -m py_compile src/compass_makecode.py
```
- MakeCode へのブロック変換前の構文検証
- ローカル `pre-commit` hook で自動実行
- CI の最初のステップ

### 層2: Playwright シミュレーターテスト（Pre-push Hook + CI）
**目的**: MakeCode シミュレーター上での実装の動作確認
```bash
uv run pytest test/test_simulator.py -v
```
- micro:bit シミュレーター環境で compass.py の動作をテスト
- クリックシミュレーション、画面表示、ログ出力を検証
- `pre-push` hook と CI パイプライン (`integration-tests.yml`) で実行
- **完全な仕様検証**（UI/UX, キャリブレーション, 8方位判定を網羅）

### 層3: 実機デバイステスト（手動 / オプション）
**目的**: 実際の micro:bit ハードウェアでの動作確認
- ページレポート: 実機への `.hex` ファイルの書き込みと動作検証
- 本プロジェクトでは自動化されていません（手動テスト）

**戦略的配置:**
- 層1（コンパイル）: 全プッシュで実行、高速
- 層2（シミュレーター）: 全プッシュで実行、動作を完全検証
- 層3（実機）: 本番環境/最終リリース時に実施

### テストカバレッジ

**対象**: `src/compass_makecode.py`

```bash
# カバレッジレポート付きテスト実行
uv run pytest test/test_simulator.py --cov=src/compass_makecode.py --cov-report=html

# 100% 達成を CI で検査（全テスト実行時）
npm run test:python
```

- CI では 100% カバレッジが必須（`pyproject.toml` で設定）
- 設計段階でテスト可能性を優先

## 環境設定

### 必須ツール
- Python 3.12.8（asdf または pyenv で管理）
- uv（Python パッケージマネージャー）
- Playwright（ブラウザ自動化フレームワーク）

### 初期セットアップ

```bash
# 環境構築
uv sync

# 確認
uv run python --version  # Python 3.12.8
uv run pytest --version  # pytest >= 7.0
```

## よくある作業

### コンパイルチェックのみ
```bash
uv run python -m py_compile src/compass_makecode.py
```
- 構文チェックのみ（動作検証なし）
- 編集中の軽量な確認に便利

### シミュレーターテストを実行
```bash
# 全テスト
uv run pytest test/test_simulator.py -v

# 特定のテストのみ
uv run pytest test/test_simulator.py -v -k "test_name"

# 詳細ログ付き
uv run pytest test/test_simulator.py -v -s
```

### 新しいテストを追加する

**例: ボタン B 押下時の動作テスト**

```python
# test/test_simulator.py に追加
async def test_button_b_press(page):
    """ボタン B 押下時の動作をテスト"""
    await page.goto("...")
    
    # キャリブレーション完了
    compass = Compass()  # または page.evaluate などでシミュレーターを操作
    compass.calibrate()
    
    # ボタン B を押下（シミュレーター上で）
    # ... ページ操作コード ...
    
    # 期待される動作を検証
    # ... assertion ...
```

### テストが失敗した場合

```bash
# 詳細なエラーメッセージを表示
uv run pytest test/test_simulator.py -v -s

# スタックトレースを含めて表示
uv run pytest test/test_simulator.py -v --tb=long
```

## MakeCode Python の特性

### Static Python とは
- MakeCode が **ブロックエディターに自動変換可能** な Python のサブセット
- 型ヒント、デコレータ、複雑な制御構文が制限される
- micro:bit の制限されたメモリ上で実行可能

### compass_makecode.py の制約
- グローバル変数や複数の関数定義は使用可
- クラスは限定的なサポート
- 型ヒントは使用可（読み込み時に変換）

### 検証方法
1. **構文チェック** (`py_compile`) で基本的な制約を確認
2. **シミュレーター** で MakeCode 環境での動作を検証
3. **実機** で最終検証（オプション）

## コード規約

### Python スタイル
- **PEP 8 準拠** （可能な範囲で）
- **型ヒント使用** - `def get_heading() -> float:` のように明示
- **docstring 使用** - 関数・モジュールの説明

**例:**
```python
"""
Compass application for micro:bit

This module provides calibration and direction detection for the micro:bit compass sensor.
"""

def calibrate_compass() -> None:
    """
    Calibrate the compass sensor.
    
    Displays a diamond pattern on LED grid during calibration.
    """
    pass
```

### MakeCode 互換性のチェックリスト
- [ ] `py_compile` で構文エラーなし
- [ ] グローバル変数は最小限に
- [ ] クラス使用は慎重に（MakeCode サポート限定）
- [ ] 複雑な制御構文は避ける
- [ ] シミュレーターテストで動作確認

## コード品質チェック

### Ruff（リンター + フォーマッター）
```bash
# リントチェック
uv run ruff check src/compass_makecode.py

# 自動修正
uv run ruff check --fix src/compass_makecode.py

# コード整形
uv run ruff format src/compass_makecode.py
```

**設定** (`pyproject.toml` / `[tool.ruff]`):
- 行幅: 100字
- ターゲット: Python 3.12
- ルール: E（エラー）, F（Pyflakes）, W（警告）, I（import）, N（命名）, UP（アップグレード）, B（バグベア）, C4（comprehension）
- `E501`（行長）はoff（別途チェック）

### 構文チェック
```bash
# MakeCode へのブロック変換前に実行
uv run python -m py_compile src/compass_makecode.py
```

## Git Hooks 連携

### Pre-commit Hook
コミット前に自動実行：
```bash
uv run python -m py_compile src/compass_makecode.py
```

### Pre-push Hook
プッシュ前に以下を実行：
```bash
uv run pytest test/test_simulator.py -v
```

詳細は `../.husky/` を参照。

## トラブルシューティング

### `uv sync` が失敗する
```bash
# キャッシュをクリア
rm -rf .venv

# 再度同期
uv sync
```

### Playwright でシミュレーターに接続できない
```bash
# ブラウザをクリア
uv run playwright install

# テスト再実行
uv run pytest test/test_simulator.py -v
```

### コンパイルチェックは通るが、シミュレーターテストが失敗
- シミュレーター環境での MakeCode API の使用方法が異なる可能性
- `test_simulator.py` のテストコードを参考に、ページ操作を確認
- console.log や LED 表示の検証が正しいか確認

### pyproject.toml の testpaths が機能しない
```bash
# 直接パスを指定
uv run pytest test/test_simulator.py -v
```

## CI/CD 統合

### GitHub Actions ワークフロー
`.github/workflows/integration-tests.yml` で以下を実行：
1. Python 3.12.8 環境をセットアップ
2. `uv sync` で依存関係をインストール
3. `pytest test/test_simulator.py -v` を実行

### ローカルでのテスト
```bash
# すべてのプロジェクトのテストをシミュレート
cd ..
npm run test:all
```

## 外部リソース

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [MakeCode JavaScript Blocks](https://makecode.microbit.org/reference)
- [Playwright Python](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
