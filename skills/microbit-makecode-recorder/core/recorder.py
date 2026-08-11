"""メソッドチェーン形式の MakeCode 操作 API。"""

import asyncio
from enum import Enum
from dataclasses import dataclass
from PIL import Image

from core.makecode_browser import MakeCodeBrowser
from rendering.cursor_renderer import CursorRenderer
from rendering.gif_generator import GifGenerator


class EventType(Enum):
    """操作イベントの種類。"""

    CLICK = "click"
    TYPE = "type"
    KEY = "key"
    WAIT = "wait"
    SCREENSHOT = "screenshot"


@dataclass
class Event:
    """操作イベント。"""

    event_type: EventType
    params: dict


class MicrobotRecorder:
    """メソッドチェーン形式の MakeCode 操作 API。"""

    def __init__(self, hex_file: str, browser_width: int = 1280, browser_height: int = 800):
        """
        初期化

        Args:
            hex_file: micro:bit hex ファイルのパス
            browser_width: ブラウザ幅
            browser_height: ブラウザ高さ
        """
        self.hex_file = hex_file
        self.browser_width = browser_width
        self.browser_height = browser_height
        self._events: list[Event] = []
        self._browser: MakeCodeBrowser | None = None
        self._screenshots: list[Image.Image] = []

    def click(self, x: int, y: int) -> "MicrobotRecorder":
        """クリック操作（チェーン可能）。"""
        self._events.append(Event(EventType.CLICK, {"x": x, "y": y}))
        return self

    def type(self, text: str) -> "MicrobotRecorder":
        """テキスト入力（チェーン可能）。"""
        self._events.append(Event(EventType.TYPE, {"text": text}))
        return self

    def key(self, key_name: str) -> "MicrobotRecorder":
        """キー入力（チェーン可能）。"""
        self._events.append(Event(EventType.KEY, {"key": key_name}))
        return self

    def wait(self, seconds: float) -> "MicrobotRecorder":
        """待機（チェーン可能）。"""
        self._events.append(Event(EventType.WAIT, {"seconds": seconds}))
        return self

    def screenshot(self, label: str = "") -> "MicrobotRecorder":
        """スクリーンショット（チェーン可能）。"""
        self._events.append(Event(EventType.SCREENSHOT, {"label": label}))
        return self

    async def open_makecode(self) -> "MicrobotRecorder":
        """MakeCode を起動し hex ファイルをロード。"""
        self._browser = MakeCodeBrowser(width=self.browser_width, height=self.browser_height)
        await self._browser.open(self.hex_file)

        # 初期スクリーンショットを取得
        screenshot = await self._browser.screenshot()
        self._screenshots.append(screenshot)

        return self

    async def record_gif(self, output_path: str, fps: int = 10) -> None:
        """
        GIF アニメーションを記録・保存

        Args:
            output_path: 出力ファイルパス
            fps: フレームレート
        """
        if not self._browser:
            raise RuntimeError("Browser not initialized. Call open_makecode() first.")

        # イベントを実行
        click_positions = []
        for event in self._events:
            if event.event_type == EventType.CLICK:
                x, y = event.params["x"], event.params["y"]
                click_positions.append((len(self._screenshots), x, y))
                screenshot = await self._browser.click(x, y)
                self._screenshots.append(screenshot)

            elif event.event_type == EventType.TYPE:
                screenshot = await self._browser.type(event.params["text"])
                self._screenshots.append(screenshot)

            elif event.event_type == EventType.KEY:
                screenshot = await self._browser.key(event.params["key"])
                self._screenshots.append(screenshot)

            elif event.event_type == EventType.WAIT:
                screenshot = await self._browser.wait(event.params["seconds"])
                self._screenshots.append(screenshot)

            elif event.event_type == EventType.SCREENSHOT:
                screenshot = await self._browser.screenshot()
                self._screenshots.append(screenshot)

        # カーソルを描画
        cursor_renderer = CursorRenderer()
        enhanced_screenshots: list[Image.Image] = []

        for i, screenshot in enumerate(self._screenshots):
            # デフォルト位置にカーソルを描画
            with_cursor = cursor_renderer.draw_cursor(screenshot, 640, 400)
            enhanced_screenshots.append(with_cursor)

        # クリック効果を追加（最後のクリック位置に対して）
        if click_positions:
            last_click_index, last_x, last_y = click_positions[-1]
            final_screenshots = cursor_renderer.draw_click_effect(
                enhanced_screenshots, x=last_x, y=last_y, duration_frames=5
            )
        else:
            final_screenshots = enhanced_screenshots

        # GIF を生成
        gif_generator = GifGenerator()
        gif_generator.create(final_screenshots, output_path, fps=fps)

    async def close(self) -> None:
        """ブラウザとリソースをクローズ。"""
        if self._browser:
            await self._browser.close()
