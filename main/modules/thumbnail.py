import cv2, random
from string import ascii_uppercase, hexdigits
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup as bs
from .cv2_utils import get_screenshot

file = "./a.mkv"

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""
    pos = 0    
    for i in list:
        if len(text1) + len(i) < 25 and pos == 0:        
            text1 += " " + i
        elif len(text2) + len(i) < 25:
            pos = 1       
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return text1,text2

def get_cover(id):
    url = "https://anilist.co/anime/" + str(id)

    r = requests.get(url).content
    soup = bs(r,"html.parser")

    img = soup.find("img","cover")
    img = img.get("src")

    r = requests.get(img).content

    fname = "./" + "".join(random.choices(ascii_uppercase + hexdigits,k = 10)) + ".jpg"
    with open(fname,"wb") as file:
        file = file.write(r)

    return fname

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def generate_thumbnail(id,file,title,ep_num,size,dur):
    print(id,file,title,ep_num,size,dur)
    ss = get_screenshot(file)
    cc = get_cover(id)

    border = make_col()
    image = Image.open(ss)
    image = image.convert("RGBA")
    image = changeImageSize(1280,720,image)

    cover = Image.open(cc)
    cover = cover.convert("RGBA")
    w, h = cover.size
    w = round((w*720)/h)
    cover = changeImageSize(w,720,cover)

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
    font1 = ImageFont.truetype('downloads/Roboto-Bold.ttf', 65)
    font2 = ImageFont.truetype('downloads/Oswald-Regular.ttf', 60)
    font3 = ImageFont.truetype('downloads/Raleway-Bold.ttf', 35)

    image3 = ImageDraw.Draw(image2)

    image3.text((((1280-w)/2)-70,100),"AniDec",make_col(),font2)

    text1, text2 = truncate(title)
    image3.text((60,250),text1,"white",font1)
    if text2 != "":
        image3.text((60,330),text2,"white",font1)

    image3.text((60,430),f"Episode : {ep_num}","white",font3)
    image3.text((60,490),f"File Size : {size}","white",font3)
    image3.text((60,550),f"Duration : {dur}","white",font3)

    image2.thumbnail((320,320))
    w,h = image2.size

    thumb = "./" + "".join(random.choices(ascii_uppercase + hexdigits,k = 10)) + ".jpg"
    image2.save(thumb)
    return thumb, w, h