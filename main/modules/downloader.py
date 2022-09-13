from genericpath import exists
import os
import shutil
from pyrogram.types import Message
from main.modules.utils import download_progress, get_progress_text
import requests, time
import aiohttp, aiofiles, asyncio



async def downloader(message: Message, link, header, filename, total_size, title):
    try:
        os.remove('downloads/video.mp4')
    except:
        pass
    try:
        shutil.rmtree('downloads/ts_files')
    except:
        pass
    try:
        os.mkdir('downloads/ts_files')
    except:
        pass
    m3u8 = requests.get(link, headers=header).text
    m3u8 = m3u8.splitlines()
    urls = []
    for url in m3u8:
        if url.startswith('http'):
            urls.append(url)
    total = len(urls)

    text_file = await aiofiles.open('downloads/files_list.txt', mode='w')
    file_text = '' 
    if True:
        current = 0
        start = time.time()
        downloaded = 0
        async with aiohttp.ClientSession() as session:
            for url in urls:
                async with session.get(url,headers=header) as resp:
                    current +=1
                    ts = await aiofiles.open(f'downloads/ts_files/file{current}.ts', mode='wb')
                    await ts.write(await resp.read())
                    file_text += f"file 'ts_files/file{current}.ts'\n"

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
                await asyncio.sleep(0.2)
        await text_file.write(file_text)
        await text_file.close()
    return 'downloads/files_list.txt'
