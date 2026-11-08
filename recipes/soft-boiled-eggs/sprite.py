from spritekit import *

STYLE_VERSION = 1
c = canvas()

# Light comes from the top-left: tone index 0 = brightest.
LX, LY = -0.6, -0.8


def lit_ellipse(cx, cy, rx, ry, tones, bias=0.0, skip=None):
    """Ellipse shaded in bands from top-left (tones[0]) to bottom-right (tones[-1])."""
    for y in range(64):
        for x in range(64):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            if dx * dx + dy * dy > 1 or (skip and skip(x, y)):
                continue
            light = -(dx * LX + dy * LY)  # -1 lit .. +1 shadow
            t = (light + 1) / 2 + bias
            i = min(len(tones) - 1, max(0, int(t * len(tones))))
            px(c, x, y, tones[i])


def inside(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


# Serveware: earthenware plate with a warm rim and a cool shadow side.
lit_ellipse(32, 53, 26, 8, ['clay', 'clay', 'clay', 'copper', 'wood_dark'])
lit_ellipse(32, 52, 22, 6, ['wood_light', 'wood_light', 'wood_light', 'wood'])
line(c, 12, 51, 20, 48, 'amber')  # candle rim light, top-left


def egg_half(cx, cy, w, h):
    # Rounded white underside, a step darker than the cut face so the two read apart.
    lit_ellipse(cx, cy + 3, w, h + 2, ['cream', 'parchment', 'paper_dark', 'paper_dark', 'slate'])
    # Flat cut face of the white: bright, catching the candlelight.
    face = inside(cx, cy, w - 1, h)
    lit_ellipse(cx, cy, w - 1, h, ['paper', 'paper', 'paper', 'paper', 'cream'])
    # Lip along the front edge of the face.
    for x in range(cx - w, cx + w + 1):
        for y in range(cy, cy + h + 2):
            if face(x, y) and not face(x, y + 1):
                px(c, x, y, 'parchment')
                break
    # Big runny yolk filling most of the face, with a soft lobe toward the back.
    ycx, ycy = cx - 1, cy
    tones = ['amber_glow', 'amber', 'orange', 'orange', 'amber_dark']
    lit_ellipse(ycx, ycy, int(w * 0.6), h - 2, tones)
    lit_ellipse(ycx - 3, ycy - 2, 4, 2, tones, bias=-0.15)
    # Drip spilling over the front lip and down the side.
    for x, y in [(ycx + 2, ycy + h - 2), (ycx + 2, ycy + h - 1), (ycx + 3, ycy + h),
                 (ycx + 3, ycy + h + 1), (ycx + 3, ycy + h + 2), (ycx + 3, ycy + h + 3)]:
        px(c, x, y, 'orange')
        px(c, x + 1, y, 'amber_dark')
    px(c, ycx + 2, ycy + h, 'amber_glow')
    px(c, ycx + 3, ycy + h + 4, 'amber_dark')
    px(c, ycx + 4, ycy + h + 4, 'amber_dark')
    # Glossy glints, top-left.
    gx, gy = ycx - int(w * 0.3), ycy - h // 2 + 1
    for x, y in [(gx, gy), (gx + 1, gy), (gx, gy + 1)]:
        px(c, x, y, 'paper')
    px(c, gx + 4, gy - 1, 'cream')
    # Cracked black pepper.
    for x, y in [(ycx + 2, ycy - 2), (ycx + 4, ycy + 1), (ycx - 3, ycy + 2), (cx - w + 3, cy + 1)]:
        px(c, x, y, 'plum_shadow')


egg_half(23, 30, 12, 7)   # back half
egg_half(38, 41, 14, 8)   # front half, overlapping

# Cool shadow pooled on the plate right of the front egg.
for x, y in [(53, 49), (54, 49), (53, 50), (54, 50), (55, 50), (52, 51), (53, 51)]:
    px(c, x, y, 'wood')

# A few salt flakes on the plate.
for x, y in [(13, 53), (18, 56), (27, 57), (49, 56), (44, 58)]:
    px(c, x, y, 'paper')
