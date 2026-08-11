"""
microbit-makecode-recorder: Record micro:bit program execution as GIF animations.
"""

from core.recorder import MicrobotRecorder
from core.errors import MakeCodeError, HexFileNotFoundError, MakeCodeLoadError

__version__ = "0.1.0"
__all__ = [
    "MicrobotRecorder",
    "MakeCodeError",
    "HexFileNotFoundError",
    "MakeCodeLoadError",
]
