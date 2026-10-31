"""Minimal PIL line charts for round 3. No extra packages."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font():
    for p in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(p, 12)
        except Exception:
            continue
    return ImageFont.load_default()


def line_chart(path: Path, series: list[tuple[str, list[tuple[int, float]]]], title: str, w=900, h=420):
    """series: (label, [(x_index, y), ...]) with x_index 0..n-1 or any comparable ints."""
    img = Image.new("RGB", (w, h), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    font = _font()
    pad_l, pad_r, pad_t, pad_b = 55, 16, 36, 36
    pts = [p for _, s in series for p in s]
    if not pts:
        dr.text((10, 10), title + " (empty)", fill=(0, 0, 0), font=font)
        img.save(path)
        return
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    if xmax <= xmin:
        xmax = xmin + 1
    if ymax <= ymin:
        ymax = ymin + 1e-6
    def sx(x):
        return pad_l + (x - xmin) / (xmax - xmin) * (w - pad_l - pad_r)
    def sy(y):
        return pad_t + (ymax - y) / (ymax - ymin) * (h - pad_t - pad_b)
    dr.rectangle([pad_l, pad_t, w - pad_r, h - pad_b], outline=(0, 0, 0))
    dr.text((pad_l, 8), title, fill=(0, 0, 0), font=font)
    pal = [(180, 40, 40), (40, 80, 180), (30, 130, 70), (140, 90, 20), (90, 40, 140)]
    for i, (lab, s) in enumerate(series):
        if len(s) < 2:
            continue
        col = pal[i % len(pal)]
        xy = [(sx(x), sy(y)) for x, y in s]
        dr.line(xy, fill=col, width=2)
        dr.text((pad_l + 8, pad_t + 8 + 14 * i), lab, fill=col, font=font)
    dr.text((pad_l, h - 22), f"{xmin} → {xmax}", fill=(80, 80, 80), font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def three_panel(path: Path, panels: list[tuple[str, list[tuple[str, list[tuple[int, float]]]]]], w=900, h=780):
    img = Image.new("RGB", (w, h), (255, 255, 255))
    ph = h // max(len(panels), 1)
    font = _font()
    pal = [(180, 40, 40), (40, 80, 180), (30, 130, 70)]
    for pi, (title, series) in enumerate(panels):
        y0 = pi * ph
        dr = ImageDraw.Draw(img)
        pad_l, pad_r, pad_t, pad_b = 50, 12, 28, 20
        box = (pad_l, y0 + pad_t, w - pad_r, y0 + ph - pad_b)
        dr.rectangle(box, outline=(0, 0, 0))
        dr.text((pad_l, y0 + 6), title, fill=(0, 0, 0), font=font)
        pts = [p for _, s in series for p in s]
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        if xmax <= xmin:
            xmax = xmin + 1
        if ymax <= ymin:
            ymax = ymin + 1e-6
        def sx(x):
            return box[0] + (x - xmin) / (xmax - xmin) * (box[2] - box[0])
        def sy(y):
            return box[1] + (ymax - y) / (ymax - ymin) * (box[3] - box[1])
        for i, (lab, s) in enumerate(series):
            if len(s) < 2:
                continue
            col = pal[i % len(pal)]
            dr.line([(sx(x), sy(y)) for x, y in s], fill=col, width=2)
            dr.text((pad_l + 6, y0 + pad_t + 4 + 12 * i), lab, fill=col, font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
