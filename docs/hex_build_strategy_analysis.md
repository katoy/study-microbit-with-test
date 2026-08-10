# HEX ビルド戦略分析

本書は、`docs/repository_review_2026-08-10.md` の R-1 / R-2 を、2026-08-10 時点の現在の作業ツリーで再確認し、2つの対応案を比較するための資料である。ここでは方針を決定せず、実装変更も行わない。

## 1. 現状分析 (Current State)

### R-1: `npm run build:hex`

#### 現在の作業ツリーで確認できた事実

- ルートの `package.json` には `build:hex` が存在するが、現在の定義は `npm run build:hex:makecode` への委譲である。続く `build:hex:makecode` は `sample-compass-makecode` の `build:hex` を呼ぶ（`package.json:26-27`）。
- MakeCode サブプロジェクトの `build:hex` は `npm run build` であり、その `build` は PXT のセットアップ、`pxt install`、`pxt build` を実行する（`sample-compass-makecode/package.json:7-10`）。PXT の入力ファイルは `src/main.ts` と `src/compass.ts` として設定されており（`sample-compass-makecode/pxt.json:8-11`）、両ファイルとも実在する。
- したがって、**現在の `npm run build:hex` には uflash 呼び出しが含まれていない**。R-1 に記載された「壊れた uflash 呼び出しが現在も `build:hex` に残っている」という状態は、現在の作業ツリーでは確認できなかった。なお、本分析は変更を伴わない現物確認を目的とするため、生成物を書き換える `npm run build:hex` 自体の完走確認は実施していない。
- `sample-compass/compass.py`、`sample-compass/src/compass.py`、`sample-compass/build_hex.py` はいずれも存在しない。`sample-compass` 内で現在確認できる実装用 Python ファイルは `sample-compass/src/compass_makecode.py` であり、これは MakeCode Static Python の実装として説明されている（`sample-compass/CLAUDE.md:10-15,20-29`）。削除済みの MicroPython 実装をそのまま uflash の入力にできない、という R-1 の前提は確認できた。
- Python プロジェクトは引き続き `uflash==2.0.0` に依存し（`sample-compass/pyproject.toml:6-11`）、setuptools の `py-modules` には存在しない `compass` が残っている（`sample-compass/pyproject.toml:17-18`）。現行の MakeCode-only ビルド経路との不整合が残っている。
- 現在の `HEX_BUILD_GUIDE.md` は既に「実機用 HEX の自動生成は MakeCode のみ」と説明している（`HEX_BUILD_GUIDE.md:3-10`）。一方、ルート `README.md` には「micro:bit V1/V2 用 Universal HEX の生成と検証」という学習項目（`README.md:10-17`）と、MakeCode Python からも実機用 HEX を生成可能とする表（`README.md:66-72`）が残っている。

#### レビュー文書との差異

レビュー文書は対象を `8d467e0` の clean な作業ツリーとしている（`docs/repository_review_2026-08-10.md:1-6`）が、再確認時の HEAD は同じ `8d467e0` である一方、`package.json` や `HEX_BUILD_GUIDE.md` などには未コミットの変更が存在する。レビューに記録された旧 `build:hex` の uflash コマンド（`docs/repository_review_2026-08-10.md:102-116`）は、その後の作業ツリー変更で MakeCode PXT 経路へ置き換わっている。

そのため、現在の状態に対する正確な整理は次のとおりである。

- MicroPython のソースと `build_hex.py` が存在しない点は、レビューどおりである。
- 現在のルート `build:hex` が壊れた uflash を実行する、という点は現在の作業ツリーには当てはまらない。
- MakeCode PXT への一本化は既に一部進んでいるが、Option A で想定する「ルートの `build:hex` 自体を削除する」段階までは進んでいない。

### R-2: `npm run verify:blocks`

#### 現在の作業ツリーで確認できた事実

