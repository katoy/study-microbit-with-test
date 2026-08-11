"""MicrobotRecorder のユニットテスト。"""

from core.recorder import MicrobotRecorder, EventType


def test_recorder_initialization():
    """MicrobotRecorder の初期化テスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    assert recorder.hex_file == "test.hex"
    assert recorder.browser_width == 1280
    assert recorder.browser_height == 800


def test_recorder_custom_dimensions():
    """カスタム寸法での初期化テスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex", browser_width=800, browser_height=600)
    assert recorder.browser_width == 800
    assert recorder.browser_height == 600


def test_recorder_method_chaining():
    """メソッドチェーンが機能するテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")

    result = recorder.click(100, 100)
    assert isinstance(result, MicrobotRecorder)
    assert result is recorder

    result = result.type("test")
    assert isinstance(result, MicrobotRecorder)

    result = result.wait(1)
    assert isinstance(result, MicrobotRecorder)


def test_recorder_events_collected():
    """イベントが順序通りに収集されるテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")

    recorder.click(100, 100).type("test").wait(1).click(200, 200)

    assert len(recorder._events) == 4
    assert recorder._events[0].event_type == EventType.CLICK
    assert recorder._events[1].event_type == EventType.TYPE
    assert recorder._events[2].event_type == EventType.WAIT
    assert recorder._events[3].event_type == EventType.CLICK


def test_recorder_click_params():
    """クリックイベントのパラメータテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    recorder.click(150, 250)

    event = recorder._events[0]
    assert event.params["x"] == 150
    assert event.params["y"] == 250


def test_recorder_type_params():
    """テキスト入力イベントのパラメータテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    recorder.type("Hello World")

    event = recorder._events[0]
    assert event.params["text"] == "Hello World"


def test_recorder_wait_params():
    """待機イベントのパラメータテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    recorder.wait(2.5)

    event = recorder._events[0]
    assert event.params["seconds"] == 2.5


def test_recorder_key_params():
    """キー入力イベントのパラメータテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    recorder.key("Enter")

    event = recorder._events[0]
    assert event.params["key"] == "Enter"


def test_recorder_screenshot_params():
    """スクリーンショットイベントのパラメータテスト。"""
    recorder = MicrobotRecorder(hex_file="test.hex")
    recorder.screenshot(label="step1")

    event = recorder._events[0]
    assert event.params["label"] == "step1"
