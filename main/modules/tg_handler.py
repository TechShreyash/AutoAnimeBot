import asyncio
from pyrogram.types import Message
from main.modules.thumbnail import generate_thumbnail
from main.modules.uploader import upload_video
import os
from main.modules.db import del_anime, save_channel, save_uploads
from main.modules.downloader import downloader
from main.modules.anilist import get_anime_img, get_anime_name
from config import CHANNEL_ID
from main import app, queue, status

status: Message
async def tg_handler():
    while True:
        if len(queue) != 0:
            for i in queue:
                val, tit = await start_uploading(i)
                queue.remove(i)
                await del_anime(i["title"])
                await save_uploads(i["title"])

                if val != "err":
                    await channel_handler(val,tit)
                await status.edit("Sleeping...")
                await asyncio.sleep(300)
    
        os.system("rm -r downloads/*")
        
        if status.text != "Idle...":
            await status.edit("Idle...")
        await asyncio.sleep(1800)

async def start_uploading(data):
    title = data["title"]
    link = data["link"]
    size = data["size"]

    name, ext = title.split(".")
    name += " [@AniDec]." + ext
    fpath = "downloads/" + name

    id, img, tit = await get_anime_img(get_anime_name(title))
    msg = await app.send_photo(CHANNEL_ID,photo=img,caption=title)

    await status.edit(f"Downloading {name}")
    file = await downloader(msg,link,size,title)
    
    if not os.path.isfile(file):
        print(file)
        os.system("ls downloads")
        await msg.delete()        
        return "err", tit

    print("Downloaded -> ",file)
    await msg.edit(f"Download Complete : {name}")
    
    os.rename(file,fpath)

    await status.edit(f"Uploading {name}")    
    print(f"Uploading {name}")
    name = title.split(".")[0]

    message_id = int(msg.id) + 1
    x = await upload_video(msg,fpath,id,tit,name,message_id,size)
    return message_id, tit


async def channel_handler(msg_id,val):
    return