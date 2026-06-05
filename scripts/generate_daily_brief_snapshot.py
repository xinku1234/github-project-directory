#!/usr/bin/env python3
"""Generate the daily-brief share snapshot PNG from data/github-rising.json.

This intentionally does not use a browser screenshot so GitHub Actions can update
`assets/daily-brief-share.png` deterministically every day after the rising data
sync.
"""
from __future__ import annotations

import json
import math
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "github-rising.json"
OUT = ROOT / "assets" / "daily-brief-share.png"
BASE = "daohang.bot.cd"

FONT_CANDIDATES = [
    "/usr/share/fonts/google-droid/DroidSansFallback.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
]
BOLD_CANDIDATES = [
    "/usr/share/fonts/google-droid/DroidSansFallback.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
]


def font(size: int, bold: bool = False) -> Any:
    candidates = BOLD_CANDIDATES if bold else FONT_CANDIDATES
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def esc_text(value: object) -> str:
    return str(value or "").replace("\n", " ").strip()


def wrap_cn(text: str, width: int) -> list[str]:
    text = esc_text(text)
    if len(text) <= width:
        return [text]
    # Mixed Chinese/English: textwrap is fine for English runs; CJK can break by char.
    lines: list[str] = []
    for para in textwrap.wrap(text, width=width, break_long_words=True, replace_whitespace=False):
        lines.append(para)
    return lines or [text[:width]]


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_gradient_bg(img: Image.Image) -> None:
    pix = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            nx = x / w
            ny = y / h
            # Deep navy -> purple/teal glow.
            r = int(9 + 35 * ny + 36 * math.exp(-((nx - 0.12) ** 2 + (ny - 0.18) ** 2) / 0.05))
            g = int(17 + 24 * ny + 80 * math.exp(-((nx - 0.82) ** 2 + (ny - 0.12) ** 2) / 0.04))
            b = int(38 + 65 * ny + 70 * math.exp(-((nx - 0.55) ** 2 + (ny - 0.78) ** 2) / 0.08))
            pix[x, y] = (min(r, 115), min(g, 150), min(b, 190))


def main() -> int:
    data = json.loads(DATA.read_text("utf-8"))
    projects = (data.get("projects") or [])[:10]
    synced = data.get("synced_at") or datetime.now(timezone.utc).isoformat()
    date_label = synced[:10]

    W, H = 1200, 1600
    img = Image.new("RGB", (W, H), (9, 17, 38))
    draw_gradient_bg(img)
    d = ImageDraw.Draw(img)

    # Soft grid / glow accents.
    for x in range(80, W, 120):
        d.line((x, 0, x, H), fill=(255, 255, 255, 12), width=1)
    for y in range(80, H, 120):
        d.line((0, y, W, y), fill=(255, 255, 255, 10), width=1)
    d.ellipse((-220, -180, 440, 360), fill=(32, 211, 238))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-250, -210, 470, 390), fill=(45, 212, 255, 34))
    od.ellipse((760, 40, 1380, 620), fill=(168, 85, 247, 42))
    od.ellipse((250, 1120, 980, 1800), fill=(16, 185, 129, 28))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    f_brand = font(32, True)
    f_title = font(68, True)
    f_sub = font(30)
    f_date = font(26)
    f_rank = font(31, True)
    f_name = font(30, True)
    f_desc = font(23)
    f_meta = font(21)
    f_footer = font(26, True)

    # Header.
    d.text((70, 58), "拾品号导航", font=f_brand, fill=(224, 242, 254))
    rounded(d, (250, 56, 476, 102), 23, fill=(14, 165, 233), outline=(125, 211, 252))
    d.text((274, 65), "每日分享快照", font=font(24, True), fill=(255, 255, 255))
    d.text((70, 136), "GitHub 每日增速 Top10", font=f_title, fill=(255, 255, 255))
    d.text((74, 226), "每天发现值得收藏的开源项目 · 适合转发/收藏/选题", font=f_sub, fill=(191, 219, 254))
    d.text((74, 276), f"{date_label} · {BASE}/daily-brief/", font=f_date, fill=(167, 243, 208))

    # Cards.
    y = 350
    card_h = 103
    gap = 14
    for idx, p in enumerate(projects, 1):
        x0, y0, x1, y1 = 70, y, 1130, y + card_h
        fill = (15, 23, 42)
        outline = (77, 120, 174) if idx <= 3 else (51, 65, 85)
        rounded(d, (x0, y0, x1, y1), 24, fill=fill, outline=outline, width=2 if idx <= 3 else 1)
        rank_fill = (250, 204, 21) if idx == 1 else ((56, 189, 248) if idx <= 3 else (71, 85, 105))
        rounded(d, (x0 + 18, y0 + 22, x0 + 92, y0 + 78), 18, fill=rank_fill)
        d.text((x0 + 33, y0 + 32), f"#{idx}", font=f_rank, fill=(15, 23, 42) if idx == 1 else (255, 255, 255))

        name = esc_text(p.get("name"))[:34]
        desc = esc_text(p.get("desc_cn") or p.get("desc"))
        desc_lines = wrap_cn(desc, 47)[:1]
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day") or 0
        stars = int(p.get("stars") or 0)
        d.text((x0 + 116, y0 + 18), name, font=f_name, fill=(248, 250, 252))
        d.text((x0 + 116, y0 + 58), desc_lines[0], font=f_desc, fill=(203, 213, 225))
        # Keep the share poster readable at thumbnail size; detailed language/category
        # remain on the HTML daily-brief page.
        meta = f"↗ {round(float(spd), 2)} 星/天   ★ {stars:,}"
        d.text((x1 - 34, y0 + 32), meta, font=f_meta, fill=(125, 211, 252), anchor="ra")
        y += card_h + gap

    # Footer.
    footer_y = 1505
    d.line((70, footer_y - 24, 1130, footer_y - 24), fill=(148, 163, 184), width=1)
    d.text((70, footer_y), "完整榜单 / 项目导航 / 免费提交：daohang.bot.cd", font=f_footer, fill=(255, 255, 255))
    d.text((878, footer_y), "拾品号导航", font=f_footer, fill=(167, 243, 208))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"generated {OUT} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
