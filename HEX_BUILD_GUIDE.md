# HEX ファイル生成ガイド

このリポジトリでは、実機用HEXを生成できる実装を次の2つに限定しています。

| 実装 | 正規ツールチェーン | 出力 |
|---|---|---|
| MicroPython | `uflash==2.0.0` | `sample-compass/dist/hex/compass.hex` |
| MakeCode TypeScript | `pxt build` | `sample-compass-makecode/built/binary.hex` |

`sample-compass-ts` はNode.js上で方位ロジックを学習・テストするための実装です。
MakeCode/PXTプロジェクトではないため、実機用HEXは生成しません。

## セットアップ

```bash
cd sample-compass
uv sync

cd ../sample-compass-makecode
npm ci

cd ..
```

## 一括ビルド

ルートディレクトリから実行します。

```bash
npm run build:hex
```

これは次の2コマンドを順番に実行します。

```bash
npm run build:hex:python
npm run build:hex:makecode
```

どちらかのコンパイラが失敗した場合、一括ビルドも失敗します。

## MicroPython版

```bash
cd sample-compass
uv run python build_hex.py
```

ビルドスクリプトは `uflash` を使ってMicroPythonランタイムと `compass.py` を
Universal Hexへ結合します。生成後にIntel HEXのレコード長、チェックサム、
終端レコードに加え、micro:bit V1（target `0x9900`）とV2（target `0x9903`）の
両ブロックに対応形式のファームウェアデータがあることを検証します。単一機種向けの
通常Intel HEXや、片方のブロックしかない出力は成功として扱いません。

コンパイラが見つからない、コンパイルに失敗する、または出力が不正な場合は
終了コード1になります。ダミーHEXへのフォールバックはありません。

## MakeCode版

```bash
cd sample-compass-makecode
npm run build:hex
```

Microsoft MakeCodeのPXT CLIが `pxt.json`、`main.ts`、`compass.ts` を対象に
実機用HEXをコンパイルします。

## 実機への転送

生成された `.hex` ファイルをUSBストレージとして表示された `MICROBIT` ドライブへ
コピーします。Python版のUniversal Hexはmicro:bit V1/V2の両方を収録します。

## トラブルシューティング

### Python: `uflash is required`

```bash
cd sample-compass
uv sync
uv run python build_hex.py
```

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
- [uflash](https://github.com/ntoll/uflash)
