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
microbit.Image = MagicMock()
microbit.Image.SQUARE = MagicMock()

sys.modules['microbit'] = microbit


@pytest.fixture(autouse=True)
def reset_mocks():
    """各テスト前後に microbit モックをリセット"""
    microbit.display.reset_mock()
    microbit.button_a.reset_mock()
    microbit.button_a.is_pressed.return_value = False
    microbit.Image.reset_mock()
    yield
    microbit.display.reset_mock()
    microbit.button_a.reset_mock()
    microbit.Image.reset_mock()

