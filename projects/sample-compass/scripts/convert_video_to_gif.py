#!/usr/bin/env python3
"""Convert Playwright recorded video to GIF animation."""

import os
import subprocess
import shutil
import sys
import glob

def convert_video_to_gif(project_root):
    """Convert .webm video from Playwright to GIF."""
    # project_root は sample-compass/ の親ディレクトリ
    sample_compass_dir = os.path.join(project_root, "sample-compass")
    video_temp = os.path.join(sample_compass_dir, ".video-temp")
    screenshots_dir = os.path.join(sample_compass_dir, "screenshots")
    
    # 出力 GIF パス
    output_gif = os.path.join(screenshots_dir, "simulator-demo.gif")
    
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # ビデオファイルを探す
    video_file = None
    if os.path.exists(video_temp):
        # .webm ファイルをサーチ（タイムスタンプ付き）
        webm_files = glob.glob(os.path.join(video_temp, "*.webm"))
        if webm_files:
            video_file = webm_files[0]
    
    if not video_file:
        print(f"⚠️  No .webm video file found in {video_temp}")
        print(f"Available files: {os.listdir(video_temp) if os.path.exists(video_temp) else 'directory does not exist'}")
        return False
    
    print(f"📹 Found video: {video_file}")
    
    # ffmpeg でビデオを GIF に変換
    # フレームレート: 5fps, 幅: 1280px に制限
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-i", video_file,
        "-vf", "fps=5,scale=1280:-1:flags=lanczos",
        "-loop", "0",
        output_gif
    ]
    
    print(f"🔄 Converting video to GIF with: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  FFmpeg warning/info: {result.stderr}")
    except FileNotFoundError:
        print("❌ ffmpeg not found at /opt/homebrew/bin/ffmpeg. Install with: brew install ffmpeg")
        return False
    
    # 一時ファイルをクリーンアップ
    if os.path.exists(video_temp):
        shutil.rmtree(video_temp)
        print(f"🗑️  Cleaned up temporary video directory")
    
    # 成功確認
    if os.path.exists(output_gif):
        size_mb = os.path.getsize(output_gif) / (1024 * 1024)
        print(f"✅ GIF saved: {output_gif} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"❌ GIF not created at {output_gif}")
        return False

if __name__ == "__main__":
    # このスクリプトの親ディレクトリ (sample-compass) から、さらに親へ (projects root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_compass_dir = os.path.dirname(script_dir)
    project_root = os.path.dirname(sample_compass_dir)
    
    success = convert_video_to_gif(project_root)
    sys.exit(0 if success else 1)

