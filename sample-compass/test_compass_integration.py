"""
Compass アプリケーション統合テスト

モック化した micro:bit API の境界から実機入力を与え、
Compass との連携を検証する
"""

import runpy
from unittest.mock import patch

import pytest
from compass import Compass, main
from microbit import button_a, button_b, compass as compass_sensor, display, Image


class TestCompassIntegration:
    """モック化した micro:bit API と Compass の統合テスト"""

    @pytest.fixture
    def compass(self):
        """コンパスのフィクスチャ"""
        return Compass()

    def test_complete_compass_workflow(self, compass):
        """初期化、校正、実機 API からの方位取得を一連で検証する"""
        assert compass.heading == 0
        assert compass.is_calibrated() is False

        compass.calibrate()
        assert compass.is_calibrated() is True

        compass_sensor.heading.return_value = 90
        assert compass.get_heading() == 90
        assert compass.get_direction() == 'E'

    def test_all_eight_directions(self, compass):
        """実機 API の 8 方位全てが正しく判定されることを検証する"""
        compass.calibrate()
        test_cases = [
            (0, 'N'),
            (45, 'NE'),
            (90, 'E'),
            (135, 'SE'),
            (180, 'S'),
            (225, 'SW'),
            (270, 'W'),
            (315, 'NW'),
        ]

        for heading, expected_direction in test_cases:
            compass_sensor.heading.return_value = heading
            assert compass.get_direction() == expected_direction, (
                f"heading={heading} は {expected_direction} を返すべき"
            )

    def test_boundary_value_transitions(self, compass):
        """実機 API の方位が境界値をまたぐ場合の遷移を検証する"""
        compass.calibrate()
        test_cases = [
            (22.4, 'N'),
            (22.5, 'NE'),
            (157.4, 'SE'),
            (157.5, 'S'),
        ]

        for heading, expected_direction in test_cases:
            compass_sensor.heading.return_value = heading
            assert compass.get_direction() == expected_direction

    def test_north_wrap_around(self, compass):
        """北で 359 度から 0 度へ戻る実機入力を検証する"""
        compass.calibrate()

        for heading in (359, 0, 337.5, 360):
            compass_sensor.heading.return_value = heading
            assert compass.get_direction() == 'N'

    def test_continuous_rotation_simulation(self, compass):
        """実機を時計回りに 1 周させる入力を検証する"""
        compass.calibrate()
        directions = []

        for heading in range(0, 360, 45):
            compass_sensor.heading.return_value = heading
            directions.append(compass.get_direction())

        assert directions == ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def test_rapid_direction_queries(self, compass):
        """同じ実機入力を連続取得しても結果が一貫することを検証する"""
        compass.calibrate()
        compass_sensor.heading.return_value = 45

        for _ in range(100):
            assert compass.get_direction() == 'NE'
            assert compass.get_heading() == 45

    def test_multiple_compass_instances_keep_independent_cached_values(self):
        """
        複数インスタンスが実機 API の前回値を別々に保持することを検証する
        """
        compass1 = Compass()
        compass2 = Compass()

        compass_sensor.heading.return_value = 0
        assert compass1.get_direction() == 'N'
        compass_sensor.heading.return_value = 90
        assert compass2.get_direction() == 'E'

        compass_sensor.heading.side_effect = OSError("Device error")
        assert compass1.get_direction() == 'N'
        assert compass2.get_direction() == 'E'

    def test_calibration_state_comes_from_hardware_api(self, compass):
        """校正状態を自前で複製せず実機 API から取得することを検証する"""
        assert compass.is_calibrated() is False

        compass.calibrate()
        assert compass.is_calibrated() is True

        compass_sensor.is_calibrated.return_value = False
        assert compass.is_calibrated() is False

    def test_repeated_updates_preserve_correctness(self, compass):
        """多数回の更新後も最後の方位が正しいことを決定的に検証する"""
        compass.calibrate()

        for index in range(10000):
            compass_sensor.heading.return_value = (index * 13) % 360
            compass.get_direction()

        assert compass.get_heading() == (9999 * 13) % 360

    def test_direction_consistency_across_queries(self, compass):
        """実機 API の同じ方位に対する結果の一貫性を検証する"""
        compass.calibrate()
        compass_sensor.heading.return_value = 123

        results = [compass.get_direction() for _ in range(1000)]
        assert all(direction == 'SE' for direction in results)

    def test_comprehensive_workflow_with_state_verification(self, compass):
        """校正後に実機を主要 4 方位へ向けるワークフローを検証する"""
        assert compass.is_calibrated() is False
        compass.calibrate()

        for heading, expected_direction in (
            (0, 'N'),
            (90, 'E'),
            (180, 'S'),
            (270, 'W'),
            (0, 'N'),
        ):
            compass_sensor.heading.return_value = heading
            assert compass.get_direction() == expected_direction

        assert compass.is_calibrated() is True

    def test_main_function_workflow(self):
        """main() の A 校正、B 確認、常時表示を実機 API 境界で検証する"""
        button_a.was_pressed.side_effect = [False, True, KeyboardInterrupt()]
        button_b.was_pressed.side_effect = [True, False]

        with pytest.raises(KeyboardInterrupt):
            main()

        compass_sensor.calibrate.assert_called_once_with()
        display.show.assert_any_call(Image.SQUARE)
        display.show.assert_any_call(Image.ARROW_N)
        display.scroll.assert_any_call("B: CHK")
        button_b.was_pressed.assert_called()

    def test_main_function_entry_point(self):
        """compass.py をスクリプトとして実行できることを検証する"""
        with patch(
            'microbit.button_a.was_pressed',
            side_effect=[False, KeyboardInterrupt()],
        ):
            with pytest.raises(KeyboardInterrupt):
                runpy.run_module('compass', run_name='__main__', alter_sys=True)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
