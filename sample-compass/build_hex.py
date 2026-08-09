#!/usr/bin/env python3
"""Generate a flashable Universal Hex file for the BBC micro:bit."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.resolve()
DIST_DIR = PROJECT_ROOT / "dist"
HEX_DIR = DIST_DIR / "hex"
PY_FILE = PROJECT_ROOT / "compass.py"
HEX_OUTPUT_PATH = HEX_DIR / "compass.hex"


def _load_uflash():
    """Load the compiler dependency with an actionable error message."""
    try:
        import uflash
    except ImportError as exc:  # pragma: no cover - uv sync installs it
        raise RuntimeError(
            "uflash is required to generate a flashable HEX file; run `uv sync`."
        ) from exc
    return uflash


def validate_microbit_hex(hex_path: Path) -> None:
    """Reject malformed HEX files and metadata-only placeholder artifacts."""
    if not hex_path.is_file():
        raise ValueError(f"HEX compiler did not create {hex_path}")

    data_record_count = 0
    has_end_of_file = False

    try:
        lines = hex_path.read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"Unable to read HEX output: {hex_path}") from exc

    for line_number, line in enumerate(lines, start=1):
        if not line:
            continue
        if not line.startswith(":"):
            raise ValueError(f"Invalid Intel HEX record at line {line_number}")

        try:
            record = bytes.fromhex(line[1:])
        except ValueError as exc:
            raise ValueError(f"Invalid hexadecimal data at line {line_number}") from exc

        if len(record) < 5 or len(record) != record[0] + 5:
            raise ValueError(f"Invalid Intel HEX length at line {line_number}")
        if sum(record) & 0xFF:
            raise ValueError(f"Invalid Intel HEX checksum at line {line_number}")

        record_type = record[3]
        if record_type == 0x00 and record[0] > 0:
            data_record_count += 1
        elif record_type == 0x01:
            has_end_of_file = True

    if data_record_count == 0:
        raise ValueError("HEX output contains no firmware data records")
    if not has_end_of_file:
        raise ValueError("HEX output has no end-of-file record")


def create_hex_from_python(
    source_path: Path = PY_FILE,
    output_path: Path = HEX_OUTPUT_PATH,
) -> Path:
    """Compile a Python program into a validated Universal Hex artifact."""
    source_path = Path(source_path)
    output_path = Path(output_path)

    print("🔨 Generating a flashable micro:bit HEX file from Python...")
    print(f"  Input: {source_path}")
    print(f"  Output: {output_path}")

    if not source_path.is_file():
        raise FileNotFoundError(f"Python source not found: {source_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.unlink(missing_ok=True)

    generated_path = output_path.parent / f"{source_path.stem}.hex"
    try:
        uflash = _load_uflash()
        uflash.flash(
            path_to_python=str(source_path),
            paths_to_microbits=[str(output_path.parent)],
            keepname=True,
        )

        if generated_path != output_path:
            generated_path.replace(output_path)

        validate_microbit_hex(output_path)
    except Exception:
        output_path.unlink(missing_ok=True)
        if generated_path != output_path:
            generated_path.unlink(missing_ok=True)
        raise

    print_success_message(output_path)
    return output_path


def print_success_message(output_path: Path) -> None:
    """Report the validated build artifact."""
    file_size = output_path.stat().st_size
    print("✅ Flashable HEX file generated successfully!")
    print(f"   {output_path}")
    print(f"   File size: {file_size} bytes")


def main() -> None:
    try:
        create_hex_from_python()
    except Exception as exc:
        print(f"❌ HEX generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
