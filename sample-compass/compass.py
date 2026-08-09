"""
micro:bit 用シンプルな方位磁石アプリ

方位磁石機能を提供し、北、南、東、西の方向を判定する
"""

from microbit import compass, display, button_a, button_b, Image

DIRECTION_IMAGES = {
    'N': Image.ARROW_N,
    'NE': Image.ARROW_NE,
    'E': Image.ARROW_E,
    'SE': Image.ARROW_SE,
    'S': Image.ARROW_S,
    'SW': Image.ARROW_SW,
    'W': Image.ARROW_W,
    'NW': Image.ARROW_NW,
}


class Compass:
    """方位磁石を管理するクラス"""

    def __init__(self):
        """コンパスを初期化する"""
        self.heading = 0

    def calibrate(self):
        """コンパスをキャリブレーションする"""
        compass.calibrate()

    def is_calibrated(self):
        """
        micro:bit のコンパスがキャリブレーション済みか返す

        Returns:
            bool: キャリブレーション済みなら True
        """
        return compass.is_calibrated()

    def get_heading(self):
        """
        現在の方位角を取得する
        
        Returns:
            int: 0-359 度（0 = 北）
        """
        try:
            val = compass.heading()
            # 公式 API の範囲外でも壊れないかを考える、
            # 防御的プログラミングの練習
            if val != val or val < 0 or val > 360:
                return self.heading
            self.heading = val % 360
        except (OSError, RuntimeError):
            # センサーエラー時は前回の有効値を返す
            return self.heading
        return self.heading

    def get_direction(self):
        """
        現在の方角を取得する
        
        Returns:
            str: 'N'（北）、'S'（南）、'E'（東）、'W'（西）、'NE'、'NW'、'SE'、'SW'
        """
        heading = self.get_heading()
        return self._heading_to_direction(heading)

    @staticmethod
    def _heading_to_direction(heading):
        """
        方位角を方向文字列に変換する
        
        Args:
            heading (int): 0-359 度
            
        Returns:
            str: 方向を示す文字列

        Raises:
            ValueError: 方位角が 0 度以上 360 度未満の有限値でない場合
        """
        if heading != heading or heading < 0 or heading >= 360:
            raise ValueError("方位角は 0-359 度である必要があります")

        # 8 方位を判定（各方位は 45 度幅）
        if heading < 22.5 or heading >= 337.5:
            return 'N'
        elif heading < 67.5:
            return 'NE'
        elif heading < 112.5:
            return 'E'
        elif heading < 157.5:
            return 'SE'
        elif heading < 202.5:
            return 'S'
        elif heading < 247.5:
            return 'SW'
        elif heading < 292.5:
            return 'W'
        else:  # heading < 337.5
            return 'NW'

    def display_direction(self):
        """
        ディスプレイに現在の方向を表示する
        キャリブレーションされていない場合は 'CAL' を表示して促す
        """
        if not self.is_calibrated():
            display.scroll("CAL")
            return
            
        direction = self.get_direction()
        heading = self.get_heading()
        display.scroll(f"{direction} {heading}")


def main():
    """MakeCode 版と同じボタン操作で方位を表示する"""
    compass_app = Compass()

    # 起動時に操作方法を表示する
    display.scroll("COMPASS")
    display.scroll("A: CAL")
    display.scroll("B: CHK")

    # ループ開始
    while True:
        # スクロール中の押下も記録する was_pressed() で取りこぼしを防ぐ
        if button_a.was_pressed():
            display.show(Image.SQUARE)
            compass_app.calibrate()
            display.scroll("OK")

        # ボタン B を押して現在の方角と角度を確認する
        if button_b.was_pressed():
            compass_app.display_direction()

        # MakeCode 版の forever と同様に LED へ方角を表示する
        if compass_app.is_calibrated():
            direction = compass_app.get_direction()
            display.show(DIRECTION_IMAGES[direction])
        else:
            display.scroll("CAL")


if __name__ == '__main__':
    main()
