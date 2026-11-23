from spritekit import *

STYLE_VERSION = 1
c = canvas()

# Light comes from the top-left: tone index 0 = brightest.
LX, LY = -0.6, -0.8


def lit_ellipse(cx, cy, rx, ry, tones, bias=0.0):
    """Ellipse shaded in bands from top-left (tones[0]) to bottom-right (tones[-1])."""
    for y in range(64):
        for x in range(64):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            if dx * dx + dy * dy > 1:
                continue
            t = (-(dx * LX + dy * LY) + 1) / 2 + bias
            i = min(len(tones) - 1, max(0, int(t * len(tones))))
            px(c, x, y, tones[i])


def in_ellipse(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


# Serveware: wide blue-glazed stoneware plate with a brown clay rim.
lit_ellipse(31, 47, 28, 12, ['copper', 'clay', 'copper', 'wood_dark'])
lit_ellipse(31, 47, 26, 10, ['slate', 'slate', 'shadow', 'shadow', 'navy'])
lit_ellipse(31, 48, 21, 7, ['shadow', 'shadow', 'navy'])
line(c, 9, 43, 17, 38, 'cyan')  # glaze glint, top-left

# Bowl: rounded blue-glazed body sitting toward the back right.
BX, BY = 39, 27
for y in range(BY, BY + 16):
    for x in range(64):
        if in_ellipse(x, y, BX, BY, 17, 15):
            dx, dy = (x - BX) / 17, (y - BY) / 15
            t = (-(dx * LX + dy * LY) + 1) / 2
            tone = ['slate', 'slate', 'shadow', 'shadow', 'navy', 'navy'][min(5, int(t * 6))]
            px(c, x, y, tone)
rect(c, BX - 5, BY + 14, BX + 5, BY + 15, 'navy')       # foot ring
lit_ellipse(BX, BY, 17, 7, ['clay', 'copper', 'copper', 'wood_dark'])   # clay rim
lit_ellipse(BX, BY, 15, 6, ['amber_glow', 'gold', 'gold', 'amber'], bias=-0.05)  # clear golden broth
line(c, 24, 30, 26, 35, 'cyan')   # glaze glint, top-left
line(c, 25, 30, 25, 31, 'paper')

# Soup chunks: a few big, readable pieces with broth showing between them.
for x, y in [(30, 24), (41, 22), (36, 28), (46, 27)]:                 # chicken
    rect(c, x, y, x + 4, y + 2, 'parchment')
    rect(c, x, y, x + 2, y, 'paper')
    rect(c, x + 2, y + 2, x + 4, y + 2, 'crust')
    px(c, x + 4, y + 1, 'tomato')                                     # chili-powder dusting
    px(c, x + 1, y + 1, 'plum_shadow')                                # black pepper
for x, y in [(36, 22), (43, 30)]:                                     # carrot
    rect(c, x, y, x + 3, y + 2, 'orange')
    rect(c, x, y, x + 1, y, 'amber_glow')
    rect(c, x + 2, y + 2, x + 3, y + 2, 'amber_dark')
for x, y in [(47, 23), (30, 28)]:                                     # tomato
    rect(c, x, y, x + 2, y + 2, 'tomato')
    px(c, x, y, 'sauce')
    rect(c, x + 1, y + 2, x + 2, y + 2, 'tomato_dark')
for x, y in [(41, 26), (51, 28)]:                                     # celery
    rect(c, x, y, x + 2, y + 1, 'moss')
    rect(c, x, y + 1, x + 2, y + 1, 'leaf')
for x, y in [(34, 26), (39, 31), (27, 27)]:                           # ditalini
    rect(c, x, y, x + 1, y, 'cream')
    px(c, x + 1, y + 1, 'paper_dark')
for x, y in [(26, 25), (27, 24), (28, 24)]:                           # broth glints
    px(c, x, y, 'paper')

# Oyster crackers piled on the plate, front-left: back of the pile first.
CRACKER = [
    '.oooo.',
    'ohhccd',
    'ohcccd',
    '.dddd.',
]
TONE = {'o': 'crust_dark', 'h': 'cheese', 'c': 'crust', 'd': 'crust_dark'}
for cx, cy in [(10, 41), (16, 40), (22, 43), (7, 46), (13, 45), (19, 47), (25, 49),
               (10, 51), (16, 52), (22, 54), (29, 54)]:
    for j, row in enumerate(CRACKER):
        for i, ch in enumerate(row):
            if ch != '.':
                px(c, cx + i, cy + j, TONE[ch])
    px(c, cx + 3, cy + 2, 'crust_dark')   # docking hole
