import asyncio
from main.modules.cv2_utils import episode_linker, get_epnum
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.uploader import upload_video
import os
from main.modules.db import del_anime, get_channel, save_channel, save_uploads
from main.modules.downloader import downloader
from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name
from config import CHANNEL_ID, MAIN
from main import app, queue, status
from pyrogram.errors import FloodWait

status: Message
async def tg_handler():
    while True:
        try:
            if len(queue) != 0:
                i = queue[0]                
                val, id, name, ep_num, video = await start_uploading(i)
                queue.remove(i)
                await del_anime(i["title"])
                await save_uploads(i["title"])
                if val != "err":
                    await status.edit("Status : Adding Links To Main Channel...")
                    await channel_handler(val,id,name,ep_num, video)
                await status.edit("Status : Sleeping...")
                await asyncio.sleep(60)
            else:        
                os.system("rm -r downloads/*")
                
                if status.text != "Status : Idle...":
                    await status.edit("Status : Idle...")
                await asyncio.sleep(120)
        except FloodWait as e:
            flood_time = int(e.x)
            try:
                await status.edit(f"Status : Floodwait... Sleeping For {flood_time} Seconds")
            except:
                pass
            await asyncio.sleep(flood_time)
            

async def start_uploading(data):
    try:
        title = data["title"]
        link = data["link"]
        size = data["size"]

        name, ext = title.split(".")
        name += " [@AniDec]." + ext
        fpath = "downloads/" + name

        id, img, tit = await get_anime_img(get_anime_name(title))
        msg = await app.send_photo(CHANNEL_ID,photo=img,caption=title)

        await status.edit(f"Status : Downloading {name}")
        file = await downloader(msg,link,size,title)
        
        if not os.path.isfile(file):
            print("path error ", file)
            os.system("ls downloads")
            await msg.delete()
            await app.send_message("Tech_Shreyash",f"error check\n\n{file}")        
            return "err", tit, 1,1,1

        print("Downloaded -> ",file)
        await msg.edit(f"Download Complete : {name}")
        
        os.rename(file,fpath)

        await status.edit(f"Status : Uploading {name}")    
        print(f"Uploading {name}")
        name = title.split(".")[0]

        message_id = int(msg.message_id) + 1
        video = await upload_video(msg,fpath,id,tit,name,message_id,size)

        name = name.replace(" [@AniDec].","").replace(ext,"").strip()
    except FloodWait as e:
        flood_time = int(e.x)
        try:
            await status.edit(f"Status : Floodwait... Sleeping For {flood_time} Seconds")
        except:
            pass
        await asyncio.sleep(flood_time)
    return message_id, id, tit, name, video

VOTE_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👍", callback_data="vote1"),
            InlineKeyboardButton(text="♥️", callback_data="vote2"),
            InlineKeyboardButton(text="👎", callback_data="vote3")
        ]
    ]
)

EPITEXT = """
🔰 **Episodes :**

{}
"""
async def channel_handler(msg_id,id,name,ep_num,video):
    try:
        anilist = await get_channel(id)

        if anilist == 0:
            img, caption = await get_anilist_data(name)
            main = await app.send_photo(MAIN,photo=img,caption=caption,reply_markup=VOTE_MARKUP)

            link = f"[{ep_num}](https://t.me/AniDec/{video})"
            dl = await app.send_message(
                MAIN,
                EPITEXT.format(link)
            )

            await app.send_sticker(MAIN,"CAACAgUAAx0CXbNEVgABATemYrg6dYZGimb4zx9Q1DAAARzJ_M_NAAI6BQAC7s_BVQFFcU052MmMHgQ")
            dl_id = dl.message_id
            caption += f"\n📥 **Download -** [{name}](https://t.me/Anime_Dex/{dl_id})"
            await main.edit_caption(caption,reply_markup=VOTE_MARKUP)
            dl_id = int(dl_id)
            # db
            await save_channel(id,dl_id)
        else:
            dl_id = await get_channel(id)
            dl_id = int(dl_id)
            
            dl_msg = await app.get_messages(MAIN,dl_id)
            text = dl_msg.text
            text += f"\n{ep_num}"

            ent = episode_linker(dl_msg.text,dl_msg.entities,ep_num,f"https://t.me/AniDec/{video}")            
            
            await app.edit_message_text(MAIN,dl_id,text,entities=ent,disable_web_page_preview=True)

        main_id = dl_id
        buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Info", url=f"https://t.me/Anime_Dex/{main_id}"),
                    InlineKeyboardButton(text="Comments", url=f"https://t.me/Anime_Dex/{main_id}?thread={main_id}")
                ]
            ])
        await app.edit_message_reply_markup(CHANNEL_ID,video,reply_markup=buttons)

    except FloodWait as e:
        flood_time = int(e.x)
        try:
            await status.edit(f"Status : Floodwait... Sleeping For {flood_time} Seconds")
        except:
            pass
        await asyncio.sleep(flood_time)
    return
