from __future__ import annotations

import random
from pathlib import Path
from typing import Tuple, Union

from PIL import Image

PALETTE_PATH = Path(__file__).resolve().parent.parent / 'style' / 'palette.hex'
PALETTE = {}
for line in PALETTE_PATH.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split()
    if len(parts) >= 2:
        name, hex_value = parts[0], parts[1]
        hex_value = hex_value.lstrip('#')
        PALETTE[name] = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4)) + (255,)


def palette_color(name: str):
    if name not in PALETTE:
        raise ValueError(f'Unknown color: {name}')
    return PALETTE[name]


class Canvas:
    def __init__(self, width: int = 64, height: int = 64):
        self.width = width
        self.height = height
        self.img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    def set_pixel(self, x: int, y: int, color: Union[str, Tuple[int, int, int, int], None]):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        if color is None:
            self.img.putpixel((x, y), (0, 0, 0, 0))
            return
        if isinstance(color, str):
            color = palette_color(color)
        self.img.putpixel((x, y), color)

    def get_pixel(self, x: int, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return (0, 0, 0, 0)
        return self.img.getpixel((x, y))


def canvas():
    return Canvas()


def px(c, x, y, color):
    c.set_pixel(x, y, color)


def rect(c, x0, y0, x1, y1, color):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.set_pixel(x, y, color)


def line(c, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        c.set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def ellipse(c, cx, cy, rx, ry, color, fill=True):
    for y in range(c.height):
        for x in range(c.width):
            dx = (x - cx) / rx if rx else 0
            dy = (y - cy) / ry if ry else 0
            if dx * dx + dy * dy <= 1:
                c.set_pixel(x, y, color)


def poly(c, points, color):
    from PIL import ImageDraw
    mask = Image.new('L', (c.width, c.height), 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    for y in range(c.height):
        for x in range(c.width):
            if mask.getpixel((x, y)) > 0:
                c.set_pixel(x, y, color)


def fill(c, x, y, color):
    target = c.get_pixel(x, y)
    stack = [(x, y)]
    while stack:
        xx, yy = stack.pop()
        if xx < 0 or xx >= c.width or yy < 0 or yy >= c.height:
            continue
        if c.get_pixel(xx, yy) != target:
            continue
        c.set_pixel(xx, yy, color)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            stack.append((xx + dx, yy + dy))


def shade(c, region=None, light=None, dark=None, region_mask=None):
    if region is None and region_mask is None:
        return
    if region is not None:
        target = palette_color(region)
        for y in range(c.height):
            for x in range(c.width):
                px = c.get_pixel(x, y)
                if px[3] == 0:
                    continue
                if px[:3] == target[:3]:
                    if x + y < (c.width + c.height) * 0.9:
                        c.img.putpixel((x, y), palette_color(light)[:3] + (255,))
                    else:
                        c.img.putpixel((x, y), palette_color(dark)[:3] + (255,))
        return
    if region_mask is not None:
        mask = region_mask
        for y in range(c.height):
            for x in range(c.width):
                if mask[x, y]:
                    c.img.putpixel((x, y), palette_color(light)[:3] + (255,))


def speckle(c, box, colors, density=0.1, seed=0):
    if isinstance(box, dict):
        x0, y0, x1, y1 = box['x0'], box['y0'], box['x1'], box['y1']
    elif isinstance(box, tuple) and len(box) == 4:
        x0, y0, x1, y1 = box
    else:
        x0, y0, x1, y1 = 0, 0, c.width, c.height
    rng = random.Random(seed)
    palette_colors = [palette_color(name) for name in colors]
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if rng.random() < density:
                c.set_pixel(x, y, palette_colors[rng.randrange(len(palette_colors))])


def grid(rows, key):
    return {'rows': rows, 'key': key}


def plate(c):
    ellipse(c, 32, 54, 22, 7, 'wood')
    ellipse(c, 32, 54, 19, 5, 'wood_light')
    return (18, 42, 46, 62)


def bowl(c):
    ellipse(c, 32, 53, 18, 6, 'wood_dark')
    ellipse(c, 32, 53, 15, 4, 'wood_light')
    return (20, 43, 44, 58)


def board(c):
    rect(c, 12, 42, 52, 60, 'wood')
    rect(c, 14, 44, 50, 58, 'wood_light')
    line(c, 15, 44, 50, 44, 'wood_dark')
    return (16, 43, 48, 58)


def pan(c):
    ellipse(c, 32, 54, 20, 6, 'copper')
    ellipse(c, 32, 54, 17, 4, 'amber_dark')
    rect(c, 50, 51, 56, 56, 'amber_dark')
    return (18, 44, 46, 58)


def glass(c):
    rect(c, 28, 33, 36, 52, 'slate')
    ellipse(c, 32, 36, 8, 7, 'slate')
    ellipse(c, 32, 42, 10, 10, 'cyan')
    return (24, 36, 40, 50)


__all__ = ['canvas', 'px', 'rect', 'line', 'ellipse', 'poly', 'fill', 'plate', 'bowl', 'board', 'pan', 'glass', 'shade', 'speckle', 'grid', 'palette_color']
