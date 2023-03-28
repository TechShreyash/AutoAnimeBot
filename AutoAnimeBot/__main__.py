import asyncio
from pyrogram import filters
from pyrogram.types import Message

from uvloop import install
from contextlib import closing, suppress
from pyrogram import idle
import AutoAnimeBot.modules.vote
from AutoAnimeBot import app

loop = asyncio.get_event_loop()


@app.on_message(filters.command(["start", "help", "ping"]))
async def start(bot, message: Message):
    await message.reply_photo(
        "assets/thumb.jpg",
        caption="⭐️ **Bot Is Online...**\n\n**Updates :** @TechZBots **| Support :** @TechZBots_Support",
    )


@app.on_message(filters.command("logs"))
async def logs(bot, message: Message):
    await message.reply_document(
        "logs.txt",
        caption="AutoAnimeBot Logs, Send this to @TechZBots_Support if you need help",
    )


async def main():
    await app.start()

    await idle()
    app.logger.info("BOT STOPPED")
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()


if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(main())
            loop.run_until_complete(asyncio.sleep(3.0))
