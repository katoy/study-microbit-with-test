# CLAUDE.md - Development Guide for AI Assistants

このファイルは AI アシスタント（Claude、Copilot など）がこのプロジェクトで作業する際の指南書です。

## プロジェクト概要

**目的**: micro:bit 用の方位磁石アプリケーション学習プロジェクト

**構成**:
- **Python 実装** (`sample-compass/`) - pytest + E2E テスト
- **TypeScript 実装** (`sample-compass-ts/`) - Jest + E2E テスト
- **MakeCode 実装** (`sample-compass-makecode/`) - 別プロジェクト

**テスト総数**: 90個（Python: 25個、TypeScript: 65個）

## ディレクトリ構造

```
study-microbit-with-test/
├── .github/workflows/        # GitHub Actions CI/CD
│   ├── python-tests.yml      # Python 3.11
│   ├── typescript-tests.yml  # Node 20.x
│   └── e2e-tests.yml         # 統合E2E
├── .husky/                   # Git Hooks
│   ├── pre-commit            # コミット前テスト
│   └── pre-push              # プッシュ前テスト
├── sample-compass/           # Python プロジェクト
│   ├── CLAUDE.md            # Python 開発ガイド
│   ├── compass.py
│   ├── test_compass.py      # ユニットテスト (13)
│   └── e2e_test_compass.py  # E2E テスト (12)
├── sample-compass-ts/       # TypeScript プロジェクト
│   ├── CLAUDE.md            # TypeScript 開発ガイド
│   ├── src/compass.ts
│   └── test/
│       ├── compass.test.ts      # ユニットテスト (42)
│       └── compass.e2e.test.ts  # E2E テスト (23)
└── sample-compass-makecode/  # MakeCode プロジェクト
```

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

### E2E テスト実行
```bash
# ルートディレクトリから
npm run e2e
```

### 特定プロジェクトのテスト
```bash
# Python
cd sample-compass
python3 -m pytest -v

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
    └→ Python 3.11, Node 20.x でテスト
    └→ カバレッジレポート生成
```

## Git Hooks

### Pre-commit Hook
各プロジェクトの変更に対してコミット前に自動実行：
- Python: `pytest test_compass.py` + `pytest e2e_test_compass.py`
- TypeScript: `npm test`

### Pre-push Hook
プッシュ前に変更ファイルを検出して全テスト実行

詳細は `.husky/` ディレクトリを参照。

## GitHub Actions CI/CD

### ワークフロー一覧

| Workflow | トリガー | 実行内容 |
|----------|---------|---------|
| `python-tests.yml` | push/PR (sample-compass) | Python 3.11 でテスト |
| `typescript-tests.yml` | push/PR (sample-compass-ts) | Node 20.x でテスト |
| `e2e-tests.yml` | push/PR (両方) | 統合E2Eテスト |

### 実行環境
- **Python**: 3.11（最新安定版）
- **Node.js**: 20.x（最新 LTS）
- **実行環境**: Ubuntu latest

## TDD ワークフロー

推奨される開発手順（Test-Driven Development）：

```bash
# 1. ブランチ作成
git checkout -b feature/new-feature

# 2. テストを先に書く
# test_compass.py または compass.test.ts に追加

# 3. テスト実行（失敗する）
pytest -v  # または npm test

# 4. 実装を追加
# compass.py または src/compass.ts を編集

# 5. テスト実行（成功する）
pytest -v  # または npm test

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

# Python のみ
npm run test:python

# TypeScript のみ
npm run test:ts

# E2E のみ
npm run e2e

# カバレッジ付き
npm run test:coverage
```

### 特定の環境でテストする
```bash
# Python E2E テスト
cd sample-compass && python3 -m pytest e2e_test_compass.py -v

# TypeScript E2E テスト
cd sample-compass-ts && npm run test:e2e
```

### CI/CD をローカルでシミュレートする
```bash
# docker が必要
act -l                    # 使用可能なワークフローを表示
act --list                # 詳細表示
act -j test               # 特定のジョブ実行
```

## 重要な npm スクリプト（ルート）

| コマンド | 説明 |
|---------|------|
| `npm run test:python` | Python テスト実行 |
| `npm run e2e:python` | Python E2E テスト実行 |
| `npm run test:ts` | TypeScript テスト実行 |
| `npm run e2e:ts` | TypeScript E2E テスト実行 |
| `npm run test:all` | 全テスト実行 |
| `npm run e2e` | 全E2Eテスト実行 |

詳細は各プロジェクトの CLAUDE.md を参照。

## 開発規約

### 共通ルール
- **VCS**: Git
- **コミットメッセージ**: 英語、明確で簡潔
- **ブランチ戦略**: フィーチャーブランチ（`feature/xxx`）
- **テスト**: 全変更に対してテストを必須

### 言語別規約
詳細は各プロジェクトの CLAUDE.md を参照：
- **Python**: `sample-compass/CLAUDE.md`
- **TypeScript**: `sample-compass-ts/CLAUDE.md`

## トラブルシューティング

### テスト実行時のエラー
```bash
# 依存関係を再インストール
npm install

# Python の場合
python3 -m pip install pytest pytest-cov

# TypeScript の場合
cd sample-compass-ts
rm -rf node_modules package-lock.json
npm install
```

### Git Hooks が実行されない
```bash
# husky を再インストール
npm run prepare

# hooks の実行権限を確認
chmod +x .husky/pre-commit
chmod +x .husky/pre-push
```

### GitHub Actions が失敗する
1. ローカルでテストが成功することを確認
2. GitHub Actions ログを確認
3. キャッシュをクリア（GitHub UI）

詳細なトラブルシューティングは各プロジェクトの CLAUDE.md を参照。

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
