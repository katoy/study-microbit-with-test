# Git hooksガイド

このリポジトリはHuskyで、変更したサブプロジェクトのテストをcommit/push前に実行します。hooksは高速な手元の安全網であり、GitHub Actionsの代わりではありません。

## セットアップ

```bash
npm ci
npm --prefix sample-compass-ts ci
npm --prefix sample-compass-makecode ci
uv sync --project sample-compass
npm run prepare
```

Dev Containerでは自動実行されます。

## pre-commit

ステージ済みのパスを見て、該当プロジェクトだけを検査します。

| 変更パス | 実行内容 |
|---|---|
| `sample-compass/**` | Python構文チェック（`py_compile`） |
| `sample-compass-ts/**` | TypeScriptコンパイル + Jest全テスト |
| `sample-compass-makecode/**` | PXTコンパイル・シミュレーターテスト |

テストが1つでも失敗するとcommitを中止します。

## pre-push

送信するrefの差分を調べます。新規refでは送信ツリー全体を安全側に検査します。

| 変更プロジェクト | 実行順序 | 内容 |
|---|---|---|
| **sample-compass** (Python) | 1 | Python構文チェック（`py_compile`） |
| **sample-compass-ts** (TypeScript) | 2 | TypeScriptコンパイル → Jest全テスト |
| **sample-compass-makecode** (MakeCode) | 3 | ビルド → PXTコンパイル・シミュレーターテスト |

**テスト失敗、差分取得失敗、ビルド失敗はpushを中止します。**

**重要**: TypeScriptは pre-commit で build を含め、pre-push でも build + test を実行します。これにより、型安全性とコンパイル可能性をcommit時点で確認できます。

## 手動の完全検査

hooksは変更されたサブプロジェクトに絞るため、提出・レビュー前にはルート品質ゲートも実行します。

```bash
npm run test:all
npm run lint
npm run build:hex
```

## トラブルシューティング

### hooksが動かない

```bash
npm run prepare
ls -l .husky/pre-commit .husky/pre-push
```

実行属性がなければ `chmod +x .husky/pre-commit .husky/pre-push` を実行します。

### `pxt` が見つからない

グローバルインストールは不要です。

```bash
npm --prefix sample-compass-makecode ci
```

### PXTキャッシュの権限エラー

PXTはホームディレクトリの `.pxt/cache` を使います。そのディレクトリが現在の利用者へ書込可能か確認してください。CIやコンテナでは利用者のホームを正しく設定します。

### 緊急時にhooksを飛ばす

`--no-verify` はローカル検査を飛ばしますが、失敗を直すものではありません。障害対応など理由が明確な場合だけ使い、push前またはCIで同じ検査を必ず実行してください。

## 実装

- [`.husky/pre-commit`](./.husky/pre-commit)
- [`.husky/pre-push`](./.husky/pre-push)
- [`test/git-hooks.test.js`](./test/git-hooks.test.js)

hooks自体もリポジトリ設定テストで、安全側に失敗することを検査しています。
