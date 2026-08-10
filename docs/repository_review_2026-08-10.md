# リポジトリ全体レビュー（2026-08-10 時点）

対象コミット: `8d467e0` (main, working tree clean)

観点: 正確性 / 可読性 / アーキテクチャ / セキュリティ / パフォーマンスの 5 軸。
記載内容は作成時点のスナップショットです。現在の状態は各テストランナーの出力を正とします。

## 検証方法

このレビューは読解だけでなく、以下を実測して裏付けています。

| 実行したもの | 結果 |
|---|---|
| `node --test test/`（ルート設定テスト） | 46 件中 9 件失敗 |
| `npx jest --coverage`（sample-compass-ts） | 74 件全通過 / カバレッジ 100% |
| `uv run ruff check src/compass_makecode.py` | 31 件のエラー |
| `npx eslint src test --max-warnings 0`（sample-compass-ts） | エラー 3 件 / 警告 2 件 |
| `npm run prepare`（ルート） | exit 1（スクリプト未定義） |
| GitHub Actions 実行ログ（run 31336335150 ほか） | 全ジョブ success |

未実測: `npm run test:all` の完走（PXT ビルドとネットワーク必須の Playwright テストを含むため）。

## 総評

学習教材としての設計（同一仕様を 3 実装で比較、境界値テストの網羅、多層の品質ゲート）はよく考えられている。
一方で、直近の大規模リファクタ（`compass.py` 削除・npm workspaces 化・npm audit 廃止）の後始末が広範に取り残されており、
**「CI は緑だが、実際には何も検証していない」ゲートが複数存在する**状態にある。

---

## Critical — 対処必須

### C-1. Bandit セキュリティスキャンが 0 行しか走っていない

`.github/workflows/security.yml:70`

```yaml
run: uvx bandit@1.9.4 sample-compass/compass_makecode.py
```

実ファイルは `sample-compass/src/compass_makecode.py`。CI 実行ログ（run 31336335150）の実際の出力:

```
Test results:
	No issues identified.
Code scanned:
	Total lines of code: 0
```

bandit は存在しないパスを渡されても exit 0 を返すため、**「Security Scan ✅」バッジはスキャン 0 行の結果**である。
セキュリティゲートの偽の安心は最も危険な欠陥。

**対応**: パスを `sample-compass/src/compass_makecode.py` に修正する。あわせて、スキャン対象 0 件を失敗として扱えないか検討する。

### C-2. ルートの `test/` 46 テストがどこからも実行されていない

`test/` には 11 ファイル・46 件のリポジトリ設定テストがあるが、実行経路が存在しない。

`package.json:18-19`

```json
"test:config": "npm run test:config:ci",
"test:config:ci": "echo 'npm audit チェックは無効化されています'"
```

`.github/workflows/repository-checks.yml` はこの `test:config` を実行して即座に成功する。
つまり **Repository Checks ワークフローは echo 1 行を実行しているだけ**である。

`node --test test/` を実行すると 46 件中 9 件が失敗し、いずれも実在する退行を正しく検出している。

| 失敗テスト | 検出している問題 |
|---|---|
| `device HEX builds use only the MakeCode toolchain` | `build:hex` が壊れた uflash 呼び出しのまま（R-1） |
| `MakeCode tests execute in the simulator from root scripts and CI` | 期待するスクリプトが `undefined` |
| `TypeScript lint preserves the compiler exit code` | `lint:ts` スクリプトが消滅 |
| `mocked workflows are named integration tests rather than end-to-end tests` | `integration:ts` の呼び出し形式が変更済み |
| `TypeScript development and CI use the supported Node 22 line` | 参照先 `sample-compass-ts/.tool-versions` が存在しない |
| `the local all-tests command enforces the documented coverage threshold` | `test:all` からカバレッジ検査が消えた |
| `security workflow audits every dependency ecosystem in the repository` | npm audit 廃止・workspaces 化に未追随（テスト側の更新が必要） |
| `blocks-generator.test.js` / `simulator.test.js` | `playwright` がルートの依存に無い |

最後の 2 つとセキュリティワークフローのテストは workspaces 化に伴う意図的変更への未追随なのでテスト側を更新すべきだが、
残りは**本物の退行を握りつぶしている**。

**対応**: `test:config` をルート `test/` の実行に戻し、9 件を「テストを直す / コードを直す」に仕分ける。

### C-3. Git hooks が clone しても有効にならない

- ルート `package.json` に `devDependencies` も `prepare` スクリプトも無い
- `node_modules/husky` が存在しない

