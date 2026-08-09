# Git Hooks セットアップ完了

✅ `git commit` 時に **Lint** が走るように設定しました  
✅ `git push` 時に **MakeCode ビルド + コンパイル・シミュレーターテスト** が走るように設定しました

## 🚀 クイックスタート

### 1. 依存関係をインストール

```bash
# リポジトリルートで実行
npm install
```

### 2. sample-compass-makecode の依存関係をインストール

```bash
cd sample-compass-makecode
npm install
cd ..
```

### 3. 動作確認

```bash
# テスト用のファイルを修正
echo "// test" >> sample-compass-makecode/main.ts

# Commit してみる
git add sample-compass-makecode/main.ts
git commit -m "Test hooks"

# 自動的に pre-commit hook が実行されます
```

## 📋 実行フロー

### `git commit` 時

```
commit コマンド
  ↓
.husky/pre-commit
  ↓
sample-compass-makecode が変更されているか確認
  ↓
npm test （コンパイル・シミュレーターテスト）
  ↓
✅ 成功 → commit 続行
❌ 失敗 → commit キャンセル
```

### `git push` 時

```
push コマンド
  ↓
.husky/pre-push
  ↓
sample-compass-makecode が変更されているか確認
  ↓
2 つのチェックを順に実行：
  1. npm run build （MakeCode ビルド）
  2. npm test （コンパイル・シミュレーターテスト）
  ↓
✅ すべて成功 → push 続行
❌ 1 つでも失敗 → push キャンセル
```

## 📁 ファイル構成

```
.
├── .husky/
│   ├── pre-commit        ← commit 時に実行
│   └── pre-push          ← push 時に実行
├── package.json          ← husky & lint-staged 設定
├── GIT_HOOKS_GUIDE.md    ← 詳細ドキュメント
└── sample-compass-makecode/
    └── package.json      ← MakeCode ビルド・テスト依存関係
```

## 🛠️ トラブルシューティング

### Hooks が実行されない

```bash
# 実行権限を確認
chmod +x .husky/pre-commit .husky/pre-push

# Husky を再インストール
npm install husky --save-dev
npx husky install
```

### Hooks をスキップしたい

```bash
# Commit をスキップ
git commit --no-verify -m "message"

# Push をスキップ
git push --no-verify
```

## 📖 詳細ドキュメント

詳しい使い方は `GIT_HOOKS_GUIDE.md` を参照してください

## 🎯 各環境での実行内容

| 環境 | 実行タイミング | テスト |
|------|--------------|-------|
| **ローカル（Pre-commit）** | `git commit` | Lint |
| **ローカル（Pre-push）** | `git push` | MakeCodeビルド + コンパイル・シミュレーター |
| **GitHub Actions** | Push 後 | ユニット + 統合 + MakeCodeシミュレーター |

## ✨ メリット

✅ コード品質を保証  
✅ テスト漏れを防ぐ  
✅ CI/CD の失敗を事前に検出  
✅ チーム全体で同じ基準を共有  

---

💡 **Tip:** `npm run lint:makecode` で Lint のみを手動実行することも可能です。