- ルートの `verify:blocks` は `npm --prefix sample-compass run verify:blocks` を実行する（`package.json:28`）。しかし `sample-compass/package.json` は存在せず、同ディレクトリは `pyproject.toml` を持つ uv プロジェクトである。
- 実際に `npm run verify:blocks` を実行すると、`sample-compass/package.json` の `ENOENT` で終了し、終了コードは 254 だった。したがって、ルートコマンドが実行不能という R-2 の指摘は確認できた。
- `scripts/generate-blocks-hex.js` は実在するが、現在のルート `verify:blocks` からは呼ばれていない。現在の入口の問題は、生成スクリプト内のパス以前に、`verify:blocks` が存在しない npm パッケージへ向いていることである。
- 生成スクリプトが参照する3つの入力パスは、いずれも現在の配置と一致しない。

  | スクリプト内の参照 | 行 | 現在実在するパス |
  |---|---:|---|
  | `sample-compass/compass_makecode.py` | `scripts/generate-blocks-hex.js:198` | `sample-compass/src/compass_makecode.py` |
  | `sample-compass-makecode/compass.ts` | `scripts/generate-blocks-hex.js:207` | `sample-compass-makecode/src/compass.ts` |
  | `sample-compass-makecode/main.ts` | `scripts/generate-blocks-hex.js:208` | `sample-compass-makecode/src/main.ts` |

- Python ソースが見つからない場合は警告だけで処理を続け（`scripts/generate-blocks-hex.js:199-204`）、MakeCode TypeScript の2ファイルが見つからない場合も警告だけで終了する（`scripts/generate-blocks-hex.js:210-219`）。実際に `node scripts/generate-blocks-hex.js` を実行すると、2つの警告を出し、何も生成せず終了コード 0 になった。
- 一方、例外が送出された場合の最上位ハンドラーは既に `process.exit(1)` を実行する（`scripts/generate-blocks-hex.js:222-226`）。したがって「すべての失敗経路が exit 0」なのではなく、**ソース未検出を失敗として扱っていないため、その場合だけ no-op の成功になる**、というのが正確である。
- 現在の `test/blocks-generator.test.js` は出力パスとブロック変換判定を検査する（`test/blocks-generator.test.js:11-34,50-88`）が、3つの入力パスの実在や、入力欠落時のプロセス終了コードは検査していない。

#### レビュー文書との差異

R-2 の主要な指摘、すなわちルートコマンドの誤配線、3つの stale path、入力欠落時の exit 0 は現在も再現する。ただし、次の表現上の補正が必要である。

- `scripts/generate-blocks-hex.js` は `verify:blocks` の意図された実装と考えられるものの、現在の `package.json` からは到達しない。
- 修正対象は最上位の `process.exit(1)` そのものではなく、ソース未検出時に `console.warn` だけで終える分岐である。ここで例外を送出するか `process.exitCode = 1` を設定すれば、既存の例外ハンドラーを活用できる。

## 2. オプション A: 削除・一本化

### 実装手順

1. ルート `package.json` から公開コマンド `build:hex` と `verify:blocks` を削除する。ルートの `build:hex:makecode` も公開する必要がなければ同時に整理し、MakeCode サブプロジェクトの `npm run build:hex` を唯一の正規ビルド入口とする。
2. 実機用 HEX の生成手順を `npm --prefix sample-compass-makecode run build:hex`、または `sample-compass-makecode` 内の `npm run build:hex` に統一する。
3. `verify:blocks` を廃止する範囲に応じて、到達不能になる `scripts/generate-blocks-hex.js`、関連テスト、生成用スキル／フックを削除するか、「手動の補助ツール」として明確に切り離す。中途半端な dead code を残さないよう、参照元を一括確認する。
4. Python 側で他に用途がなければ、`sample-compass/pyproject.toml` の uflash 依存と、存在しない `compass` を指す setuptools 設定を整理する。
5. 教材文書を MakeCode PXT の単一経路に合わせる。特に、ルート `README.md:17` の Universal HEX、`README.md:68-72` の Python 実装からの HEX 生成、`sample-compass/README.md:63-70` と `sample-compass-makecode/README.md:73-81` の `verify:blocks` 説明を更新する。現在の `HEX_BUILD_GUIDE.md:3-10` は既に一本化後の説明に近いが、ルート `build:hex` を削除するなら同文書の実行例（`HEX_BUILD_GUIDE.md:20-38`）も変更する。
6. `test/build-config.test.js:17-22` など、現在のルート `build:hex` を契約としている設定テストを、新しい正規入口に合わせて更新する。

