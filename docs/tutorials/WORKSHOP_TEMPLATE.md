# 90分ワークショップ: micro:bit方位磁石と自動テスト

MakeCodeで動きを観察し、PythonとTypeScriptで同じ境界値を検証する授業案です。対象はプログラミング入門を終えた中学生以上、定員は1名から30名程度を想定します。

## 到達目標

終了時に学習者は次を説明・実行できます。

- 方位角と8方位の対応を説明する
- `input.compassHeading()` と加速度APIを区別する
- 境界値テストを1件追加する
- モック、シミュレーター、実機の保証範囲を区別する
- ルート品質ゲートを実行し、失敗箇所を読める

## 準備

講師は授業前に次を確認します。

```bash
npm ci
npm --prefix sample-compass-ts ci
npm --prefix sample-compass-makecode ci
uv sync --project sample-compass
npm run test:all
npm run build:hex
npm run verify:blocks
```

ブロック変換は MakeCode Web に依存するため、講師だけがネットワークの安定した環境で [`sample-compass/src/compass_makecode.py`](./sample-compass/src/compass_makecode.py) を貼り付け、ブロックへ切り替えられることを授業前に確認します。授業中の必須手順にはしません。

実機を使う場合は、micro:bit V1/V2、USB ケーブル、磁石から離れた校正場所を用意します。ネットワークが不安定な授業では依存関係と MakeCode 画面を事前に準備してください。2 人 1 台でも進行できます。

## 時間割

| 時間 | 内容 | 成果物 |
|---|---|---|
| 0〜10分 | 導入と環境確認 | 3実装の役割を言える |
| 10〜30分 | MakeCodeで観察 | コンパスAPIとLED表示を確認 |
| 30〜50分 | TypeScript境界値テスト | テストを1件追加 |
| 50〜65分 | MakeCode Python比較 | 型とAPIの違いを説明 |
| 65〜80分 | 品質ゲート | 失敗→修正→成功を体験 |
| 80〜88 分 | 実機またはシミュレーター確認 | HEX 転送または操作確認 |
| 88〜90分 | 振り返り | 保証範囲を一言で共有 |

合計90分です。

## 0〜10分: 導入

ルートREADMEの「3つの実装」を見せます。次の問いから始めます。

> micro:bitが「67.5度」と返したとき、NEとEのどちらにしますか？

範囲表を示し、境界値は仕様で決める必要があることを確認します。テストはその決定を実行可能な形で残すものだと説明します。

チェックポイント: 学習者が `sample-compass-ts` は実機HEXを作らないと答えられる。

## 10〜30分: MakeCode

1. [`sample-compass-makecode/src/main.ts`](./sample-compass-makecode/src/main.ts) を開く
2. ボタンA、ボタンB、`basic.forever` の3つを探す
3. [`compass.ts`](./sample-compass-makecode/src/compass.ts) で `input.compassHeading()` を探す
4. `input.acceleration(Dimension.X)` が方位角の代用にならない理由を話す

実行:

```bash
npm --prefix sample-compass-makecode test
```

出力末尾の `MAKECODE_TEST_RESULT` を探します。テストは `setHeadingForTest()` を使うため、実機センサーを読んでいないことも確認します。

実機がある場合は、生成済みHEXを転送し、Aで校正、Bで状態表示を試します。校正中は本体の指示に従って動かします。

## 30〜50分: TypeScript境界値テスト

1. [`sample-compass-ts/test/compass.test.ts`](./sample-compass-ts/test/compass.test.ts) を開く
2. 境界値テストに次を追加する

```typescript
test('337.5 度の直前と境界を判定する', () => {
  expect(Compass.headingToDirection(337.49)).toBe('NW');
  expect(Compass.headingToDirection(337.5)).toBe('N');
});
```

3. テストを実行する

```bash
npm --prefix sample-compass-ts test
```

4. [`sample-compass-ts/src/compass.ts`](./sample-compass-ts/src/compass.ts) の `heading < 22.5 || heading >= 337.5` と対応させる

早く終わった学習者は、`-1`、`360`、`NaN` を与えるテストを読み、無効な値を `ERR` に変換する防御的プログラミングの狙いを考えます。

## 50〜65分: MakeCode Python比較

[`sample-compass/src/compass_makecode.py`](./sample-compass/src/compass_makecode.py) と [`sample-compass-ts/src/compass.ts`](./sample-compass-ts/src/compass.ts) を開きます。

- `Direction` が許す文字列
- `Number.isFinite` が必要な理由
- MakeCode が提供する `input.compass_heading()` とPC上の内部値の違い

を探します。

```bash
npm --prefix sample-compass-ts run build
```

ペアで「MakeCode Pythonは実機APIを呼び、Node TypeScriptは純粋ロジックを検証する」という役割の違いを説明します。

## 65〜80分: 品質ゲート

講師は学習用ブランチで、先ほど追加した期待値を一時的に誤った値へ変え、テスト失敗を見せます。学習者は失敗したテスト名、期待値、実際値を読み、正しい値へ戻します。

```bash
npm run test:all
```

次に `.github/workflows/` と `.husky/` を見て、ローカルとCIの二重の安全網を確認します。`test:all` はカバレッジも含むため、単に「テストが通る」だけでなく未実行経路も検査します。

設問: `sample-compass-ts/src/compass.ts` のカバレッジが 100% でも、`sample-compass/src/compass_makecode.py` の不具合や、`-5`、`400`、`NaN` の期待結果が未検証なら見逃せるのはなぜでしょうか。「カバレッジ 100% = バグゼロ」ではない理由を 1 文で答えます。

## 80〜88分: 最終確認

### 実機を使う場合

```bash
npm run build:hex
```

生成されたMakeCodeのHEXを確認し、micro:bitへ転送します。

### 実機がない場合

MakeCode シミュレーターで A ボタンによる校正、B ボタンによる状態確認、LED の方位表示を操作します。ブロック変換の自動検査結果は、講師が準備節で確認した結果を共有します。

## 88〜90分: 振り返り

各自が次の文を完成させます。

- モックテストが保証するのは「___」で、保証しないのは「___」
- 境界値テストが必要なのは「___」
- カバレッジ 100% でも保証できないのは「___」
- 実機で最後に確認したいのは「___」

## つまずき対応

| 症状 | 確認 |
|---|---|
| `uv` が見つからない | Dev Containerを使うか、uvを導入する |
| `pxt` が見つからない | `npm --prefix sample-compass-makecode ci` を実行 |
| PXTキャッシュの権限エラー | 所有者とホームディレクトリの書込権限を確認 |
| コンパスが正しく向かない | 校正し、磁石・スピーカー・金属から離す |
| MakeCodeでブロック変換できない | `sample-compass/src/compass_makecode.py` を使っているか確認 |

授業でリポジトリ本体を汚さないため、学習者ごとにブランチを作るか、終了後に自分の変更だけを戻してください。
