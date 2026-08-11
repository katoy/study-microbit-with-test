"""カーソルの描画とクリックエフェクトを扱うモジュール。"""

from PIL import Image, ImageDraw

# カーソル円の輪郭線の太さ（px）
_CURSOR_OUTLINE_WIDTH = 2

# クリックエフェクトの円の輪郭線の太さ（px）
_CLICK_EFFECT_OUTLINE_WIDTH = 2

# クリックエフェクトの開始・終了半径（px）
_CLICK_EFFECT_START_RADIUS = 8
_CLICK_EFFECT_END_RADIUS = 32


class CursorRenderer:
    """画像上にカーソルとクリックエフェクトを描画するクラス。"""

    def __init__(
        self,
        cursor_color: tuple[int, int, int] = (255, 0, 0),
        cursor_size: int = 24,
    ):
        """カーソルの色とサイズを設定する。

        Args:
            cursor_color: カーソルの色 (R, G, B)。デフォルトは赤。
            cursor_size: カーソルの直径（px）。デフォルトは 24px。
        """
        self.cursor_color = cursor_color
        self.cursor_size = cursor_size

    def draw_cursor(self, image: Image.Image, x: int, y: int) -> Image.Image:
        """指定座標 (x, y) を中心にカーソル円を画像に描画する。

        Args:
            image: 描画対象の画像。
            x: カーソル中心の x 座標。
            y: カーソル中心の y 座標。

        Returns:
            カーソルが描画された画像。
        """
        result = image.copy()
        draw = ImageDraw.Draw(result)
        radius = self.cursor_size / 2
        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.ellipse(bbox, outline=self.cursor_color, width=_CURSOR_OUTLINE_WIDTH)
        return result

    def draw_click_effect(
        self,
        images: list[Image.Image],
        x: int,
        y: int,
        duration_frames: int = 5,
    ) -> list[Image.Image]:
        """画像シーケンスの末尾フレームにクリックエフェクト（拡大円）を追加する。

        Args:
            images: 対象の画像リスト。
            x: クリック位置の x 座標。
            y: クリック位置の y 座標。
            duration_frames: エフェクトを適用するフレーム数。デフォルトは 5。

        Returns:
            クリックエフェクトが適用された画像リスト。
        """
        if not images:
            return []

        result = list(images)
        # エフェクトを適用するフレーム数は画像枚数を超えない
        effect_frames = min(duration_frames, len(result))

        for i in range(effect_frames):
            # 末尾から effect_frames 枚を対象に、進行度 progress (0 始まり) を計算する
            frame_index = len(result) - effect_frames + i
            result[frame_index] = self._add_click_effect_frame(
                result[frame_index], x, y, progress=i, total_frames=effect_frames
            )

        return result

    def _add_click_effect_frame(
        self,
        image: Image.Image,
        x: int,
        y: int,
        progress: int,
        total_frames: int,
    ) -> Image.Image:
        """クリックエフェクトの 1 フレーム分（拡大円）を画像に描画する。

        Args:
            image: 描画対象の画像。
            x: クリック位置の x 座標。
            y: クリック位置の y 座標。
            progress: 現在のフレーム番号（0 始まり）。
            total_frames: エフェクトの総フレーム数。

        Returns:
            クリックエフェクトの円が描画された画像。
        """
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # progress に応じて半径を start から end まで線形に拡大する
        if total_frames > 1:
            ratio = progress / (total_frames - 1)
        else:
            ratio = 1.0
        radius = (
            _CLICK_EFFECT_START_RADIUS
            + (_CLICK_EFFECT_END_RADIUS - _CLICK_EFFECT_START_RADIUS) * ratio
        )

        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.ellipse(
            bbox, outline=self.cursor_color, width=_CLICK_EFFECT_OUTLINE_WIDTH
        )
        return result
