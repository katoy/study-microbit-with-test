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
MicrobotRecorder(hex_file: str, browser_width: int = 1280, browser_height: int = 800)
```

#### 操作メソッド（チェーン可能）
- `click(x: int, y: int) -> MicrobotRecorder`: クリック操作
- `type(text: str) -> MicrobotRecorder`: テキスト入力
- `key(key_name: str) -> MicrobotRecorder`: キー入力
- `wait(seconds: float) -> MicrobotRecorder`: 待機
- `screenshot(label: str = "") -> MicrobotRecorder`: スクリーンショット

#### 最終化メソッド
- `async open_makecode() -> MicrobotRecorder`: MakeCode 起動
- `async record_gif(output_path: str, fps: int = 10) -> None`: GIF 記録
- `async close() -> None`: クローズ

## 依存関係

- Playwright >= 1.40.0
- Pillow >= 10.0.0
- Python 3.9+

## ライセンス

MIT
