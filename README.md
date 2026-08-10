# study-microbit-with-test

[![Integration Tests](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/katoy/study-microbit-with-test/actions/workflows/integration-tests.yml)
[![TypeScript Tests](https://github.com/katoy/study-microbit-with-test/actions/workflows/typescript-tests.yml/badge.svg)](https://github.com/katoy/study-microbit-with-test/actions/workflows/typescript-tests.yml)
[![Security Scan](https://github.com/katoy/study-microbit-with-test/actions/workflows/security.yml/badge.svg)](https://github.com/katoy/study-microbit-with-test/actions/workflows/security.yml)
[![Repository Checks](https://github.com/katoy/study-microbit-with-test/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/katoy/study-microbit-with-test/actions/workflows/repository-checks.yml)

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

### ステップ 0: インストール不要で LED を光らせる

最初の 5 分はセットアップをせず、ブラウザーだけで MakeCode Python 版を動かします。

1. <https://makecode.microbit.org/> で新しいプロジェクトを作る
2. Python へ切り替え、[`sample-compass/src/compass_makecode.py`](./sample-compass/src/compass_makecode.py) の内容を貼り付ける
3. シミュレーターの A ボタンで校正し、LED の方位表示を確認する
4. 実機があればダウンロードした HEX を転送する

ブロックへ切り替えると、同じプログラムをブロックでも観察できます。開発環境と自動テストは、動きを確認した後で準備します。

### Dev Container / Codespaces

リポジトリをDev Containerで開くと、`.devcontainer/setup-dev.sh` が依存関係を導入し、完全な品質ゲートを実行します。成功を隠さない fail-fast 構成です。

### ローカル環境

Node.js 22、Python 3.12、`uv` を用意して、リポジトリのルートで実行します。

```bash
npm ci
npm --prefix sample-compass-ts ci
npm --prefix sample-compass-makecode ci
uv sync --project sample-compass
npm run test:all
```

`npm run test:all` はユニット／統合／MakeCodeシミュレーターテストに加え、テストカバレッジ検査を実行します。

**カバレッジ要件:**
- **Python** (`sample-compass/src/compass_makecode.py`): 100% 以上（100% 未満なら失敗）
- **TypeScript** (`sample-compass-ts/src/compass.ts`): 100% 以上（branches/functions/lines/statements）

## 3つの実装

| ディレクトリ | 実行環境 | 主な教材テーマ | 実機用HEX |
|---|---|---|---|
| [`sample-compass`](./sample-compass/) | MakeCode Python | MakeCode API、境界値、シミュレーター | 生成可能 |
| [`sample-compass-ts`](./sample-compass-ts/) | Node.js | 純粋ロジック、型、例外、Jest | 生成しない |
| [`sample-compass-makecode`](./sample-compass-makecode/) | MakeCode / PXT | ブロックAPI、イベント、シミュレーター | 生成可能 |

`sample-compass-ts` はPCで設計とテストを学ぶ実装です。micro:bitへ転送するTypeScriptは `sample-compass-makecode` を使います。

## よく使うコマンド

| コマンド | 内容 |
|---|---|
| `npm run test:all` | ローカルの完全な品質ゲート |
| `npm run test:config` | ルート設定テスト |
| `npm run test:python` | Pythonユニット／HEX検証テスト |
| `npm run integration:python` | モックを使うPython統合テスト |
| `npm run test:ts` | TypeScriptユニットテスト |
| `npm run integration:ts` | TypeScript統合テスト |
| `npm run test:makecode` | PXTコンパイルとシミュレーターテスト |
| `npm run lint` | Python構文、TypeScript、MakeCodeビルド検査 |
| `npm run build:hex` | MakeCode版のHEXを生成 |

## 実機へ転送する

```bash
npm run build:hex
```

生成物は次の場所です。

- `sample-compass-makecode/built/binary.hex` — MakeCode

HEXをmicro:bitのUSBドライブへコピーします。初回や周囲の磁場が変わった場合は校正してください。詳細は [HEX_BUILD_GUIDE.md](./HEX_BUILD_GUIDE.md) を参照してください。

### MakeCode Python シミュレーター動作テスト（Playwright）

MakeCodeのWebエディターのシミュレーター機能を利用し、PC上で自動的に方位センサーを回転させてLED表示パターンを検証する Playwright 統合テストです。

```bash
npm run integration:python
```

- **検証対象**: `sample-compass/src/compass_makecode.py` (MakeCode Python)
- **テスト仕様**: シミュレーター上の micro:bit を 45度ずつ回転させ、各角度（`0°`, `45°`, `90°`, `135°`, `180°`, `225°`, `270°`, `315°`）における5x5 LED マトリクスの点灯・消灯状態が期待通り（N, E, S, W マークおよびスクロール消去時の消灯）かアサーションします。
- **最適化処理**: テスト実行を高速・安定化するため、テスト中のコード注入時に起動時や方位変更時の文字列スクロール表示を一時的に `basic.clear_screen()` に置換します。テスト結果のシミュレーター画面は `dist/rotation-test-py.png` にスクリーンショットとして保存されます。

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
./sync-ai-skills.sh          # dry-run（変更しない）
./sync-ai-skills.sh --apply  # 既存設定を日時付きバックアップして適用
```

**前提条件:**
- `$HOME/.gemini/config/skills/` ディレクトリが存在すること（Gemini AI ツール向け）
- 実行権限: `.skills/` 配下の `*.md` ファイルが読み取り可能であること
- バックアップ先: `$HOME/.config/` が書き込み可能であること

**同期対象:**
| ツール | ファイル | 用途 |
|--------|---------|------|
| **Gemini (agy)** | `~/.gemini/config/GEMINI.md` | グローバルルール |
| **Claude Code** | `~/.claudecode.md` | CLI ルール |
| **Cursor (Codex)** | `~/.cursorrules` | デフォルトルール |

**VS Code 統合** (自動ではなく手動):
- `.vscode/settings.json` の `github.copilot.chat.codeGeneration.instructions` に CLAUDE.md をリンク

詳細は [`./sync-ai-skills.sh`](./sync-ai-skills.sh) の内部コメントと [`docs/README.md`](./docs/README.md) を参照。

## CIと安全性

GitHub ActionsはPython、TypeScript、MakeCode、統合テスト、リポジトリ設定、依存関係監査を分けて実行します。ローカルhooksは変更されたサブプロジェクトのテストをcommit/push前に実行します。CIを通すためだけにテスト失敗を無視する構成にはしていません。

### npm 依存関係監査

依存関係監査の自動実行は現在無効です。監査を再開する場合の例外（allowlist）は [`security/npm-audit-allowlist.json`](./security/npm-audit-allowlist.json) で管理し、関連スクリプトは [`scripts/audit-npm.js`](./scripts/audit-npm.js) にあります。

### 一時生成物の管理

一時生成物の確認と削除には次を使います。

```bash
./scripts/clean.sh --dry-run
./scripts/clean.sh
```

**スクリプト**: [`scripts/clean.sh`](./scripts/clean.sh)

**対象**:
- ビルド出力: `dist/`, `built/`, `.pytest_cache/`
- カバレッジ: `.coverage/`, `htmlcov/`
- その他: `node_modules/`, `.venv/`

追跡中ファイル、lockfile、`.vscode`／`.idea` のローカル設定は保持されます。Gitの保護判定やファイル走査に失敗した場合は、安全のため削除を中止します。

## ドキュメント構造

本プロジェクトのドキュメントは以下の構造で管理されています：

| ドキュメント | 対象者 | 内容 |
|---|---|---|
| **README.md** (このファイル) | 全員 | プロジェクト全体の概要・クイックスタート・コマンド一覧 |
| **CLAUDE.md** | AI アシスタント | プロジェクト全体の開発ガイド・コード品質ツール定義 |
| **sample-compass/CLAUDE.md** | AI アシスタント (Python) | Python プロジェクト固有のガイド・テスト戦略 |
| **sample-compass-ts/CLAUDE.md** | AI アシスタント (TypeScript) | TypeScript プロジェクト固有のガイド・テスト戦略 |
| **GIT_HOOKS_GUIDE.md** | 開発者 | Git hooks の詳細・トラブルシューティング |
| **MULTILANGUAGE_GUIDE.md** | 学習者 | 複数言語学習ガイド |
| **WORKSHOP_TEMPLATE.md** | 講師 | 90分ワークショップテンプレート |

**推奨**: 開発時は README を入口として、詳細は各 CLAUDE.md を参照してください。

## ライセンス

[MIT License](./LICENSE)
