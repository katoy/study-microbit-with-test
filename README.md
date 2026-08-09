# study-microbit-with-test

micro:bit の方位磁石を題材に、ブロック、Python、TypeScript、自動テストを段階的に学ぶプログラミング環境教材です。同じ「0〜359度を8方位へ変換する」課題を、実機・シミュレーター・PC上のテストで比較できます。

## この教材で学べること

- MakeCode ブロックと MakeCode Python／TypeScript の対応
- MicroPython と MakeCode Static Python の違い
- センサー値と、テストしやすい方位判定ロジックの分離
- 境界値テスト（22.5度、67.5度など）
- モック、型、安全なビルド、CI、Git hooks の役割
- micro:bit V1/V2 用 Universal HEX の生成と検証

> [!IMPORTANT]
> PC上のPython統合テストは `microbit` APIをモックします。MakeCodeテストはPXTシミュレーター上で動きます。どちらも実機の磁気センサー、校正、USB転送そのものを保証するテストではありません。最後に実機確認を行ってください。

## 推奨学習ルート

1. **MakeCode** — ブロックでイベント、コンパス、LED表示を観察する
2. **Python** — 方位判定をpytestの境界値テストで確かめる
3. **TypeScript** — 同じ仕様を型と例外で表現する
4. **開発環境** — ルート品質ゲート、CI、Git hooksが何を守るか調べる

90分授業には [WORKSHOP_TEMPLATE.md](./WORKSHOP_TEMPLATE.md)、自習には [MULTILANGUAGE_GUIDE.md](./MULTILANGUAGE_GUIDE.md) を使います。

## すぐに始める

### Dev Container / Codespaces

リポジトリをDev Containerで開くと、`.devcontainer/setup-dev.sh` が依存関係を導入し、完全な品質ゲートを実行します。成功を隠さない fail-fast 構成です。

### ローカル環境

Node.js 22、Python 3.11以上、`uv` を用意して、リポジトリのルートで実行します。

```bash
npm ci
npm --prefix sample-compass-ts ci
npm --prefix sample-compass-makecode ci
uv sync --project sample-compass
npm run test:all
```

`npm run test:all` はユニット／統合／MakeCodeシミュレーターテストに加え、PythonとTypeScriptのカバレッジ検査を実行します。Pythonは100%未満なら失敗します。

## 3つの実装

| ディレクトリ | 実行環境 | 主な教材テーマ | 実機用HEX |
|---|---|---|---|
| [`sample-compass`](./sample-compass/) | MicroPython / MakeCode Python | モック、境界値、2種類のPython API | 生成可能 |
| [`sample-compass-ts`](./sample-compass-ts/) | Node.js | 純粋ロジック、型、例外、Jest | 生成しない |
| [`sample-compass-makecode`](./sample-compass-makecode/) | MakeCode / PXT | ブロックAPI、イベント、シミュレーター | 生成可能 |

`sample-compass-ts` はPCで設計とテストを学ぶ実装です。micro:bitへ転送するTypeScriptは `sample-compass-makecode` を使います。

## よく使うコマンド

| コマンド | 内容 |
|---|---|
| `npm run test:all` | ローカルの完全な品質ゲート |
| `npm run test:config` | 文書・CI・安全スクリプトなどリポジトリ設定のテスト |
| `npm run test:python` | Pythonユニット／HEX検証テスト |
| `npm run integration:python` | モックを使うPython統合テスト |
| `npm run test:ts` | TypeScriptユニットテスト |
| `npm run integration:ts` | TypeScript統合テスト |
| `npm run test:makecode` | PXTコンパイルとシミュレーターテスト |
| `npm run lint` | Python構文、TypeScript、MakeCodeビルド検査 |
| `npm run build:hex` | Python版とMakeCode版のHEXを生成 |
| `npm run verify:blocks` | MakeCode WebでPython／TSをブロックへ変換し、エラーとグレーブロックを検査 |
| `npm run audit:npm` | 全npm lockfileのhigh/critical脆弱性を検査 |

## 実機へ転送する

```bash
npm run build:hex
```

生成物は次の場所です。

- `sample-compass/dist/hex/compass.hex` — MicroPython、V1/V2 Universal HEX
- `sample-compass-makecode/built/binary.hex` — MakeCode

HEXをmicro:bitのUSBドライブへコピーします。初回や周囲の磁場が変わった場合は校正してください。詳細は [HEX_BUILD_GUIDE.md](./HEX_BUILD_GUIDE.md) を参照してください。

ブロック互換性を含めて確認する場合は `npm run verify:blocks` を実行します。この検査はMakeCode WebとPlaywrightを使うため、ネットワーク接続が必要です。成功条件は、ソース注入、ブロックワークスペース表示、変換エラー0、グレーブロック0です。

## MakeCode Webとの行き来

最も確実な方法は、生成したMakeCode HEXを <https://makecode.microbit.org/> へドラッグ＆ドロップする方法です。ローカル編集には `npm --prefix sample-compass-makecode run serve` も使えます。

このモノレポのルートには `pxt.json` がないため、ルートのGitHub URLをMakeCodeへ直接インポートしないでください。GitHub連携が必要なら `sample-compass-makecode` の内容を専用リポジトリのルートへ置きます。詳しくは [MakeCode版README](./sample-compass-makecode/README.md) を参照してください。

## 教材・運用文書

- [複数言語学習ガイド](./MULTILANGUAGE_GUIDE.md)
- [90分ワークショップ](./WORKSHOP_TEMPLATE.md)
- [動画収録台本](./VIDEO_TUTORIAL_SCRIPT.md)
- [Git hooksガイド](./GIT_HOOKS_GUIDE.md)
- [文書索引と過去レビュー](./docs/README.md)

過去の評価レポートに書かれたテスト件数は作成時点のスナップショットです。現在の状態は `npm run test:all` の実行結果を正とします。

## 保守者向け: AIルール同期

`sync-ai-skills.sh` は学習に必須ではありません。既定ではファイルを変更せず、対象だけを表示します。

```bash
./sync-ai-skills.sh          # dry-run
./sync-ai-skills.sh --apply  # 既存設定を日時付きバックアップして適用
```

VS Code設定や、このリポジトリの `CLAUDE.md` は自動変更しません。

## CIと安全性

GitHub ActionsはPython、TypeScript、MakeCode、統合テスト、リポジトリ設定、依存関係監査を分けて実行します。ローカルhooksは変更されたサブプロジェクトのテストをcommit/push前に実行します。CIを通すためだけにテスト失敗を無視する構成にはしていません。

一時生成物の確認と削除には次を使います。

```bash
./scripts/clean.sh --dry-run
./scripts/clean.sh
```

追跡中ファイルとlockfileは保持されます。

## ライセンス

[MIT License](./LICENSE)
