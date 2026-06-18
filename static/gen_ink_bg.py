#!/usr/bin/env python3
"""
凌霄剑域 · 水墨山水背景生成器
Procedural Chinese Ink Wash Painting Background
Output: 1920x1080 PNG
"""
import math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

W, H = 1920, 1080
random.seed(42)

# ===== 色板 =====
C_VOID    = (11, 16, 24)       # #0b1018 深蓝黑
C_DEEP    = (17, 24, 39)       # #111827
C_MID     = (31, 41, 55)       # #1f2937
C_GRAY    = (55, 65, 81)       # #374151
C_PAPER   = (214, 211, 209)    # #d6d3d1
C_BRIGHT  = (231, 229, 228)    # #e7e5e4
C_GOLD_D  = (176, 141, 87)     # #b08d57
C_GOLD    = (201, 166, 107)    # #c9a66b
C_INK     = (8, 12, 18)        # 焦墨

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def make_noise_layer(w, h, scale=1.0, opacity=0.15, color=(20,18,14)):
    """生成噪声纹理层（宣纸纤维感）"""
    img = Image.new('RGB', (w, h), (0,0,0))
    px = img.load()
    for y in range(h):
        for x in range(w):
            n = random.random()
            v = int(n * 255 * opacity)
            px[x,y] = (color[0]*v//255, color[1]*v//255, color[2]*v//255)
    return img.filter(ImageFilter.GaussianBlur(radius=0.5))

def draw_rice_paper(base):
    """宣纸纹理：多层细噪声 + 微黄底色"""
    # 底色渐变
    grad = Image.new('RGB', (W, H), C_VOID)
    px = grad.load()
    for y in range(H):
        t = y / H
        c = lerp_color(C_VOID, C_DEEP, t * 0.6)
        for x in range(W):
            xt = x / W
            # 中心稍亮
            cx = 1.0 - abs(xt - 0.5) * 0.8
            cy = 1.0 - abs(y/H - 0.4) * 0.6
            bright = cx * cy
            c2 = lerp_color(c, C_MID, bright * 0.15)
            px[x,y] = c2
    
    # 纤维噪声层
    for i in range(3):
        noise = make_noise_layer(W//2, H//2, opacity=0.08)
        noise = noise.resize((W, H), Image.BILINEAR)
        base.paste(ImageChops.screen(grad, noise), (0,0))
    
    return base

def draw_mountain_layer(draw, base_y, amplitude, color, blur=0, seed_offset=0):
    """画一层远山"""
    random.seed(42 + seed_offset)
    points = []
    num_peaks = random.randint(5, 9)
    
    # 生成山脊线
    x = -50
    points.append((x, H))
    points.append((x, base_y))
    
    while x < W + 50:
        # 山峰
        peak_h = base_y - random.uniform(amplitude * 0.3, amplitude)
        peak_w = random.uniform(80, 200)
        points.append((x + peak_w * 0.3, peak_h))
        points.append((x + peak_w * 0.5, peak_h - random.uniform(0, amplitude*0.15)))
        points.append((x + peak_w * 0.7, peak_h + random.uniform(0, amplitude*0.2)))
        # 山谷
        valley_y = base_y + random.uniform(amplitude * 0.1, amplitude * 0.3)
        points.append((x + peak_w, valley_y))
        x += peak_w
    
    points.append((W + 50, base_y))
    points.append((W + 50, H))
    
    # 画填充
    draw.polygon(points, fill=color)
    return points

def draw_mountains(img):
    """6-8层远山叠嶂"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    layers = [
        # (base_y, amplitude, color, blur, seed)
        (550, 120, (*C_GRAY, 60), 8, 1),    # 最远：淡灰
        (600, 140, (*C_MID, 80), 6, 2),
        (650, 160, (*C_DEEP, 100), 5, 3),
        (700, 180, (*C_VOID, 130), 4, 4),
        (750, 200, (*C_INK, 160), 3, 5),
        (800, 220, (*C_INK, 200), 2, 6),    # 最近：浓墨
    ]
    
    for base_y, amp, color, blur, seed in layers:
        layer = Image.new('RGBA', (W, H), (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        draw_mountain_layer(ld, base_y, amp, color, blur, seed)
        if blur > 0:
            layer = layer.filter(ImageFilter.GaussianBlur(radius=blur))
        overlay = Image.alpha_composite(overlay, layer)
    
    # 山间雾气
    for i in range(4):
        mist_y = 500 + i * 80
        mist = Image.new('RGBA', (W, 60), (*C_DEEP, 15))
        mist = mist.filter(ImageFilter.GaussianBlur(radius=20))
        overlay.paste(mist, (0, mist_y), mist)
    
    return overlay

def draw_ink_wash(img):
    """水墨晕染：墨滴在宣纸上化开"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    
    washes = [
        (200, 150, 350, 200, 40),   # 左上
        (1400, 200, 400, 250, 35),  # 右上
        (800, 400, 500, 300, 30),   # 中
        (150, 650, 300, 180, 35),   # 左下
        (1300, 600, 350, 200, 40),  # 右下
    ]
    
    for cx, cy, rx, ry, opacity in washes:
        wash = Image.new('RGBA', (W, H), (0,0,0,0))
        draw = ImageDraw.Draw(wash)
        # 多层椭圆模拟墨晕
        for i in range(8):
            t = i / 8
            r = 1.0 - t * 0.3
            a = int(opacity * (1.0 - t) * 0.4)
            color = (*C_MID, a)
            draw.ellipse([
                cx - rx*r, cy - ry*r,
                cx + rx*r, cy + ry*r
            ], fill=color)
        # 模糊化开
        wash = wash.filter(ImageFilter.GaussianBlur(radius=40))
        overlay = Image.alpha_composite(overlay, wash)
    
    return overlay

def draw_cloud(draw, cx, cy, scale=1.0, color=(214,211,209,25)):
    """画一朵祥云"""
    s = scale
    # 云芯螺旋
    for i in range(5):
        r = (15 - i*2) * s
        if r < 2: continue
        a = color[3] + i * 3
        draw.ellipse([
            cx - r, cy - r,
            cx + r, cy + r
        ], fill=(*color[:3], min(a, 40)))
    
    # 云尾 —— 流动的弧线
    tails = [
        [(cx, cy), (cx - 60*s, cy - 15*s), (cx - 120*s, cy - 5*s)],
        [(cx, cy), (cx + 50*s, cy - 20*s), (cx + 110*s, cy - 10*s)],
        [(cx, cy), (cx - 30*s, cy + 25*s), (cx - 80*s, cy + 35*s)],
        [(cx, cy), (cx + 40*s, cy + 20*s), (cx + 90*s, cy + 30*s)],
    ]
    for tail in tails:
        for i in range(len(tail)-1):
            draw.line([tail[i], tail[i+1]], fill=color, width=max(1, int(3*s)))

def draw_clouds(img):
    """四角祥云"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    clouds = [
        (180, 120, 1.2),    # 左上
        (1650, 150, 1.0),   # 右上
        (150, 850, 1.1),    # 左下
        (1700, 800, 1.3),   # 右下
        (900, 80, 0.8),     # 顶部中
    ]
    
    for cx, cy, s in clouds:
        draw_cloud(draw, cx, cy, s, (*C_PAPER, 20))
    
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=3))
    return overlay

def draw_gold_particles(img):
    """金粉流光"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # 金粉粒子
    for _ in range(80):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.uniform(0.5, 2.0)
        a = random.randint(30, 80)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(*C_GOLD, a))
    
    # 金色流光线
    for _ in range(6):
        x1 = random.randint(0, W)
        y1 = random.randint(100, H-100)
        x2 = x1 + random.randint(-200, 200)
        y2 = y1 + random.randint(-50, 50)
        draw.line([(x1,y1),(x2,y2)], fill=(*C_GOLD_D, 15), width=1)
    
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    return overlay

def draw_mist(img):
    """薄雾层"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    
    for i in range(5):
        y = 400 + i * 80 + random.randint(-20, 20)
        h = random.randint(40, 80)
        mist = Image.new('RGBA', (W, h), (*C_DEEP, random.randint(8, 20)))
        mist = mist.filter(ImageFilter.GaussianBlur(radius=25))
        overlay.paste(mist, (0, y), mist)
    
    return overlay

def draw_birds(img):
    """远飞孤鸟"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    birds = [
        (600, 200), (650, 190), (700, 210),  # 一组
        (1200, 150), (1240, 165),              # 一组
        (400, 300),                             # 孤鸟
    ]
    
    for bx, by in birds:
        s = 8
        # 简笔飞鸟：两条弧线
        draw.arc([bx-s, by-s//2, bx, by+s//2], 200, 360, fill=(*C_PAPER, 40), width=1)
        draw.arc([bx, by-s//2, bx+s, by+s//2], 180, 340, fill=(*C_PAPER, 40), width=1)
    
    return overlay

def draw_vignette(img):
    """暗角"""
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # 四角渐暗
    for i in range(60):
        a = int(80 * (1 - i/60))
        margin = i * 3
        draw.rectangle([
            margin, margin, W-margin, H-margin
        ], outline=(0,0,0,0))
    
    # 用径向渐变模拟暗角
    vignette = Image.new('L', (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    cx, cy = W//2, H//2
    max_r = math.sqrt(cx**2 + cy**2)
    px = vignette.load()
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            d = math.sqrt((x-cx)**2 + (y-cy)**2)
            t = d / max_r
            v = int(120 * t**2)
            for dy in range(4):
                for dx in range(4):
                    if x+dx < W and y+dy < H:
                        px[x+dx, y+dy] = v
    
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=30))
    black = Image.new('RGBA', (W, H), (0,0,0,255))
    overlay = Image.composite(black, Image.new('RGBA',(W,H),(0,0,0,0)), vignette)
    return overlay

def main():
    print("生成水墨山水背景...")
    
    # 1. 宣纸底色
    base = Image.new('RGB', (W, H), C_VOID)
    base = draw_rice_paper(base)
    base = base.convert('RGBA')
    
    # 2. 水墨晕染
    print("  ✓ 水墨晕染")
    base = Image.alpha_composite(base, draw_ink_wash(base))
    
    # 3. 远山叠嶂
    print("  ✓ 远山叠嶂")
    base = Image.alpha_composite(base, draw_mountains(base))
    
    # 4. 薄雾
    print("  ✓ 薄雾层")
    base = Image.alpha_composite(base, draw_mist(base))
    
    # 5. 祥云
    print("  ✓ 祥云")
    base = Image.alpha_composite(base, draw_clouds(base))
    
    # 6. 金粉
    print("  ✓ 金粉流光")
    base = Image.alpha_composite(base, draw_gold_particles(base))
    
    # 7. 飞鸟
    print("  ✓ 远飞孤鸟")
    base = Image.alpha_composite(base, draw_birds(base))
    
    # 8. 暗角
    print("  ✓ 暗角")
    base = Image.alpha_composite(base, draw_vignette(base))
    
    # 9. 整体微调
    base = ImageEnhance.Contrast(base).enhance(0.95)
    base = ImageEnhance.Color(base).enhance(0.85)
    
    # 保存
    out_path = os.path.join(os.path.dirname(__file__), 'ink-bg.png')
    base.convert('RGB').save(out_path, 'PNG', quality=95)
    print(f"✓ 完成: {out_path} ({W}x{H})")
    
    # 同时存一份到 screenshots
    return out_path

if __name__ == '__main__':
    main()
