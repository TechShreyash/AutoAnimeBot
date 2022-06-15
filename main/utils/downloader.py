import asyncio
import time
import os
import glob
from main import ses
import libtorrent as lt
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from main.utils.progress import *
from main.utils.parser import *

def get_download_text(name,status,completed,speed):
  return


async def downloader(message: Message, link: str):
  params = {
  'save_path': './downloads',
  'storage_mode': lt.storage_mode_t(2),}

  handle = lt.add_magnet_uri(ses, link, params)
  ses.start_dht()

  r = message
  await r.edit('Downloading Metadata...')
    
  while (not handle.has_metadata()):
    
    await asyncio.sleep(1)
    
  await r.edit(f'Got Metadata, Starting Download Of **{str(handle.name())}**...')

  trgt = str(handle.name())

  while (handle.status().state != lt.torrent_status.seeding):
    
    s = handle.status()
    
    state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
    
    try:
      
      await r.edit(
        text=get_download_text(
          trgt, 
          str(state_str[s.state]).capitalize(), 
          round(s.progress * 100, 2),
          round(s.download_rate / 1000, 1)
        )
      )
    except:
      pass
  
  return "./downloads/" + trgt