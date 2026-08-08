# Git Hooks 設定ガイド

Git commit/push 時に自動的にテストを実行するように設定しました。

## セットアップ

### 1. npm dependencies をインストール

```bash
cd /Users/katoy/github/study-microbit-with-test
npm install
```

これにより以下がインストール・設定されます：
- ✅ husky（Git hooks マネージャー）
- ✅ lint-staged（ステージング済みファイルのみに lint を実行）
- ✅ .husky ディレクトリ内の hooks

### 2. sample-compass-makecode の依存関係をインストール

```bash
cd sample-compass-makecode
npm install
```

## Git Hooks の動作

### 1️⃣ `git commit` 時 → **Pre-commit Hook**

**実行される処理:**
```
変更ファイルが sample-compass-makecode に含まれる
  ↓
pxt build --cloud （Lint）
  ↓
✅ 成功 → commit を続行
❌ 失敗 → commit をキャンセル
```

**例:**
```bash
$ git commit -m "Add compass feature"
🔍 Git commit 前の lint チェック...
📝 sample-compass-makecode のファイルが変更されています
🔨 pxt build を実行中...
✅ Build 成功！
✅ Pre-commit チェック完了！
[main abc1234] Add compass feature
```

### 2️⃣ `git push` 時 → **Pre-push Hook**

**実行される処理:**
```
変更ファイルが sample-compass-makecode に含まれる
  ↓
ステップ 1/3: pxt build --cloud （Lint）
  ↓
ステップ 2/3: pxt test （ユニットテスト）
  ↓
ステップ 3/3: npm run e2e:advanced （E2E テスト）
  ↓
✅ すべて成功 → push を続行
❌ 1つでも失敗 → push をキャンセル
```

**例:**
```bash
$ git push origin main
🚀 Git push 前のテスト実行...
📦 sample-compass-makecode のファイルが変更されています

🔨 ステップ 1/3: Lint チェック (pxt build)...
✅ Lint 完了！

🧪 ステップ 2/3: ユニットテスト実行 (pxt test)...
✓ テスト成功
✅ ユニットテスト 完了！

🌐 ステップ 3/3: E2E テスト実行...
✅ Build 成功！
✅ シミュレーターが表示されます
...
✅ E2E テスト 完了！

🎉 すべてのテストに成功しました！Push を続行します。
```

## Hooks をスキップする

### Commit Hooks をスキップ

```bash
git commit --no-verify -m "Skip pre-commit check"
# または
git commit -n -m "Skip pre-commit check"
```

### Push Hooks をスキップ

```bash
git push --no-verify
# または
git push -n
```

⚠️ **注意:** Hooks をスキップすることは推奨されません。CI/CD で失敗する可能性があります。

## トラブルシューティング

### Hooks が実行されない

**問題:** Pre-commit/pre-push hook が実行されない

**解決方法:**

```bash
# 1. Hooks ファイルに実行権限があるか確認
chmod +x .husky/pre-commit
chmod +x .husky/pre-push

# 2. Husky が正しくインストールされているか確認
cat .husky/pre-commit

# 3. Husky を再インストール
npm install husky --save-dev
npx husky install
```

### "pxt: command not found"

**問題:** Hooks 実行時に pxt が見つからない

**解決方法:**

```bash
# 1. pxt をグローバルにインストール
npm install -g pxt

# 2. または、package.json のスクリプトを修正
npx pxt build --cloud
```

### E2E テストがタイムアウト

**問題:** Pre-push hook で E2E テストがタイムアウト

**解決方法:**

```bash
# 1. Hooks をスキップして push
git push --no-verify

# 2. または、E2E テストの timeout を増やす
# .husky/pre-push 内の timeout を調整
```

## Hook ファイルの位置

```
.husky/
├── _/husky.sh         ← husky のメインスクリプト
├── pre-commit         ← Commit 時に実行
└── pre-push           ← Push 時に実行
```

## Pre-commit Hook の詳細

### `.husky/pre-commit`

```bash
#!/bin/sh
# 1. sample-compass-makecode のファイルが変更されているかチェック
# 2. 変更されている場合、pxt build を実行
# 3. 失敗すると commit をキャンセル
```

**チェック対象ファイル:**
- sample-compass-makecode/**/*.ts
- sample-compass-makecode/**/*.js

## Pre-push Hook の詳細

### `.husky/pre-push`

```bash
#!/bin/sh
# 1. Origin ブランチからのコミット差分をチェック
# 2. sample-compass-makecode が変更されていれば以下を実行：
#    - pxt build --cloud （Lint）
#    - pxt test （ユニットテスト）
#    - npm run e2e:advanced （E2E テスト）
# 3. 1つでも失敗すると push をキャンセル
```

## Git Hooks の有効化・無効化

### すべての Hooks を一時的に無効化

```bash
husky uninstall
```

### Hooks を再度有効化

```bash
npm install
```

## Package.json での関連スクリプト

```json
{
  "scripts": {
    "lint:makecode": "cd sample-compass-makecode && pxt build --cloud",
    "test:makecode": "cd sample-compass-makecode && pxt test",
    "e2e:makecode": "cd sample-compass-makecode && npm run e2e:advanced"
  }
}
```

これらは以下で手動実行もできます：

```bash
npm run lint:makecode   # Lint のみ
npm run test:makecode   # ユニットテストのみ
npm run e2e:makecode    # E2E テストのみ
```

## GitHub Actions との関係

| 実行環境 | 実行タイミング | テスト内容 |
|---------|--------------|----------|
| **ローカル（Pre-commit）** | `git commit` 時 | Lint のみ |
| **ローカル（Pre-push）** | `git push` 時 | Lint + Unit + E2E |
| **GitHub Actions（CI/CD）** | push 後（自動） | Build + Unit + E2E |

## ベストプラクティス

### 1. 定期的に Hooks を更新

```bash
# 定期的に Hooks を確認
cat .husky/pre-commit
cat .husky/pre-push
```

### 2. ローカルと CI/CD の一貫性を保つ

- ローカル hooks ≈ GitHub Actions ワークフロー
- 両方で同じテストを実行

### 3. チーム全体で Hooks を共有

```bash
# リポジトリに .husky を含める
git add .husky/
git commit -m "Add Git hooks"
```

## 参考資料

- [Husky ドキュメント](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/okonet/lint-staged)
- [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
