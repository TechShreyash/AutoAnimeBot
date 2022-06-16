import asyncio
import time
import os
import glob
from main import ses
import libtorrent as lt
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.progress import *
from main.modules.parser import *

def get_download_text(name,status,completed,speed,total):
  text = """Name: {}
{}: {}%
[▪️▫️▫️▫️▫️▫️▫️▫️▫️▫️]
{} MB of {} MB
Speed: {}/sec
"""

  text = text.format(
    name,
    status,
    round(((completed/total)*100),2),
    completed,
    total,
    speed
  )
  return text


async def downloader(message: Message, link: str,total):
  params = {
  'save_path': './downloads/',
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
          trgt, 
          str(state_str[s.state]).capitalize(), 
          round(s.progress * 100, 2),
          round(s.download_rate / 1000, 1),
          total
        )
      await r.edit(
        text=text
      )
    except:
      pass

    await asyncio.sleep(5)
  
  return "./downloads/" + trgt