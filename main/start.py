import asyncio
from main.modules.tg_handler import tg_handler


async def start_tg_handler():
  asyncio.create_task(tg_handler())
  return