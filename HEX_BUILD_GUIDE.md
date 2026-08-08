# HEX ファイル生成ガイド

このプロジェクトの各実装から micro:bit 用の HEX ファイルを生成できます。

## クイックスタート

### すべてのプロジェクトの HEX を生成

```bash
npm run build:hex
```

### 個別プロジェクトの HEX を生成

**TypeScript プロジェクト:**
```bash
cd sample-compass-ts
npm run build:hex
```

**Python プロジェクト:**
```bash
cd sample-compass
uv run python build_hex.py
```

## 生成されるファイル

HEX ファイルは各プロジェクトの `dist/hex/` ディレクトリに生成されます。

```
sample-compass/dist/hex/compass.hex       # Python 実装
sample-compass-ts/dist/hex/compass.hex    # TypeScript 実装
```

## 詳細

### TypeScript HEX ビルド (`sample-compass-ts`)

**方法**: TypeScript → JavaScript → HEX 変換

**ビルドスクリプト**: `scripts/generate-hex.js`

**特徴**:
- TypeScript をコンパイルして JavaScript に変換
- JavaScript コードを micro:bit HEX ラッパーに変換
- Intel HEX フォーマットで出力

**実行**:
```bash
npm run build       # TypeScript をコンパイル
npm run build:hex   # HEX ファイルを生成
```

### Python HEX ビルド (`sample-compass`)

**方法**: Python → MicroPython → HEX 変換（uflash 使用、またはフォールバック）

**ビルドスクリプト**: `build_hex.py`

**特徴**:
- uflash がインストールされている場合は、uflash で正式にコンパイル
- uflash がない場合は、フォールバック版 HEX を生成
- Intel HEX フォーマットで出力

**実行**:
```bash
uv run python build_hex.py
```

**uflash をインストール** (オプション、より正確な HEX を生成):
```bash
cd sample-compass
uv pip install uflash
```

その後、実際のコマンドラインでも使用可能：
```bash
uflash compass.py
```

## HEX ファイル形式について

生成される HEX ファイルは [Intel HEX](https://ja.wikipedia.org/wiki/Intel_HEX) フォーマットです。

- **実装版**: uflash でコンパイルされた完全な MicroPython バイナリ
- **フォールバック版**: ソースコードを含むシンプルな HEX ラッパー（テスト・デモ用）

実際の micro:bit へのデプロイには：
1. **MakeCode オンラインエディタ** を使用（推奨）
2. または **uflash** コマンドで直接フラッシュ：
   ```bash
   uflash compass.py
   ```

## CI/CD での自動生成

GitHub Actions ワークフローは以下の場合に HEX ファイルを自動生成できます：
（設定例は `.github/workflows/` を参照）

```yaml
- name: Generate HEX files
  run: npm run build:hex
```

## トラブルシューティング

### Python HEX ビルドでエラーが出る

**原因**: uflash が見つからない

**解決方法 1**: uflash をインストール
```bash
cd sample-compass
uv pip install uflash
```

**解決方法 2**: Python が asdf で管理されている場合
```bash
asdf install python 3.11.5
asdf local python 3.11.5
uv pip install uflash
```

### TypeScript HEX ビルドでエラーが出る

**原因**: TypeScript がコンパイルされていない

**解決方法**: ビルドを実行
```bash
cd sample-compass-ts
npm run build
npm run build:hex
```

### HEX ファイルが生成されない

**確認**:
1. `dist/` ディレクトリが存在するか確認
2. コンパイルエラーがないか確認
3. スクリプトの実行権限を確認

```bash
# TypeScript の場合
cd sample-compass-ts
npm run clean
npm run build

# Python の場合
cd sample-compass
uv run python build_hex.py
```

## npm Scripts リファレンス

### ルート プロジェクト

| コマンド | 説明 |
|---------|------|
| `npm run build:hex` | 全プロジェクトの HEX を生成 |
| `npm run build:hex:python` | Python HEX を生成 |
| `npm run build:hex:ts` | TypeScript HEX を生成 |

### TypeScript プロジェクト

| コマンド | 説明 |
|---------|------|
| `npm run build` | TypeScript をコンパイル |
| `npm run build:hex` | HEX ファイルを生成 |

### Python プロジェクト

```bash
cd sample-compass
uv run python build_hex.py
```

## さらに詳しく

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [Intel HEX フォーマット](https://en.wikipedia.org/wiki/Intel_HEX)
- [uflash GitHub](https://github.com/ntoll/uflash)
- [MakeCode Editor](https://makecode.microbit.org/)
