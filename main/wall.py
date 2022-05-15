from main import WALL_API, UNSPLASH_API, session
from typing import Optional
import aiohttp, random

async def get_wallpapers(query: str):  
  try:
    url = WALL_API + query  
    resp = await session.get(url)
    json = await resp.json()
    images = json["images"]
    random.shuffle(images)
  except Exception as e:
    return "error" + str(e)      
  return images