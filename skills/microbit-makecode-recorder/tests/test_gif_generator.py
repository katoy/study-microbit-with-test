"""GifGenerator のユニットテスト。"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image

from rendering.gif_generator import GifGenerator
from core.errors import GifGenerationError


def test_create_basic_gif():
    """基本的な GIF の作成テスト。"""
    generator = GifGenerator()

    # サンプル画像を作成
    images = [Image.new("RGB", (100, 100), color="white") for _ in range(5)]

    # 一時出力ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        output_path = f.name

    try:
        generator.create(images, output_path, fps=10)

        # GIF が作成されたか確認
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

        # 有効な GIF か確認
        with Image.open(output_path) as gif:
            assert gif.format == "GIF"
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_create_gif_with_different_fps():
    """異なる fps で GIF を作成するテスト。"""
    generator = GifGenerator()
    images = [Image.new("RGB", (100, 100), color="white") for _ in range(5)]

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        output_path = f.name

    try:
        generator.create(images, output_path, fps=20)
        assert Path(output_path).exists()
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_create_gif_empty_list():
    """空の画像リストでエラーが発生するテスト。"""
    generator = GifGenerator()

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        output_path = f.name

    try:
        with pytest.raises(GifGenerationError):
            generator.create([], output_path)
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_create_gif_invalid_output_path():
    """無効な出力ディレクトリでエラーが発生するテスト。"""
    generator = GifGenerator()
    images = [Image.new("RGB", (100, 100), color="white") for _ in range(5)]

    # 存在しないディレクトリ
    output_path = "/nonexistent/directory/output.gif"

    with pytest.raises(GifGenerationError):
        generator.create(images, output_path)
