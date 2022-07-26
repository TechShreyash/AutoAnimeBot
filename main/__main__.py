import asyncio
from main.modules.parser import auto_parser
from main import app
from pyrogram import filters, idle
from pyrogram.types import Message
from uvloop import install
from contextlib import closing, suppress
from main.modules.tg_handler import tg_handler

loop = asyncio.get_event_loop()

@app.on_message(filters.command(["start","help","ping"]))
async def start(bot, message: Message):
  return await message.reply_text("Yo, It's Me **The Pirate Hunter...**[Roronoa Zoro](https://te.legra.ph/file/50731236ce8f4c5a0558d.mp4) This Side\n\n**My Owner 👀**: **@Vedant_vn** \n**Bot Support 🤖**: **@NarutoRobot_Support** \n**Auto Anime Channel**: **@Auto_Anime**")

async def start_bot():
  print("==================================")
  print("[INFO]: Sigma Auto AnimeBot Started Bot Successfully")
  print("==========JOIN @AnimeSigma=========")

  print("[INFO]: Adding Parsing Task")
  asyncio.create_task(auto_parser())
  asyncio.create_task(tg_handler())
  
  await idle()
  print("[INFO]: BOT STOPPED")
  await app.stop()  
  for task in asyncio.all_tasks():
    task.cancel()

if __name__ == "__main__":
  install()
  with closing(loop):
    with suppress(asyncio.exceptions.CancelledError):
      loop.run_until_complete(start_bot())
      loop.run_until_complete(asyncio.sleep(3.0))
