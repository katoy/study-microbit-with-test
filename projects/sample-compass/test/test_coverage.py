"""
Unit tests for compass_makecode.py to achieve 100% code coverage.

These tests verify all functions in the compass_makecode module,
including those that depend on MakeCode API.
"""

import sys
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


# Mock MakeCode API to allow importing compass_makecode.py
class MockBasic:
    @staticmethod
    def clear_screen():
        pass

    @staticmethod
    def show_leds(pattern):
        pass

    @staticmethod
    def show_string(text):
        pass

    @staticmethod
    def show_arrow(arrow):
        pass

    @staticmethod
    def pause(ms):
        pass

    @staticmethod
    def forever(func):
        pass


class MockInput:
    @staticmethod
    def calibrate_compass():
        pass

    @staticmethod
    def compass_heading():
        return 0

    @staticmethod
    def running_time():
        return 0

    @staticmethod
    def on_button_pressed(button, handler):
        pass


class MockConsole:
    @staticmethod
    def log(text):
        pass


class MockButton:
    A = 1
    B = 2


class MockArrowNames:
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7


# Inject mocks into builtins before importing compass_makecode
import builtins

builtins.basic = MockBasic()
builtins.input = MockInput()
builtins.console = MockConsole()
builtins.Button = MockButton()
builtins.ArrowNames = MockArrowNames()
builtins.number = float

# Import the compass module
import compass_makecode
from compass_makecode import (
    calibrate_compass,
    get_direction_string,
    on_button_pressed_a,
    on_forever,
)


class TestGetDirectionString:
    """Test cases for get_direction_string() function."""

    # Test NORTH direction (heading < 22.5 or heading >= 337.5)
    def test_direction_north_at_0(self):
        """Test N direction at 0°"""
        assert get_direction_string(0) == "N"

    def test_direction_north_at_359(self):
        """Test N direction at 359°"""
        assert get_direction_string(359) == "N"

    def test_direction_north_at_337_5(self):
        """Test N direction at boundary 337.5°"""
        assert get_direction_string(337.5) == "N"

    def test_direction_north_at_22_4(self):
        """Test N direction just below NE boundary"""
        assert get_direction_string(22.4) == "N"

    # Test NORTH_EAST direction (22.5 <= heading < 67.5)
    def test_direction_northeast_at_22_5(self):
        """Test NE direction at boundary 22.5°"""
        assert get_direction_string(22.5) == "NE"

    def test_direction_northeast_at_45(self):
        """Test NE direction at 45°"""
        assert get_direction_string(45) == "NE"

    def test_direction_northeast_at_67_4(self):
        """Test NE direction just below E boundary"""
        assert get_direction_string(67.4) == "NE"

    # Test EAST direction (67.5 <= heading < 112.5)
    def test_direction_east_at_67_5(self):
        """Test E direction at boundary 67.5°"""
        assert get_direction_string(67.5) == "E"

    def test_direction_east_at_90(self):
        """Test E direction at 90°"""
        assert get_direction_string(90) == "E"

    def test_direction_east_at_112_4(self):
        """Test E direction just below SE boundary"""
        assert get_direction_string(112.4) == "E"

    # Test SOUTH_EAST direction (112.5 <= heading < 157.5)
    def test_direction_southeast_at_112_5(self):
        """Test SE direction at boundary 112.5°"""
        assert get_direction_string(112.5) == "SE"

    def test_direction_southeast_at_135(self):
        """Test SE direction at 135°"""
        assert get_direction_string(135) == "SE"

    def test_direction_southeast_at_157_4(self):
        """Test SE direction just below S boundary"""
        assert get_direction_string(157.4) == "SE"

    # Test SOUTH direction (157.5 <= heading < 202.5)
    def test_direction_south_at_157_5(self):
        """Test S direction at boundary 157.5°"""
        assert get_direction_string(157.5) == "S"

    def test_direction_south_at_180(self):
        """Test S direction at 180°"""
        assert get_direction_string(180) == "S"

    def test_direction_south_at_202_4(self):
        """Test S direction just below SW boundary"""
        assert get_direction_string(202.4) == "S"

    # Test SOUTH_WEST direction (202.5 <= heading < 247.5)
    def test_direction_southwest_at_202_5(self):
        """Test SW direction at boundary 202.5°"""
        assert get_direction_string(202.5) == "SW"

    def test_direction_southwest_at_225(self):
        """Test SW direction at 225°"""
        assert get_direction_string(225) == "SW"

    def test_direction_southwest_at_247_4(self):
        """Test SW direction just below W boundary"""
        assert get_direction_string(247.4) == "SW"

    # Test WEST direction (247.5 <= heading < 292.5)
    def test_direction_west_at_247_5(self):
        """Test W direction at boundary 247.5°"""
        assert get_direction_string(247.5) == "W"

    def test_direction_west_at_270(self):
        """Test W direction at 270°"""
        assert get_direction_string(270) == "W"

    def test_direction_west_at_292_4(self):
        """Test W direction just below NW boundary"""
        assert get_direction_string(292.4) == "W"

    # Test NORTH_WEST direction (292.5 <= heading < 337.5)
    def test_direction_northwest_at_292_5(self):
        """Test NW direction at boundary 292.5°"""
        assert get_direction_string(292.5) == "NW"

    def test_direction_northwest_at_315(self):
        """Test NW direction at 315°"""
        assert get_direction_string(315) == "NW"

    def test_direction_northwest_at_337_4(self):
        """Test NW direction just below N boundary"""
        assert get_direction_string(337.4) == "NW"

    # Test error cases
    def test_direction_negative_heading(self):
        """Test error handling for negative heading"""
        assert get_direction_string(-1) == "ERR"

    def test_direction_heading_360(self):
        """Test error handling for heading >= 360"""
        assert get_direction_string(360) == "ERR"

    def test_direction_heading_above_360(self):
        """Test error handling for heading > 360"""
        assert get_direction_string(720) == "ERR"

    def test_direction_nan_heading(self):
        """Test error handling for NaN heading"""
        nan_value = float("nan")
        assert get_direction_string(nan_value) == "ERR"

    # Additional boundary tests for comprehensive coverage
    def test_direction_near_boundaries(self):
        """Test near critical boundaries"""
        # Near 0°/360° boundary
        assert get_direction_string(0.1) == "N"
        assert get_direction_string(359.9) == "N"

        # Test middle values in each range
        assert get_direction_string(11.25) == "N"
        assert get_direction_string(45) == "NE"
        assert get_direction_string(90) == "E"
        assert get_direction_string(135) == "SE"
        assert get_direction_string(180) == "S"
        assert get_direction_string(225) == "SW"
        assert get_direction_string(270) == "W"
        assert get_direction_string(315) == "NW"


