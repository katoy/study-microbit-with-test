#!/usr/bin/env python3
"""
Record actual MakeCode simulator showing compass program operation.

Uses direct editor navigation and creates a proper project.
"""

import asyncio
import sys
import math
from pathlib import Path
from PIL import Image
from io import BytesIO

# Add skill to path
skill_root = Path(__file__).parent.parent.parent.parent / ".copilot" / "skills" / "microbit-makecode-recorder"
sys.path.insert(0, str(skill_root))


async def record_compass_simulator():
    """Record the compass simulator with actual code execution."""
    
    try:
        from playwright.async_api import async_playwright
        from rendering.cursor_renderer import CursorRenderer
        from rendering.gif_generator import GifGenerator
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    project_dir = Path(__file__).parent.parent
    src_file = project_dir / "src" / "compass_makecode.py"
    screenshots_dir = project_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    output_gif = screenshots_dir / "demo.gif"
    
    print("🎬 Recording compass simulator with actual code execution...")
    
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return False
    
    compass_code = src_file.read_text()
    screenshots: list[Image.Image] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1600, "height": 900})
        
        try:
            print("\n🌐 Opening MakeCode editor...")
            # Try to go directly to a new project
            await page.goto("https://makecode.microbit.org/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            
            print("📝 Creating new project...")
            # Click new project or skip intro
            try:
                # Try clicking anywhere to dismiss intro if present
                await page.click("body", position={"x": 800, "y": 450})
                await page.wait_for_timeout(500)
            except Exception:
                pass
            
            # Try to find and click the "New Project" button
            buttons = await page.locator("button").all()
            print(f"  Found {len(buttons)} buttons")
            
            # Look for buttons that might create new project
            for button in buttons:
                text = await button.text_content()
                if text and ("new" in text.lower() or "create" in text.lower() or "start" in text.lower()):
                    print(f"  Clicking button: {text}")
                    await button.click()
                    await page.wait_for_timeout(3000)
                    break
            
            # Alternative: navigate directly to editor
            print("⚙️  Navigating to editor...")
            await page.goto("https://makecode.microbit.org/#editor", 
                          wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(4000)
            
            # Try to ensure we're in the editor and take a screenshot to verify
            print("📸 Checking editor state...")
            screenshot_bytes = await page.screenshot()
            img = Image.open(BytesIO(screenshot_bytes))
            
            # Check if we see editor elements
            content = await page.content()
            if "editor" not in content.lower():
                print("⚠️  Warning: 'editor' not found in page content")
            
            print("📝 Injecting compass code...")
            
            # Try multiple approaches to get focus on editor
            # 1. Click in the middle of the page
            await page.click("body", position={"x": 800, "y": 450})
            await page.wait_for_timeout(500)
            
            # 2. Try Ctrl+A to select all (might focus editor)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(500)
            
            # 3. Type the code
            print(f"  Typing {len(compass_code)} characters...")
            for i, char in enumerate(compass_code):
                if i % 500 == 0 and i > 0:
                    pct = int(100 * i / len(compass_code))
                    print(f"    {pct}%")
                
                await page.keyboard.type(char, delay=1)
                if char == "\n":
                    await page.wait_for_timeout(3)
            
            await page.wait_for_timeout(3000)
            print("  ✓ Code injected")
            
            # Wait for code to compile and simulator to start
            print("\n⏳ Waiting for simulator to start...")
            await page.wait_for_timeout(5000)
            
            # Now take screenshots as we change heading
            print("📸 Capturing simulator frames...")
            
            directions = [
                (0, "North"),
                (45, "Northeast"),
                (90, "East"),
                (135, "Southeast"),
                (180, "South"),
                (225, "Southwest"),
                (270, "West"),
                (315, "Northwest"),
            ]
            
            for idx, (heading, label) in enumerate(directions):
                print(f"  [{idx+1}/8] 🔄 {label} ({heading}°)...", end=" ", flush=True)
                
                # Try to update heading via JavaScript
                try:
                    # Method 1: Direct state manipulation
                    js = f"""
                    if (window.pxsim) {{
                        const runtime = window.pxsim.runtime;
                        if (runtime && runtime.board && runtime.board.state) {{
                            runtime.board.state.heading = {heading};
                        }}
                    }}
                    """
                    await page.evaluate(js)
                except Exception:
                    pass
                
                # Try alternative approaches
                try:
                    # Method 2: Via input element if it exists
                    inputs = await page.locator("input[type='range'], input[type='number']").all()
                    for inp in inputs:
                        try:
                            await inp.fill(str(heading))
                        except Exception:
                            pass
                except Exception:
                    pass
                
                # Wait for display to update
                await page.wait_for_timeout(1200)
                
                # Take screenshot
                try:
                    screenshot_bytes = await page.screenshot()
                    img = Image.open(BytesIO(screenshot_bytes))
                    screenshots.append(img)
                    print("✓")
                except Exception as e:
                    print(f"✗ ({e})")
            
            if not screenshots:
                print("❌ No screenshots captured")
                return False
            
            print(f"\n✅ Captured {len(screenshots)} frames")
            
            # Add cursor visualization
            print("🎨 Adding cursor effects...")
            cursor_renderer = CursorRenderer()
            enhanced: list[Image.Image] = []
            
            for i, screenshot in enumerate(screenshots):
                # Draw cursor to show interaction
                angle_rad = math.radians(i * 45 - 90)
                center_x, center_y = 1600 // 2, 900 // 2
                radius = 250
                cursor_x = int(center_x + radius * math.cos(angle_rad))
                cursor_y = int(center_y + radius * math.sin(angle_rad))
                
                with_cursor = cursor_renderer.draw_cursor(screenshot, cursor_x, cursor_y)
                enhanced.append(with_cursor)
            
            # Generate GIF
            print("🎞️  Generating animated GIF...")
            gif_gen = GifGenerator()
            gif_gen.create(enhanced, str(output_gif), fps=0.5)
            
            file_size = output_gif.stat().st_size
            print(f"\n✅ GIF created successfully!")
            print(f"📊 File: {output_gif}")
            print(f"📊 Size: {file_size / (1024*1024):.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await browser.close()


async def main():
    """Main entry point."""
    success = await record_compass_simulator()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
