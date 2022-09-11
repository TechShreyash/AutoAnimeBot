from pyrogram.types import Message
from main.modules.utils import download_progress, get_progress_text
import requests, time
import aiohttp, aiofiles

async def downloader(message: Message, link, header, filename, total_size, title):
    m3u8 = requests.get(link, headers=header).text
    m3u8 = m3u8.splitlines()
    urls = []
    for url in m3u8:
        if url.startswith('http'):
            urls.append(url)
    total = len(urls)

    file = await aiofiles.open(filename, mode='wb') 
    if True:
        current = 0
        start = time.time()
        downloaded = 0
        with aiohttp.ClientSession() as session:
            for url in urls:
                async with session.get(url,headers=header) as resp:
                    current +=1
                    await file.write(await resp.read())

                    passed = time.time()
                    x = (passed-start)>10
                    if x: # will edit message in iff atleast 10 seconds have passed and 5 chunks are downloaded
                        start = passed
                        try:
                            text, downloaded = download_progress(
                                title,
                                current,
                                total,
                                total_size,
                                downloaded
                            )
                            await message.edit(
                                text=text
                            )
                        except:
                            pass
        await file.close()
    return filename