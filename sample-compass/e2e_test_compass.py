"""
Compass アプリケーション E2E テスト

実際のユースケースに基づいた統合テストを実施する
"""

import pytest
from compass import Compass


class TestCompassE2E:
    """E2E テスト：Compass アプリケーション統合テスト"""

    @pytest.fixture
    def compass(self):
        """コンパスのフィクスチャ"""
        return Compass()

    def test_complete_compass_workflow(self, compass):
        """
        シナリオ: 方位磁石の完全なワークフロー
        1. 初期化
        2. キャリブレーション
        3. 方位角を設定
        4. 方角を確認
        """
        # 初期状態の確認
        assert compass.heading == 0
        assert compass.calibrated is False
        assert compass.get_direction() == 'N'

        # キャリブレーション
        compass.calibrate()
        assert compass.calibrated is True

        # 方位角を更新して方角を確認
        compass.heading = 90
        assert compass.get_heading() == 90
        assert compass.get_direction() == 'E'

    def test_all_eight_directions(self, compass):
        """
        シナリオ: 8 方位全てが正しく判定されること
        """
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
            compass.heading = heading
            assert compass.get_direction() == expected_direction, \
                f"heading={heading} は {expected_direction} を返すべき"

    def test_boundary_value_transitions(self, compass):
        """
        シナリオ: 方位の境界値での正確な遷移
        """
        compass.calibrate()

        # 北から北東への遷移（22.5°）
        compass.heading = 22.4
        assert compass.get_direction() == 'N'

        compass.heading = 22.5
        assert compass.get_direction() == 'NE'

        # 南東から南への遷移（157.5°）
        compass.heading = 157.4
        assert compass.get_direction() == 'SE'

        compass.heading = 157.5
        assert compass.get_direction() == 'S'

    def test_north_wrap_around(self, compass):
        """
        シナリオ: 北での角度ラップアラウンド（359°から0°への遷移）
        """
        compass.calibrate()

        # 359°も北
        compass.heading = 359
        assert compass.get_direction() == 'N'

        # 0°も北
        compass.heading = 0
        assert compass.get_direction() == 'N'

        # 337.5°以上は北
        compass.heading = 337.5
        assert compass.get_direction() == 'N'

    def test_continuous_rotation_simulation(self, compass):
        """
        シナリオ: 360°連続回転シミュレーション
        デバイスが時計回りに1周する場合
        """
        compass.calibrate()

        directions = []
        for heading in range(0, 360, 45):
            compass.heading = heading
            directions.append(compass.get_direction())

        expected = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        assert directions == expected

    def test_rapid_direction_queries(self, compass):
        """
        シナリオ: 同じ方位角での連続クエリ
        状態が一貫していることを確認
        """
        compass.calibrate()
        compass.heading = 45

        # 100 回クエリしても結果は一貫している
        for _ in range(100):
            assert compass.get_direction() == 'NE'
            assert compass.get_heading() == 45

    def test_multiple_compass_instances(self):
        """
        シナリオ: 複数のコンパスインスタンスが独立して動作
        """
        compass1 = Compass()
        compass2 = Compass()

        compass1.calibrate()
        compass1.heading = 0

        compass2.calibrate()
        compass2.heading = 90

        assert compass1.get_direction() == 'N'
        assert compass2.get_direction() == 'E'

        # インスタンスは独立している
        compass1.heading = 180
        assert compass1.get_direction() == 'S'
        assert compass2.get_direction() == 'E'

    def test_calibration_state_persistence(self, compass):
        """
        シナリオ: キャリブレーション状態が保持される
        複数の操作後もキャリブレーション状態は保持される
        """
        compass.calibrate()
        assert compass.calibrated is True

        # 複数の操作を実行
        compass.heading = 45
        assert compass.calibrated is True

        compass.heading = 90
        assert compass.calibrated is True

        compass.get_direction()
        assert compass.calibrated is True

    def test_performance_stress_test(self, compass):
        """
        シナリオ: 高負荷条件下でのパフォーマンス
        10000 回の連続更新でも正確に動作する
        """
        import time

        compass.calibrate()

        start = time.time()
        for i in range(10000):
            heading = (i * 13) % 360
            compass.heading = heading
            compass.get_direction()
        elapsed = time.time() - start

        # 1 秒以内に完了するべき
        assert elapsed < 1.0

    def test_direction_consistency_across_queries(self, compass):
        """
        シナリオ: 複数回のクエリで方角の一貫性を保証
        """
        compass.calibrate()
        compass.heading = 123

        # 1000 回クエリして全て同じ結果
        results = [compass.get_direction() for _ in range(1000)]
        assert all(direction == 'SE' for direction in results)

    def test_comprehensive_workflow_with_state_verification(self, compass):
        """
        シナリオ: 包括的なワークフロー with 状態検証
        通常のユースケースを再現する
        """
        # 初期状態を確認
        assert compass.calibrated is False
        state_heading = compass.get_heading()
        state_direction = compass.get_direction()
        assert state_heading == 0
        assert state_direction == 'N'

        # キャリブレーション
        compass.calibrate()

        # 北方向確認
        compass.heading = 0
        assert compass.get_direction() == 'N'

        # 東方向へ移動
        compass.heading = 90
        assert compass.get_direction() == 'E'

        # 南方向へ移動
        compass.heading = 180
        assert compass.get_direction() == 'S'

        # 西方向へ移動
        compass.heading = 270
        assert compass.get_direction() == 'W'

        # 北に戻す
        compass.heading = 0
        assert compass.get_direction() == 'N'
        assert compass.calibrated is True

    def test_complete_compass_workflow(self, compass):
        """
        シナリオ: 方位磁石の完全なワークフロー
        1. 初期化
        2. キャリブレーション
        3. 方位角を設定
        4. 方角を確認
        """
        # 初期状態の確認
        assert compass.heading == 0
        assert compass.calibrated is False
        assert compass.get_direction() == 'N'

        # キャリブレーション
        compass.calibrate()
        assert compass.calibrated is True

        # 方位角を更新して方角を確認
        compass.heading = 90
        assert compass.get_heading() == 90
        assert compass.get_direction() == 'E'

    def test_all_eight_directions(self, compass):
        """
        シナリオ: 8 方位全てが正しく判定されること
        """
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
            compass.heading = heading
            assert compass.get_direction() == expected_direction, \
                f"heading={heading} は {expected_direction} を返すべき"

    def test_boundary_value_transitions(self, compass):
        """
        シナリオ: 方位の境界値での正確な遷移
        """
        compass.calibrate()

        # 北から北東への遷移（22.5°）
        compass.heading = 22.4
        assert compass.get_direction() == 'N'

        compass.heading = 22.5
        assert compass.get_direction() == 'NE'

        # 南東から南への遷移（157.5°）
        compass.heading = 157.4
        assert compass.get_direction() == 'SE'

        compass.heading = 157.5
        assert compass.get_direction() == 'S'

    def test_north_wrap_around(self, compass):
        """
        シナリオ: 北での角度ラップアラウンド（359°から0°への遷移）
        """
        compass.calibrate()

        # 359°も北
        compass.heading = 359
        assert compass.get_direction() == 'N'

        # 0°も北
        compass.heading = 0
        assert compass.get_direction() == 'N'

        # 337.5°以上は北
        compass.heading = 337.5
        assert compass.get_direction() == 'N'

    def test_continuous_rotation_simulation(self, compass):
        """
        シナリオ: 360°連続回転シミュレーション
        デバイスが時計回りに1周する場合
        """
        compass.calibrate()

        directions = []
        for heading in range(0, 360, 45):
            compass.heading = heading
            directions.append(compass.get_direction())

        expected = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        assert directions == expected

    def test_rapid_direction_queries(self, compass):
        """
        シナリオ: 同じ方位角での連続クエリ
        状態が一貫していることを確認
        """
        compass.calibrate()
        compass.heading = 45

        # 100 回クエリしても結果は一貫している
        for _ in range(100):
            assert compass.get_direction() == 'NE'
            assert compass.get_heading() == 45

    def test_multiple_compass_instances(self):
        """
        シナリオ: 複数のコンパスインスタンスが独立して動作
        """
        compass1 = Compass()
        compass2 = Compass()

        compass1.calibrate()
        compass1.heading = 0

        compass2.calibrate()
        compass2.heading = 90

        assert compass1.get_direction() == 'N'
        assert compass2.get_direction() == 'E'

        # インスタンスは独立している
        compass1.heading = 180
        assert compass1.get_direction() == 'S'
        assert compass2.get_direction() == 'E'

    def test_calibration_state_persistence(self, compass):
        """
        シナリオ: キャリブレーション状態が保持される
        複数の操作後もキャリブレーション状態は保持される
        """
        compass.calibrate()
        assert compass.calibrated is True

        # 複数の操作を実行
        compass.heading = 45
        assert compass.calibrated is True

        compass.heading = 90
        assert compass.calibrated is True

        compass.get_direction()
        assert compass.calibrated is True

    def test_performance_stress_test(self, compass):
        """
        シナリオ: 高負荷条件下でのパフォーマンス
        10000 回の連続更新でも正確に動作する
        """
        import time

        compass.calibrate()

        start = time.time()
        for i in range(10000):
            heading = (i * 13) % 360
            compass.heading = heading
            compass.get_direction()
        elapsed = time.time() - start

        # 1 秒以内に完了するべき
        assert elapsed < 1.0

    def test_direction_consistency_across_queries(self, compass):
        """
        シナリオ: 複数回のクエリで方角の一貫性を保証
        """
        compass.calibrate()
        compass.heading = 123

        # 1000 回クエリして全て同じ結果
        results = [compass.get_direction() for _ in range(1000)]
        assert all(direction == 'SE' for direction in results)

    def test_comprehensive_workflow_with_state_verification(self, compass):
        """
        シナリオ: 包括的なワークフロー with 状態検証
        通常のユースケースを再現する
        """
        # 初期状態を確認
        assert compass.calibrated is False
        state = {'heading': compass.get_heading(), 'direction': compass.get_direction()}
        assert state['heading'] == 0
        assert state['direction'] == 'N'

        # キャリブレーション
        compass.calibrate()

        # 北方向確認
        compass.heading = 0
        assert compass.get_direction() == 'N'

        # 東方向へ移動
        compass.heading = 90
        assert compass.get_direction() == 'E'

        # 南方向へ移動
        compass.heading = 180
        assert compass.get_direction() == 'S'

        # 西方向へ移動
        compass.heading = 270
        assert compass.get_direction() == 'W'

        # 北に戻す
        compass.heading = 0
        assert compass.get_direction() == 'N'
        assert compass.calibrated is True

    def test_main_function_workflow(self):
        """
        シナリオ: main() 関数でのデバイス統合テスト
        初期化、ボタン操作、キャリブレーションをシミュレート
        """
        from microbit import display, button_a, Image
        from compass import main
        
        # ボタン操作をシミュレート：1回目 False、2回目 True、3回目で例外をスロー
        call_count = [0]
        
        def button_press_simulation():
            call_count[0] += 1
            if call_count[0] == 1:
                return False
            elif call_count[0] == 2:
                return True  # ボタンが押されたことをシミュレート
            else:
                # 3回目のチェック時にループ終了（例外をスロー）
                raise KeyboardInterrupt("Test loop exit")
        
        button_a.is_pressed.side_effect = button_press_simulation
        
        # main() 実行（例外でループを終了）
        try:
            main()
        except KeyboardInterrupt:
            pass
        
        # display.show() が Image.SQUARE で呼び出されたことを確認（初期 + キャリブレーション）
        display.show.assert_called()
        assert display.show.call_count >= 2  # 初期 + キャリブレーション時
        
        # display.scroll() が呼び出されたことを確認
        display.scroll.assert_called()
        assert display.scroll.call_count >= 1
        
    def test_main_function_entry_point(self):
        """
        シナリオ: compass.py をスクリプトとして実行
        if __name__ == '__main__' ブロックをカバー
        """
        import runpy
        from unittest.mock import patch, MagicMock
        
        # button_a を1回チェック後に終了させる
        call_count = [0]
        
        def exit_after_check():
            call_count[0] += 1
            if call_count[0] > 1:
                raise KeyboardInterrupt()
            return False
        
        with patch('microbit.button_a.is_pressed', side_effect=exit_after_check):
            try:
                runpy.run_module('compass', run_name='__main__', alter_sys=True)
            except (KeyboardInterrupt, SystemExit):
                pass  # 正常終了
        
        # button_a が呼び出されたことを確認
        assert call_count[0] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
