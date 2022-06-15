import asyncio
from main.db import get_animes, save_anime
import feedparser

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
        await asyncio.sleep(1800)

        rss = parse()
        data = await get_animes()

        saved_anime = []
        for i in data:
            saved_anime.append(i["title"])

        for anime in rss: 
            if anime["title"] not in saved_anime:
                title = anime["title"]
                await save_anime(title,anime)
                print(f"Saved {title}")