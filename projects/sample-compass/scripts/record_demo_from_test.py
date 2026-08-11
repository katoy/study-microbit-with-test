#!/usr/bin/env python3
"""
Record compass simulator demo using the existing test infrastructure.

This extracts the test logic and captures screenshots during execution.
"""

import os
import re
import time
import sys
from pathlib import Path
from io import BytesIO
import math

# Playwright sync API for recording
from playwright.sync_api import sync_playwright
from PIL import Image

# Add skill to path for GIF generation
skill_root = Path(__file__).parent.parent.parent.parent / ".copilot" / "skills" / "microbit-makecode-recorder"
sys.path.insert(0, str(skill_root))


def record_compass_demo_gif():
    """Record compass simulator demo using test infrastructure."""
    
    try:
        from rendering.cursor_renderer import CursorRenderer
        from rendering.gif_generator import GifGenerator
    except ImportError as e:
        print(f"❌ Cannot import rendering: {e}")
        return False
    
    project_root = Path(__file__).parent.parent
    python_path = project_root / "src" / "compass_makecode.py"
    screenshots_dir = project_root / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    output_gif = screenshots_dir / "demo.gif"
    
    if not python_path.exists():
        print(f"❌ Source file not found: {python_path}")
        return False
    
    print("🎬 Recording compass simulator demo...")
    print(f"📄 Source: {python_path}")
    print(f"📁 Output: {output_gif}")
    
    with open(python_path, "r", encoding="utf-8") as f:
        raw_python_code = f.read()
    
    # Modify code for testing: bypass calibration, replace show_string
    python_code = raw_python_code.replace("is_calibrated = False", "is_calibrated = True")
    python_code = re.sub(r"if not is_calibrated:", "if False:", python_code)
    python_code = re.sub(r"basic\.show_string\([^)]*\)", "basic.clear_screen()", python_code)
    
    print("\n🌐 Starting MakeCode simulator...")
    
    screenshots: list[Image.Image] = []
    logs = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(locale="ja-JP")
            page = context.new_page()
            
            # Capture console logs
            page.on("console", lambda msg: logs.append(msg.text))
            
            # Navigate to MakeCode
            print("📖 Opening MakeCode...")
            page.goto("https://makecode.microbit.org/", wait_until="networkidle", timeout=60000)
            time.sleep(3)
            
            # Switch to Python editor
            print("⚙️  Setting up Python editor...")
            page.keyboard.press("Control+K")  # Open command palette
            time.sleep(1)
            page.keyboard.type("Python")
            page.keyboard.press("Enter")
            time.sleep(2)
            
            # Inject code
            print("📝 Injecting compass code...")
            page.keyboard.press("Control+A")
            page.keyboard.press("Delete")
            time.sleep(0.5)
            
            # Type code carefully
            for i, line in enumerate(python_code.split("\n")):
                if i % 20 == 0 and i > 0:
                    print(f"  {i} lines...")
                page.keyboard.type(line)
                page.keyboard.press("Enter")
                time.sleep(0.1)
            
            time.sleep(5)
            print("  ✓ Code injected")
            
            # Wait for simulator to initialize
            print("⏳ Waiting for simulator...")
            time.sleep(5)
            
            # Capture screenshots at different headings
            print("\n📸 Capturing frames...")
            
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
                
                # Try to set heading via JavaScript
                try:
                    page.evaluate(f"""
                    (() => {{
                        const iframe = document.querySelector('iframe[class*="sim"]');
                        if (iframe && iframe.contentWindow) {{
                            const state = iframe.contentWindow.pxsim?.runtime?.board?.state;
                            if (state) state.heading = {heading};
                        }}
                        const state = window.pxsim?.runtime?.board?.state;
                        if (state) state.heading = {heading};
                    }})();
                    """)
                except Exception:
                    pass
                
                # Wait for update
                time.sleep(1.2)
                
                # Take screenshot
                try:
                    screenshot_bytes = page.screenshot()
                    img = Image.open(BytesIO(screenshot_bytes))
                    screenshots.append(img)
                    print("✓")
                except Exception as e:
                    print(f"✗ ({e})")
            
            page.close()
            context.close()
            browser.close()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    if not screenshots:
        print("❌ No screenshots captured")
        return False
    
    print(f"\n✅ Captured {len(screenshots)} frames")
    
    # Add cursor visualization
    print("🎨 Adding cursor effects...")
    cursor_renderer = CursorRenderer()
    enhanced: list[Image.Image] = []
    
    for i, screenshot in enumerate(screenshots):
        # Draw cursor at simulator area
        angle_rad = math.radians(i * 45 - 90)
        # Assume simulator is on right side
        sim_x = 1200
        sim_y = 450
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


if __name__ == "__main__":
    success = record_compass_demo_gif()
    sys.exit(0 if success else 1)
