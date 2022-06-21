import asyncio
import time
import os
import glob
from main import ses
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
  params = {
  'save_path': 'downloads/',
  'storage_mode': lt.storage_mode_t(2),}

  handle = lt.add_magnet_uri(ses, link, params)
  ses.start_dht()

  r = message
  await r.edit('Downloading Metadata...')
    
  while (not handle.has_metadata()):
    
    await asyncio.sleep(1)
    
  print(f"Downloading {str(handle.name())}")
  await r.edit(f'Got Metadata, Starting Download Of **{str(handle.name())}**...')

  trgt = str(handle.name())

  while (handle.status().state != lt.torrent_status.seeding):
    
    s = handle.status()
    
    state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
    
    try:
      text = get_download_text(
          name, 
          str(state_str[s.state]).capitalize(), 
          s.progress,
          s.download_rate,
          total
        )
      await r.edit(
        text=text
      )
    except:
      pass

    await asyncio.sleep(10)
  
  return "downloads/" + trgt
