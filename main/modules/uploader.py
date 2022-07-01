import asyncio
from main.modules.cv2_utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator
from main.modules.anilist import get_anime_name
from main.modules.anilist import get_anime_img
from main.modules.thumbnail import generate_thumbnail
from config import CHANNEL_ID
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from main.modules.progress import progress_for_pyrogram
from os.path import isfile
import os
import time
from main import app, status
from pyrogram.errors import FloodWait

async def upload_video(msg: Message,file,id,tit,name,message_id,ttl):
    try:
    
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            thumbnail,w,h = generate_thumbnail(id,file,tit,ep_num,size,format_time(duration))
            tags = tags_generator(tit)
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Info", url="https://t.me/Anime_Dex"),
                    InlineKeyboardButton(text="Comments", url=f"https://t.me/+4nUo4jBR-JgxMTVl")
                ]
            ])
            caption = f"🎥 **{name}**\n\n{tags}"
            x = await app.send_video(
                CHANNEL_ID,
            file,
            caption=caption,
            duration=duration,
            width=w,
            height=h,
            thumb=thumbnail,
            reply_markup=buttons,
            file_name=os.path.basename(file),
            progress=progress_for_pyrogram,
            progress_args=(
                os.path.basename(file),
                r,
                c_time,
                ttl
            )
            )        
        try:
            await r.delete()
            os.remove(file)
        except:
            pass
    except FloodWait as e:
        flood_time = int(e.x)
        try:
            await status.edit(await status_text(f"Status : Floodwait... Sleeping For {flood_time} Seconds"))
        except:
            pass
        await asyncio.sleep(flood_time)
    return x.message_id