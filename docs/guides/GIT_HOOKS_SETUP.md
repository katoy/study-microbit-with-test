# Git hooksセットアップ

初回だけ、リポジトリのルートで次を実行します。

```bash
npm ci
npm --prefix sample-compass-ts ci
npm --prefix sample-compass-makecode ci
uv sync --project sample-compass
npm run prepare
```

確認:

```bash
npm run test:config
```

以後は、`git commit` でステージ済み変更に対応するテスト、`git push` で送信差分に対応するテストとMakeCodeビルドが自動実行されます。全体像とトラブル対応は [GIT_HOOKS_GUIDE.md](./GIT_HOOKS_GUIDE.md) を参照してください。
