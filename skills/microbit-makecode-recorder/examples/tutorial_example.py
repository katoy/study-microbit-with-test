"""microbit-makecode-recorder の使用例。"""

import asyncio
import sys
from pathlib import Path

# skills ディレクトリを sys.path に追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.recorder import MicrobotRecorder


async def example_simple_click():
    """シンプルなクリック操作の例。"""
    recorder = MicrobotRecorder(hex_file="examples/sample.hex")

    try:
        await recorder.open_makecode() \
            .wait(2) \
            .click(640, 400) \
            .wait(1) \
            .record_gif("output_simple.gif")
    finally:
        await recorder.close()


async def example_text_input():
    """テキスト入力の例。"""
    recorder = MicrobotRecorder(hex_file="examples/sample.hex")

    try:
        await recorder.open_makecode() \
            .wait(2) \
            .click(100, 100) \
            .type("Hello World") \
            .key("Enter") \
            .wait(1) \
            .record_gif("output_text.gif")
    finally:
        await recorder.close()


async def example_complex_sequence():
    """複雑な操作シーケンスの例。"""
    recorder = MicrobotRecorder(hex_file="examples/sample.hex")

    try:
        await recorder.open_makecode() \
            .wait(2) \
            .click(150, 150) \
            .type("Start") \
            .wait(1) \
            .click(200, 200) \
            .type("Process") \
            .wait(1) \
            .click(250, 250) \
            .type("End") \
            .wait(1) \
            .record_gif("output_complex.gif", fps=10)
    finally:
        await recorder.close()


if __name__ == "__main__":
    print("Example: simple click")
    # asyncio.run(example_simple_click())

    print("Example: text input")
    # asyncio.run(example_text_input())

    print("Example: complex sequence")
    # asyncio.run(example_complex_sequence())

    print("Examples defined but not executed (requires actual hex file)")
