from main.modules.tg_handler import get_anime_name
from main.modules.anilist import get_anime_img
from main.modules.thumbnail import generate_thumbnail
from config import CHANNEL_ID
from pyrogram.types import Message
from main.modules.progress import progress_for_pyrogram
from os.path import isfile
import os
import time
from main import app

async def upload_video(msg: Message,file,id,tit):
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time(os.path.basename(file))

            thumbnail = generate_thumbnail(id,file,tit)

            caption = f"🎥 {}"
            x = await app.send_video(
                CHANNEL_ID,
            file,
            caption=os.path.basename(file),
            progress=progress_for_pyrogram,
            progress_args=(
                os.path.basename(file),
                r,
                c_time
            )
            )        
        try:
            await r.delete()
            os.remove(file)
        except:
            pass
    except Exception as e:
        print(e)
    return