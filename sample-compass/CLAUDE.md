# CLAUDE.md - Python Compass Project Guide

このファイルは AI アシスタント（Claude、Copilot など）が sample-compass プロジェクトで作業する際の指南書です。

## プロジェクト概要

**目的**: micro:bit 用 Python 方位磁石アプリケーション

**特徴**:
- シンプルな Compass クラスで方位磁石の機能を実装
- 方位角（0-359度）から8方位（N, NE, E, SE, S, SW, W, NW）への変換
- キャリブレーション機能

## ディレクトリ構造

```
sample-compass/
├── compass.py           # Main implementation
├── test_compass.py      # Unit tests (13 tests)
├── e2e_test_compass.py  # E2E tests (12 tests)
├── README.md
└── .tool-versions       # Python version management
```

## テスト実行方法

### ユニットテスト
```bash
cd sample-compass
python3 -m pytest test_compass.py -v
```

### E2E テスト
```bash
cd sample-compass
python3 -m pytest e2e_test_compass.py -v
```

### 全テスト（ユニット + E2E）
```bash
cd sample-compass
python3 -m pytest -v
```

### カバレッジ付き実行
```bash
cd sample-compass
python3 -m pytest --cov=compass --cov-report=html
```

## コード規約

### ファイル命名規則
- 実装ファイル: `snake_case.py`
- テストファイル: `test_*.py` または `*_test.py`
- E2E テスト: `e2e_*.py`

### Python スタイル
- PEP 8 に厳密に準拠
- docstring は Google スタイル
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
- テストでは MockCompass を使用して実際のデバイスなしでテスト可能
- インスタンス変数: `self.heading`, `self.calibrated`

## 重要な関数・メソッド

### `Compass` クラス

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `__init__()` | 初期化 | なし |
| `calibrate()` | キャリブレーション実行 | なし |
| `get_heading()` | 現在の方位角を取得 | int (0-359) |
| `get_direction()` | 現在の方角を取得 | str (N/NE/E/SE/S/SW/W/NW) |
| `_heading_to_direction(heading)` | 方位角を方角に変換（静的） | str |

### 方位計算ロジック
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

境界値：
- N: 337.5° 以上 または 22.5° 未満
- NE: 22.5° 以上 67.5° 未満
- 以降 45° ごとに区切る

## よくある作業

### 新しいテストを追加する

**ユニットテスト**:
```python
# test_compass.py に追加
def test_new_direction():
    """新しい方角判定のテスト"""
    compass = MockCompass()
    compass.heading = 50  # NE 方向
    assert compass.get_direction() == 'NE'
```

**E2E テスト**:
```python
# e2e_test_compass.py の TestCompassE2E クラスに追加
def test_new_scenario(self, compass):
    """新しいシナリオのテスト"""
    compass.calibrate()
    compass.set_heading(90)
    assert compass.get_direction() == 'E'
```

### 新機能を追加する

1. テストを先に書く（TDD）:
   ```python
   def test_new_method():
       compass = MockCompass()
       result = compass.new_method()
       assert result == expected_value
   ```

2. テストが失敗することを確認:
   ```bash
   python3 -m pytest test_compass.py::test_new_method -v
   ```

3. 実装を追加:
   ```python
   def new_method(self):
       """新しいメソッドの説明"""
       return calculated_value
   ```

4. テストが成功することを確認:
   ```bash
   python3 -m pytest test_compass.py::test_new_method -v
   ```

5. リファクタリング（必要に応じて）

## テスト戦略

### ユニットテスト (test_compass.py)
- **13 個のテスト**
- MockCompass を使用した単体テスト
- 各メソッドの正確性を確認
- 境界値テスト含む

テストカバレッジ:
- `__init__()`: 初期化状態の確認
- `calibrate()`: キャリブレーション状態の更新
- `get_heading()`: 方位角の取得
- `get_direction()`: 8方位すべてについて検証
- 境界値: 22.5°, 67.5°, 112.5°, 157.5°, 202.5°, 247.5°, 292.5°, 337.5°

### E2E テスト (e2e_test_compass.py)
- **12 個の統合テスト**
- 実際のユースケースに基づいたシナリオテスト
- ワークフロー全体の検証

テストシナリオ:
1. 完全なワークフロー（初期化→キャリブレーション→方角確認）
2. 8方位全体の判定
3. 境界値での正確な遷移
4. 北でのラップアラウンド
5. 360° 連続回転シミュレーション
6. 連続クエリの一貫性
7. 複数インスタンスの独立動作
8. 無効な入力の拒否
9. キャリブレーション状態の永続性
10. パフォーマンス（10000回実行）
11. 方角の一貫性（1000回クエリ）
12. 包括的なワークフロー検証

## よくある問題とトラブルシューティング

### pytest が見つからない
```bash
python3 -m pip install pytest pytest-cov
```

### テストが検出されない
```bash
# テストファイルの命名を確認
# test_*.py または *_test.py である必要があります
ls -la test_*.py e2e_*.py
```

### カバレッジレポートが生成されない
```bash
python3 -m pip install pytest-cov
python3 -m pytest --cov=compass --cov-report=html
# htmlcov/index.html を開く
```

### 単一テストだけを実行したい
```bash
# テスト関数を指定
python3 -m pytest test_compass.py::test_compass_init -v

# クラスとメソッドを指定
python3 -m pytest test_compass.py::TestCompass::test_calibrate -v

# E2E テストのみ
python3 -m pytest e2e_test_compass.py -v

# パターンマッチで実行
python3 -m pytest test_compass.py -k "direction" -v
```

## Git Hooks との連携

### Pre-commit Hook
コミット前に自動的に以下が実行されます：
```bash
python3 -m pytest test_compass.py -v
python3 -m pytest e2e_test_compass.py -v
```

### Pre-push Hook
プッシュ前に全テストが実行されます：
```bash
python3 -m pytest test_compass.py -v
python3 -m pytest e2e_test_compass.py -v
```

## GitHub Actions での実行

`.github/workflows/python-tests.yml` で自動実行：
- Python 3.11（最新安定版）
- push と PR トリガー
- カバレッジレポートを codecov に送信

## 推奨される変更ワークフロー

1. ブランチを作成:
   ```bash
   git checkout -b feature/add-new-direction
   ```

2. 新しいテストを書く:
   ```bash
   # test_compass.py または e2e_test_compass.py に追加
   ```

3. テストが失敗することを確認:
   ```bash
   python3 -m pytest test_compass.py -v
   ```

4. 実装を追加:
   ```bash
   # compass.py を編集
   ```

5. すべてのテストが成功することを確認:
   ```bash
   python3 -m pytest -v
   ```

6. コミット（hooks が自動実行）:
   ```bash
   git commit -m "Add new feature"
   ```

7. プッシュ（hooks が全テスト実行）:
   ```bash
   git push origin feature/add-new-direction
   ```

8. PR を作成（GitHub Actions が自動実行）

## 外部リソース

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide - Docstring](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)

## 環境設定

### 必須パッケージ
```bash
python3 -m pip install pytest pytest-cov
```

### Python バージョン
- 推奨: Python 3.11（`.tool-versions` で指定）
- 最小: Python 3.9

### asdf でバージョン管理する場合
```bash
asdf install python 3.11.5
asdf local python 3.11.5
```

## 質問や改善提案

このファイルは継続的に改善されています。
プロジェクトのベストプラクティスを発見したら、このファイルを更新してください。
