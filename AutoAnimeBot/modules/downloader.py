import os
import shutil
from pyrogram.types import Message
from AutoAnimeBot.core.log import LOGGER
from AutoAnimeBot.modules.progress import progress_text
import time
import aiohttp
import aiofiles

logger = LOGGER("Downloader")


async def downloader(message: Message, l, title, file_name):
    logger.info(f"Downloading {title}")
    try:
        shutil.rmtree("downloads")
    except:
        pass

    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    file_name = f"downloads/{file_name}"

    t1 = time.time()
    dcount = 1  # Downloaded count in 10 sec

    try:
        t_out = aiohttp.ClientTimeout(
            total=7200.0, connect=7200.0, sock_read=7200.0, sock_connect=7200.0
        )
        async with aiohttp.ClientSession(timeout=t_out) as session:
            async with session.get(l) as response:
                if response.content_length:
                    total = response.content_length / 1024
                else:
                    total = 1

                done = 1
                async with aiofiles.open(file_name, "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        await f.write(data)
                        done += 1

                        t2 = time.time()
                        if t2 - t1 > 10:
                            try:
                                t1 = t2
                                text = progress_text(
                                    "Downloading", title, done, total, dcount
                                )
                                await message.edit_caption(text)
                                dcount = done
                            except Exception as e:
                                logger.warning(str(e))
    except Exception as e:
        logger.warning(str(e))
    logger.info(f"Downloaded {title}")
    return file_name