class TestCalibrateFunctions:
    """Test cases for calibration and other MakeCode-dependent functions."""

    def test_calibrate_compass(self):
        """Test calibrate_compass function"""
        # Reset calibration state
        compass_makecode.is_calibrated = False

        # Mock the MakeCode API
        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            # Call calibrate_compass
            calibrate_compass()

            # Verify that the function calls the expected methods
            mock_basic.clear_screen.assert_called()
            mock_basic.show_leds.assert_called_once()
            mock_input.calibrate_compass.assert_called_once()
            mock_basic.show_string.assert_called_with("OK")

            # Verify calibration state changed
            assert compass_makecode.is_calibrated is True

    def test_on_button_pressed_a_not_calibrated(self):
        """Test on_button_pressed_a when not calibrated"""
        # Reset calibration state
        compass_makecode.is_calibrated = False

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input, \
             mock.patch("builtins.console") as mock_console:

            # Call button A handler
            on_button_pressed_a()

            # Should trigger calibration
            mock_basic.clear_screen.assert_called()
            mock_basic.show_leds.assert_called_once()

    def test_on_button_pressed_a_calibrated(self):
        """Test on_button_pressed_a when calibrated"""
        # Set calibration state
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input, \
             mock.patch("builtins.console") as mock_console:

            mock_input.compass_heading.return_value = 90
            mock_input.running_time.return_value = 1000

            # Call button A handler
            on_button_pressed_a()

            # Should log heading and direction
            mock_input.compass_heading.assert_called()
            mock_input.running_time.assert_called()
            mock_console.log.assert_called()

    def test_on_forever_not_calibrated(self):
        """Test on_forever loop when not calibrated"""
        # Reset calibration state
        compass_makecode.is_calibrated = False

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            # Call one iteration of forever loop
            on_forever()

            # Should show "CAL" message
            mock_basic.show_string.assert_called_with("CAL")
            mock_basic.pause.assert_called_with(1000)

    def test_on_forever_calibrated_north(self):
        """Test on_forever loop when calibrated and heading North"""
        # Set calibration state
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 0  # North

            # Call one iteration of forever loop
            on_forever()

            # Should show arrow for North
            mock_input.compass_heading.assert_called()
            mock_basic.show_arrow.assert_called_with(0)  # NORTH = 0
            mock_basic.pause.assert_called_with(500)

    def test_on_forever_calibrated_east(self):
        """Test on_forever loop when calibrated and heading East"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 90  # East

            on_forever()

            mock_basic.show_arrow.assert_called_with(2)  # EAST = 2

    def test_on_forever_calibrated_south(self):
        """Test on_forever loop when calibrated and heading South"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 180  # South

            on_forever()

            mock_basic.show_arrow.assert_called_with(4)  # SOUTH = 4

    def test_on_forever_calibrated_west(self):
        """Test on_forever loop when calibrated and heading West"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 270  # West

            on_forever()

            mock_basic.show_arrow.assert_called_with(6)  # WEST = 6

    def test_on_forever_calibrated_northeast(self):
        """Test on_forever loop when calibrated and heading Northeast"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 45  # Northeast

            on_forever()

            mock_basic.show_arrow.assert_called_with(1)  # NORTH_EAST = 1

    def test_on_forever_calibrated_southeast(self):
        """Test on_forever loop when calibrated and heading Southeast"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 135  # Southeast

            on_forever()

            mock_basic.show_arrow.assert_called_with(3)  # SOUTH_EAST = 3

    def test_on_forever_calibrated_southwest(self):
        """Test on_forever loop when calibrated and heading Southwest"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 225  # Southwest

            on_forever()

            mock_basic.show_arrow.assert_called_with(5)  # SOUTH_WEST = 5

    def test_on_forever_calibrated_northwest(self):
        """Test on_forever loop when calibrated and heading Northwest"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = 315  # Northwest

            on_forever()

            mock_basic.show_arrow.assert_called_with(7)  # NORTH_WEST = 7

    def test_on_forever_error_heading(self):
        """Test on_forever loop when compass returns error"""
        compass_makecode.is_calibrated = True

        with mock.patch("builtins.basic") as mock_basic, \
             mock.patch("builtins.input") as mock_input:

            mock_input.compass_heading.return_value = -1  # Error

            on_forever()

            # Should show "ERR" message
            mock_basic.show_string.assert_called_with("ERR")
            mock_basic.pause.assert_called_with(1000)
