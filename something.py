import os, math, random
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H

# ====== SỬA Ở ĐÂY ======
girl_name   = "Em"
date_line   = "Tối 24/12"
time_line   = "19:00"
place_line  = "Hẹn: (điểm đón / quán cà phê)"
plan_line   = "Đi: (địa điểm bí mật 😉)"
dress_code  = "Dress code: đỏ / trắng / ấm áp"
qr_url      = "https://maps.google.com/?q=Ho+Chi+Minh+City"  # link bất ngờ
out_gif     = "thiep_noel_animated.gif"
# =======================

W, H = 1080, 1920
FPS = 20
SECONDS = 6
N_FRAMES = FPS * SECONDS
DURATION_MS = int(1000 / FPS)

title = f"{girl_name} ơi, đi chơi Noel với anh nhé?"
subtitle = "Scan QR để mở bất ngờ"

# Font trên Windows (có tiếng Việt)
def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\seguiemj.ttf",   # emoji (nếu có)
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    path = None
    for p in candidates:
        if os.path.exists(p):
            path = p
            break
    if not path:
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)

f_title = load_font(64)
f_body  = load_font(46)
f_small = load_font(36)
f_tiny  = load_font(30)

# QR
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
qr.add_data(qr_url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
qr_size = 430
qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)

def draw_centered(draw, text, y, font, fill=(245,245,245), maxw=960, spacing=12):
    lines = []
    for part in text.split("\n"):
        if not part.strip():
            lines.append("")
            continue
        # wrap thô theo ký tự
        w = 28
        chunk = []
        cur = ""
        for word in part.split(" "):
            if len((cur + " " + word).strip()) <= w:
                cur = (cur + " " + word).strip()
            else:
                chunk.append(cur)
                cur = word
        if cur: chunk.append(cur)
        lines += chunk

    yy = y
    for line in lines:
        box = draw.textbbox((0,0), line if line else " ", font=font)
        tw = box[2]-box[0]
        x = (W - tw)//2
        draw.text((x, yy), line, font=font, fill=fill)
        yy += (box[3]-box[1]) + spacing

def heart_shape(draw, x, y, s, color):
    # trái tim: 2 vòng tròn + tam giác
    r = s // 3
    draw.ellipse([x, y, x + 2*r, y + 2*r], fill=color)
    draw.ellipse([x + 2*r, y, x + 4*r, y + 2*r], fill=color)
    draw.polygon([(x, y + r), (x + 4*r, y + r), (x + 2*r, y + 4*r)], fill=color)

def draw_tree(draw, base_x, base_y, scale=1.0):
    # Cây thông 3 tầng + thân + đồ trang trí
    def tri(cx, cy, w, h, fill):
        draw.polygon([(cx, cy), (cx - w//2, cy + h), (cx + w//2, cy + h)], fill=fill)

    green1 = (22, 110, 70)
    green2 = (18, 90, 58)
    trunk  = (110, 70, 40)

    w1, h1 = int(520*scale), int(320*scale)
    w2, h2 = int(420*scale), int(280*scale)
    w3, h3 = int(320*scale), int(240*scale)

    tri(base_x, base_y - h1 - h2 - h3 + 40, w3, h3, green2)
    tri(base_x, base_y - h1 - h2 + 20, w2, h2, green1)
    tri(base_x, base_y - h1, w1, h1, green2)

    # thân cây
    tw, th = int(120*scale), int(140*scale)
    draw.rounded_rectangle([base_x - tw//2, base_y, base_x + tw//2, base_y + th], radius=18, fill=trunk)

    # sao trên đỉnh
    star_y = base_y - h1 - h2 - h3 + 20
    star = [(base_x, star_y),
            (base_x+22, star_y+58),
            (base_x-40, star_y+22),
            (base_x+40, star_y+22),
            (base_x-22, star_y+58)]
    draw.polygon(star, fill=(255, 220, 90))

    # đồ trang trí ngẫu nhiên
    colors = [(230,60,70), (255,255,255), (255,200,70), (120,200,255)]
    for _ in range(22):
        ox = base_x + random.randint(-240, 240)
        oy = base_y - random.randint(120, 760)
        rr = random.randint(10, 18)
        c = random.choice(colors)
        draw.ellipse([ox-rr, oy-rr, ox+rr, oy+rr], fill=c)

# particles
random.seed(7)
hearts = []
for _ in range(18):
    hearts.append({
        "x": random.randint(60, W-60),
        "y": random.randint(int(H*0.6), H+400),
        "v": random.uniform(2.2, 4.6),
        "amp": random.uniform(10, 40),
        "ph": random.uniform(0, math.tau),
        "s": random.randint(42, 78)
    })

snow = []
for _ in range(120):
    snow.append({
        "x": random.randint(0, W),
        "y": random.randint(0, H),
        "v": random.uniform(1.0, 3.2),
        "r": random.randint(1, 3)
    })

frames = []
for i in range(N_FRAMES):
    # nền gradient
    img = Image.new("RGBA", (W, H), (10, 24, 18, 255))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y/(H-1)
        r = int(10 + 18*t); g = int(24 + 30*t); b = int(18 + 22*t)
        d.line([(0,y),(W,y)], fill=(r,g,b,255))

    # tuyết
    for fl in snow:
        fl["y"] += fl["v"]
        fl["x"] += math.sin((i/18)+fl["x"]/150)*0.6
        if fl["y"] > H+10:
            fl["y"] = -10
            fl["x"] = random.randint(0, W)
        d.ellipse([fl["x"]-fl["r"], fl["y"]-fl["r"], fl["x"]+fl["r"], fl["y"]+fl["r"]], fill=(255,255,255,180))

    # cây thông
    draw_tree(d, base_x=W//2, base_y=H-360, scale=1.0)

    # tim bay bay
    for h in hearts:
        h["y"] -= h["v"]
        xw = h["x"] + math.sin(i/12 + h["ph"]) * h["amp"]
        if h["y"] < -200:
            h["y"] = H + random.randint(100, 500)
            h["x"] = random.randint(60, W-60)
        heart_shape(d, int(xw - h["s"]//2), int(h["y"]), h["s"], (255, 80, 110, 200))

    # text
    draw_centered(d, title, 130, f_title, fill=(252,252,252))
    body = f"{date_line} • {time_line}\n{place_line}\n{plan_line}\n{dress_code}"
    draw_centered(d, body, 460, f_body, fill=(240,240,240))

    # QR (card trắng)
    qr_x = (W - qr_size)//2
    qr_y = 1260
    pad = 22
    d.rounded_rectangle([qr_x-pad, qr_y-pad, qr_x+qr_size+pad, qr_y+qr_size+pad],
                        radius=26, fill=(250,250,250,255))
    img.alpha_composite(qr_img, (qr_x, qr_y))
    draw_centered(d, subtitle, qr_y + qr_size + 60, f_small, fill=(245,245,245))

    footer = "Gợi ý: QR có thể mở Maps / playlist / album ảnh / lời mời."
    draw_centered(d, footer, H-120, f_tiny, fill=(210,210,210), maxw=980, spacing=8)

    frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE))

# lưu GIF
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION_MS,
    loop=0,
    disposal=2
)

print("OK:", out_gif)
