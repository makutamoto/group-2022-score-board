from datetime import datetime
from escpos.printer import Usb
from escpos import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from receipt import receipt

now_datetime = datetime.now()

width = 500
height = 355


font1 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 28, encoding='unic')
font2 = ImageFont.truetype('./scoreboard-fonts/DSEG14Classic-BoldItalic.ttf', 100, encoding='unic')
font3 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 50, encoding='unic')
font4 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 35, encoding='unic')
font5 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 37, encoding='unic')

p = Usb(0x0416, 0x5011, 0, 0x81, 0x07)

def score_draw(score:int):
    p.text(" ")
    p.image(receipt(score))
    p.cut()

if __name__ == '__main__':
    score_draw(100)
