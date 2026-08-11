"""MakeCodeBrowser のユニットテスト。"""

import pytest
from pathlib import Path

from core.makecode_browser import MakeCodeBrowser
from core.errors import HexFileNotFoundError


@pytest.mark.asyncio
async def test_makecode_browser_init():
    """MakeCodeBrowser の初期化テスト。"""
    browser = MakeCodeBrowser(width=1280, height=800)
    assert browser.width == 1280
    assert browser.height == 800
    await browser.close()


@pytest.mark.asyncio
async def test_open_nonexistent_hex_file():
    """存在しない hex ファイルでエラーが発生するテスト。"""
    browser = MakeCodeBrowser()
    with pytest.raises(HexFileNotFoundError):
        await browser.open("/nonexistent/file.hex")
    await browser.close()


def test_makecode_url_constant():
    """MakeCode URL 定数のテスト。"""
    assert MakeCodeBrowser.MAKECODE_URL == "https://makecode.microbit.org/"


def test_retry_constants():
    """リトライ定数のテスト。"""
    assert MakeCodeBrowser.MAX_LOAD_RETRIES == 3
    assert MakeCodeBrowser.MAX_SCREENSHOT_RETRIES == 2
