"""CursorRenderer のユニットテスト。"""

from PIL import Image

from rendering.cursor_renderer import CursorRenderer


def _make_image(size: tuple[int, int] = (100, 100)) -> Image.Image:
    """テスト用の白背景画像を生成する。"""
    return Image.new("RGB", size, color=(255, 255, 255))


class TestDrawCursor:
    """draw_cursor メソッドのテスト。"""

    def test_draw_cursor_basic(self):
        """基本的なカーソル描画が画像上に行われることを確認する。"""
        renderer = CursorRenderer()
        image = _make_image()

        result = renderer.draw_cursor(image, 50, 50)

        assert isinstance(result, Image.Image)
        assert result.size == image.size

    def test_draw_cursor_near_top_left_edge(self):
        """画像の左上端付近 (5, 5) でもエラーなく描画できることを確認する。"""
        renderer = CursorRenderer()
        image = _make_image()

        result = renderer.draw_cursor(image, 5, 5)

        assert isinstance(result, Image.Image)
        assert result.size == image.size

    def test_draw_cursor_near_bottom_right_edge(self):
        """画像の右下端付近 (95, 95) でもエラーなく描画できることを確認する。"""
        renderer = CursorRenderer()
        image = _make_image()

        result = renderer.draw_cursor(image, 95, 95)

        assert isinstance(result, Image.Image)
        assert result.size == image.size

    def test_draw_cursor_custom_color(self):
        """カスタムカーソル色を指定した場合でも正しく描画できることを確認する。"""
        renderer = CursorRenderer(cursor_color=(0, 255, 0))
        image = _make_image()

        result = renderer.draw_cursor(image, 50, 50)

        assert isinstance(result, Image.Image)
        assert result.size == image.size


class TestDrawClickEffect:
    """draw_click_effect メソッドのテスト。"""

    def test_empty_image_list(self):
        """画像リストが空の場合、空リストが返されることを確認する。"""
        renderer = CursorRenderer()

        result = renderer.draw_click_effect([], 50, 50)

        assert result == []

    def test_single_image(self):
        """画像が 1 枚のみの場合でもクリックエフェクトが適用できることを確認する。"""
        renderer = CursorRenderer()
        images = [_make_image()]

        result = renderer.draw_click_effect(images, 50, 50)

        assert len(result) == 1
        for img in result:
            assert isinstance(img, Image.Image)
            assert img.size == images[0].size

    def test_multiple_images(self):
        """複数枚の画像に対してクリックエフェクトが適用できることを確認する。"""
        renderer = CursorRenderer()
        images = [_make_image() for _ in range(5)]

        result = renderer.draw_click_effect(images, 50, 50, duration_frames=5)

        assert len(result) == 5
        for img in result:
            assert isinstance(img, Image.Image)
            assert img.size == (100, 100)
