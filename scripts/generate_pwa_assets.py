"""
Gerador de Ícones e Assets Oficiais PWA - IBPM Carvalho Ramos.
Gera ícones em 192x192, 512x512, maskable, apple-touch-icon e favicon com design Coração Ardente.
"""
import os
import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "web" / "icons"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def draw_church_icon(size: int, is_maskable: bool = False) -> Image.Image:
    # 1. Base Image
    img = Image.new("RGBA", (size, size), (7, 9, 14, 255)) # Dark Obsidian
    draw = ImageDraw.Draw(img)

    center_x = size / 2
    center_y = size / 2
    radius = size * (0.42 if not is_maskable else 0.36)

    # 2. Glowing outer ring / gradient background circle
    # Layer 1: Background circular gradient
    for r in range(int(radius + size * 0.08), int(radius), -1):
        alpha = int(30 * (1 - (r - radius) / (size * 0.08)))
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=(225, 29, 72, alpha) # Rubi glow
        )

    # Layer 2: Main circle
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=(19, 23, 34, 255), # Surface dark
        outline=(245, 158, 11, 200), # Gold border
        width=max(2, int(size * 0.015))
    )

    # 3. Flame Shape (Pentecostal Ruby / Gold Fire)
    flame_height = radius * 1.2
    flame_width = radius * 0.85
    base_y = center_y + radius * 0.45

    # Outer Ruby Flame
    points_flame_outer = [
        (center_x, base_y - flame_height), # Peak
        (center_x + flame_width * 0.5, base_y - flame_height * 0.6),
        (center_x + flame_width * 0.65, base_y - flame_height * 0.25),
        (center_x + flame_width * 0.4, base_y),
        (center_x, base_y + flame_height * 0.08),
        (center_x - flame_width * 0.4, base_y),
        (center_x - flame_width * 0.65, base_y - flame_height * 0.25),
        (center_x - flame_width * 0.5, base_y - flame_height * 0.6),
    ]
    draw.polygon(points_flame_outer, fill=(225, 29, 72, 240)) # Primary Rubi

    # Inner Gold Flame
    inner_h = flame_height * 0.7
    inner_w = flame_width * 0.55
    inner_base_y = base_y
    points_flame_inner = [
        (center_x, inner_base_y - inner_h),
        (center_x + inner_w * 0.5, inner_base_y - inner_h * 0.55),
        (center_x + inner_w * 0.6, inner_base_y - inner_h * 0.2),
        (center_x + inner_w * 0.35, inner_base_y),
        (center_x, inner_base_y + inner_h * 0.05),
        (center_x - inner_w * 0.35, inner_base_y),
        (center_x - inner_w * 0.6, inner_base_y - inner_h * 0.2),
        (center_x - inner_w * 0.5, inner_base_y - inner_h * 0.55),
    ]
    draw.polygon(points_flame_inner, fill=(245, 158, 11, 240)) # Secondary Gold

    # Center Bright Yellow Core
    core_h = inner_h * 0.45
    core_w = inner_w * 0.45
    points_core = [
        (center_x, inner_base_y - core_h),
        (center_x + core_w * 0.5, inner_base_y - core_h * 0.4),
        (center_x, inner_base_y),
        (center_x - core_w * 0.5, inner_base_y - core_h * 0.4),
    ]
    draw.polygon(points_core, fill=(254, 240, 138, 255)) # Warm White/Gold

    # 4. Golden Cross in the Foreground
    cross_top = center_y - radius * 0.4
    cross_bot = center_y + radius * 0.35
    cross_thick = max(3, int(size * 0.04))
    
    cross_arm_y = center_y - radius * 0.15
    cross_arm_w = radius * 0.55

    # Vertical bar of the Cross
    draw.rectangle(
        [center_x - cross_thick/2, cross_top, center_x + cross_thick/2, cross_bot],
        fill=(255, 255, 255, 250), # Pure White with Gold outline
        outline=(245, 158, 11, 255),
        width=max(1, int(size * 0.008))
    )
    # Horizontal arm of the Cross
    draw.rectangle(
        [center_x - cross_arm_w/2, cross_arm_y - cross_thick/2, center_x + cross_arm_w/2, cross_arm_y + cross_thick/2],
        fill=(255, 255, 255, 250),
        outline=(245, 158, 11, 255),
        width=max(1, int(size * 0.008))
    )

    return img

def generate_all_icons():
    print("🎨 Gerando ícones PWA oficiais da IBPM CR...")
    
    # 1. icon-192.png
    icon192 = draw_church_icon(192)
    icon192.save(OUTPUT_DIR / "icon-192.png", "PNG")
    print("✅ icon-192.png gerado")

    # 2. icon-512.png
    icon512 = draw_church_icon(512)
    icon512.save(OUTPUT_DIR / "icon-512.png", "PNG")
    print("✅ icon-512.png gerado")

    # 3. icon-maskable.png (com safe zone de 80%)
    icon_mask = draw_church_icon(512, is_maskable=True)
    icon_mask.save(OUTPUT_DIR / "icon-maskable.png", "PNG")
    print("✅ icon-maskable.png gerado")

    # 4. apple-touch-icon.png (180x180)
    apple_icon = draw_church_icon(180)
    apple_icon.save(OUTPUT_DIR / "apple-touch-icon.png", "PNG")
    print("✅ apple-touch-icon.png gerado")

    # 5. favicon.ico (64x64)
    fav = draw_church_icon(64)
    fav.save(OUTPUT_DIR / "favicon.ico", "ICO")
    print("✅ favicon.ico gerado")

    # 6. favicon.png (32x32)
    fav32 = draw_church_icon(32)
    fav32.save(OUTPUT_DIR / "favicon.png", "PNG")
    print("✅ favicon.png gerado")

if __name__ == "__main__":
    generate_all_icons()
