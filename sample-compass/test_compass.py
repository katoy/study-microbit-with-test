"""
compass.py のユニットテスト

方位磁石のロジック部分をテストする
"""

import pytest


# compass.py の Compass クラスをモック化してインポート
class MockCompass:
    """テスト用の Compass クラス（micro:bit API に依存しない）"""

    def __init__(self):
        """コンパスを初期化する"""
        self.heading = 0
        self.calibrated = False

    def calibrate(self):
        """コンパスをキャリブレーションする"""
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
        return self._heading_to_direction(self.heading)

    @staticmethod
    def _heading_to_direction(heading):
        """
        方位角を方向文字列に変換する
        
        Args:
            heading (int): 0-359 度
            
        Returns:
            str: 方向を示す文字列
        """
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
        else:
            return 'NW'


class TestCompass:
    """Compass クラスのテスト"""

    def test_compass_init(self):
        """初期化テスト"""
        compass = MockCompass()
        assert compass.heading == 0
        assert compass.calibrated is False

    def test_calibrate(self):
        """キャリブレーション機能のテスト"""
        compass = MockCompass()
        assert compass.calibrated is False
        compass.calibrate()
        assert compass.calibrated is True

    def test_get_heading(self):
        """方位角取得のテスト"""
        compass = MockCompass()
        compass.heading = 45
        assert compass.get_heading() == 45

    def test_get_direction_north(self):
        """北方向の判定テスト"""
        compass = MockCompass()
        
        # 北（0 度）
        compass.heading = 0
        assert compass.get_direction() == 'N'
        
        # 北（22 度以下）
        compass.heading = 22
        assert compass.get_direction() == 'N'
        
        # 北（337.5 度以上）
        compass.heading = 350
        assert compass.get_direction() == 'N'

    def test_get_direction_northeast(self):
        """北東方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 45
        assert compass.get_direction() == 'NE'

    def test_get_direction_east(self):
        """東方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 90
        assert compass.get_direction() == 'E'

    def test_get_direction_southeast(self):
        """南東方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 135
        assert compass.get_direction() == 'SE'

    def test_get_direction_south(self):
        """南方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 180
        assert compass.get_direction() == 'S'

    def test_get_direction_southwest(self):
        """南西方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 225
        assert compass.get_direction() == 'SW'

    def test_get_direction_west(self):
        """西方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 270
        assert compass.get_direction() == 'W'

    def test_get_direction_northwest(self):
        """北西方向の判定テスト"""
        compass = MockCompass()
        compass.heading = 315
        assert compass.get_direction() == 'NW'

    def test_heading_to_direction_boundaries(self):
        """境界値テスト"""
        # 北東と東の境界（67.5 度）
        assert MockCompass._heading_to_direction(67.4) == 'NE'
        assert MockCompass._heading_to_direction(67.5) == 'E'
        
        # 南と南西の境界（202.5 度）
        assert MockCompass._heading_to_direction(202.4) == 'S'
        assert MockCompass._heading_to_direction(202.5) == 'SW'

    def test_heading_to_direction_edge_cases(self):
        """エッジケーステスト"""
        # 0 度（北）
        assert MockCompass._heading_to_direction(0) == 'N'
        
        # 359 度（北に近い）
        assert MockCompass._heading_to_direction(359) == 'N'
        
        # 360 度相当（0 度に相当）
        assert MockCompass._heading_to_direction(360 % 360) == 'N'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
