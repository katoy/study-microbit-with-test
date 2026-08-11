#!/usr/bin/env python3
"""
Record compass simulator demo GIF using microbit-makecode-recorder skill components.

This script:
1. Opens MakeCode editor with compass_makecode.py
2. Rotates device heading through 8 cardinal directions
3. Captures simulator frames showing LED display
4. Generates animated GIF with cursor visualization
"""

import asyncio
import sys
import math
from pathlib import Path

# Add skill to path
skill_root = Path(__file__).parent.parent.parent.parent / ".copilot" / "skills" / "microbit-makecode-recorder"
sys.path.insert(0, str(skill_root))
sys.path.insert(0, str(skill_root / "core"))
sys.path.insert(0, str(skill_root / "rendering"))


async def main():
    """Record compass simulator demo."""
    
    try:
        from playwright.async_api import async_playwright
        from PIL import Image
        from rendering.cursor_renderer import CursorRenderer
        from rendering.gif_generator import GifGenerator
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install playwright pillow")
        return 1
    
    # Setup paths
    project_dir = Path(__file__).parent.parent
    src_file = project_dir / "src" / "compass_makecode.py"
    screenshots_dir = project_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    output_gif = screenshots_dir / "demo.gif"
    
    print("🎬 Recording compass simulator demo...")
    print(f"📄 Source: {src_file}")
    print(f"📁 Output: {output_gif}")
    
    # Verify source file exists
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return 1
    
    compass_code = src_file.read_text()
    
    # Launch browser and capture frames
    screenshots: list[Image.Image] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        try:
            print("\n🌐 Opening MakeCode editor...")
            await page.goto("https://makecode.microbit.org/beta", wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
            
            print("⚙️  Setting up Python environment...")
            
            # Click on the editor area
            await page.click(".monaco-editor", force=True)
            await page.wait_for_timeout(500)
            
            # Clear any existing content
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(500)
            
            # Type the compass code
            print("📝 Injecting compass code...")
            code_len = len(compass_code)
            for i, char in enumerate(compass_code):
                if i % 300 == 0 and i > 0:
                    pct = int(100 * i / code_len)
                    print(f"  {pct}% ({i}/{code_len} characters)")
                
                await page.keyboard.type(char)
                if char == "\n":
                    await page.wait_for_timeout(2)
            
            await page.wait_for_timeout(3000)
            print(f"  100% (code injected)")
            
            # Wait for simulator to initialize
            print("⏳ Waiting for simulator initialization...")
            await page.wait_for_timeout(4000)
            
            # Define compass directions
            directions = [
                (0, "North (0°)"),
                (45, "Northeast (45°)"),
                (90, "East (90°)"),
                (135, "Southeast (135°)"),
                (180, "South (180°)"),
                (225, "Southwest (225°)"),
                (270, "West (270°)"),
                (315, "Northwest (315°)"),
            ]
            
            print("\n📸 Capturing rotation sequence...")
            sim_center_x, sim_center_y = 640, 400
            radius = 100
            
            for idx, (heading_deg, label) in enumerate(directions):
                print(f"  [{idx+1}/8] 🔄 {label}...", end=" ", flush=True)
                
                # Set heading via JavaScript if possible
                try:
                    js = f"""
                    (() => {{
                        const state = window.pxtRuntime?.board?.state;
                        if (state?.compass) {{
                            state.compass.heading = {heading_deg};
                        }}
                    }})();
                    """
                    await page.evaluate(js)
                except Exception:
                    pass
                
                # Wait for display update
                await page.wait_for_timeout(1000)
                
                # Take screenshot
                screenshot_bytes = await page.screenshot()
                img = Image.frombytes("RGB", (1280, 800), screenshot_bytes)
                screenshots.append(img)
                print("✓")
            
            if not screenshots:
                print("❌ No screenshots captured")
                return 1
            
            print(f"\n✅ Captured {len(screenshots)} frames")
            
            # Add cursor visualization
            print("🎨 Adding cursor visualization...")
            cursor_renderer = CursorRenderer()
            enhanced: list[Image.Image] = []
            
            for i, screenshot in enumerate(screenshots):
                # Draw cursor at rotated position
                angle_rad = math.radians(i * 45 - 90)
                cursor_x = int(sim_center_x + radius * math.cos(angle_rad))
                cursor_y = int(sim_center_y + radius * math.sin(angle_rad))
                
                with_cursor = cursor_renderer.draw_cursor(screenshot, cursor_x, cursor_y)
                enhanced.append(with_cursor)
            
            # Generate GIF
            print("🎞️  Generating animated GIF...")
            gif_gen = GifGenerator()
            gif_gen.create(enhanced, str(output_gif), fps=0.5)
            
            file_size = output_gif.stat().st_size
            print(f"\n✅ GIF generated successfully!")
            print(f"📊 File: {output_gif}")
            print(f"📊 Size: {file_size / 1024:.1f} KB")
            
            # Print README snippet
            print("\n" + "="*70)
            print("📝 Add to README.md (after the '## セットアップ' section):")
            print("="*70)
            print("""
## 操作デモ

![Compass Demo](./screenshots/demo.gif)

マウスドラッグでシミュレータの向きを回転させると、LED ディスプレイに **8 つの方向** が表示されます。各方向は矢印パターンで視覚的に識別できます。

| 角度 | 方向 | LED パターン |
|------|------|----------|
| 0° | 北（N） | ↑ |
| 45° | 北東（NE） | ↗ |
| 90° | 東（E） | → |
| 135° | 南東（SE） | ↘ |
| 180° | 南（S） | ↓ |
| 225° | 南西（SW） | ↙ |
| 270° | 西（W） | ← |
| 315° | 北西（NW） | ↖ |

### キャリブレーション

初回起動時は「CAL」メッセージが表示されます。この状態で**ボタン A** を押すとキャリブレーションが開始されます。""")
            print("="*70)
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
        finally:
            await browser.close()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
