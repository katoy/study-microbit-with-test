# sample-compass: Python版

[![Integration Tests](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml/badge.svg?branch=main)](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml)

> **📚 参照**: プロジェクト全体については [`../README.md`](../README.md) を、開発ガイドについては [`CLAUDE.md`](./CLAUDE.md) を参照してください。

micro:bit方位磁石のPython教材です。MakeCodeのブロックへ変換できるStatic Pythonを扱っています。

## 概要

**目的**: Python 3.12.8 で MakeCode 互換の方位磁石アプリケーションを実装・テスト

**テスト戦略**:
1. **コンパイルチェック** (`py_compile`) - 構文検証
2. **シミュレーターテスト** (`pytest` + Playwright) - MakeCode 環境での動作検証
3. **実機テスト** - 手動による micro:bit での動作確認

詳細は [`CLAUDE.md`](./CLAUDE.md) を参照。

## ファイル構成

| ファイル | 実行環境 | センサーAPI | ブロック変換 |
|---|---|---|---|
| [`compass_makecode.py`](./src/compass_makecode.py) | MakeCode Python | `input.compass_heading()` | 対応 |

## セットアップ

```bash
# プロジェクト依存関係のインストール
cd sample-compass
uv sync

# ブラウザ自動化ツールのセットアップ（初回のみ）
uv run playwright install chromium
```

## よく使うコマンド

| コマンド | 説明 |
|---|---|
| `uv run python -m py_compile src/compass_makecode.py` | 構文チェック |
| `uv run pytest test/test_simulator.py -v` | シミュレーターテスト実行 |
| `uv run pytest test/test_simulator.py -v -s` | 詳細ログ付きテスト |

## テスト実行

### 構文チェック（高速）
```bash
uv run python -m py_compile src/compass_makecode.py
```
- Pre-commit hook で自動実行
- MakeCode への変換前のバリデーション

### シミュレーターテスト（完全検証）
```bash
uv run pytest test/test_simulator.py -v
```
- Playwright で MakeCode Web シミュレーター上での動作を検証
- 45度ずつの回転と LED 表示パターンを確認
- Pre-push hook と CI パイプラインで実行
- 最も重要なテスト

### ブロック変換検証
```bash
cd ..
npm run verify:blocks
```
- MakeCode Web でコードをブロックに変換可能か確認
- 変換エラーやグレーブロックをチェック
- ネットワーク接続が必要

## MakeCode で実行する

1. <https://makecode.microbit.org/> で新規プロジェクト作成
2. Python へ切り替え
3. [`src/compass_makecode.py`](./src/compass_makecode.py) の内容をコピーペースト
4. ブロックへ切り替えて変換を確認
5. シミュレーター（または実機）で動作確認

## CI/CD 統合

### GitHub Actions
`.github/workflows/integration-tests.yml` で自動実行：
- Python 3.12.8 環境をセットアップ
- `uv sync` で依存関係をインストール
- `pytest test/test_simulator.py -v` でテスト実行
- すべて成功してから CI の他の実装テストへ

### ローカルテスト
```bash
# ルートディレクトリから
npm run test:python     # Python テストのみ
npm run test:all        # すべての実装をテスト
```

## トラブルシューティング

### `uv sync` が失敗する
```bash
rm -rf .venv
uv sync
```

### Playwright インストール失敗
```bash
uv run playwright install chromium
```

### テストがタイムアウトする
- ネットワーク遅延の可能性
- `pytest test/test_simulator.py -v --timeout=30` で制限時間を設定

### シミュレーターに接続できない
- MakeCode Web の サーバーが一時的に不安定な可能性
- しばらく待ってから再実行

## ドキュメント

- [`CLAUDE.md`](./CLAUDE.md) - AI アシスタント向けの詳細ガイド（テスト戦略・デバッグ方法）
- [`../compass_spec.md`](../compass_spec.md) - 共通アプリケーション仕様
- [`../CLAUDE.md`](../CLAUDE.md) - プロジェクト全体のガイド
- [`../HEX_BUILD_GUIDE.md`](../HEX_BUILD_GUIDE.md) - HEX ファイル生成手順

## 学習課題

- **16 方位** へ拡張し、11.25 度の境界テストを設計する
- シミュレーターテストに **追加のテストケース** を設計する
- **エラーハンドリング** を改善する（磁気センサーが利用不可な場合など）
- 複数回の方位角から**移動平均**を求め、359 度と 1 度の扱いを工夫する
- 加速度センサーを組み合わせた**傾き補正**の入力を設計する
- 実機を安全な金属へ近づけ、方位角の揺れという**磁気干渉**を記録する

## ライセンス

[MIT License](../LICENSE)