現状動作しているのは、開発機で `git config core.hooksPath .husky` が手動設定されているため。
新規に clone した学習者・講師の環境では pre-commit / pre-push は**一切動かない**。
`README.md` と `GIT_HOOKS_GUIDE.md` はこれらが自動で動く前提で書かれている。

**対応**: husky を devDependency として追加し、`"prepare": "husky install"` を定義する。

---

## 要修正

### R-1. `npm run build:hex` が実行不能

`package.json:23`

```
cd sample-compass && uv run python -m uflash dist/hex/compass.hex && npm --prefix sample-compass-makecode run build
```

uflash の第 1 引数は「ソース `.py`」であり、出力先 HEX パスではない。
さらに MicroPython 実装 `compass.py` はすでに削除済みで、ビルド対象そのものが存在しない。

`HEX_BUILD_GUIDE.md` は全編が `uv run python build_hex.py`（存在しないスクリプト）と `compass.py` を前提に書かれている。
また `npm run build:hex:python` / `npm run build:hex:makecode` を説明しているが、どちらも `package.json` に定義が無い。

**対応**: MicroPython 実装を削除した以上、Python 側の HEX 生成は撤去して MakeCode ビルドのみに一本化するのが一貫する。

### R-2. `npm run verify:blocks` が実行不能、かつ中身が no-op

- `package.json:24` は `npm --prefix sample-compass run verify:blocks` を呼ぶが、`sample-compass/` に `package.json` は無い（uv プロジェクト）
- 仮に到達しても `scripts/generate-blocks-hex.js` のパスがすべて古い

```
198: sample-compass/compass_makecode.py        → 実際は src/ 配下
207: sample-compass-makecode/compass.ts        → 実際は src/ 配下
208: sample-compass-makecode/main.ts           → 実際は src/ 配下
```

しかも見つからない場合は `console.warn` して**正常終了**するため、失敗が終了コードに現れない。
`main()` は「何も生成せずに成功」を返す。

**対応**: パスを修正したうえで、ソース未検出時は例外を投げて失敗させる。

### R-3. Python のカバレッジ 100% は達成されていない（測定もされていない）

`sample-compass/pyproject.toml:26` は `source = ["src/compass_makecode.py"]` を指定しているが、
`test/test_simulator.py` はこのファイルを **import せず、テキストとして読んでブラウザに注入する**（`test_simulator.py:112-121`）。
したがって coverage は構造上 0% であり、そもそも `--cov` を付ける実行経路も存在しない。

にもかかわらず以下の記載がある。

- `README.md:63` — 「**Python** (`sample-compass/src/compass_makecode.py`): 100% 以上（100% 未満なら失敗）」
- `sample-compass/CLAUDE.md` — 「CI では 100% カバレッジが必須（`pyproject.toml` で設定）」

教材としてこの虚偽記載は看過できない（学習者にカバレッジの意味を誤って教えることになる）。

なお TypeScript 側は実測で 74 テスト全通過・statements/branches/functions/lines すべて 100% であり、記載どおり。

**対応**: 記載を実態に合わせるか、Python 側にロジック単体テストを追加して実際に測定する（R-7 と併せて解決するのが望ましい）。

### R-4. MakeCode 実装がセンサーを 2 回読むため表示とログが食い違う

`sample-compass-makecode/src/main.ts:21-23`

```typescript
const heading = Compass.getHeading();
const direction = Compass.getDirection();   // 内部で getHeading() を再実行
console.log("Time: " + input.runningTime() + "ms, Heading: " + heading + ", Dir: " + direction);
```

`Compass.getDirection()` は `src/compass.ts:80` で `getHeading()` を呼び直し、`getHeading()` は `input.compassHeading()` を再実行する。
2 回の読み取りの間に本体が回転すると、**ログの角度と方向名が矛盾する**。
`main.ts:38-43` の forever ループも同様で、`heading < 0` の判定に使った値と矢印表示に使う値が別サンプルになる。

Python 実装（`sample-compass/src/compass_makecode.py:70-75`）は 1 回読んだ `heading` から
`get_direction_string(heading)` を導出しており一貫している。
同一仕様を 3 実装で比較することが教材の核なので、これは仕様レベルの不整合。

シミュレーターテストは heading を固定して評価するため、この不具合を原理的に検出できない。

**対応**: `heading` を 1 回だけ読み、`Compass.headingToDirection(heading)` に渡す形へ統一する。

### R-5. `Compass.getHeading()` の隠れた副作用

`sample-compass-makecode/src/compass.ts:66-68`

```typescript
if (_heading < 0) {
  _isCalibrated = false;   // getter が状態を書き換える
}
```