### 工数・リスク

- **工数:** 低〜中。ビルドロジックの新規実装は不要だが、コマンド名が複数の教材文書、テスト、補助スクリプトに登場するため、参照の棚卸しが主な作業になる。
- **主なリスク:** 古い授業資料や外部手順がルートの `npm run build:hex` / `verify:blocks` を呼び続けること、Python からブロックへ戻せることの自動検査を失うこと、旧フロー向けの「Universal HEX」説明だけが残り学習者を混乱させること。
- **確認ポイント:** PXT が生成する成果物の対象デバイスと形式を実測し、旧 MicroPython フローで説明していた V1/V2 対応や検証内容をそのまま転記しないこと。

### 教材としての利点

- 実機用成果物の生成元が1つになり、「どのソースがどのコンパイラへ渡るか」を説明しやすい。
- Python/uv/uflash と Node/PXT の二重セットアップを HEX 生成のためだけに維持する必要がなくなる。
- 削除済みの MicroPython 実装に依存する説明をなくし、現在の MakeCode Static Python と MakeCode TypeScript を中心に教材を再構成できる。
- 外部 Web UI を操作する Playwright ベースのブロック検証を正規ビルドから外す場合、授業中のネットワークや MakeCode UI 変更による不安定さを減らせる。

### 教材としての欠点

- MicroPython と MakeCode のランタイム、API、配布形式の違いを実際のビルドで比較する機会がなくなる。
- MakeCode Static Python と TypeScript の双方をブロックへ戻せることを自動で示す教材要素が縮小する。
- ルートから全成果物をまとめて生成する統一コマンドがなくなるため、サブプロジェクトへ移動する操作を学習者に説明する必要がある。
- 既存教材が掲げる「複数言語・複数ツールチェーンの比較」という範囲を狭めることになる。

## 3. オプション B: 修正・両立

### 実装手順

1. Python 側の HEX ビルド対象を明確にする。現在の `src/compass_makecode.py` は MakeCode Static Python であり、削除済みの MicroPython `compass.py` の代替としてそのまま uflash に渡す設計ではない。R-1 で意図された両立を実現するには、MicroPython 用 `compass.py` を復元し、MakeCode Static Python とは別実装として責務を明記する必要がある。
2. 次のいずれかで Python HEX 生成経路を復元する。
   - `build_hex.py` を復元し、uflash で MicroPython ランタイムと復元したソースを結合し、所定の出力先へ保存・検証する。
   - uflash の呼び出しを、実在する `.py` を source として渡す正しい形へ修正する。ただし uflash 2.0.0 の CLI では target は micro:bit の転送先として扱われるため、`dist/hex/compass.hex` という名前付き成果物を作る要件まで含めて設計・検証する。
3. ルートに `build:hex:python` と `build:hex:makecode` を定義し、`build:hex` から両方を fail-fast で順に呼ぶ。片方だけ成功した状態を利用者が「一括ビルド成功」と誤認しない出力にする。
4. `scripts/generate-blocks-hex.js` の3つの入力を、それぞれ `src/` 配下の実在パスへ修正する。
5. 3入力をブラウザー起動前に一括検査し、1つでも欠けていれば例外を送出する。これにより既存の `main().catch(... process.exit(1))` を通し、no-op の exit 0 と、一部だけ生成される状態を防ぐ。
6. ルート `verify:blocks` を `node scripts/generate-blocks-hex.js` へ直接接続する。現在の `npm --prefix sample-compass` 経路は使用しない。
7. 入力パスの実在、欠落時の非ゼロ終了、Python/TypeScript 両方の成果物生成をテストへ追加する。MakeCode Web を使う E2E 検証は、ネットワーク依存の実行頻度と CI 上の扱いを別途定める。
8. 教材文書では、少なくとも「MicroPython + uflash」「MakeCode Static Python + MakeCode Web」「MakeCode TypeScript + PXT」を別の経路として図示し、各成果物名、対応デバイス、検証範囲を混同しないよう更新する。

