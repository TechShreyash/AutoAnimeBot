from main.modules.db import get_animes


async def tg_handler():
    data = await get_animes()