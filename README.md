# study-microbit-with-test

[![Python Tests](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions/workflows/python-tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions)
[![TypeScript Tests](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions/workflows/typescript-tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/study-microbit-with-test/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/study-microbit-with-test/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/study-microbit-with-test)

micro:bit 用のシンプルな方位磁石アプリケーション学習プロジェクト

**品質ゲート**: `npm run test:all` | **カバレッジ目標**: Python・TypeScriptともに100%

## Table of Contents

- [概要](#概要)
- [プロジェクト構成](#プロジェクト構成)
- [プログラム概要](#プログラム概要)
- [AIアシスタント連携](#aiアシスタント連携)
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

- **sample-compass**: Python による実装（実機向け MicroPython 版と、MakeCode ブロック相互変換に対応した Python 版の2種類を同梱。pytest による単体・統合テスト付き）
- **sample-compass-ts**: TypeScript による実装（ハードウェアに依存しないロジックの Jest テスト付き。未キャリブレーション時に例外を投げるなど、高度なエラーハンドリングを包含）
- **sample-compass-makecode**: MakeCode Editor 用の実装（PXT CLI を用いたシミュレータ上での自動テストランナー付き。テスト時にハードウェア制御をスキップするモック構造を包含）

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

## AIアシスタント連携

本プロジェクトには、Antigravity（`agy`）、Claude Code、GitHub Copilot、Cursor（Codex）などの各種AIアシスタント間で、開発ガイドやカスタムルール（Skills）をグローバル共有・同期するためのスクリプトが用意されています。

```bash
# 各AIアシスタントのグローバル設定にカスタムスキルをマージして適用する
./sync-ai-skills.sh
```

### 適用される設定
- **Antigravity (agy)**: `~/.gemini/config/GEMINI.md` に同期され、`agy` コマンド実行時にグローバル適用されます。
- **Claude Code (CLI)**: `~/.claudecode.md` にグローバル適用されるほか、プロジェクトルートに `CLAUDE.md` を作成して適用します。
- **GitHub Copilot**: VS Code の `settings.json` のグローバル指示に自動登録されます。
- **Cursor (Codex)**: グローバルな `~/.cursorrules` にシンボリックリンクされます。

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

### MakeCode 環境（sample-compass-makecode）

```bash
cd sample-compass-makecode
npm ci
```

MakeCode CLI はプロジェクトの開発依存関係としてインストールされるため、グローバルインストールは不要です。

## テスト実行

### すべてのテスト実行

```bash
# ルートディレクトリから
npm run test:all

# または個別に
npm run test:python && npm run test:ts && npm run test:makecode
```

### Python テスト

```bash
cd sample-compass
uv run pytest test_compass.py -v           # ユニットテスト
uv run pytest test_compass_integration.py -v # 統合テスト（micro:bit API はモック）
uv run pytest -v                           # 全テスト
```

### TypeScript テスト

```bash
cd sample-compass-ts
npm test                            # 全テスト
npm run test:unit                   # ユニットテストのみ
npm run test:integration            # 統合テストのみ
npm run test:coverage               # カバレッジレポート付き
npm run test:watch                  # ウォッチモード
```

### MakeCode テスト

```bash
cd sample-compass-makecode
npm test
```

`pxt test` によるコンパイル確認に加え、28件の方位判定テストを PXT の内蔵シミュレーターで実行します。失敗・結果欠落・件数不整合はいずれも非ゼロ終了になります。

## ビルド

### TypeScript のビルド

```bash
cd sample-compass-ts
npm run build
```

## HEX ファイル生成

MicroPython 版と MakeCode 版から、micro:bit に転送可能な HEX ファイルを生成できます。

### 対応する実装から HEX を生成

```bash
npm run build:hex
```

### 個別プロジェクトから HEX を生成

```bash
# MakeCode
cd sample-compass-makecode
npm run build:hex

# Python
cd sample-compass
uv run python build_hex.py
```

生成された HEX ファイル：

```
sample-compass/dist/hex/compass.hex
sample-compass-makecode/built/binary.hex
```

`sample-compass-ts` はNode.js上で方位ロジックを学習・テストするための実装であり、
micro:bit用HEXは生成しません。実機向けTypeScriptにはMakeCode版を使用してください。

詳細は [HEX_BUILD_GUIDE.md](./HEX_BUILD_GUIDE.md) を参照してください。

### Web エディターとの連携（相互インポート/エクスポート）

MakeCode 版のコードは、ローカル開発環境と Web 画面上の [MakeCode エディター](https://makecode.microbit.org) を相互に行き来することができます。

- **HEX ドラッグ＆ドロップ**: 生成された `sample-compass-makecode/built/binary.hex` を Web エディターにドラッグ＆ドロップすると、プロジェクト（ブロックや TypeScript コード）が瞬時に復元されます。
- **GitHub 連携**: リポジトリを GitHub にプッシュし、Web エディターからインポートすることで、Web での編集とローカルの変更を `git pull/push` で同期できます。
- **ローカルサーバー連携 (`npm run serve`)**: ローカルで Web サーバーを起動し、VS Code 等でのコード保存をブラウザのブロック/シミュレータにリアルタイム同期します。

詳細は [sample-compass-makecode/README.md](file:///Users/katoy/github/study-microbit-with-test/sample-compass-makecode/README.md#makecode-web-エディターとの相互インポートエクスポート) を参照してください。

## Code Quality & Linting

### すべてのプロジェクトをチェック

```bash
# Python、TypeScript、MakeCode のすべてをチェック
npm run lint
```

実行内容：
- **Python**: `py_compile` で構文チェック
- **TypeScript**: `tsc` コンパイル確認
- **MakeCode**: `pxt build` でビルド検証

### 個別プロジェクトのリント

```bash
npm run lint:python   # Python 構文チェック
npm run lint:ts       # TypeScript ビルド確認
npm run lint:makecode # MakeCode ビルド検証
```

## CI/CD

このプロジェクトは GitHub Actions を使用して自動的にテストを実行します。

- **Python テスト**: `sample-compass/` のテストが実行されます
- **TypeScript テスト**: `sample-compass-ts/` のテストが実行されます
- **統合・シミュレーターテスト**: Python・TypeScript の統合テストと MakeCode のPXTシミュレーターテストが実行されます
- **セキュリティ**: Bandit、Trivy、全npm lockfile、`uv.lock` 由来のPython依存を監査します

ローカルで全npm lockfileの high/critical 脆弱性を確認するには `npm run audit:npm` を実行します。修正版がないビルド時依存だけは [`security/npm-audit-allowlist.json`](./security/npm-audit-allowlist.json) で対象パッケージと見直し期限を限定しています。

詳細は `.github/workflows/` を参照してください。

### npm Scripts リファレンス

#### テスト

| コマンド | 説明 |
|---------|------|
| `npm run lint` | 全プロジェクトのコード品質チェック |
| `npm run lint:python` | Python 構文チェック |
| `npm run lint:ts` | TypeScript ビルド確認 |
| `npm run lint:makecode` | MakeCode ビルド検証 |
| `npm run test:python` | Python ユニットテスト |
| `npm run integration:python` | Python 統合テスト（micro:bit API はモック） |
| `npm run test:ts` | TypeScript ユニットテスト |
| `npm run test:makecode` | MakeCode コンパイル・シミュレーターテスト |
| `npm run integration:ts` | TypeScript 統合テスト |
| `npm run test` | 全ユニットテスト |
| `npm run integration` | Python・TypeScript 統合テスト |
| `npm run test:all` | 全テスト（ユニット + 統合 + MakeCodeシミュレーター） |
| `npm run audit:npm` | 全npm lockfileの high/critical 脆弱性監査 |

#### ビルド

| コマンド | 説明 |
|---------|------|
| `npm run build:hex` | Python版とMakeCode版の HEX ファイルを生成 |
| `npm run build:hex:python` | Python HEX ファイルを生成 |
| `npm run build:hex:makecode` | MakeCode HEX ファイルを生成 |

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

削除されるファイル（Git追跡中のパスは常に保持されます）：
- **Python**: `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.coverage`, `coverage.xml`, `htmlcov/`, `.venv/`
- **Node.js / PXT**: `node_modules/`, `pxt_modules/`
- **ビルド**: `dist/`, `build/`, `built/`
- **キャッシュ**: `.jest-cache/`, `.pxt/`, `.nyc_output/`, `.cache/`, `coverage/`
- **IDE**: `.vscode/`, `.idea/`, `.DS_Store`（プロジェクト指定時のみ）

`package-lock.json`、`pnpm-lock.yaml`、`uv.lock` は再現可能なビルドに必要なため削除しません。事前確認には `./scripts/clean.sh --dry-run` を使えます。

## プログラム概要

### sample-compass（Python 実装）
- **言語**: Python (MicroPython / MakeCode Python)
- **テスト**: pytest（ユニットテスト + モック環境での統合テスト）
- **特徴**:
  - `compass.py`: 標準 MicroPython 向けの実装。未キャリブレーション時に "CAL" 警告をスクロール表示するエッジケース対応付き。
  - `compass_makecode.py`: MakeCode Web エディタの Python モード（Static Python）との互換コード。ブロックへの相互変換が可能。
- 詳細は [sample-compass/CLAUDE.md](./sample-compass/CLAUDE.md) を参照

### sample-compass-ts（TypeScript 実装）
- **言語**: TypeScript
- **テスト**: Jest（ユニットテスト + Node.js上の統合テスト）
- **ビルド**: npm run build で JavaScript に変換
- **特徴**: 型安全な実装、豊富なテストカバレッジ。未キャリブレーション状態で状態取得時に明確な例外（`Error`）をスローする厳密なエラーハンドリングの学習用モデル。
- 詳細は [sample-compass-ts/CLAUDE.md](./sample-compass-ts/CLAUDE.md) を参照

### sample-compass-makecode（MakeCode 実装）
- **プラットフォーム**: MakeCode Editor
- **言語**: TypeScript/PXT
- **特徴**: ビジュアルプログラミングと統合。テスト時にシミュレータ環境特有の undefined 例外を防ぐ `skipHardware` フラグやテストモードを搭載し、安全な自動テストが可能。
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
