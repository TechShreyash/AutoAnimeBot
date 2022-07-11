import asyncio
from config import CHANNEL_TITLE
import os
import random, cv2
from string import ascii_uppercase, digits
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup as bs
from .utils import get_screenshot

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""
    pos = 0    
    for i in list:
        if len(text1) + len(i) < 16 and pos == 0:        
            text1 += " " + i
        elif len(text2) + len(i) < 16:
            pos = 1       
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return text1,text2

err = 0

async def get_cover(id):
    global err
    
    try:
        url = "https://anilist.co/anime/" + str(id)

        r = requests.get(url).content
        soup = bs(r,"html.parser")

        img = soup.find("img","cover")
        img = img.get("src")

        r = requests.get(img).content

        fname = "./" + "".join(random.choices(ascii_uppercase + digits,k = 10)) + ".jpg"
        with open(fname,"wb") as file:
            file = file.write(r)

        err = 0
        return fname
    except:
        await asyncio.sleep(2)

        err += 1
        if err != 5:
            return await get_cover(id)
        else:
            err = 0
            return "assets/c4UUTC4DAe.jpg"

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_thumbnail(id,file,title,ep_num,size,dur):
    ss = get_screenshot(file)
    cc = await get_cover(id)

    border = make_col()
    image = Image.open(ss)
    image = image.convert("RGBA")
    image = image.resize((1280,720))

    cover = Image.open(cc)
    cover = cover.convert("RGBA")
    w, h = cover.size
    w = round((w*720)/h)
    cover = cover.resize((w,720))

    original = cover
    xy = [(50,0),(0,720),(w,720),(w,0)]
    mask = Image.new("L", original.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(xy, fill=255, outline=None)
    black =  Image.new("RGBA", original.size, 0)
    result = Image.composite(original, black, mask)
    cover = result

    image2 = image.filter(filter=ImageFilter.GaussianBlur(10))
    black = Image.new("RGB",(1280,720),"black").convert("RGBA")
    image2 = Image.blend(image2,black,0.5)

    image2.paste(cover,(1280-w,0),cover)
    image2 = image2.convert("RGB")

    image2 = ImageOps.expand(image2,20,border)
    image2 = image2.resize((1280,720))

    ldraw = ImageDraw.Draw(image2)
    line = [((1280-w)+50,0),((1280-w)+0,720)]
    ldraw.line(line,border,20)
    # fonts
    font1 = ImageFont.truetype('assets/Roboto-Bold.ttf', 70)
    font2 = ImageFont.truetype('assets/Oswald-Regular.ttf', 80)
    font3 = ImageFont.truetype('assets/Raleway-Bold.ttf', 50)

    image3 = ImageDraw.Draw(image2)

    image3.text((150,80),f"{CHANNEL_TITLE}","white",font2,stroke_width=5,stroke_fill="black")

    text1, text2 = truncate(title)
    image3.text((60,230),text1,"white",font1,stroke_width=5,stroke_fill="black")
    if text2 != "":
        image3.text((60,310),text2,"white",font1,stroke_width=5,stroke_fill="black")

    image3.text((60,420),f"Episode : {ep_num}","white",font3,stroke_width=2,stroke_fill="black")
    image3.text((60,500),f"File Size : {size}","white",font3,stroke_width=2,stroke_fill="black")
    image3.text((60,580),f"Duration : {dur}","white",font3,stroke_width=2,stroke_fill="black")

    image2.thumbnail((1280,720))
    w,h = image2.size

    thumb = "./" + "".join(random.choices(ascii_uppercase + digits,k = 10)) + ".jpg"
    image2.save(thumb)
    
    try:
        os.remove(ss)
        if cc != "assets/c4UUTC4DAe.jpg":
            os.remove(cc)
    except:
        pass
    return thumb, w, h