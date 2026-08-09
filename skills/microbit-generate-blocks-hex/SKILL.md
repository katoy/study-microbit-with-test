---
name: microbit-generate-blocks-hex
description: Python や TypeScript の micro:bit ソースコードから、MakeCode Web エディタ経由で「ブロック表示対応の HEX ファイル」を Playwright ブラウザ自動操作によって自動生成します。
---

# Micro:bit Blocks-Compatible HEX Generator

このスキルは、micro:bit のローカルソースコード（TypeScript または Python）を MakeCode Web エディタに流し込み、ブロック（Blocks）に変換した状態で HEX ファイルを自動でダウンロードして保存します。

## 実行方法

プロジェクトルートにある自動化スクリプトを実行することで、自動的にヘッドレスブラウザが立ち上がり、HEX ファイルを生成・上書き保存します。

```bash
node ./scripts/generate-blocks-hex.js
```

### 生成される出力ファイル
- **Python 版**: `sample-compass/dist/hex/binary.hex`
- **TypeScript / MakeCode 版**: `sample-compass-makecode/built/binary.hex`

どちらもプログラム名に依存しない固定ファイル名 `binary.hex` へ直接出力し、既存ファイルがあれば上書きします。

## ライフサイクルフックによる自動実行
このスキルはグローバルのライフサイクルフック (`hooks.json`) に登録されています。
そのため、あなたがエージェントやターミナルで `npm run build:hex` または `build_hex.py` を含むコマンドを実行した際、この Playwright 生成処理が**自動的にインターセプト（割り込み）して実行**されます。
