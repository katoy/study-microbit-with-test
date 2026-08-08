"""
micro:bit 用シンプルな方位磁石アプリ

方位磁石機能を提供し、北、南、東、西の方向を判定する
"""

from microbit import compass, display, button_a, Image


class Compass:
    """方位磁石を管理するクラス"""

    def __init__(self):
        """コンパスを初期化する"""
        self.heading = 0
        self.calibrated = False

    def calibrate(self):
        """コンパスをキャリブレーションする"""
        compass.calibrate()
        self.calibrated = True

    def get_heading(self):
        """
        現在の方位角を取得する
        
        Returns:
            int: 0-359 度（0 = 北）
        """
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
        """
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
        """
        direction = self.get_direction()
        heading = self.get_heading()
        display.scroll(f"{direction} {heading}")


def main():
    """メイン処理"""
    compass_app = Compass()
    
    # キャリブレーション指示
    display.show(Image.SQUARE)
    compass_app.calibrate()
    
    # ループ開始
    while True:
        compass_app.display_direction()
        
        # ボタンA を押してキャリブレーション
        if button_a.is_pressed():
            display.show(Image.SQUARE)
            compass_app.calibrate()


if __name__ == '__main__':
    main()
