#!/usr/bin/env python3
"""
Record compass simulator demo by capturing during actual test execution.

Uses the existing test infrastructure to load and run the compass program.
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


async def record_via_test():
    """Record compass simulator using test infrastructure."""
    
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
    
    print("🎬 Recording compass simulator demo via test execution...")
    
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return False
    
    compass_code = src_file.read_text()
    screenshots: list[Image.Image] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1600, "height": 900})
        
        try:
            print("\n🌐 Opening MakeCode (blocks view)...")
            # Open MakeCode in blocks view
            await page.goto("https://makecode.microbit.org/", wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(3000)
            
            print("📝 Switching to Python editor...")
            # Switch to Python tab
            try:
                # Look for Python option in the interface
                python_elements = await page.locator("text=Python").all()
                if python_elements:
                    await python_elements[0].click()
                    await page.wait_for_timeout(3000)
                else:
                    # Try to find Python in a dropdown menu
                    await page.click("[aria-label*='Edit'], button:has-text('Edit')")
                    await page.wait_for_timeout(1000)
            except Exception as e:
                print(f"  ⚠️ Could not switch to Python tab: {e}")
            
            # Take screenshot to see current state
            print("⚙️  Setting up Python environment...")
            screenshot_bytes = await page.screenshot()
            with open("/tmp/debug_screen.png", "wb") as f:
                f.write(screenshot_bytes)
            print("  Saved debug screenshot to /tmp/debug_screen.png")
            
            # Try to paste Python code
            print("📝 Injecting compass code...")
            
            # Click somewhere on the page first
            await page.click("body", position={"x": 800, "y": 450})
            await page.wait_for_timeout(300)
            
            # Try to access the code editor
            # In MakeCode, when in Python mode, there should be a code editor
            try:
                # Try using keyboard shortcuts
                await page.keyboard.press("Control+A")
                await page.keyboard.type(compass_code, delay=0.5)
            except Exception as e:
                print(f"  ⚠️  Keyboard input failed: {e}")
            
            await page.wait_for_timeout(5000)
            
            # The simulator should now be running
            # Try clicking on the simulator to see if we can interact with it
            print("\n🎨 Capturing simulator frames...")
            
            # Define directions to test
            directions = [
                (0, "North", 0),
                (45, "Northeast", 1),
                (90, "East", 2),
                (135, "Southeast", 3),
                (180, "South", 4),
                (225, "Southwest", 5),
                (270, "West", 6),
                (315, "Northwest", 7),
            ]
            
            for idx, (heading, label, frame_idx) in enumerate(directions):
                print(f"  [{idx+1}/8] 🔄 {label} ({heading}°)...", end=" ", flush=True)
                
                # Try to manipulate heading
                try:
                    # Look for a heading input or way to change it
                    # In MakeCode simulator, there might be a rotation indicator
                    
                    # Try JavaScript injection to modify state
                    js = f"""
                    (() => {{
                        // Try to find and modify the compass heading
                        const iframe = document.querySelector('iframe[src*="microbit"]');
                        if (iframe && iframe.contentWindow) {{
                            const iwin = iframe.contentWindow;
                            if (iwin.pxsim && iwin.pxsim.runtime) {{
                                iwin.pxsim.runtime.board.heading = {heading};
                            }}
                        }}
                        
                        // Alternative: try direct access
                        if (window.pxsim && window.pxsim.runtime) {{
                            window.pxsim.runtime.board.heading = {heading};
                        }}
                    }})();
                    """
                    await page.evaluate(js)
                except Exception as e:
                    print(f"  (JS failed: {e})")
                
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
                # Draw cursor to show interaction at different points
                angle_rad = math.radians(i * 45 - 90)
                # Use simulator center - approximately at right side of screen
                sim_x = 1200  # Simulator is usually on the right
                sim_y = 450   # Middle height
                radius = 150
                cursor_x = int(sim_x + radius * math.cos(angle_rad))
                cursor_y = int(sim_y + radius * math.sin(angle_rad))
                
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
    success = await record_via_test()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
