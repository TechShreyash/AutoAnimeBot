import asyncio
from main.modules.thumbnail import generate_thumbnail
from main.modules.uploader import upload_video
import os
from main.modules.db import del_anime, save_uploads
from main.modules.downloader import downloader
from main.modules.anilist import get_anime_img, get_anime_name
from config import CHANNEL_ID
from main import app, queue

async def tg_handler():
    if len(queue) != 0:
        for i in queue:
            val = await start_uploading(i)
            queue.remove(i)
            await del_anime(i["title"])
            await save_uploads(i["title"])
    
    await asyncio.sleep(600)

async def start_uploading(data):
    title = data["title"]
    link = data["link"]
    size = data["size"]
    id, img, tit = await get_anime_img(get_anime_name(title))
    msg = await app.send_photo(CHANNEL_ID,photo=img,caption=title)

    file = await downloader(msg,link,size,title)
    print("Downloaded -> ",file)

    name, ext = title.split(".")
    name += " [@AniDec]." + ext
    fpath = "downloads/" + name
    os.rename(file,fpath)

    await msg.edit(f"Uploading {name}")
    print(f"Uploading {name}")
    name = title.split(".")[0]

    message_id = int(msg.id) + 1
    x = await upload_video(msg,fpath,id,tit,name,message_id,size)
    return "val"
