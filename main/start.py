import asyncio
from main.modules.tg_handler import tg_handler

is_hadler_started = 0

def start_tg_handler():
  global is_hadler_started
  if is_hadler_started == 0:
    asyncio.create_task(tg_handler())
    is_hadler_started = 1
  return