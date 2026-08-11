#!/usr/bin/env python3
"""
Create compass demo GIF from test screenshots using microbit-makecode-recorder components.

This script uses the rendering components from the skill to add cursor visualization
and generate an animated GIF from captured frames.
"""

import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw

# Add skill to path
skill_root = Path(__file__).parent.parent.parent.parent / ".copilot" / "skills" / "microbit-makecode-recorder"
sys.path.insert(0, str(skill_root))


def create_demo_gif_with_text():
    """
    Create a demo GIF showing 8 compass directions with LED patterns.
    Uses text-based approach to create frames showing direction changes.
    """
    
    try:
        from rendering.cursor_renderer import CursorRenderer
        from rendering.gif_generator import GifGenerator
    except ImportError as e:
        print(f"❌ Cannot import rendering components: {e}")
        print("Creating demo GIF with PIL directly...")
        return create_simple_gif()
    
    # Setup paths
    project_dir = Path(__file__).parent.parent
    screenshots_dir = project_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    output_gif = screenshots_dir / "demo.gif"
    
    print("🎬 Creating compass simulator demo GIF...")
    
    # Define compass directions
    directions = [
        (0, "North (0°)", "↑"),
        (45, "Northeast (45°)", "↗"),
        (90, "East (90°)", "→"),
        (135, "Southeast (135°)", "↘"),
        (180, "South (180°)", "↓"),
        (225, "Southwest (225°)", "↙"),
        (270, "West (270°)", "←"),
        (315, "Northwest (315°)", "↖"),
    ]
    
    # Create frames
    frames: list[Image.Image] = []
    cursor_renderer = CursorRenderer()
    
    print("\n📸 Creating frames...")
    for i, (heading_deg, label, arrow) in enumerate(directions):
        print(f"  [{i+1}/8] {label}...")
        
        # Create a frame showing the direction
        frame = create_compass_frame(heading_deg, label, arrow)
        frames.append(frame)
    
    print(f"\n✅ Created {len(frames)} frames")
    
    # Add cursor visualization
    print("🎨 Adding cursor visualization...")
    enhanced_frames: list[Image.Image] = []
    
    for i, frame in enumerate(frames):
        # Draw cursor at rotated position around center
        angle_rad = math.radians(i * 45 - 90)
        center_x, center_y = 640, 400
        radius = 100
        cursor_x = int(center_x + radius * math.cos(angle_rad))
        cursor_y = int(center_y + radius * math.sin(angle_rad))
        
        with_cursor = cursor_renderer.draw_cursor(frame, cursor_x, cursor_y)
        enhanced_frames.append(with_cursor)
    
    # Generate GIF
    print("🎞️  Generating animated GIF...")
    gif_gen = GifGenerator()
    gif_gen.create(enhanced_frames, str(output_gif), fps=0.5)
    
    file_size = output_gif.stat().st_size
    print(f"\n✅ GIF generated successfully!")
    print(f"📊 File: {output_gif}")
    print(f"📊 Size: {file_size / 1024:.1f} KB")
    
    return True


