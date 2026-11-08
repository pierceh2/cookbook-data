from spritekit import *

STYLE_VERSION = 1
c = canvas()
plate(c)

ellipse(c, 32, 38, 18, 8, 'crust')
ellipse(c, 32, 30, 18, 8, 'crust')
ellipse(c, 32, 22, 18, 8, 'crust')
shade(c, region='crust', light='amber_glow', dark='navy')

ellipse(c, 32, 31, 8, 3, 'cheese')
rect(c, 26, 34, 29, 44, 'sauce')
rect(c, 35, 34, 38, 44, 'sauce')
shade(c, region='sauce', light='cream', dark='wine')

line(c, 26, 36, 27, 38, 'cream')
line(c, 35, 36, 36, 38, 'cream')

for y in range(0, 64):
    for x in range(0, 64):
        if c.get_pixel(x, y)[3] == 0:
            continue
        if x + y < 50 and c.get_pixel(x, y)[:3] == palette_color('crust')[:3]:
            c.img.putpixel((x, y), (242, 208, 140, 255))
        if x + y > 75 and c.get_pixel(x, y)[:3] == palette_color('crust')[:3]:
            c.img.putpixel((x, y), (66, 86, 120, 255))

line(c, 21, 16, 18, 10, 'cream')
line(c, 23, 15, 20, 9, 'cream')
line(c, 41, 16, 44, 10, 'cream')
line(c, 39, 15, 42, 9, 'cream')
