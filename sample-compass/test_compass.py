"""
compass.py のユニットテスト

方位磁石のロジック部分をテストする
"""

import pytest
from compass import Compass


class TestCompass:
    """Compass クラスのテスト"""

    def test_compass_init(self):
        """初期化テスト"""
        compass = Compass()
        assert compass.heading == 0
        assert compass.calibrated is False

    def test_calibrate(self):
        """キャリブレーション機能のテスト"""
        compass = Compass()
        assert compass.calibrated is False
        compass.calibrate()
        assert compass.calibrated is True

    def test_get_heading(self):
        """方位角取得のテスト"""
        compass = Compass()
        compass.heading = 45
        assert compass.get_heading() == 45

    def test_get_direction_north(self):
        """北方向の判定テスト"""
        compass = Compass()
        
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
        compass = Compass()
        compass.heading = 45
        assert compass.get_direction() == 'NE'

    def test_get_direction_east(self):
        """東方向の判定テスト"""
        compass = Compass()
        compass.heading = 90
        assert compass.get_direction() == 'E'

    def test_get_direction_southeast(self):
        """南東方向の判定テスト"""
        compass = Compass()
        compass.heading = 135
        assert compass.get_direction() == 'SE'

    def test_get_direction_south(self):
        """南方向の判定テスト"""
        compass = Compass()
        compass.heading = 180
        assert compass.get_direction() == 'S'

    def test_get_direction_southwest(self):
        """南西方向の判定テスト"""
        compass = Compass()
        compass.heading = 225
        assert compass.get_direction() == 'SW'

    def test_get_direction_west(self):
        """西方向の判定テスト"""
        compass = Compass()
        compass.heading = 270
        assert compass.get_direction() == 'W'

    def test_get_direction_northwest(self):
        """北西方向の判定テスト"""
        compass = Compass()
        compass.heading = 315
        assert compass.get_direction() == 'NW'

    def test_heading_to_direction_boundaries(self):
        """境界値テスト"""
        # 北東と東の境界（67.5 度）
        assert Compass._heading_to_direction(67.4) == 'NE'
        assert Compass._heading_to_direction(67.5) == 'E'
        
        # 南と南西の境界（202.5 度）
        assert Compass._heading_to_direction(202.4) == 'S'
        assert Compass._heading_to_direction(202.5) == 'SW'

    def test_heading_to_direction_edge_cases(self):
        """エッジケーステスト"""
        # 0 度（北）
        assert Compass._heading_to_direction(0) == 'N'
        
        # 359 度（北に近い）
        assert Compass._heading_to_direction(359) == 'N'
        
        # 360 度相当（0 度に相当）
        assert Compass._heading_to_direction(360 % 360) == 'N'

    def test_display_direction(self):
        """ディスプレイに方向を表示するテスト"""
        compass = Compass()
        compass.heading = 90
        
        # display_direction() を呼び出し（display.scroll() がモックされている）
        compass.display_direction()
        
        # モックの display.scroll() が呼ばれたことを確認
        from microbit import display
        display.scroll.assert_called_once()
        # 呼び出し時の引数に "E 90" が含まれていることを確認
        call_args = display.scroll.call_args[0][0]
        assert "E" in call_args and "90" in call_args

    def test_get_heading_with_exception(self):
        """compass.heading() が例外を発生させる場合のテスト"""
        compass = Compass()
        compass.heading = 42
        
        # compass.heading() が例外を発生させるようにモック
        from microbit import compass as compass_module
        original_heading = compass_module.heading
        
        def mock_heading_with_exception():
            raise RuntimeError("Device error")
        
        compass_module.heading = mock_heading_with_exception
        
        try:
            # 例外が発生しても、前の値を返すべき
            result = compass.get_heading()
            assert result == 42
        finally:
            # モックを復元
            compass_module.heading = original_heading

    def test_get_heading_with_numeric_value(self):
        """compass.heading() が数値を返す場合のテスト"""
        compass = Compass()
        
        from microbit import compass as compass_module
        original_heading = compass_module.heading
        
        def mock_heading_with_number():
            return 123
        
        compass_module.heading = mock_heading_with_number
        
        try:
            # 数値が返されると self.heading が更新される
            result = compass.get_heading()
            assert result == 123
            assert compass.heading == 123
        finally:
            # モックを復元
            compass_module.heading = original_heading


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
