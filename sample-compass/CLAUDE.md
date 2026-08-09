# CLAUDE.md - Python Compass Project Guide

このファイルは AI アシスタント（Claude、Copilot など）が sample-compass プロジェクトで作業する際のプロジェクト固有ガイドです。

**プロジェクト全体のガイドは `../CLAUDE.md` を参照してください。**

## プロジェクト概要

**目的**: micro:bit 用 Python 方位磁石アプリケーション

**特徴**:
- シンプルな Compass クラスで方位磁石の機能を実装
- 方位角（0-359度）から8方位への変換
- テスト: ユニット、HEX生成、モック環境での統合テスト

## ディレクトリ構造

```
sample-compass/
├── compass.py           # Main implementation
├── test_compass.py      # Unit tests
├── test_build_hex.py    # HEX build tests
├── test_compass_integration.py # Integration tests with mocked micro:bit APIs
├── pyproject.toml       # uv project configuration
├── CLAUDE.md            # このファイル
├── README.md
└── .tool-versions       # Python version management (3.11.5)
```

## テスト実行方法

### ユニットテスト
```bash
uv run pytest test_compass.py -v
```

### 統合テスト
```bash
uv run pytest test_compass_integration.py -v
```

### 全テスト
```bash
uv run pytest -v
```

### 特定のテストのみ実行
```bash
# テスト関数を指定
uv run pytest test_compass.py::test_compass_init -v

# クラスとメソッド
uv run pytest test_compass.py::TestCompass::test_calibrate -v

# パターンマッチ
uv run pytest test_compass.py -k "direction" -v
```

### カバレッジ付き実行
```bash
uv run pytest --cov=compass --cov-report=html
```

## Python コード規約

### ファイル命名規則
- 実装ファイル: `snake_case.py` （例: `compass.py`）
- テストファイル: `test_*.py` または `*_test.py`
- 統合テスト: `test_*_integration.py`

### Python スタイル
- **PEP 8** に厳密に準拠
- **docstring は Google スタイル**
  ```python
  def get_direction(self):
      """
      現在の方角を取得する
      
      Returns:
          str: 'N'（北）、'S'（南）、'E'（東）、'W'（西）、'NE'、'NW'、'SE'、'SW'
      """
  ```

### クラス設計
- Compass クラスは micro:bit API に依存しない
- テストでは MockCompass を使用（デバイスなしでテスト可能）
- インスタンス変数: `self.heading`, `self.calibrated`

## 重要なメソッド

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `calibrate()` | キャリブレーション実行 | None |
| `get_heading()` | 現在の方位角を取得 | int (0-359) |
| `get_direction()` | 現在の方角を取得 | str (N/NE/E/SE/S/SW/W/NW) |
| `_heading_to_direction(heading)` | 方位角を方角に変換 | str |

## テスト戦略

### ユニットテスト (test_compass.py) - 13個
- 初期化状態の確認
- キャリブレーション状態の更新
- 8方位すべての判定
- 境界値テスト（22.5°, 67.5°, 112.5° など）

### 統合テスト (test_compass_integration.py)
- 完全なワークフロー（初期化→キャリブレーション→方角確認）
- 8方位全体の判定
- 境界値での正確な遷移
- 北でのラップアラウンド（359° → 0°）
- 360° 連続回転シミュレーション
- 複数インスタンスの独立動作
- 無効な入力の拒否
- パフォーマンステスト（10000回実行）

## よくある作業

### 新しいテストを追加する

**ユニットテスト**:
```python
# test_compass.py に追加
def test_new_direction():
    """新しい方角判定のテスト"""
    compass = MockCompass()
    compass.heading = 50  # NE方向
    assert compass.get_direction() == 'NE'
```

**統合テスト**:
```python
# test_compass_integration.py の TestCompassIntegration クラスに追加
def test_new_scenario(self, compass):
    """新しいシナリオのテスト"""
    compass.calibrate()
    compass.heading = 90
    assert compass.get_direction() == 'E'
```

### 新機能を追加する（TDD）

1. テストを先に書く
2. テスト実行（失敗）
3. 実装を追加
4. テスト実行（成功）
5. 必要に応じてリファクタリング

```bash
# テスト実行
uv run pytest test_compass.py::test_new_method -v

# 実装追加後
uv run pytest test_compass.py::test_new_method -v
```

### Git Hooks 連携

### Pre-commit Hook
コミット前に自動実行：
```bash
uv run pytest test_compass.py -v
uv run pytest test_compass_integration.py -v
```

### Pre-push Hook
プッシュ前に全テスト実行

詳細は `../.husky/` を参照。

## トラブルシューティング

### pytest が見つからない
```bash
uv sync
```

### テストが検出されない
```bash
# テストファイル名を確認
# test_*.py または *_test.py である必要があります
ls -la test_*.py
```

### 特定のテストだけを実行したい
```bash
# テスト関数を指定
uv run pytest test_compass.py::TestCompass::test_calibrate -v

# キーワードで実行
uv run pytest -k "direction" -v
```

### カバレッジレポートが表示されない
```bash
uv run pytest --cov=compass --cov-report=html
# htmlcov/index.html をブラウザで開く
```

## 環境設定

### 必須パッケージ
```bash
uv sync
```

### Python バージョン
- 推奨: Python 3.11.5（`.tool-versions` で指定）
- 最小: Python 3.9

### asdf でバージョン管理する場合
```bash
asdf install python 3.11.5
asdf local python 3.11.5
```

## CI/CD

### GitHub Actions
`.github/workflows/python-tests.yml` で自動実行：
- Python 3.11 でテスト
- push と PR トリガー
- カバレッジレポートを codecov に送信

### ローカルテスト
```bash
# すべてのテストを実行
uv run pytest -v --cov=compass
```

## 方位計算ロジック

```
0°: N (北)
45°: NE (北東)
90°: E (東)
135°: SE (南東)
180°: S (南)
225°: SW (南西)
270°: W (西)
315°: NW (北西)
```

### 境界値
- N: 337.5° 以上 または 22.5° 未満
- NE: 22.5° 以上 67.5° 未満
- 以降 45° ごとに区切る

## 外部リソース

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Docstring Guide](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)
