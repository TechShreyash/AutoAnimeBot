import asyncio
from main.modules.tg_handler import tg_handler

is_on = 0

async def start_hand():
    if is_on == 0:
        asyncio.create_task(tg_handler())