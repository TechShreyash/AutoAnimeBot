import asyncio
from main.modules.db import del_anime, save_uploads
from main.modules.downloader import downloader
from main.modules.anilist import get_anime_img
from config import CHANNEL_ID
from main import app, queue

async def tg_handler():
    while True:
        await asyncio.sleep(60)
        if len(queue) != 0:
            for i in queue:
                val = await start_uploading(i)
                queue.remove(i)
                await del_anime(i["title"])
                await save_uploads(i["title"])

        await asyncio.sleep(1800)


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