`build_hex.py` だけを復元しても、入力となる MicroPython 実装がないままでは Python 側 HEX ビルドは成立しない。また、uflash の引数順だけを直して MakeCode Static Python を入力にすることも、実行時 API が異なるため「MicroPython 経路の復元」にはならない。このソース復元は Option B の必須作業として見積もる必要がある。

### 工数・リスク

- **工数:** 高。削除済み実装の復元、2系統の HEX ビルド、Web UI ベースのブロック変換、成果物検証、複数文書の同期が必要になる。
- **主なリスク:** MicroPython 版と MakeCode 版の仕様差分、同じ方位ロジックの重複保守、uflash/PXT/MakeCode Web の更新、ネットワークや UI 変更による `verify:blocks` の不安定化、複数の HEX の用途を学習者が取り違えること。
- **確認ポイント:** 復元した MicroPython 実装が現在の共通仕様とテストに一致すること、生成した HEX が対象 micro:bit で実際に起動すること、失敗時に古い成果物を成功結果として残さないこと。

### 教材としての利点

- 同じ題材を MicroPython、MakeCode Static Python、MakeCode TypeScript で比較でき、言語構文だけでなくランタイムとツールチェーンの違いまで学べる。
- uflash と PXT の双方を実際に動かすことで、ソース埋め込み型ファームウェアと MakeCode プロジェクトのビルド過程を対比できる。
- Python/TypeScript からブロックへ戻せるかを自動検査するため、MakeCode の相互変換制約やグレーブロックを具体的に扱える。
- 複数実装間の仕様整合性テストを教材テーマとして残せる。

### 教材としての欠点

- 初学者が「Python」と呼ばれる2種類の実行環境を混同しやすく、説明量とセットアップ時間が増える。
- ビルド失敗が教材コード、コンパイラ、ブラウザー自動操作、ネットワークのどこにあるかを切り分けにくい。
- 同一仕様を複数実装へ反映する運用が必要になり、教材更新時に差分が生じやすい。
- 授業の主題が方位判定やテスト設計から、環境構築とツールチェーン保守へ逸れる可能性がある。

## 4. 比較表

| 観点 | オプション A: 削除・一本化 | オプション B: 修正・両立 |
|---|---|---|
| 難易度 | 低〜中 | 高 |
| 影響範囲 | ルート npm スクリプト、補助スクリプト、設定テスト、教材文書 | 左記に加え、MicroPython 実装、Python HEX ビルド、成果物検証、CI |
| 正規 HEX 経路 | MakeCode PXT のみ | MicroPython/uflash と MakeCode/PXT |
| 保守性 | 単一経路で比較的高い | 複数実装・複数外部ツールの同期が必要 |
| 失敗要因 | 主に PXT とプロジェクト設定 | Python/uflash、PXT、Playwright、MakeCode Web、ネットワーク |
| 教材の分かりやすさ | 構成を単純化しやすい | 概念を明確に分離しないと複雑になりやすい |
| 教材としての比較価値 | MakeCode 内の Python/TypeScript とテストへ集中 | 言語、ランタイム、ビルド方式を横断して比較可能 |
| 文書更新 | 旧 MicroPython/Universal HEX/`verify:blocks` 説明の撤去・更新 | 3経路と成果物・用語の厳密な再整理 |
| 継続コスト | 低め | 高め |

## 5. 結論

本書では Option A と Option B のどちらを採用するかを決定しない。現在の作業ツリーでは R-1 の uflash 問題は既に MakeCode PXT への委譲によって表面上解消されている一方、MicroPython 実装の不在と関連設定・教材の不整合は残っている。R-2 は、ルートコマンドの誤配線、3つの stale path、入力欠落時の exit 0 を現在も確認できた。

以上を、katoy が「教材を単純化して MakeCode PXT に一本化するか」「保守コストを受け入れて複数言語・複数ツールチェーンの比較を復元するか」を選ぶための分析材料とする。選択後の実装内容と結果報告は別の作業で扱う。
