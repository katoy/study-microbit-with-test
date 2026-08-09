"""Tests for producing a flashable micro:bit HEX artifact."""

from pathlib import Path

import pytest

import build_hex


METADATA_ONLY_HEX = ":020000040000FA\n:00000001FF\n"
HEX_WITH_DATA = ":0400000001020304F2\n:00000001FF\n"


def test_validate_microbit_hex_rejects_a_file_without_firmware_data(tmp_path):
    hex_path = tmp_path / "compass.hex"
    hex_path.write_text(METADATA_ONLY_HEX, encoding="ascii")

    with pytest.raises(ValueError, match="firmware data"):
        build_hex.validate_microbit_hex(hex_path)


def test_validate_microbit_hex_accepts_valid_intel_hex_data(tmp_path):
    hex_path = tmp_path / "compass.hex"
    hex_path.write_text(HEX_WITH_DATA, encoding="ascii")

    build_hex.validate_microbit_hex(hex_path)


def test_create_hex_does_not_replace_a_compiler_failure_with_a_dummy_file(
    monkeypatch, tmp_path
):
    source_path = tmp_path / "compass.py"
    output_path = tmp_path / "dist" / "hex" / "compass.hex"
    source_path.write_text("from microbit import display\n", encoding="utf-8")
    output_path.parent.mkdir(parents=True)
    output_path.write_text(METADATA_ONLY_HEX, encoding="ascii")

    class FailingUflash:
        @staticmethod
        def flash(**_kwargs):
            raise RuntimeError("compiler failed")

    monkeypatch.setattr(build_hex, "_load_uflash", lambda: FailingUflash)

    with pytest.raises(RuntimeError, match="compiler failed"):
        build_hex.create_hex_from_python(source_path, output_path)

    assert not output_path.exists()


def test_create_hex_rejects_non_flashable_compiler_output(monkeypatch, tmp_path):
    source_path = tmp_path / "compass.py"
    output_path = tmp_path / "dist" / "hex" / "compass.hex"
    source_path.write_text("from microbit import display\n", encoding="utf-8")

    class DummyUflash:
        @staticmethod
        def flash(*, paths_to_microbits, **_kwargs):
            output_dir = Path(paths_to_microbits[0])
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "compass.hex").write_text(METADATA_ONLY_HEX, encoding="ascii")

    monkeypatch.setattr(build_hex, "_load_uflash", lambda: DummyUflash)

    with pytest.raises(ValueError, match="firmware data"):
        build_hex.create_hex_from_python(source_path, output_path)

    assert not output_path.exists()
