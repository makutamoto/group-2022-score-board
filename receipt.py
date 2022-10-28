from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


width = 377
height = 390

font1 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 28, encoding='unic')
font2 = ImageFont.truetype('./scoreboard-fonts/DSEG14Classic-BoldItalic.ttf', 100, encoding='unic')
font3 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 50, encoding='unic')
font4 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 35, encoding='unic')
font5 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 37, encoding='unic')
font6 = ImageFont.truetype('./scoreboard-fonts/PixelMplus12-Bold.ttf', 18, encoding='unic')

def receipt(score:int):
    now_datetime = datetime.now()
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), f"{now_datetime.strftime('%Y/%m/%d %H:%M')}", font=font1, fill=0)
    draw.text((0, 30), "Basket-Shooter", font=font5, fill=0)
    draw.text((0, 100), f"{score}", font=font2, fill=0)
    draw.text((300, 195), "point", font=font1, fill=0)
    draw.text((0, 225), "- - - - キリトリ線 - - - -", font=font1, fill=0)
    draw.text((0, 255), "5E たこ焼き", font=font3, fill=0)
    draw.text((125, 315), "ねぎ・明太マヨ", font=font4, fill=0)
    draw.text((171, 350), "50円割引き！", font=font4, fill=0)
    return image

if __name__ == '__main__':
    receipt(100).save('receipt.png')
