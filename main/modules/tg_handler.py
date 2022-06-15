from config import CHANNEL_ID
from main.modules.db import get_animes, get_uploads
from main import app

procs = []

async def tg_handler():
    data = await get_animes()
    uploaded = await get_uploads()

    for i in data:
        if i in uploaded:
            data.remove(i)

    for i in data:
        if i not in procs:
            procs.append(i)
            val = await start_uploading(i["link"])



async def start_uploading(link):
    msg = await app.send_photo(CHANNEL_ID,)
    return "val"