import asyncio
from config import CHANNEL_ID
from main.modules.parser import auto_parser
from main import app, status, queue
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from uvloop import install
from contextlib import closing, suppress
from main.modules.tg_handler import tg_handler

loop = asyncio.get_event_loop()

@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  await message.reply_text(str(queue[:3]))

async def start_bot():
  print("==================================")
  print("[INFO]: BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  #await app.send_message(CHANNEL_ID,text="Bot Started")

  print("Creating Parse task")
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