この結果、`getDirection()` は 1 回目 `'ERR'`、2 回目以降 `'CAL'` を返す非冪等な関数になる。
「防御的プログラミングの練習」というコメントがあるが、getter の副作用は教材として逆の教訓になる。

**対応**: 値の取得と状態遷移を分離する。

### R-6. Lint が両言語とも壊れており、かつどこからも実行されていない

**TypeScript** — `npx eslint src test --max-warnings 0` でエラー 3 件:

- `.eslintrc.json:23` の `@typescript-eslint/explicit-function-return-types` は存在しないルール名
  （正しくは単数形 `explicit-function-return-type`）→ `Definition for rule ... was not found`
- `tsconfig.json:18-19` が `test/` を include していないため、型付き lint が全テストファイルで Parsing error

**Python** — `uv run ruff check src/compass_makecode.py` で **31 件の F821**。
MakeCode が注入する `basic` / `input` / `console` / `Button` / `ArrowNames` / `number` がすべて未定義名として報告される。

両方とも各 `CLAUDE.md` に品質ツールとして明記されているが、`package.json` / hooks / CI のどこからも呼ばれていない。

**対応**:
- ESLint はルール名を修正し、テスト用 tsconfig を用意する
- ruff は MakeCode Static Python の性質上 F821 が正当なので、
  `[tool.ruff.lint.per-file-ignores]` で `src/compass_makecode.py` の F821 を除外したうえで**有効化する**

### R-7. `test:python` の実体はネットワーク必須の Playwright テスト

`package.json:12,16`

```json
"test:python":        "cd sample-compass && uv run pytest test/test_simulator.py -v",
"integration:python": "cd sample-compass && uv run pytest test/test_simulator.py -v",
```

両者は**完全に同一のコマンド**で、中身は `makecode.microbit.org` に実アクセスする Playwright テスト。結果として:

- `npm run test:all` はネットワーク必須・数分オーダー・外部サイトの UI 変更で壊れる
- `README.md:83` の「Pythonユニット／HEX検証テスト」、`README.md:84` の「モックを使うPython統合テスト」はいずれも事実と異なる
  （モックベースのテストは削除済みで存在しない）
- `README.md:20` の「PC上のPython統合テストは `microbit` API をモックします」も同様

高速なロジック単体テストが Python 側に 1 つも無いのは、TDD を教える教材として弱い。

**対応**: `get_direction_string` の純粋関数部分に対する pytest を追加し、`test:python` をそちらに割り当てる。
Playwright テストは `integration:python` に残す。

### R-8. Dev Container のセットアップが必ず失敗する

`.devcontainer/setup-dev.sh:45`

```bash
npm run prepare > /dev/null 2>&1
```

ルートに `prepare` スクリプトが無いため exit 1。冒頭の `set -euo pipefail` により**ここで確実に停止する**（実測で `EXIT=1` を確認）。
`README.md:46` が謳う「Codespaces で開けば完全な品質ゲートが走る」は成立していない。

C-3 で `prepare` を定義すれば同時に解消する。

### R-9. README のコマンド表に存在しないコマンドが並んでいる

`README.md:76-91` の表の実態:

| コマンド | 状態 |
|---|---|
| `npm run test:simulator:playwright` | **存在しない** |
| `npm run audit:npm` | **存在しない**（commit `8e3187c` で削除） |
| `npm run verify:blocks` | 実行不能（R-2） |
| `npm run build:hex` | 実行不能（R-1） |
| `npm run test:config` | 実体は echo（C-2） |

その他の不一致:

- `README.md:177` の `security/.npm-audit-exceptions.json` — 実ファイル名は `security/npm-audit-allowlist.json`
- `README.md:116` の `sample-compass/compass_makecode.py` — パスが古い（`src/` 配下）
- `README.md:118` の `dist/rotation-test-ts.png` — これを生成するテストは存在しない（Python 版のみ）
- `README.md:50` の「Python 3.11以上」 — `requires-python = ">=3.12"` および `.tool-versions`（3.12.8）と矛盾
- `README.md:70` の `sample-compass` 実行環境「MicroPython / MakeCode Python」 — MicroPython 実装は削除済み

### R-10. 教材ドキュメントが削除済みファイルを前提にしている

学習者が直接手を動かす文書に、存在しないファイルへの手順が残っている。

