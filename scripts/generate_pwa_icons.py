import math
import os
from PIL import Image, ImageDraw, ImageFilter

def create_gradient_canvas(size, start_col=(2, 132, 199), end_col=(99, 102, 241)):
    # Create smooth diagonal linear gradient
    img = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            factor = (x + y) / (2.0 * size)
            r = int(start_col[0] + factor * (end_col[0] - start_col[0]))
            g = int(start_col[1] + factor * (end_col[1] - start_col[1]))
            b = int(start_col[2] + factor * (end_col[2] - start_col[2]))
            img.putpixel((x, y), (r, g, b, 255))
    return img

def render_icon(size, is_maskable=False):
    # Scale base coordinate system
    scale = size / 512.0
    
    # Base background: gradient
    img = create_gradient_canvas(size)
    draw = ImageDraw.Draw(img)
    
    # Safe zone scale for maskable: safe area is inner 80% circle (radius = 0.4 * size)
    content_scale = 0.72 if is_maskable else 0.88
    center_x = size / 2.0
    center_y = size / 2.0
    
    # Draw soft glowing radial aura in the center
    aura_radius = int(180 * scale * content_scale)
    aura_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura_layer)
    aura_draw.ellipse(
        [center_x - aura_radius, center_y - aura_radius, center_x + aura_radius, center_y + aura_radius],
        fill=(255, 255, 255, 45)
    )
    aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(radius=int(25 * scale)))
    img = Image.alpha_composite(img, aura_layer)
    draw = ImageDraw.Draw(img)

    # Main symbol: Isometric Neo-Arcade Cube + Lightning/Sparkle
    # Cube coordinates (isometric projection)
    s = 110 * scale * content_scale
    cy = center_y - 15 * scale * content_scale
    cx = center_x

    # Top face
    p_top = (cx, cy - s * 0.9)
    p_right = (cx + s * 0.866, cy - s * 0.4)
    p_center = (cx, cy + s * 0.1)
    p_left = (cx - s * 0.866, cy - s * 0.4)

    # Bottom face vertices
    h = s * 0.95
    p_bot_left = (p_left[0], p_left[1] + h)
    p_bot_center = (p_center[0], p_center[1] + h)
    p_bot_right = (p_right[0], p_right[1] + h)

    # Draw left face
    draw.polygon([p_left, p_center, p_bot_center, p_bot_left], fill=(224, 242, 254, 240))
    # Draw right face
    draw.polygon([p_center, p_right, p_bot_right, p_bot_center], fill=(186, 230, 253, 220))
    # Draw top face
    draw.polygon([p_top, p_right, p_center, p_left], fill=(255, 255, 255, 255))

    # Add Arcade D-Pad and Button accents on top face
    # Draw stylized playful cross / rocket streak
    cross_w = 12 * scale * content_scale
    dpad_y = cy - s * 0.4
    draw.line([(cx - 24 * scale * content_scale, dpad_y), (cx + 24 * scale * content_scale, dpad_y)], fill=(14, 165, 233, 255), width=int(cross_w))
    draw.line([(cx, dpad_y - 24 * scale * content_scale), (cx, dpad_y + 24 * scale * content_scale)], fill=(14, 165, 233, 255), width=int(cross_w))

    # Add 4-pointed sparkle star at top right
    def draw_sparkle(sx, sy, r1, r2):
        pts = []
        for i in range(8):
            ang = i * math.pi / 4
            r = r1 if i % 2 == 0 else r2
            pts.append((sx + r * math.cos(ang), sy + r * math.sin(ang)))
        draw.polygon(pts, fill=(255, 255, 255, 250))

    draw_sparkle(cx + 90 * scale * content_scale, cy - 80 * scale * content_scale, 32 * scale * content_scale, 8 * scale * content_scale)
    draw_sparkle(cx - 85 * scale * content_scale, cy + 85 * scale * content_scale, 20 * scale * content_scale, 5 * scale * content_scale)

    # For standard non-maskable icon, apply a sleek squircle/rounded corner mask if requested,
    # or keep it edge-to-edge for PWA standard compliance (PWA manifest standard recommends edge-to-edge for 512, browser will crop).
    return img

def create_svg():
    svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>
    <linearGradient id="topFace" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f0f9ff"/>
    </linearGradient>
    <linearGradient id="leftFace" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e0f2fe"/>
      <stop offset="100%" stop-color="#bae6fd"/>
    </linearGradient>
    <linearGradient id="rightFace" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#bae6fd"/>
      <stop offset="100%" stop-color="#7dd3fc"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="512" height="512" rx="108" fill="url(#bgGrad)"/>
  
  <!-- Subtle Glow -->
  <circle cx="256" cy="240" r="160" fill="#ffffff" opacity="0.15" filter="url(#glow)"/>
  
  <!-- Isometric Cube -->
  <g transform="translate(0, -10)">
    <!-- Top Face -->
    <polygon points="256,150 355,207 256,264 157,207" fill="url(#topFace)"/>
    <!-- Left Face -->
    <polygon points="157,207 256,264 256,370 157,313" fill="url(#leftFace)"/>
    <!-- Right Face -->
    <polygon points="256,264 355,207 355,313 256,370" fill="url(#rightFace)"/>
    
    <!-- D-Pad symbol on top -->
    <path d="M256 182 L256 232 M231 207 L281 207" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
    
    <!-- Sparkles -->
    <path d="M355 160 Q355 180 375 180 Q355 180 355 200 Q355 180 335 180 Q355 180 355 160 Z" fill="#ffffff"/>
    <path d="M165 310 Q165 325 180 325 Q165 325 165 340 Q165 325 150 325 Q165 325 165 310 Z" fill="#ffffff" opacity="0.85"/>
  </g>
</svg>
'''
    return svg_code

if __name__ == '__main__':
    os.makedirs('icons', exist_ok=True)
    
    # Generate SVG
    with open('icons/icon.svg', 'w', encoding='utf-8') as f:
        f.write(create_svg())
    with open('icons/favicon.svg', 'w', encoding='utf-8') as f:
        f.write(create_svg())
    print("SVG icons generated.")
    
    # Generate standard PNGs
    print("Rendering 512x512 standard...")
    img512 = render_icon(512, is_maskable=False)
    img512.save('icons/icon-512.png', 'PNG')
    
    print("Rendering 192x192 standard...")
    img192 = render_icon(192, is_maskable=False)
    img192.save('icons/icon-192.png', 'PNG')
    
    print("Rendering 512x512 maskable...")
    img512_mask = render_icon(512, is_maskable=True)
    img512_mask.save('icons/icon-maskable-512.png', 'PNG')
    
    print("Rendering 192x192 maskable...")
    img192_mask = render_icon(192, is_maskable=True)
    img192_mask.save('icons/icon-maskable-192.png', 'PNG')
    
    print("Rendering 180x180 apple touch icon...")
    img_apple = render_icon(180, is_maskable=False)
    img_apple.save('icons/apple-touch-icon.png', 'PNG')
    
    # Favicon 32x32
    img32 = img192.resize((32, 32), Image.Resampling.LANCZOS)
    img32.save('icons/favicon-32x32.png', 'PNG')
    img32.save('favicon.ico', format='ICO')
    
    print("All icons generated successfully.")
