from spritekit import *

STYLE_VERSION = 1
c = canvas()

# Light comes from the top-left: tone index 0 = brightest.
LX, LY = -0.6, -0.8


def tone_at(x, y, cx, cy, rx, ry, tones, bias=0.0):
    dx, dy = (x - cx) / rx, (y - cy) / ry
    t = (-(dx * LX + dy * LY) + 1) / 2 + bias
    return tones[min(len(tones) - 1, max(0, int(t * len(tones))))]


def in_ellipse(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def lit_ellipse(cx, cy, rx, ry, tones, bias=0.0, rows=None):
    for y in range(64):
        if rows and not (rows[0] <= y <= rows[1]):
            continue
        for x in range(64):
            if in_ellipse(x, y, cx, cy, rx, ry):
                px(c, x, y, tone_at(x, y, cx, cy, rx, ry, tones, bias))


# Serveware: wide, shallow blue-glazed stoneware bowl with a brown clay rim.
BX, BY = 32, 38
lit_ellipse(BX, BY, 28, 18, ['slate', 'slate', 'shadow', 'shadow', 'navy', 'navy'], rows=(BY, BY + 17))
rect(c, BX - 8, BY + 16, BX + 8, BY + 17, 'navy')                          # foot ring
lit_ellipse(BX, BY, 28, 12, ['clay', 'copper', 'copper', 'wood_dark'])    # clay rim
lit_ellipse(BX, BY, 26, 10, ['shadow', 'shadow', 'navy', 'navy'])          # glazed well (in shade)
line(c, 8, 33, 13, 29, 'cyan')                                             # glaze glint, top-left
line(c, 7, 41, 9, 46, 'cyan')

# Cherry tomatoes, blistered, peeking out around the rice.
def tomato(x, y):
    lit_ellipse(x, y, 3.6, 3, ['sauce', 'tomato', 'tomato', 'tomato_dark'])
    px(c, x - 1, y - 1, 'paper')         # glossy glint
    px(c, x - 2, y - 1, 'cream')
    px(c, x + 1, y + 1, 'tomato_dark')    # blistered wrinkle
    px(c, x + 2, y, 'tomato_dark')

for x, y in [(19, 31), (11, 38), (52, 36)]:
    tomato(x, y)

# Domed mound of white rice with a lumpy, grainy edge.
lit_ellipse(32, 41, 19, 7, ['cream', 'paper_dark', 'paper_dark', 'parchment'])    # base in shade
lit_ellipse(32, 37, 17, 9, ['paper', 'paper', 'cream', 'cream', 'paper_dark'])   # dome
for x, y in [(15, 37), (14, 40), (49, 36), (50, 39), (19, 45), (45, 45), (31, 47), (38, 47)]:
    px(c, x, y, 'paper')                                                       # stray grains
for i, (x, y) in enumerate([(18, 38), (22, 42), (27, 44), (35, 43), (41, 41), (46, 38),
                            (25, 39), (38, 39), (43, 44), (30, 41)]):
    px(c, x, y, 'paper_dark')                                                  # grain shading
    px(c, x + 1, y, 'paper' if i % 2 else 'cream')

tomato(46, 45)                            # one tumbled to the front-right


# Salmon: broad seasoned top, short pink-orange side, flaky layers.
def salmon(x0, y0, w, top_h, side_h, seed):
    for y in range(y0, y0 + top_h):
        inset = max(0, 2 - (y - y0))
        for x in range(x0 + inset, x0 + w - inset):
            px(c, x, y, tone_at(x, y, x0 + w / 2, y0 + top_h / 2, w / 2, top_h / 2,
                                ['amber', 'orange', 'orange', 'sauce', 'sauce']))
    for y in range(y0 + top_h, y0 + top_h + side_h):
        for x in range(x0 + 1, x0 + w - 1):
            px(c, x, y, tone_at(x, y, x0 + w / 2, y0 + top_h, w / 2, side_h,
                                ['orange', 'sauce', 'sauce', 'tomato_dark']))
    for k in range(x0 + 4, x0 + w - 2, 5):                    # flaky layer lines
        px(c, k, y0 + top_h, 'parchment')
        px(c, k - 1, y0 + top_h + 1, 'parchment')
    # Lemon pepper: cracked pepper and golden zest on the crust.
    speckle(c, (x0 + 2, y0 + 1, x0 + w - 3, y0 + top_h - 1), ['plum_shadow', 'gold', 'moss'],
            density=0.16, seed=seed)
    line(c, x0 + 2, y0, x0 + w // 2, y0, 'amber_glow')         # rim light along the top edge
    px(c, x0 + 1, y0 + 1, 'amber_glow')
    # Round off the bottom corners so it reads as a fillet, not a block.
    for dx, dy in [(1, -1), (2, -1), (1, -2), (w - 2, -1), (w - 3, -1), (w - 2, -2)]:
        px(c, x0 + dx, y0 + top_h + side_h + dy, 'cream')
    for dx in (0, w - 1):
        px(c, x0 + dx, y0 + top_h - 1, 'cream')


salmon(27, 20, 22, 10, 4, 11)             # big fillet on top of the rice
salmon(14, 34, 13, 6, 3, 7)               # smaller piece, front-left
rect(c, 27, 35, 28, 36, 'sauce')          # a loose flake
px(c, 27, 35, 'orange')
