"""MakeCode エディタを Playwright で自動操作するモジュール。"""

import asyncio
from pathlib import Path
from PIL import Image

try:
    from playwright.async_api import async_playwright, Browser, Page
except ImportError:
    # Playwright がインストールされていない場合のスタブ
    Browser = None
    Page = None

from core.errors import HexFileNotFoundError, MakeCodeLoadError, ScreenshotError


class MakeCodeBrowser:
    """Playwright を使用して MakeCode エディタを操作する。"""

    MAKECODE_URL = "https://makecode.microbit.org/"
    MAX_LOAD_RETRIES = 3
    MAX_SCREENSHOT_RETRIES = 2

    def __init__(self, width: int = 1280, height: int = 800):
        """
        初期化

        Args:
            width: ブラウザ幅
            height: ブラウザ高さ
        """
        self.width = width
        self.height = height
        self.browser: "Browser | None" = None
        self.page: "Page | None" = None

    async def open(self, hex_file: str) -> None:
        """
        MakeCode を起動し hex ファイルをロード

        Args:
            hex_file: hex ファイルのパス

        Raises:
            HexFileNotFoundError: hex ファイルが見つからない場合
            MakeCodeLoadError: ページ読み込みに失敗した場合
        """
        # hex ファイルをチェック
        hex_path = Path(hex_file)
        if not hex_path.exists():
            raise HexFileNotFoundError(hex_file)

        # Playwright を初期化
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page(
                viewport={"width": self.width, "height": self.height}
            )
        except Exception as e:
            raise MakeCodeLoadError(f"Failed to launch browser: {str(e)}")

        # MakeCode を開く（リトライ付き）
        for attempt in range(self.MAX_LOAD_RETRIES):
            try:
                await self.page.goto(self.MAKECODE_URL, wait_until="networkidle")
                break
            except Exception as e:
                if attempt == self.MAX_LOAD_RETRIES - 1:
                    raise MakeCodeLoadError(
                        f"Failed to load MakeCode: {str(e)}", retries=attempt
                    )
                await asyncio.sleep(1)

        # hex ファイルをロード
        await self._load_hex_file(hex_path)

    async def _load_hex_file(self, hex_path: Path) -> None:
        """hex ファイルをロードする（内部メソッド）。"""
        # TODO: Implement hex file loading via drag & drop or upload
        pass

    async def click(self, x: int, y: int) -> Image.Image:
        """
        クリック操作を実行

        Args:
            x: X 座標
            y: Y 座標

        Returns:
            クリック後のスクリーンショット
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Call open() first.")

        await self.page.click(f"[data-x='{x}'][data-y='{y}']", force=True)
        return await self.screenshot()

    async def type(self, text: str) -> Image.Image:
        """
        テキスト入力

        Args:
            text: 入力テキスト

        Returns:
            入力後のスクリーンショット
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Call open() first.")

        await self.page.keyboard.type(text)
        return await self.screenshot()

    async def key(self, key_name: str) -> Image.Image:
        """
        キー入力

        Args:
            key_name: キー名（"Enter", "Escape" など）

        Returns:
            入力後のスクリーンショット
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Call open() first.")

        await self.page.keyboard.press(key_name)
        return await self.screenshot()

    async def wait(self, seconds: float) -> Image.Image:
        """
        待機

        Args:
            seconds: 待機秒数

        Returns:
            待機後のスクリーンショット
        """
        await asyncio.sleep(seconds)
        return await self.screenshot()

    async def screenshot(self) -> Image.Image:
        """
        スクリーンショットを取得

        Returns:
            スクリーンショット画像

        Raises:
            ScreenshotError: スクリーンショット取得に失敗した場合
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Call open() first.")

        for attempt in range(self.MAX_SCREENSHOT_RETRIES):
            try:
                screenshot_bytes = await self.page.screenshot()
                return Image.frombytes(
                    "RGB", (self.width, self.height), screenshot_bytes
                )
            except Exception as e:
                if attempt == self.MAX_SCREENSHOT_RETRIES - 1:
                    raise ScreenshotError(
                        f"Failed to capture screenshot: {str(e)}", retries=attempt
                    )
                await asyncio.sleep(0.5)

    async def close(self) -> None:
        """ブラウザをクローズ。"""
        if self.browser:
            await self.browser.close()
