import asyncio
from main.start import start_tg_handler
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue

def trim_title(title: str):
    title, ext = title.replace("[SubsPlease]","").strip().split("[",maxsplit=2)
    _, ext = ext.split("]",maxsplit=2)
    title = title.strip() + ext
    return title

def parse():
    a = feedparser.parse("https://subsplease.org/rss/")
    b = a["entries"]

    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['size'] = i['subsplease_size']
        item['link'] = i['link']
        data.append(item)

    data.reverse()
    return data

async def auto_parser():
    while True:

        rss = parse()
        data = await get_animesdb()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        for anime in rss: 
            if anime["title"] not in saved_anime:
                title = anime["title"]
                await save_animedb(title,anime)
                print(f"Saved {title}")

        data = await get_animesdb()
        uploaded = await get_uploads()

        for i in data:
            if i["name"] in uploaded:
                data.remove(i)

        for i in data:
            queue.append(i["data"])

        start_tg_handler()
        
        await asyncio.sleep(1800)