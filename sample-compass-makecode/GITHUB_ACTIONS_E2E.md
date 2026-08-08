# GitHub Actions での E2E テスト実行

## 実行状況

✅ **E2E テストは GitHub Actions で実行可能です**

## ワークフローの構成

### 1. `test.yml` - ビルド + ユニットテスト + E2E テスト

```
push/PR → GitHub Actions
  ├─ build ジョブ (ユニットテスト)
  └─ e2e ジョブ (E2E テスト)
```

**実行トリガー:**
- main / develop ブランチへの push
- main / develop ブランチへの pull request

### 2. `e2e-test.yml` - E2E テスト単独実行（オプション）

E2E テストのみを単独で実行する場合に使用できます。

## テスト実行フロー

### Build ジョブ（既存）
```
1. チェックアウト
2. Node.js 18 セットアップ
3. pxt インストール
4. プロジェクト依存関係インストール
5. MakeCode ビルド
6. pxt テスト実行 ← ユニットテスト
7. HEX ファイルをアーティファクトにアップロード
```

### E2E ジョブ（新規）
```
1. チェックアウト
2. Node.js 18 セットアップ
3. Chromium ブラウザをインストール
4. pxt インストール
5. npm 依存関係をインストール（Puppeteer）
6. E2E テスト実行 ← pxt serve + Puppeteer
7. スクリーンショット・ログをアーティファクトにアップロード
```

## GitHub Actions での確認方法

### 1. Actions ページを開く

```
https://github.com/katoy/study-microbit-with-test/actions
```

### 2. ワークフロー実行状況を確認

各コミット/PR ごとに以下が表示されます：
- ✅ `build` ジョブの状態（ユニットテスト）
- ✅ `e2e` ジョブの状態（E2E テスト）

### 3. テスト結果を確認

**Build ジョブ:**
- ✅ / ❌ ステータス
- HEX ファイル（Artifacts）

**E2E ジョブ:**
- ✅ / ❌ ステータス
- 📸 スクリーンショット（Artifacts）
- 📋 テストログ（Artifacts）

## GitHub Actions での制限事項

| 項目 | 制限 | 対応 |
|------|------|------|
| **実行環境** | ubuntu-latest | ✅ Chromium インストール可能 |
| **ブラウザ** | GUI 不要 | ✅ ヘッドレスモード |
| **タイムアウト** | ジョブ単位 6 時間 | ✅ 15 分に設定 |
| **CPU/メモリ** | 2-core, 7GB | ✅ 十分 |
| **ネットワーク** | インターネット接続可 | ✅ localhost のみ使用 |

## テスト実行中に表示される情報

### Console 出力

```
Run npm run e2e:advanced
🚀 pxt serve を起動中...
✅ pxt serve が起動しました

🌐 ブラウザを起動中...
🔗 http://localhost:3232 にアクセス中...

========== 高度な E2E テスト開始 ==========

📋 テスト 1: ページが正常にロードされるか
✅ PASS

📋 テスト 2: シミュレーター UI が表示されるか
✅ PASS: iframe が検出されました

...

========== E2E テスト結果 ==========
✅ 成功: 6
❌ 失敗: 0
合計: 6

================================
🎉 すべてのテストに成功しました！
```

### アーティファクト

**e2e-test-results:**
```
e2e-screenshot-full-2024-01-15T12-30-45-123.png
e2e-screenshot-viewport-2024-01-15T12-30-45-123.png
e2e-test.log
```

## トラブルシューティング

### E2E テストが失敗する場合

**1. タイムアウトエラー**

```
Error: Timeout waiting for pxt serve
```

→ 対応: `.github/workflows/test.yml` の `timeout-minutes` を増やす

**2. Chrome/Chromium が見つからない**

```
Error: Chromium not found
```

→ 対応: ワークフローの `sudo apt-get install -y chromium-browser` が実行されているか確認

**3. Puppeteer インストール失敗**

```
npm ERR! gyp ERR! build error
```

→ 対応: npm キャッシュをクリア、`npm install` を再実行

## ローカル環境との同期

GitHub Actions と同じ環境でテストするには：

```bash
# Docker で Ubuntu 環境をシミュレート
docker run -it ubuntu:22.04

# または WSL 2 を使用（Windows の場合）
```

## パフォーマンス

| テスト項目 | 実行時間 |
|-----------|--------|
| Build ジョブ全体 | 2-3 分 |
| E2E ジョブ全体 | 3-4 分 |
| 合計（並列実行） | 4-5 分 |

## 詳細ログ

### ワークフロー YAML の確認

```bash
cat .github/workflows/test.yml
cat .github/workflows/e2e-test.yml
```

### デバッグモードの有効化

ワークフロー実行時に以下の secret を設定すると、デバッグ情報が詳しく出力されます：

```
ACTIONS_STEP_DEBUG: true
```

## 今後の改善案

### 1. マトリックステスト

複数の Node.js バージョンでテスト：

```yaml
strategy:
  matrix:
    node-version: [16, 18, 20]
```

### 2. キャッシング

依存関係をキャッシュして高速化：

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

### 3. ステータスチェック

PR にステータスチェックを追加：

```
Settings → Branches → Require status checks before merging
```

## 参考資料

- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [Puppeteer in CI/CD](https://pptr.dev/guides/ci-cd)
- [ubuntu-latest 環境](https://github.com/actions/runner-images)
