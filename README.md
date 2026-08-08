# study-microbit-with-test

[![Python Tests](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions/workflows/python-tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions)
[![TypeScript Tests](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions/workflows/typescript-tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/study-microbit-with-test/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/study-microbit-with-test)

micro:bit 用のシンプルな方位磁石アプリケーション学習プロジェクト

**テスト状況**: 96/96 テスト成功 ✅ | **カバレッジ**: 100% (Python 100%, TypeScript 100%)

## Table of Contents

- [概要](#概要)
- [プロジェクト構成](#プロジェクト構成)
- [プログラム概要](#プログラム概要)
- [セットアップ](#セットアップ)
- [テスト実行](#テスト実行)
- [ビルド](#ビルド)
- [HEX ファイル生成](#hex-ファイル生成)
- [Cleanup Scripts](#cleanup-scripts)
- [CI/CD](#cicd)
- [npm Scripts リファレンス](#npm-scripts-リファレンス)
- [ライセンス](#ライセンス)
- [参考リンク](#参考リンク)

## 概要

3つのサンプル実装を含んでいます：
- **sample-compass**: Python による実装（micro:bit API を使用）
- **sample-compass-ts**: TypeScript による実装（Jest テスト付き）
- **sample-compass-makecode**: MakeCode Editor 用の実装

## プロジェクト構成

```
.
├── sample-compass/           # Python 実装
├── sample-compass-ts/        # TypeScript 実装
├── sample-compass-makecode/  # MakeCode 実装
├── .github/workflows/        # GitHub Actions CI/CD
├── CLAUDE.md                 # プロジェクト全体の開発ガイド
├── HEX_BUILD_GUIDE.md        # HEX ファイル生成ガイド
├── GIT_HOOKS_GUIDE.md        # Git Hooks ガイド
├── GIT_HOOKS_SETUP.md        # Git Hooks セットアップ
├── package.json              # ルートプロジェクト設定
└── README.md                 # このファイル
```

詳細は各プログラムのディレクトリの CLAUDE.md を参照してください。

## セットアップ

### Python 環境（sample-compass）

```bash
cd sample-compass
uv sync
```

### TypeScript 環境（sample-compass-ts）

```bash
cd sample-compass-ts
npm install
```

## テスト実行

### すべてのテスト実行

```bash
# ルートディレクトリから
npm run test:all

# または個別に
npm run test:python && npm run test:ts
```

### Python テスト

```bash
cd sample-compass
uv run pytest test_compass.py -v           # ユニットテスト
uv run pytest e2e_test_compass.py -v       # E2E テスト
uv run pytest -v                           # 全テスト
```

### TypeScript テスト

```bash
cd sample-compass-ts
npm test                            # 全テスト
npm run test:unit                   # ユニットテストのみ
npm run test:e2e                    # E2E テストのみ
npm run test:coverage               # カバレッジレポート付き
npm run test:watch                  # ウォッチモード
```

## ビルド

### TypeScript のビルド

```bash
cd sample-compass-ts
npm run build
```

## HEX ファイル生成

micro:bit に転送可能な HEX ファイルを生成できます。

### すべてのプロジェクトから HEX を生成

```bash
npm run build:hex
```

### 個別プロジェクトから HEX を生成

```bash
# TypeScript
cd sample-compass-ts
npm run build:hex

# Python
cd sample-compass
uv run python build_hex.py
```

生成された HEX ファイルは各プロジェクトの `dist/hex/` ディレクトリに保存されます：

```
sample-compass/dist/hex/compass.hex
sample-compass-ts/dist/hex/compass.hex
```

詳細は [HEX_BUILD_GUIDE.md](./HEX_BUILD_GUIDE.md) を参照してください。

## CI/CD

このプロジェクトは GitHub Actions を使用して自動的にテストを実行します。

- **Python テスト**: `sample-compass/` のテストが実行されます
- **TypeScript テスト**: `sample-compass-ts/` のテストが実行されます
- **E2E テスト**: 全プロジェクトの統合テストが実行されます

詳細は `.github/workflows/` を参照してください。

## npm Scripts リファレンス

### テスト

| コマンド | 説明 |
|---------|------|
| `npm run test:python` | Python ユニットテスト |
| `npm run e2e:python` | Python E2E テスト |
| `npm run test:ts` | TypeScript テスト |
| `npm run e2e:ts` | TypeScript E2E テスト |
| `npm run test` | 全ユニットテスト |
| `npm run e2e` | 全 E2E テスト |
| `npm run test:all` | 全テスト（ユニット + E2E） |

### ビルド

| コマンド | 説明 |
|---------|------|
| `npm run build:hex` | 全プロジェクトの HEX ファイルを生成 |
| `npm run build:hex:python` | Python HEX ファイルを生成 |
| `npm run build:hex:ts` | TypeScript HEX ファイルを生成 |

## Cleanup Scripts

中間ファイルやキャッシュを削除するスクリプトが利用可能です。

```bash
# すべてのプロジェクトをクリーンアップ
./scripts/clean.sh

# 特定プロジェクトのみクリーンアップ
./scripts/clean.sh sample-compass
./scripts/clean.sh sample-compass-ts
./scripts/clean.sh sample-compass-makecode
```

削除されるファイル：
- **Python**: `__pycache__/`, `.pytest_cache/`, `.coverage/`, `htmlcov/`, `.venv/`
- **Node.js**: `node_modules/`, `package-lock.json/`
- **ビルド**: `dist/`, `build/`
- **キャッシュ**: Jest キャッシュ、PXT キャッシュ、coverage/
- **IDE**: `.vscode/`, `.idea/`, `.DS_Store`
- **その他**: `uv.lock`

## プログラム概要

### sample-compass（Python 実装）
- **言語**: Python
- **テスト**: pytest（ユニットテスト 13個 + E2E テスト 12個）
- **特徴**: micro:bit MicroPython API を使用した方位磁石実装
- 詳細は [sample-compass/CLAUDE.md](./sample-compass/CLAUDE.md) を参照

### sample-compass-ts（TypeScript 実装）
- **言語**: TypeScript
- **テスト**: Jest（ユニットテスト 42個 + E2E テスト 23個）
- **ビルド**: npm run build で JavaScript に変換
- **特徴**: 型安全な実装、豊富なテストカバレッジ
- 詳細は [sample-compass-ts/CLAUDE.md](./sample-compass-ts/CLAUDE.md) を参照

### sample-compass-makecode（MakeCode 実装）
- **プラットフォーム**: MakeCode Editor
- **言語**: TypeScript/PXT
- **特徴**: ビジュアルプログラミングと統合
- 詳細は [sample-compass-makecode/README.md](./sample-compass-makecode/README.md) を参照

## ライセンス

MIT License

このプロジェクトはカスタムコードとして提供されています。
自由に使用、変更、配布できます。

詳細は各プロジェクトのディレクトリを参照してください。

## 参考リンク

- [micro:bit 公式ドキュメント](https://microbit.org/)
- [MicroPython Documentation](https://microbit-micropython.readthedocs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Intel HEX Format](https://en.wikipedia.org/wiki/Intel_HEX)
