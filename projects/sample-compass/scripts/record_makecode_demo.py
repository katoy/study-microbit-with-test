#!/usr/bin/env python3
"""
Record actual MakeCode editor operation showing compass program.

This script:
1. Opens MakeCode and creates a new project
2. Injects the compass Python code
3. Captures the simulator showing rotation through 8 directions
4. Generates an animated GIF with real editor screenshots
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


async def record_makecode_demo():
    """Record MakeCode editor with compass program."""
    
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
    
    print("🎬 Recording MakeCode editor demo...")
    print(f"📄 Source: {src_file}")
    print(f"📁 Output: {output_gif}")
    
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return False
    
    compass_code = src_file.read_text()
    screenshots: list[Image.Image] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1600, "height": 900})
        
        try:
            print("\n🌐 Opening MakeCode...")
            # Navigate to MakeCode beta
            await page.goto("https://makecode.microbit.org/beta", 
                          wait_until="domcontentloaded", 
                          timeout=60000)
            
            # Wait for page to fully load
            print("⏳ Waiting for editor to load...")
            await page.wait_for_timeout(5000)
            
            # Click "New Project" button or similar
            print("📝 Creating new project...")
            
            # Look for new project button - might be different selector
            try:
                # Try to find and click new project button
                new_proj = await page.query_selector("[aria-label*='new'], [title*='new'], button:has-text('New')")
                if new_proj:
                    await new_proj.click()
                    await page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠️  Could not find new project button: {e}")
            
            # Alternative: directly navigate to new project
            await page.goto("https://makecode.microbit.org/beta#editor", 
                          wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
            
            print("⚙️  Setting up editor...")
            
            # Try to find Python tab/button
            # First, try to switch to Python view
            try:
                # Look for Python button or tab
                python_tab = await page.query_selector("button[title*='Python'], button:has-text('Python')")
                if python_tab:
                    await python_tab.click()
                    await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"⚠️  Could not switch to Python tab: {e}")
            
            # Try clicking in a likely editor area
            print("📝 Injecting code...")
            
            # Click somewhere in the middle - likely editor area
            await page.click("body", position={"x": 800, "y": 400})
            await page.wait_for_timeout(500)
            
            # Try keyboard shortcuts to ensure we're in the editor
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(500)
            
            # Type the compass code character by character
            print(f"Typing {len(compass_code)} characters...")
            for i, char in enumerate(compass_code):
                if i % 500 == 0 and i > 0:
                    pct = int(100 * i / len(compass_code))
                    print(f"  {pct}% - {i}/{len(compass_code)}")
                
                await page.keyboard.type(char, delay=2)
                if char == "\n":
                    await page.wait_for_timeout(5)
            
            await page.wait_for_timeout(3000)
            print("  100% - Code injected")
            
            # Wait for simulator to initialize and take first screenshot
            print("\n⏳ Waiting for simulator...")
            await page.wait_for_timeout(3000)
            
            # Take initial screenshot
            print("📸 Capturing rotation sequence...")
            screenshot_bytes = await page.screenshot()
            img = Image.open(BytesIO(screenshot_bytes))
            screenshots.append(img)
            print("  [1/8] Initial state ✓")
            
            # Now simulate rotating the device by changing heading values
            directions = [
                (45, "Northeast"),
                (90, "East"),
                (135, "Southeast"),
                (180, "South"),
                (225, "Southwest"),
                (270, "West"),
                (315, "Northwest"),
            ]
            
            for idx, (heading, label) in enumerate(directions, start=2):
                print(f"  [{idx}/8] 🔄 {label} ({heading}°)...", end=" ", flush=True)
                
                # Try to set heading via JavaScript
                try:
                    js = f"""
                    if (typeof pxsim !== 'undefined') {{
                        const state = pxsim.runtime?.board?.state;
                        if (state?.compass) {{
                            state.compass.heading = {heading};
                        }}
                    }}
                    """
                    await page.evaluate(js)
                except Exception:
                    pass
                
                # Wait for display to update
                await page.wait_for_timeout(1500)
                
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
            
            print(f"\n✅ Captured {len(screenshots)} frames from MakeCode")
            
            # Add cursor visualization
            print("🎨 Adding cursor effects...")
            cursor_renderer = CursorRenderer()
            enhanced: list[Image.Image] = []
            
            for i, screenshot in enumerate(screenshots):
                # Add cursor at different positions to show interaction
                angle_rad = math.radians(i * 45 - 90)
                center_x, center_y = 1600 // 2, 900 // 2
                radius = 200
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
            print(f"📊 Size: {file_size / 1024:.1f} KB")
            
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
    success = await record_makecode_demo()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