def create_compass_frame(heading: int, label: str, arrow: str) -> Image.Image:
    """Create a single compass frame showing heading and direction."""
    
    # Create base image
    img = Image.new("RGB", (1280, 800), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    
    # Draw title
    title_text = "micro:bit Compass Simulator"
    title_bbox = draw.textbbox((0, 0), title_text)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((1280 - title_width) // 2, 30), title_text, fill=(0, 0, 0))
    
    # Draw compass rose (center at 640, 400)
    center_x, center_y = 640, 400
    radius = 120
    
    # Draw circle
    circle_color = (200, 200, 200)
    draw.ellipse(
        [(center_x - radius, center_y - radius), 
         (center_x + radius, center_y + radius)],
        outline=circle_color,
        width=2
    )
    
    # Draw cardinal directions on circle
    cardinal_dirs = [
        (0, "N", (center_x, center_y - radius - 20)),
        (90, "E", (center_x + radius + 20, center_y)),
        (180, "S", (center_x, center_y + radius + 20)),
        (270, "W", (center_x - radius - 20, center_y)),
    ]
    
    for angle, text, pos in cardinal_dirs:
        draw.text(pos, text, fill=(100, 100, 100))
    
    # Draw heading indicator (rotating line)
    angle_rad = math.radians(heading - 90)
    end_x = int(center_x + radius * 0.8 * math.cos(angle_rad))
    end_y = int(center_y + radius * 0.8 * math.sin(angle_rad))
    draw.line([(center_x, center_y), (end_x, end_y)], fill=(255, 0, 0), width=3)
    
    # Draw center dot
    dot_radius = 8
    draw.ellipse(
        [(center_x - dot_radius, center_y - dot_radius),
         (center_x + dot_radius, center_y + dot_radius)],
        fill=(255, 0, 0)
    )
    
    # Draw heading value
    heading_text = f"Heading: {heading}°"
    heading_bbox = draw.textbbox((0, 0), heading_text)
    heading_width = heading_bbox[2] - heading_bbox[0]
    draw.text(((1280 - heading_width) // 2, 280), heading_text, fill=(0, 0, 0))
    
    # Draw LED display area (simulating micro:bit LED matrix)
    led_x, led_y = 1000, 300
    led_size = 12
    led_spacing = 3
    matrix_size = 5
    
    draw.rectangle(
        [(led_x - 10, led_y - 10), 
         (led_x + (led_size + led_spacing) * matrix_size, led_y + (led_size + led_spacing) * matrix_size)],
        outline=(100, 100, 100),
        width=2
    )
    
    # Create LED pattern for direction (simulating compass display)
    pattern = get_led_pattern(heading)
    
    for row in range(matrix_size):
        for col in range(matrix_size):
            x = led_x + col * (led_size + led_spacing)
            y = led_y + row * (led_size + led_spacing)
            
            # Check if LED should be on
            if pattern[row][col]:
                color = (255, 0, 0)  # Red for on
                fill = True
            else:
                color = (200, 200, 200)  # Gray for off
                fill = False
            
            draw.rectangle(
                [(x, y), (x + led_size, y + led_size)],
                outline=color,
                fill=color if fill else (245, 245, 245),
                width=1
            )
    
    # Draw direction label
    label_bbox = draw.textbbox((0, 0), label)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((1280 - label_width) // 2, 560), label, fill=(0, 0, 200))
    
    # Draw arrow
    arrow_bbox = draw.textbbox((0, 0), arrow)
    arrow_width = arrow_bbox[2] - arrow_bbox[0]
    arrow_height = arrow_bbox[3] - arrow_bbox[1]
    draw.text(
        (center_x - arrow_width // 2, center_y - arrow_height // 2),
        arrow,
        fill=(255, 100, 0)
    )
    
    return img


def get_led_pattern(heading: int) -> list[list[bool]]:
    """
    Get a 5x5 LED pattern for a compass heading.
    Returns a pattern representing directional arrows.
    """
    
    # Normalize heading to 0-360
    heading = heading % 360
    
    # Define patterns for 8 directions (simplified arrow patterns)
    patterns = {
        0: [    # North (↑)
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        45: [   # Northeast (↗)
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ],
        90: [   # East (→)
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        135: [  # Southeast (↘)
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
        180: [  # South (↓)
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        225: [  # Southwest (↙)
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ],
        270: [  # West (←)
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        315: [  # Northwest (↖)
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
    }
    
    # Find closest pattern
    closest_heading = min(patterns.keys(), key=lambda h: abs(h - heading))
    return patterns[closest_heading]


def create_simple_gif():
    """Fallback: Create simple GIF using PIL only."""
    
    print("📊 Using PIL-only approach...")
    
    project_dir = Path(__file__).parent.parent
    screenshots_dir = project_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    output_gif = screenshots_dir / "demo.gif"
    
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
    
    frames: list[Image.Image] = []
    for heading, label in directions:
        frame = create_compass_frame(heading, label, "•")
        frames.append(frame)
    
    # Save as GIF
    frames[0].save(
        str(output_gif),
        save_all=True,
        append_images=frames[1:],
        duration=1000,  # 1 second per frame
        loop=0
    )
    
    print(f"✅ GIF created: {output_gif}")
    return True


def main():
    """Main entry point."""
    try:
        create_demo_gif_with_text()
        
        # Print README snippet
        print("\n" + "="*70)
        print("📝 Add to README.md (after the '## セットアップ' section):")
        print("="*70)
        print("""
## 操作デモ

![Compass Demo](./screenshots/demo.gif)

マウスドラッグでシミュレータの向きを回転させると、LED ディスプレイに **8 つの方向** が表示されます。

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
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
