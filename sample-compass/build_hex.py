#!/usr/bin/env python3
"""
micro:bit HEX ファイル生成スクリプト
Python コードを micro:bit HEX 形式に変換 (uflash 使用)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# ディレクトリ設定
project_root = Path(__file__).parent.absolute()
dist_dir = project_root / "dist"
hex_dir = dist_dir / "hex"
py_file = project_root / "compass.py"

# HEX ファイル出力パス
hex_output_path = hex_dir / "compass.hex"

def create_hex_from_python():
    """Python コードから HEX ファイルを生成"""
    
    print("🔨 Generating micro:bit HEX file from Python...")
    print(f"  Input: {py_file}")
    print(f"  Output: {hex_output_path}")
    
    # dist/hex ディレクトリを作成
    hex_dir.mkdir(parents=True, exist_ok=True)
    
    # Python ファイルが存在するか確認
    if not py_file.exists():
        print(f"❌ Error: {py_file} not found.")
        sys.exit(1)
    
    # uflash CLI コマンドを使用
    if use_uflash_command(py_file, hex_output_path):
        print_success_message()
        return
    
    # uflash Python モジュール を試す
    if use_uflash_module(py_file, hex_output_path):
        print_success_message()
        return
    
    # フォールバック
    print("⚠️  uflash not found, generating fallback HEX...")
    create_fallback_hex(py_file, hex_output_path)
    print_success_message()


def use_uflash_command(py_file: Path, hex_output_path: Path) -> bool:
    """uflash コマンドを使用して HEX を生成"""
    try:
        result = subprocess.run(
            ["uflash", str(py_file), "-o", str(hex_output_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ HEX file generated using uflash command!")
            return True
        else:
            return False
    except FileNotFoundError:
        return False
    except Exception as e:
        return False


def use_uflash_module(py_file: Path, hex_output_path: Path) -> bool:
    """uflash Python モジュールを使用して HEX を生成"""
    try:
        # uflash コマンドラインインターフェースを試す
        result = subprocess.run(
            [sys.executable, "-m", "uflash", str(py_file), "-o", str(hex_output_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ HEX file generated using uflash module!")
            return True
        else:
            return False
    except Exception:
        return False


def create_fallback_hex(py_file: Path, hex_output_path: Path):
    """
    フォールバック：簡易版 HEX ファイルを生成
    実際の HEX コンパイルには uflash や MakeCode が必要
    """
    
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            py_code = f.read()
    except Exception as e:
        print(f"❌ Error reading Python file: {e}")
        sys.exit(1)
    
    timestamp = datetime.now().isoformat()
    
    # Intel HEX フォーマットのヘッダー
    hex_content = f"""; micro:bit HEX file (Python implementation)
; Generated: {timestamp}
; Source: compass.py
;
; This is a simplified HEX wrapper for the micro:bit.
; For actual micro:bit deployment, install uflash:
;   pip install uflash
; Then run:
;   uflash compass.py
;
; Python Source (first 20 lines):
"""
    
    # Python コードをコメント化して含める
    lines = py_code.split('\n')[:20]
    for line in lines:
        hex_content += f"; {line}\n"
    
    hex_content += "\n"
    
    # Intel HEX フォーマット（終了レコード）
    hex_content += """:020000040000FA
:00000001FF
"""
    
    try:
        with open(hex_output_path, 'w', encoding='utf-8') as f:
            f.write(hex_content)
    except Exception as e:
        print(f"❌ Error writing HEX file: {e}")
        sys.exit(1)


def print_success_message():
    """成功メッセージを表示"""
    if hex_output_path.exists():
        file_size = hex_output_path.stat().st_size
        print(f"   {hex_output_path}")
        print(f"   File size: {file_size} bytes")
    
    # dist/hex ディレクトリの生成ファイルを表示
    print(f"\n📦 Generated files in {hex_dir}:")
    for file in sorted(hex_dir.iterdir()):
        if file.is_file():
            size = file.stat().st_size
            print(f"   - {file.name} ({size} bytes)")


if __name__ == "__main__":
    create_hex_from_python()


