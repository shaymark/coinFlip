from PIL import Image, ImageDraw, ImageFilter
import os, math

def make_icon(size, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if maskable:
        # Full bleed dark background, coin at 80% safe zone
        d.rectangle([0, 0, size, size], fill=(15, 23, 42, 255))
        coin_r = int(size * 0.40)
    else:
        coin_r = int(size * 0.48)

    cx, cy = size // 2, size // 2

    # Outer ring (darker)
    d.ellipse([cx - coin_r, cy - coin_r, cx + coin_r, cy + coin_r],
              fill=(180, 83, 9, 255))

    # Inner gradient coin
    inner_r = int(coin_r * 0.92)
    steps = 60
    # Light source offset for shine (top-left)
    ox, oy = -coin_r * 0.3, -coin_r * 0.3
    for i in range(inner_r, 0, -1):
        t = i / inner_r
        # Radial gradient from light gold at center-offset to darker gold at edge
        # Base: #fbbf24 center, #b45309 edge, with highlight at offset
        r_col = int(251 * t + 180 * (1 - t))
        g_col = int(191 * t + 83 * (1 - t))
        b_col = int(36 * t + 9 * (1 - t))
        d.ellipse([cx + ox * (1-t) - i, cy + oy * (1-t) - i,
                   cx + ox * (1-t) + i, cy + oy * (1-t) + i],
                  fill=(r_col, g_col, b_col, 255))

    # Highlight spot (top-left shine)
    hl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hlr = int(coin_r * 0.35)
    hlx, hly = int(cx - coin_r * 0.35), int(cy - coin_r * 0.35)
    hd.ellipse([hlx - hlr, hly - hlr, hlx + hlr, hly + hlr],
               fill=(255, 255, 255, 90))
    hl = hl.filter(ImageFilter.GaussianBlur(radius=coin_r * 0.18))
    img = Image.alpha_composite(img, hl)
    d = ImageDraw.Draw(img)

    # Draw a crown shape in the center (geometric)
    cr = int(coin_r * 0.55)
    crown_color = (124, 45, 18, 255)

    # Crown base rectangle
    base_h = int(cr * 0.28)
    base_top = cy + int(cr * 0.25)
    d.rectangle([cx - cr, base_top, cx + cr, base_top + base_h],
                fill=crown_color)

    # Crown spikes (3 triangles + 2 side)
    spike_top = cy - int(cr * 0.55)
    spike_base = base_top
    # Center spike
    d.polygon([
        (cx, spike_top),
        (cx - int(cr * 0.28), spike_base),
        (cx + int(cr * 0.28), spike_base),
    ], fill=crown_color)
    # Left spike
    d.polygon([
        (cx - int(cr * 0.7), spike_top + int(cr * 0.15)),
        (cx - cr, spike_base),
        (cx - int(cr * 0.4), spike_base),
    ], fill=crown_color)
    # Right spike
    d.polygon([
        (cx + int(cr * 0.7), spike_top + int(cr * 0.15)),
        (cx + int(cr * 0.4), spike_base),
        (cx + cr, spike_base),
    ], fill=crown_color)

    # Gem dots on spike tips
    gem_r = max(2, int(cr * 0.08))
    for gx, gy in [(cx, spike_top),
                   (cx - int(cr * 0.7), spike_top + int(cr * 0.15)),
                   (cx + int(cr * 0.7), spike_top + int(cr * 0.15))]:
        d.ellipse([gx - gem_r, gy - gem_r, gx + gem_r, gy + gem_r],
                  fill=(254, 243, 199, 255))

    img.save(path, "PNG")
    print(f"wrote {path}")

os.makedirs("icons", exist_ok=True)
make_icon(192, "icons/icon-192.png")
make_icon(512, "icons/icon-512.png")
make_icon(512, "icons/icon-maskable-512.png", maskable=True)
make_icon(180, "icons/apple-touch-icon.png")
make_icon(32, "icons/favicon-32.png")
