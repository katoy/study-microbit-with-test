# E2E テスト実行ガイド

MakeCode シミュレーター（pxt serve）を使った E2E テストの実行方法

## 前提条件

- Node.js 14 以上
- npm または yarn
- pxt CLI

## セットアップ

### 1. 依存関係のインストール

```bash
cd sample-compass-makecode

# npm の場合
npm install

# または yarn の場合
yarn install
```

これにより以下がインストールされます：
- `puppeteer`: ブラウザ自動操作ツール
- `pxt`: MakeCode CLI

### 2. pxt 初期化（初回のみ）

```bash
pxt install
```

## テスト実行

### 方法1: 基本的な E2E テスト

```bash
npm run e2e
```

**このテストでチェック:**
- ✅ pxt serve が正常に起動するか
- ✅ ブラウザでシミュレーター URL にアクセスできるか
- ✅ ページが正常に読み込まれるか
- ✅ シミュレーター UI が表示されるか
- ✅ JavaScript エラーがないか
- ✅ コンソール出力が表示されるか

**所要時間:** 約 30-45 秒

### 方法2: 詳細な E2E テスト（推奨）

```bash
npm run e2e:advanced
```

**このテストでチェック:**
- ✅ ページ読み込み
- ✅ シミュレーター UI 要素
- ✅ JavaScript エラー監視
- ✅ コンソール出力
- ✅ ボタン要素検出
- ✅ ネットワークリクエスト監視
- 📸 スクリーンショット自動キャプチャ

**所要時間:** 約 45-60 秒

### 方法3: pxt serve を手動で実行して確認

シミュレーターをインタラクティブに確認したい場合：

```bash
npm run serve
```

ブラウザで http://localhost:3232 を開くとシミュレーターが表示されます。

## テスト結果の確認

### コンソール出力

テスト実行時に以下のような出力が表示されます：

```
🚀 pxt serve を起動中...
✅ pxt serve が起動しました

🌐 ブラウザを起動中...
🔗 http://localhost:3232 にアクセス中...

========== E2E テスト開始 ==========

📋 テスト 1: シミュレーターが表示されるか
✅ PASS: MakeCode ページが表示されています

📋 テスト 2: コンソール出力にテスト結果が含まれるか
✅ PASS: コンソール出力が検出されました

...

========== テスト結果 ==========
✓ 成功: 5
✗ 失敗: 0
合計: 5

================================
🎉 すべてのテストに成功しました！
```

### スクリーンショット

詳細テスト実行時には、スクリーンショットが自動保存されます：

```
📸 スクリーンショットを取得中...
✅ フルスクリーンショット: e2e-screenshot-full-2024-01-15T12-30-45-123.png
✅ ビューポートスクリーンショット: e2e-screenshot-viewport-2024-01-15T12-30-45-123.png
```

画像は `sample-compass-makecode` ディレクトリに保存されます。

## トラブルシューティング

### `pxt serve` が起動しない

```bash
# pxt CLI が正しくインストールされているか確認
pxt --version

# 再インストール
npm install -g pxt
pxt install
```

### Puppeteer がインストールできない

```bash
# キャッシュをクリア
npm cache clean --force

# 再インストール
npm install --no-save puppeteer
```

### ポート 3232 が既に使用されている

```bash
# プロセスを確認
lsof -i :3232

# プロセスを強制終了（PID を置き換え）
kill -9 <PID>
```

### テストがタイムアウトする

timeout エラーが発生する場合は、システムリソースを確認：

```bash
# メモリを確認
free -h (Linux/WSL) または top (macOS)

# 別のタブで実行している pxt serve を停止
pkill pxt

# テストを再実行
npm run e2e:advanced
```

## CI/CD への統合

GitHub Actions などの CI/CD パイプラインに統合する場合：

```yaml
# .github/workflows/e2e-test.yml の例

name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd sample-compass-makecode
          npm install
          pxt install
      
      - name: Run E2E tests
        run: |
          cd sample-compass-makecode
          npm run e2e:advanced
```

## パフォーマンスの最適化

### テスト実行の高速化

1. **ヘッドレスモード使用**（デフォルト）
   ```javascript
   // e2e-advanced.test.js の headless: 'new' を使用
   headless: 'new'  // グラフィックスなし
   ```

2. **タイムアウト調整**
   ```javascript
   const TEST_TIMEOUT = 30000; // ミリ秒
   ```

3. **並列実行**
   ```bash
   npm run e2e & npm run e2e:advanced &
   ```

## デバッグのコツ

### スクリーンショットを詳しく確認

生成されたスクリーンショットを見てシミュレーターの状態を確認します：

```bash
# 最新のスクリーンショットを開く
open e2e-screenshot-*.png  # macOS
xdg-open e2e-screenshot-*.png  # Linux
```

### コンソール出力を詳しく確認

テスト実行中のコンソール出力をファイルに保存：

```bash
npm run e2e 2>&1 | tee e2e-test.log
```

### ブラウザウィンドウを保持

デバッグ時は `headless: false` に変更して、ブラウザウィンドウを表示：

```javascript
// e2e-advanced.test.js 内
headless: false,  // ブラウザウィンドウを表示
```

## ライセンス

MIT

## 参考資料

- [Puppeteer ドキュメント](https://pptr.dev/)
- [pxt CLI](https://makecode.com/cli)
- [MakeCode for micro:bit](https://makecode.microbit.org)
