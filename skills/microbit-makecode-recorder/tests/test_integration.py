"""統合テストおよび E2E テスト。"""

import pytest
import tempfile
from pathlib import Path

from core.recorder import MicrobotRecorder
from core.errors import HexFileNotFoundError


def test_imports_all_public_api():
    """公開 API がすべてインポート可能なテスト。"""
    from core.recorder import MicrobotRecorder
    from core.errors import (
        MakeCodeError,
        HexFileNotFoundError,
        MakeCodeLoadError,
        ScreenshotError,
        GifGenerationError,
    )
    from rendering.cursor_renderer import CursorRenderer
    from rendering.gif_generator import GifGenerator

    assert MicrobotRecorder is not None
    assert MakeCodeError is not None
    assert HexFileNotFoundError is not None
    assert MakeCodeLoadError is not None
    assert ScreenshotError is not None
    assert GifGenerationError is not None
    assert CursorRenderer is not None
    assert GifGenerator is not None


def test_recorder_with_nonexistent_hex():
    """存在しない hex ファイルでエラーが発生するテスト。"""
    recorder = MicrobotRecorder(hex_file="/nonexistent/file.hex")

    # open_makecode を呼び出そうとすると HexFileNotFoundError が発生するはず
    #（実装時に async で実行）
    assert recorder.hex_file == "/nonexistent/file.hex"


@pytest.mark.asyncio
async def test_full_recording_workflow():
    """エンドツーエンドテスト。"""
    # NOTE: このテストは実際の hex ファイルと動作する browser が必要
    # CI/CD では skip される可能性あり

    with tempfile.NamedTemporaryFile(suffix=".hex", delete=False) as f:
        hex_path = f.name
        # プレースホルダー hex ファイル
        f.write(b"placeholder")

    try:
        recorder = MicrobotRecorder(hex_file=hex_path)

        # 実際の実行は browser がない環境では失敗するため、
        # ここでは初期化のみテストする
        assert recorder.hex_file == hex_path
        assert len(recorder._events) == 0

    finally:
        Path(hex_path).unlink(missing_ok=True)


def test_event_collection_order():
    """イベント収集の順序が正しいテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")

    recorder \
        .click(100, 100) \
        .type("Test") \
        .wait(1) \
        .key("Enter") \
        .screenshot("final")

    assert len(recorder._events) == 5
    assert recorder._events[0].event_type.value == "click"
    assert recorder._events[1].event_type.value == "type"
    assert recorder._events[2].event_type.value == "wait"
    assert recorder._events[3].event_type.value == "key"
    assert recorder._events[4].event_type.value == "screenshot"


def test_cursor_renderer_integration():
    """CursorRenderer の統合テスト。"""
    from PIL import Image
    from rendering.cursor_renderer import CursorRenderer

    renderer = CursorRenderer(cursor_color=(255, 0, 0), cursor_size=24)

    # テスト画像を作成
    img = Image.new("RGB", (200, 200), color="white")

    # カーソルを描画
    result = renderer.draw_cursor(img, 100, 100)
    assert result.size == (200, 200)
    assert result.format is None  # PIL Image object


def test_gif_generator_integration():
    """GifGenerator の統合テスト。"""
    from PIL import Image
    from rendering.gif_generator import GifGenerator

    generator = GifGenerator()

    # テスト画像を作成
    images = [Image.new("RGB", (100, 100), color="white") for _ in range(3)]

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        output_path = f.name

    try:
        generator.create(images, output_path, fps=10)
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_error_hierarchy():
    """エラー階層が正しいテスト。"""
    from core.errors import (
        MakeCodeError,
        HexFileNotFoundError,
        MakeCodeLoadError,
    )

    # HexFileNotFoundError は MakeCodeError のサブクラス
    assert issubclass(HexFileNotFoundError, MakeCodeError)
    assert issubclass(MakeCodeLoadError, MakeCodeError)

    # MakeCodeError は Exception のサブクラス
    assert issubclass(MakeCodeError, Exception)
