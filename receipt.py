from datetime import datetime
from escpos.printer import Usb
from escpos import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

now_datetime = datetime.now()

width = 500
height = 355


font1 = ImageFont.truetype('PixelMplus12-Bold.ttf', 28, encoding='unic')
font2 = ImageFont.truetype('DSEG14Classic-BoldItalic.ttf', 100, encoding='unic')
font3 = ImageFont.truetype('PixelMplus12-Bold.ttf', 50, encoding='unic')
font4 = ImageFont.truetype('PixelMplus12-Bold.ttf', 35, encoding='unic')
font5 = ImageFont.truetype('PixelMplus12-Bold.ttf', 37, encoding='unic')

p = Usb(0x0416, 0x5011, 0, 0x81, 0x07)

def score_draw(score:int):

    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), f"{now_datetime.strftime('%Y/%m/%d %H:%M')}", font=font1, fill=0)
    draw.text((0, 30), "Basket-Shooter", font=font5, fill=0)
    draw.text((0, 100), f"{score}", font=font2, fill=0)
    draw.text((300, 195), "point", font=font1, fill=0)
    draw.text((0, 225), "- - - - - - - - - - - - - - -", font=font1, fill=0)
    draw.text((0, 255), "5E たこ焼き", font=font3, fill=0)
    draw.text((0, 315), "トッピング無料", font=font4, fill=0)
    draw.rectangle((285, 255, 377, 347), width=3)
              
    
    p.text("!")
    p.image(image)
    p.cut()

    return 1

if __name__ == '__main__':
    score_draw(100)
