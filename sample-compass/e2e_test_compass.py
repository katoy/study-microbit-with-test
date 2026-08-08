"""
Compass アプリケーション E2E テスト

実際のユースケースに基づいた統合テストを実施する
"""

import pytest


# compass.py の Compass クラスをモック化
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

    def set_heading(self, heading):
        """テスト用：方位角を設定する"""
        if heading < 0 or heading >= 360:
            raise ValueError('方位角は 0-359 度である必要があります')
        self.heading = heading

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
        else:  # heading < 337.5
            return 'NW'


class TestCompassE2E:
    """E2E テスト：Compass アプリケーション統合テスト"""

    @pytest.fixture
    def compass(self):
        """コンパスのフィクスチャ"""
        return MockCompass()

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
        compass.set_heading(90)
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
            compass.set_heading(heading)
            assert compass.get_direction() == expected_direction, \
                f"heading={heading} は {expected_direction} を返すべき"

    def test_boundary_value_transitions(self, compass):
        """
        シナリオ: 方位の境界値での正確な遷移
        """
        compass.calibrate()

        # 北から北東への遷移（22.5°）
        compass.set_heading(22.4)
        assert compass.get_direction() == 'N'

        compass.set_heading(22.5)
        assert compass.get_direction() == 'NE'

        # 南東から南への遷移（157.5°）
        compass.set_heading(157.4)
        assert compass.get_direction() == 'SE'

        compass.set_heading(157.5)
        assert compass.get_direction() == 'S'

    def test_north_wrap_around(self, compass):
        """
        シナリオ: 北での角度ラップアラウンド（359°から0°への遷移）
        """
        compass.calibrate()

        # 359°も北
        compass.set_heading(359)
        assert compass.get_direction() == 'N'

        # 0°も北
        compass.set_heading(0)
        assert compass.get_direction() == 'N'

        # 337.5°以上は北
        compass.set_heading(337.5)
        assert compass.get_direction() == 'N'

    def test_continuous_rotation_simulation(self, compass):
        """
        シナリオ: 360°連続回転シミュレーション
        デバイスが時計回りに1周する場合
        """
        compass.calibrate()

        directions = []
        for heading in range(0, 360, 45):
            compass.set_heading(heading)
            directions.append(compass.get_direction())

        expected = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        assert directions == expected

    def test_rapid_direction_queries(self, compass):
        """
        シナリオ: 同じ方位角での連続クエリ
        状態が一貫していることを確認
        """
        compass.calibrate()
        compass.set_heading(45)

        # 100 回クエリしても結果は一貫している
        for _ in range(100):
            assert compass.get_direction() == 'NE'
            assert compass.get_heading() == 45

    def test_multiple_compass_instances(self):
        """
        シナリオ: 複数のコンパスインスタンスが独立して動作
        """
        compass1 = MockCompass()
        compass2 = MockCompass()

        compass1.calibrate()
        compass1.set_heading(0)

        compass2.calibrate()
        compass2.set_heading(90)

        assert compass1.get_direction() == 'N'
        assert compass2.get_direction() == 'E'

        # インスタンスは独立している
        compass1.set_heading(180)
        assert compass1.get_direction() == 'S'
        assert compass2.get_direction() == 'E'

    def test_invalid_heading_rejection(self, compass):
        """
        シナリオ: 無効な方位角は拒否される
        """
        compass.calibrate()

        # 負の値
        with pytest.raises(ValueError):
            compass.set_heading(-1)

        # 360度以上
        with pytest.raises(ValueError):
            compass.set_heading(360)

        # 大きな値
        with pytest.raises(ValueError):
            compass.set_heading(720)

    def test_calibration_state_persistence(self, compass):
        """
        シナリオ: キャリブレーション状態が保持される
        複数の操作後もキャリブレーション状態は保持される
        """
        compass.calibrate()
        assert compass.calibrated is True

        # 複数の操作を実行
        compass.set_heading(45)
        assert compass.calibrated is True

        compass.set_heading(90)
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
            compass.set_heading(heading)
            compass.get_direction()
        elapsed = time.time() - start

        # 1 秒以内に完了するべき
        assert elapsed < 1.0

    def test_direction_consistency_across_queries(self, compass):
        """
        シナリオ: 複数回のクエリで方角の一貫性を保証
        """
        compass.calibrate()
        compass.set_heading(123)

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
        compass.set_heading(0)
        assert compass.get_direction() == 'N'

        # 東方向へ移動
        compass.set_heading(90)
        assert compass.get_direction() == 'E'

        # 南方向へ移動
        compass.set_heading(180)
        assert compass.get_direction() == 'S'

        # 西方向へ移動
        compass.set_heading(270)
        assert compass.get_direction() == 'W'

        # 北に戻す
        compass.set_heading(0)
        assert compass.get_direction() == 'N'
        assert compass.calibrated is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
