"""MakeCode レコーダーのカスタム例外クラスを定義します。"""


class MakeCodeError(Exception):
    """MakeCode レコーダーエラーの基本例外クラス。"""

    pass


class HexFileNotFoundError(MakeCodeError):
    """16 進形式ファイルが見つからない場合に発生します。"""

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Hex file not found: {path}")


class MakeCodeLoadError(MakeCodeError):
    """MakeCode ページまたは 16 進形式ファイルの読み込みに失敗した場合に発生します。"""

    def __init__(self, message: str, retries: int = 0):
        self.message = message
        self.retries = retries
        super().__init__(f"{message} (retried {retries} times)")


class ScreenshotError(MakeCodeError):
    """スクリーンショットキャプチャが失敗した場合に発生します。"""

    def __init__(self, message: str, retries: int = 0):
        self.message = message
        self.retries = retries
        super().__init__(f"Screenshot failed: {message} (retried {retries} times)")


class GifGenerationError(MakeCodeError):
    """GIF 生成に失敗した場合に発生します。"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"GIF generation failed: {message}")
