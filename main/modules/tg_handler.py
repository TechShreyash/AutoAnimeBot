from main.modules.downloader import downloader
from main.modules.anilist import get_anime_img
from config import CHANNEL_ID
from main.modules.db import get_animes, get_uploads
from main import app

async def tg_handler():
    data = await get_animes()
    uploaded = await get_uploads()

    for i in data:
        if i in uploaded:
            data.remove(i)

    for i in data:
        val = await start_uploading(i["link"])


def get_anime_name(title):
    x = title.split("-")[-1]
    title = title.replace(x,"").strip()
    return title

async def start_uploading(data):
    title = data["title"]
    link = data["link"]
    size = data["size"]
    img = await get_anime_img(get_anime_name(title))
    msg = await app.send_photo(CHANNEL_ID,photo=img,caption=title)

    file = await downloader(msg,link,size)
    print(file)
    return "val"