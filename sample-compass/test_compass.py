"""
compass.py のユニットテスト

方位磁石のロジック部分をテストする
"""

import pytest
from compass import Compass
from microbit import compass as compass_sensor


class TestCompass:
    """Compass クラスのテスト"""

    def test_compass_init(self):
        """初期化テスト"""
        compass = Compass()
        assert compass.heading == 0
        assert compass.is_calibrated() is False

    def test_calibrate(self):
        """キャリブレーション機能のテスト"""
        compass = Compass()
        assert compass.is_calibrated() is False
        compass.calibrate()
        assert compass.is_calibrated() is True

    def test_get_heading(self):
        """方位角取得のテスト"""
        compass = Compass()
        compass_sensor.heading.return_value = 45
        assert compass.get_heading() == 45

    def test_get_direction_north(self):
        """北方向の判定テスト"""
        # 北（0 度）
        assert Compass._heading_to_direction(0) == 'N'
        
        # 北（22 度以下）
        assert Compass._heading_to_direction(22) == 'N'
        
        # 北（337.5 度以上）
        assert Compass._heading_to_direction(350) == 'N'

    def test_get_direction_northeast(self):
        """北東方向の判定テスト"""
        assert Compass._heading_to_direction(45) == 'NE'

    def test_get_direction_east(self):
        """東方向の判定テスト"""
        assert Compass._heading_to_direction(90) == 'E'

    def test_get_direction_southeast(self):
        """南東方向の判定テスト"""
        assert Compass._heading_to_direction(135) == 'SE'

    def test_get_direction_south(self):
        """南方向の判定テスト"""
        assert Compass._heading_to_direction(180) == 'S'

    def test_get_direction_southwest(self):
        """南西方向の判定テスト"""
        assert Compass._heading_to_direction(225) == 'SW'

    def test_get_direction_west(self):
        """西方向の判定テスト"""
        assert Compass._heading_to_direction(270) == 'W'

    def test_get_direction_northwest(self):
        """北西方向の判定テスト"""
        assert Compass._heading_to_direction(315) == 'NW'

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

        # 有効範囲外と NaN は、全実装で無効入力として扱う
        for invalid_heading in (-5, 400, float('nan')):
            with pytest.raises(ValueError, match="0-359"):
                Compass._heading_to_direction(invalid_heading)

    def test_display_direction(self):
        """ディスプレイに方向を表示するテスト"""
        compass = Compass()
        compass_sensor.heading.return_value = 90
        compass_sensor.is_calibrated.return_value = True
        
        # display_direction() を呼び出し（display.scroll() がモックされている）
        compass.display_direction()
        
        # モックの display.scroll() が呼ばれたことを確認
        from microbit import display
        display.scroll.assert_called_once()
        # 呼び出し時の引数に "E 90" が含まれていることを確認
        call_args = display.scroll.call_args[0][0]
        assert "E" in call_args and "90" in call_args

    def test_display_direction_uncalibrated(self):
        """未キャリブレーション状態でのディスプレイ表示テスト"""
        compass = Compass()
        compass_sensor.is_calibrated.return_value = False
        
        from microbit import display
        display.scroll.reset_mock()
        
        compass.display_direction()
        
        # "CAL" がスクロールされることを確認
        display.scroll.assert_called_once_with("CAL")

    def test_get_heading_with_exception(self):
        """compass.heading() が例外を発生させる場合のテスト"""
        compass = Compass()
        compass.heading = 42

        compass_sensor.heading.side_effect = RuntimeError("Device error")

        # 例外が発生しても、前の値を返すべき
        assert compass.get_heading() == 42

    def test_get_heading_with_numeric_value(self):
        """compass.heading() が数値を返す場合のテスト"""
        compass = Compass()

        compass_sensor.heading.return_value = 123

        # 数値が返されると self.heading が更新される
        result = compass.get_heading()
        assert result == 123
        assert compass.heading == 123

    def test_get_heading_keeps_previous_value_for_impossible_values(self):
        """防御的にあり得ない値を受けた場合は前回値を保つ"""
        compass = Compass()
        compass.heading = 90

        for invalid_heading in (-1, 400):
            compass_sensor.heading.return_value = invalid_heading
            assert compass.get_heading() == 90


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
