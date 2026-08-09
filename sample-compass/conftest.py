"""
pytest の共通設定ファイル

microbit モジュールをモック化して、テスト環境で import できるようにする
"""

import sys
from unittest.mock import MagicMock, patch
import pytest

# microbit モジュールをモック化
microbit = MagicMock()
microbit.compass = MagicMock()
microbit.display = MagicMock()
microbit.button_a = MagicMock()
microbit.button_b = MagicMock()
microbit.Image = MagicMock()
microbit.Image.SQUARE = MagicMock()

sys.modules['microbit'] = microbit


@pytest.fixture(autouse=True)
def reset_mocks():
    """各テスト前後に microbit モックをリセット"""
    microbit.compass.reset_mock(return_value=True, side_effect=True)
    microbit.display.reset_mock(return_value=True, side_effect=True)
    microbit.button_a.reset_mock(return_value=True, side_effect=True)
    microbit.button_b.reset_mock(return_value=True, side_effect=True)
    microbit.Image.reset_mock(return_value=True, side_effect=True)

    microbit.compass.heading.return_value = 0
    microbit.compass.is_calibrated.return_value = False

    def mark_as_calibrated():
        """校正 API の実行結果をモックの状態へ反映する"""
        microbit.compass.is_calibrated.return_value = True

    microbit.compass.calibrate.side_effect = mark_as_calibrated
    microbit.button_a.was_pressed.return_value = False
    microbit.button_b.was_pressed.return_value = False
    yield
    microbit.compass.reset_mock(return_value=True, side_effect=True)
    microbit.display.reset_mock(return_value=True, side_effect=True)
    microbit.button_a.reset_mock(return_value=True, side_effect=True)
    microbit.button_b.reset_mock(return_value=True, side_effect=True)
    microbit.Image.reset_mock(return_value=True, side_effect=True)
