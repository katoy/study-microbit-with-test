# HEX ファイル生成ガイド

このリポジトリの自動ビルドは、実機用HEXの生成にMakeCodeのみ対応しています。

| 実装 | 正規ツールチェーン | 出力 |
|---|---|---|
| MakeCode TypeScript | `pxt build` | `sample-compass-makecode/built/binary.hex` |

`sample-compass-ts` はNode.js上で方位ロジックを学習・テストするための実装です。
MakeCode/PXTプロジェクトではないため、実機用HEXは生成しません。

## セットアップ

```bash
cd sample-compass-makecode
npm ci
cd ..
```

## ビルド

ルートディレクトリから実行します。

```bash
npm run build:hex
```

ルートのスクリプトは `sample-compass-makecode` のPXTビルドを実行します。生成先は `sample-compass-makecode/built/binary.hex` です。

## MakeCode版

```bash
cd sample-compass-makecode
npm run build:hex
```

Microsoft MakeCodeのPXT CLIが `sample-compass-makecode/pxt.json`、`sample-compass-makecode/src/main.ts`、`sample-compass-makecode/src/compass.ts` を対象に
実機用HEXをコンパイルします。

## MakeCode Webでブロックを確認

生成した `sample-compass-makecode/built/binary.hex` を <https://makecode.microbit.org/> へドラッグ＆ドロップし、ブロック表示へ切り替えます。この確認にはネットワーク接続が必要です。

## 実機への転送

生成された `.hex` ファイルをUSBストレージとして表示された `MICROBIT` ドライブへ
コピーします。

## トラブルシューティング

### MakeCode: パッケージ不足

```bash
cd sample-compass-makecode
npm ci
npm run build:hex
```

### 通常TypeScript版からHEXを作りたい

`sample-compass-ts` のロジックを実機で使用する場合は、MakeCode APIに合わせて
`sample-compass-makecode` 側へ移植し、PXTでビルドしてください。

## 参考資料

- [MakeCode `pxt build`](https://makecode.com/cli/build)
- [micro:bit HEXフォーマット](https://tech.microbit.org/software/hex-format/)
