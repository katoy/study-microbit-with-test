"""GIF ファイル生成ユーティリティ。"""

from pathlib import Path
from PIL import Image
from core.errors import GifGenerationError


class GifGenerator:
    """PIL を使用して画像シーケンスから GIF を生成する。"""

    def create(
        self,
        images: list[Image.Image],
        output_path: str,
        fps: int = 10,
    ) -> None:
        """
        GIF ファイルを生成

        Args:
            images: 画像リスト
            output_path: 出力ファイルパス
            fps: フレームレート（デフォルト: 10）

        Raises:
            GifGenerationError: 生成に失敗した場合
        """
        if not images:
            raise GifGenerationError("Image list is empty")

        # 出力ディレクトリをチェック
        output_dir = Path(output_path).parent
        if not output_dir.exists():
            raise GifGenerationError(f"Output directory does not exist: {output_dir}")

        try:
            # fps からデュレーション（ミリ秒）を計算
            duration_ms = 1000 // fps

            # 最初の画像を基準に GIF を保存
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=duration_ms,
                loop=0,  # 無限ループ
                optimize=False,
            )
        except Exception as e:
            raise GifGenerationError(f"Failed to create GIF: {str(e)}")
