# MakeCodeシミュレーターテストガイド

このプロジェクトは、PXTの内蔵シミュレーターで方位角から8方位への変換を検証します。

## 実行方法

```bash
cd sample-compass-makecode
npm ci
npm test
```

`npm test` は次の処理を順に実行します。

1. `simulator-test-runner.test.cjs` で結果パーサーと失敗判定を検証
2. `pxt test` でMakeCodeテストコードをコンパイル
3. `pxt run` で28件の方位判定を実行し、成功件数と失敗件数を検証

テスト失敗、結果マーカーの欠落、件数の不一致はいずれも非ゼロ終了になります。

個別に確認する場合は次のコマンドを使用します。

```bash
npm run test:runner
npm run test:compile
npm run test:simulator
```

## 検証範囲

自動テストが検証するのは、MakeCode/PXT上で動く方位変換ロジックです。次の項目は検証しません。

- 実機の磁気センサー、ボタン、LED表示
- USB経由のHEX転送
- ブラウザ版MakeCode EditorのUI
- ブラウザ内シミュレーターのクリック操作

ブラウザ上で手動確認する場合は `npm run serve` を実行し、表示されたURLを開いてください。この操作は自動テストには含まれません。

## トラブルシューティング

依存関係やPXTモジュールが不足している場合は、再度セットアップします。

```bash
npm ci
npm run pxt:setup
npx pxt install
```

生成物を確認せず削除しないよう、クリーン処理の事前確認には次を使用します。

```bash
../scripts/clean.sh --dry-run sample-compass-makecode
```
