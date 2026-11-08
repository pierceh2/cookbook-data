from spritekit import *

STYLE_VERSION = 1
c = canvas()
plate(c)
ellipse(c, 32, 38, 18, 11, 'wood_light')
ellipse(c, 32, 28, 16, 11, 'cream')
shade(c, region='cream', light='cream', dark='navy')
line(c, 22, 20, 25, 13, 'wood')
line(c, 39, 20, 42, 13, 'wood')
rect(c, 25, 21, 39, 22, 'wood_dark')
line(c, 29, 22, 31, 28, 'paper')
line(c, 34, 22, 36, 28, 'paper')
rect(c, 28, 26, 36, 30, 'paper')
