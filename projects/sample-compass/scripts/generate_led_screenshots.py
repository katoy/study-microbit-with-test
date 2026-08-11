#!/usr/bin/env python3
"""
Generate individual LED pattern screenshots for each compass direction.

Creates a 5x5 LED matrix visualization for each of the 8 cardinal directions,
saves them as individual images, and generates a combined grid image.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_led_pattern_image(heading: int, direction: str, arrow: str) -> Image.Image:
    """
    Create an image showing a single compass direction with LED pattern.
    
    Args:
        heading: Heading angle in degrees
        direction: Direction name (e.g., "North", "Northeast")
        arrow: Arrow symbol (e.g., "↑", "↗")
    
    Returns:
        PIL Image object
    """
    
    # Image dimensions
    width, height = 300, 300
    
    # Create white background
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_color = (100, 100, 100)
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=2)
    
    # Draw heading text
    heading_text = f"{heading}°"
    heading_y = 15
    draw.text(
        (width // 2 - 15, heading_y),
        heading_text,
        fill=(0, 0, 0)
    )
    
    # Draw direction name
    direction_text = direction
    direction_y = 45
    draw.text(
        (width // 2 - len(direction_text) * 3, direction_y),
        direction_text,
        fill=(0, 0, 200)
    )
    
    # Draw LED matrix (5x5)
    led_size = 30
    led_spacing = 8
    start_x = (width - (5 * led_size + 4 * led_spacing)) // 2
    start_y = 110
    
    # Get LED pattern
    pattern = get_led_pattern(heading)
    
    # Draw each LED
    for row in range(5):
        for col in range(5):
            x = start_x + col * (led_size + led_spacing)
            y = start_y + row * (led_size + led_spacing)
            
            # Determine LED color based on pattern
            if pattern[row][col]:
                # LED is ON - red/bright
                fill_color = (255, 100, 100)
                outline_color = (255, 0, 0)
                width_outline = 2
            else:
                # LED is OFF - gray
                fill_color = (220, 220, 220)
                outline_color = (150, 150, 150)
                width_outline = 1
            
            # Draw LED rectangle
            draw.rectangle(
                [(x, y), (x + led_size, y + led_size)],
                fill=fill_color,
                outline=outline_color,
                width=width_outline
            )
    
    # Draw arrow symbol
    arrow_y = start_y + 5 * (led_size + led_spacing) + 20
    arrow_x = width // 2 - 8
    draw.text(
        (arrow_x, arrow_y),
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


def create_grid_image(images: list[tuple[Image.Image, str, int]], cols: int = 4) -> Image.Image:
    """
    Create a grid image from multiple LED pattern images.
    
    Args:
        images: List of (image, direction_label, heading) tuples
        cols: Number of columns in grid
    
    Returns:
        Combined grid image
    """
    
    cell_width, cell_height = 300, 300
    spacing = 20
    rows = (len(images) + cols - 1) // cols
    
    grid_width = cols * cell_width + (cols - 1) * spacing + 2 * spacing
    grid_height = rows * cell_height + (rows - 1) * spacing + 2 * spacing
    
    grid_img = Image.new("RGB", (grid_width, grid_height), color=(245, 245, 245))
    
    for idx, (img, label, heading) in enumerate(images):
        row = idx // cols
        col = idx % cols
        
        x = spacing + col * (cell_width + spacing)
        y = spacing + row * (cell_height + spacing)
        
        grid_img.paste(img, (x, y))
    
    return grid_img


def main():
    """Generate LED pattern screenshots."""
    
    project_dir = Path(__file__).parent.parent
    screenshots_dir = project_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    print("🎨 Generating LED pattern screenshots...")
    
    # Define compass directions
    directions = [
        (0, "North", "↑"),
        (45, "Northeast", "↗"),
        (90, "East", "→"),
        (135, "Southeast", "↘"),
        (180, "South", "↓"),
        (225, "Southwest", "↙"),
        (270, "West", "←"),
        (315, "Northwest", "↖"),
    ]
    
    images_list = []
    
    print("\n📸 Creating individual LED pattern images...")
    for heading, direction, arrow in directions:
        print(f"  {heading:3d}° {direction:10s} {arrow}...", end=" ", flush=True)
        
        # Create LED pattern image
        img = create_led_pattern_image(heading, direction, arrow)
        
        # Save individual image
        filename = f"led_{heading:03d}_{direction.lower().replace(' ', '_')}.png"
        filepath = screenshots_dir / filename
        img.save(filepath)
        
        images_list.append((img, direction, heading))
        print("✓")
    
    print(f"\n✅ Created {len(images_list)} individual images")
    
    # Create grid image
    print("\n🎨 Creating grid image...")
    grid_img = create_grid_image(images_list, cols=4)
    grid_filepath = screenshots_dir / "led_patterns_grid.png"
    grid_img.save(grid_filepath)
    print(f"✅ Grid image created: {grid_filepath}")
    
    # Print file information
    print("\n📊 Generated files:")
    for heading, direction, arrow in directions:
        filename = f"led_{heading:03d}_{direction.lower().replace(' ', '_')}.png"
        filepath = screenshots_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"  {filepath.name:40s} {size_kb:6.1f} KB")
    
    if grid_filepath.exists():
        grid_size_kb = grid_filepath.stat().st_size / 1024
        print(f"  {grid_filepath.name:40s} {grid_size_kb:6.1f} KB")
    
    # Print README snippet
    print("\n" + "="*70)
    print("📝 Add to README.md (after the '## 操作デモ' section):")
    print("="*70)
    print("""
## LED 表示パターン

各方向に対応する LED 表示パターンを以下に示します。方位磁石がキャリブレーションされ、
シミュレーターで向きが回転すると、これらのパターンが 5×5 LED マトリックスに表示されます。

### 方向別 LED パターン

![LED Patterns Grid](./screenshots/led_patterns_grid.png)

### 個別パターン

| 角度 | 方向 | LED パターン | 画像 |
|------|------|----------|------|
| 0° | 北（N） | ↑ | ![North](./screenshots/led_000_north.png) |
| 45° | 北東（NE） | ↗ | ![Northeast](./screenshots/led_045_northeast.png) |
| 90° | 東（E） | → | ![East](./screenshots/led_090_east.png) |
| 135° | 南東（SE） | ↘ | ![Southeast](./screenshots/led_135_southeast.png) |
| 180° | 南（S） | ↓ | ![South](./screenshots/led_180_south.png) |
| 225° | 南西（SW） | ↙ | ![Southwest](./screenshots/led_225_southwest.png) |
| 270° | 西（W） | ← | ![West](./screenshots/led_270_west.png) |
| 315° | 北西（NW） | ↖ | ![Northwest](./screenshots/led_315_northwest.png) |

### パターン解説

- **赤色 LED**（明るい）: 点灯している LED
- **灰色 LED**（暗い）: 消灯している LED
- **矢印**: 対応する方向を示す記号""")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
