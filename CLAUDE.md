# CLAUDE.md - Development Guide for AI Assistants

このファイルは AI アシスタント（Claude、Copilot など）がこのプロジェクトで作業する際の指南書です。

## プロジェクト概要

**目的**: micro:bit 用の方位磁石アプリケーション学習プロジェクト

**構成**:
- **Python 実装** (`sample-compass/`) - 静的コンパイルチェック
- **TypeScript 実装** (`sample-compass-ts/`) - Jestユニット・統合テスト
- **MakeCode 実装** (`sample-compass-makecode/`) - PXTコンパイル・シミュレーターテスト

テスト件数は各テストランナーの出力を正とします。


## AIアシスタント向けカスタムスキル同期

本プロジェクトには、Antigravity（`agy`）、Claude Code、GitHub Copilot、Cursor（Codex）などの各種AIアシスタント間で、開発ガイドやカスタムルール（Skills）をグローバル共有・同期するためのスクリプトが用意されています。

### 同期手順
```bash
# スキルをマージして各AIツールのグローバル設定に同期
./sync-ai-skills.sh
```

### 同期対象と効果
- **Antigravity (agy)**: `~/.gemini/config/GEMINI.md` に同期され、`agy` がすべてのカスタムルールをグローバルに認識します。
- **Claude Code (CLI)**: `~/.claudecode.md` に同期されるほか、ローカルに `CLAUDE.md` としてマージルールをリンクさせることで、即座にプロジェクトに反映できます。
- **GitHub Copilot**: VS Code の `settings.json`（`github.copilot.chat.codeGeneration.instructions`）に自動登録されます。
- **Cursor (Codex)**: グローバルな `~/.cursorrules` にシンボリックリンクされ、デフォルトルールとして動作します。

## クイックスタート

### プロジェクト別ガイド
各プロジェクトの詳細な開発ガイド：
- **Python**: `sample-compass/CLAUDE.md` を参照
- **TypeScript**: `sample-compass-ts/CLAUDE.md` を参照

### 全テスト実行
```bash
# ルートディレクトリから
npm run test:all
```

### 統合テスト実行
```bash
# ルートディレクトリから
npm run integration
```

### 特定プロジェクトのテスト
```bash
# Python (コンパイルチェック)
cd sample-compass
uv run python -m py_compile compass_makecode.py

# TypeScript
cd sample-compass-ts
npm test
```

## ワークフロー概要

### 開発フロー
```
git checkout -b feature/xxx
    ↓
コード編集
    ↓
git commit
    └→ pre-commit hook で自動テスト実行
    └→ テスト成功でコミット完了
    ↓
git push
    └→ pre-push hook で全テスト実行
    └→ テスト成功でプッシュ完了
    ↓
GitHub Actions で CI/CD実行
    └→ Python 3.12.8, Node 22.23.2 でテスト
    └→ カバレッジレポート生成
```

## Git Hooks

### Pre-commit Hook
各プロジェクトの変更に対してコミット前に自動実行：
- Python: `py_compile compass_makecode.py`
- TypeScript: `npm test`

### Pre-push Hook
プッシュ前に変更ファイルを検出して全テスト実行

詳細は `.husky/` ディレクトリを参照。

## GitHub Actions CI/CD

CI/CD ワークフローは `.github/workflows/` に定義されています。詳細は各ワークフロー定義ファイルを参照してください。

## 環境設定

### バージョン管理

本プロジェクトは **ルートレベル `.tool-versions`** で統一的にバージョンを管理します：

```
python 3.12.8
node 22.23.2
```

**各プロジェクトの対応:**
- **sample-compass/** - Python 3.12.8 を使用
- **sample-compass-ts/** - Node.js 22.23.2 を使用
- **sample-compass-makecode/** - Node.js 22.23.2（MakeCode CLI実行時）

### asdf でのセットアップ

```bash
# ルートディレクトリで実行
asdf install

# 確認
python3 --version  # Python 3.12.8
node --version     # v22.23.2
```

### 環境変数の設定

各プロジェクトのセットアップ：
```bash
# sample-compass（Python）
cd sample-compass
uv sync

# sample-compass-ts（Node.js）
cd sample-compass-ts
npm install
```

## TDD ワークフロー

推奨される開発手順（Test-Driven Development）：

```bash
# 1. ブランチ作成
git checkout -b feature/new-feature

# 2. テストを先に書く
# compass.test.ts に追加

# 3. テスト実行（失敗する）
npm test

# 4. 実装を追加
# src/compass.ts を編集

# 5. テスト実行（成功する）
npm test

# 6. リファクタリング（必要に応じて）

# 7. コミット（hooks が自動実行）
git commit -m "Add new feature"

# 8. プッシュ（hooks が全テスト実行）
git push origin feature/new-feature

# 9. PR 作成（GitHub Actions が自動実行）
```

## よくある作業

### テストを実行する
```bash
# 全テスト
npm run test:all

# Python のみ (コンパイルチェック)
npm run lint:python

# TypeScript のみ
npm run test:ts

# 統合テストのみ
npm run integration

# カバレッジ付き
npm run test:coverage
```

### 特定の環境でテストする
```bash


# TypeScript 統合テスト
cd sample-compass-ts && npm run test:integration
```

### CI/CD をローカルでシミュレートする
```bash
# docker が必要
act -l                    # 使用可能なワークフローを表示
act --list                # 詳細表示
act -j test               # 特定のジョブ実行
```

## 重要な npm スクリプト

利用可能なスクリプトは `npm run` で確認してください。詳細は `package.json` と各プロジェクトの CLAUDE.md を参照。

## 開発規約

### 共通ルール
- **VCS**: Git
- **コミットメッセージ**: 英語、明確で簡潔
- **ブランチ戦略**: フィーチャーブランチ（`feature/xxx`）
- **テスト**: 全変更に対してテストを必須
- **コード配置**: アプリケーションコードは `src/` に保存、テストコードは `test/` に保存する

### 言語別規約
詳細は各プロジェクトの CLAUDE.md を参照：
- **Python**: `sample-compass/CLAUDE.md`
- **TypeScript**: `sample-compass-ts/CLAUDE.md`

## トラブルシューティング

詳細な問題解決ガイドは各プロジェクトの CLAUDE.md を参照してください。

## 外部リソース

### 全般
- [Git Documentation](https://git-scm.com/doc)
- [micro:bit Documentation](https://microbit.org/guide/)

### Python
- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)

### TypeScript
- [Jest Documentation](https://jestjs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [micro:bit TypeScript API](https://makecode.microbit.org/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Using actions/checkout](https://github.com/actions/checkout)
- [Using actions/setup-python](https://github.com/actions/setup-python)
- [Using actions/setup-node](https://github.com/actions/setup-node)

## 質問や改善提案

このプロジェクトの開発ガイドは継続的に改善されています。
改善提案やベストプラクティスの発見があれば、このファイルを更新してください。

### CLAUDE.md ファイル構成
- **./CLAUDE.md** （このファイル）: プロジェクト全体の概要とワークフロー
- **sample-compass/CLAUDE.md**: Python プロジェクト固有ガイド
- **sample-compass-ts/CLAUDE.md**: TypeScript プロジェクト固有ガイド
