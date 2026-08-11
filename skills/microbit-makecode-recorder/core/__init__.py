"""Core components for MakeCode browser automation and API."""

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    """Lazy import to avoid circular imports."""
    if name == "MicrobotRecorder":
        from .recorder import MicrobotRecorder
        return MicrobotRecorder
    elif name == "MakeCodeBrowser":
        from .makecode_browser import MakeCodeBrowser
        return MakeCodeBrowser
    elif name == "MakeCodeError":
        from .errors import MakeCodeError
        return MakeCodeError
    elif name == "HexFileNotFoundError":
        from .errors import HexFileNotFoundError
        return HexFileNotFoundError
    elif name == "MakeCodeLoadError":
        from .errors import MakeCodeLoadError
        return MakeCodeLoadError
    elif name == "ScreenshotError":
        from .errors import ScreenshotError
        return ScreenshotError
    elif name == "GifGenerationError":
        from .errors import GifGenerationError
        return GifGenerationError
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "MicrobotRecorder",
    "MakeCodeBrowser",
    "MakeCodeError",
    "HexFileNotFoundError",
    "MakeCodeLoadError",
    "ScreenshotError",
    "GifGenerationError",
]
