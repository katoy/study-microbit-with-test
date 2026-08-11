# microbit-makecode-recorder

micro:bit プログラム実行を MakeCode オンラインエディタで GIF アニメーションとして記録するスキル。

## 特徴

- **メソッドチェーン形式 API**: 流暢で直感的な操作定義
- **自動ブラウザ操作**: Playwright による MakeCode の自動制御
- **カーソル可視化**: マウスカーソル常時表示 + クリック効果
- **GIF 生成**: 教育コンテンツ向けのアニメーション出力

## インストール

```bash
pip install -e skills/microbit-makecode-recorder/
```

## 使用方法

### 基本的な使い方

```python
from microbit_makecode_recorder import MicrobotRecorder
import asyncio

async def record_tutorial():
    # recorder インスタンスを作成
    recorder = MicrobotRecorder(hex_file="program.hex")
    
    # MakeCode を起動
    await recorder.open_makecode()
    
    # 操作をチェーンして定義
    await recorder \
        .wait(2) \
        .click(100, 200) \
        .type("Hello") \
        .wait(1) \
        .record_gif("output.gif", fps=10)
    
    # クローズ
    await recorder.close()

# 実行
asyncio.run(record_tutorial())
```

## API リファレンス

### MicrobotRecorder

#### 初期化
```python
MicrobotRecorder(
    hex_file: str,
    browser_width: int = 1280,
    browser_height: int = 800,
    cursor_x: int = 640,
    cursor_y: int = 400,
)
```

**パラメータ:**
- `hex_file`: micro:bit HEX ファイルのパス
- `browser_width`: ブラウザ幅（デフォルト: 1280px）
- `browser_height`: ブラウザ高さ（デフォルト: 800px）
- `cursor_x`: GIF に描画するカーソルの X 座標（デフォルト: 640）
- `cursor_y`: GIF に描画するカーソルの Y 座標（デフォルト: 400）

#### 操作メソッド（チェーン可能）

すべてのメソッドは `MicrobotRecorder` を返すため、メソッドチェーンが可能です。

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `click(x, y)` | 座標 (x, y) をクリック | `MicrobotRecorder` |
| `type(text)` | テキストを入力 | `MicrobotRecorder` |
| `key(key_name)` | キーを入力（"Enter", "Escape" など） | `MicrobotRecorder` |
| `wait(seconds)` | 指定秒数待機 | `MicrobotRecorder` |
| `screenshot(label)` | スクリーンショットを取得 | `MicrobotRecorder` |

#### 初期化・終了メソッド

| メソッド | 説明 | 戻り値 |
|---------|------|--------|
| `await open_makecode()` | MakeCode エディタを起動し HEX ファイルをロード | `MicrobotRecorder` |
| `await record_gif(output_path, fps)` | イベントを実行し GIF を記録・保存 | `None` |
| `await close()` | ブラウザをクローズしリソースを解放 | `None` |

## 高度な使用方法

### カスタムカーソル位置

```python
# ブラウザの中央ではなく、左上のコーナーにカーソルを表示
recorder = MicrobotRecorder(
    hex_file="program.hex",
    cursor_x=100,
    cursor_y=50
)
```

### エラーハンドリング

```python
from microbit_makecode_recorder import MicrobotRecorder
from core.errors import HexFileNotFoundError, MakeCodeLoadError, ScreenshotError

try:
    recorder = MicrobotRecorder(hex_file="nonexistent.hex")
    await recorder.open_makecode()
except HexFileNotFoundError as e:
    print(f"HEX ファイルが見つかりません: {e}")
except MakeCodeLoadError as e:
    print(f"MakeCode の読み込みに失敗しました: {e}")
```

## 依存関係

- Playwright >= 1.40.0
- Pillow >= 10.0.0
- Python 3.9+

## トラブルシューティング

### Q: "Browser not initialized" エラーが出る

**A:** `open_makecode()` を呼び出してからクリック操作を実行してください。

```python
recorder = MicrobotRecorder(hex_file="program.hex")
await recorder.open_makecode()  # ← これを忘れずに
await recorder.click(100, 200).record_gif("output.gif")
```

### Q: HEX ファイルがロードされない

**A:** ファイルパスが正しいこと、ファイルが存在することを確認してください。

```python
from pathlib import Path
hex_path = Path("program.hex")
assert hex_path.exists(), f"File not found: {hex_path}"
```

### Q: スクリーンショットがぼやけている

**A:** `browser_width`, `browser_height` を調整してください。高解像度の場合は 1920x1440 などを指定してください。

## ライセンス

MIT
