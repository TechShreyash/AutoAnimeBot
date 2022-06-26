import asyncio

from main import status
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
        await status.edit("Status : Parsing Rss, Fetching Magnet Links...")

        rss = parse()
        data = await get_animesdb()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        for anime in rss: 
            if anime["title"] not in saved_anime:
                title = anime["title"]
                await save_animedb(title,anime)

        data = await get_animesdb()
        uploaded = await get_uploads()
        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])

        for i in data:
            if i["name"] in uanimes:
                data.remove(i)

        for i in data:
            if ".mkv" in i["name"] or ".mp4" in i["name"]:
                queue.append(i["data"])

        await asyncio.sleep(1800)