| 文書 | 該当行 | 内容 |
|---|---|---|
| `WORKSHOP_TEMPLATE.md` | 79, 91, 95, 126, 159 | `sample-compass/test_compass.py` を開く / `pytest test_compass.py` / `compass.py` と対応させる |
| `VIDEO_TUTORIAL_SCRIPT.md` | 47, 58, 67 | `sample-compass/compass.py` の画面 / `test_compass.py` に追記 |
| `HEX_BUILD_GUIDE.md` | 全編 | `build_hex.py` / `npm run build:hex:python` / `build:hex:makecode` |
| `docs/` 配下 | 多数 | `test_compass.py`, `test_build_hex.py`, `compass.py` |

90 分ワークショップの手順書がその場で詰まるのは、教材としては Critical 相当の実害。

`README.md:134` に「過去の評価レポートの件数はスナップショット」という注記はあるが、
`WORKSHOP_TEMPLATE.md` / `VIDEO_TUTORIAL_SCRIPT.md` / `HEX_BUILD_GUIDE.md` は過去レポートではなく**現行の手順書**であり、この注記では免責されない。
`docs/` 配下の過去レビューは既に非規範として明示されているので対象外でよい。

---

## Consider（任意）

- **Consider**: `sample-compass-makecode/src/compass.ts:9-18` の `CompassDirection` 型と `CompassState` インターフェースは
  どこからも参照されていない dead code。`getDirection()` の戻り値を `string` から `CompassDirection` に変えれば型が機能し始める。
- **Consider**: `sample-compass-ts/src/compass.ts:63-65` の範囲チェックは `headingToDirection`（93-95 行）と完全重複。
  private `headingToDirection`（119-121 行）は static を呼ぶだけのラッパーで、
  `getDirection()` は直前に `const heading` を取りながら `this.heading` を渡している。3 点まとめて整理できる。
- **Consider**: `scripts/pre-build-hex-hook.js` と `scripts/pre-build-hook-runner.js` はログ文言以外ほぼ同一で、
  `.agents/hooks.json` が参照するのは後者のみ。前者は削除候補。両ファイルとも未使用の `require('fs')` がある。
- **Consider**: `scripts/audit-npm.js` は冒頭で `console.log` + `exitCode = 0` して以降のロジックが死んでいる
  （「テストのために保持」とあるが、そのテスト自体が実行されていない → C-2）。
  `security/npm-audit-allowlist.json` も孤児。npm audit を廃止したなら一式削除、続けるなら復活させる、どちらかに倒すべき。
- **Nit**: `sample-compass/pyproject.toml:18` の `py-modules = ["compass"]` は削除済みモジュール名。
- **Nit**: ルート `CLAUDE.md` は `sync-ai-skills.sh` が Copilot の `settings.json` に「自動登録」すると書いているが、
  スクリプト自身は `VS Code settings are intentionally unchanged.` と出力する。
  `README.md:157` は正しく「手動」と書いており、CLAUDE.md 側が古い。
- **FYI**: 開発機のローカル Node は v20.20.2 で、`.tool-versions`（22.23.2）と `engines`（>=22.23.2）を満たしていない。
  `asdf install` の実行漏れと思われる。CI は 22.23.2 で動作しているため CI 結果には影響しない。

---

## 良かった点

- `sample-compass-ts` は 74 テスト・カバレッジ 100%（実測確認済み）。境界値の網羅も丁寧。
- `scripts/clean.sh` は git 管理下パスの保護、削除ルートの拒否、プロジェクト外パスの拒否、`--dry-run` と、
  破壊的スクリプトとして模範的な作り。
- GitHub Actions の全アクションが commit SHA 固定。Trivy も `exit-code: '1'` かつバージョン固定。
- `sync-ai-skills.sh` が既定 dry-run・タイムスタンプ付きバックアップ。
- `simulator-test-runner.cjs` は結果パースで total/passed/failed の整合性まで検証しており、
  `targetVersions` を伝播させる理由がコメント（86-88 行）で説明されている。
- `.gitignore` は網羅的で、`error-rotation-*.png` などのデバッグ生成物も追跡されていない。

---

## 推奨対応順

1. **C-1** security.yml の bandit パス修正 — 1 行、影響が最も大きい
2. **C-2** `test:config` をルート `test/` の実行に戻し、9 件の失敗を仕分け
   — これが復活すれば R-1〜R-3 の多くは以後自動的に検出され続ける
3. **C-3 / R-8** husky を devDependency + `prepare` として復帰
4. **R-9 / R-10** 実行不能な手順を文書から削除または修正
5. **R-1 / R-2** `build:hex` / `verify:blocks` は「直す」か「消す」を決める
6. **R-4 / R-5** MakeCode の二重センサー読み取りと getter 副作用を修正
7. **R-6 / R-7** lint の有効化と Python 高速ユニットテストの追加
