import asyncio
import time
import os
import glob
from main import ses,qb
import libtorrent as lt
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.progress import *

def get_download_text(name,status,completed,speed,total):
  text = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}/sec
"""
  total = str(total)
  completed = round(completed*100,2)
  size, forma = total.split(' ')
  if forma == "MiB":
    size = int(round(float(size)))
  elif forma == "GiB":
    size = int(round(float(size)*1024,2))

  percent = completed
  speed = round(float(speed)/1024) #kbps

  if speed > 1024:
    speed = str(round(speed/1024)) + " MB"
  else:
    speed = str(speed) + " KB"

  completed = round((percent/100)*size)

  if completed > 1024:
    completed = str(round(completed/1024,2)) + " GB"
  else:
    completed = str(completed) + " MB"

  if size > 1024:
    size = str(round(size/1024,2)) + " GB"
  else:
    size = str(size) + " MB"

  fill = "▪️"
  blank = "▫️"
  bar = ""

  bar += round(percent/10)*fill
  bar += round(((20 - len(bar))/2))*blank

  text = text.format(
    name,
    status,
    percent,
    bar,
    completed,
    size,
    speed
  )
  return text


async def downloader(message: Message, link: str,total,name):
  qb.download_from_link(link,savepath="/downloads/")
  torrent = qb.torrents()[0]

  r = message
  name = torrent["name"]
  hash = torrent["hash"]
  total = torrent["total_size"]
  downloaded = 0
  progress = round(downloaded/total,2)
    
  print(f"Downloading {str(name)}")
  await r.edit(f'Got Metadata, Starting Download Of **{str(name)}**...')

  while downloaded < total or downloaded == 0:
    total = torrent["total_size"]
    downloaded = torrent["total_downloaded"]
    speed = torrent["dl_speed"]

    try:
      text = get_download_text(
          name, 
          "Downloading", 
          progress,
          speed,
          total
        )
      await r.edit(
        text=text
      )
    except:
      pass

    await asyncio.sleep(10)
  
  return "downloads/" + name