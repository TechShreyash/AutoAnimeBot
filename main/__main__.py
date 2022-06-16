import asyncio
from config import CHANNEL_ID
from main.modules.tg_handler import tg_handler
from main.modules.parser import auto_parser
from main.modules.downloader import downloader
from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  await message.reply_text("I am working fine :)")
  
async def parsersss():
  print("Creating Parse task")
  asyncio.create_task(auto_parser())

  print("==================================")
  print("[INFO]: BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  await app.start()
  await app.send_message(CHANNEL_ID,text="Bot Started")
  await idle()
  print("[INFO]: BOT STOPPED")
  for task in asyncio.Task.all_tasks():
        task.cancel()



if __name__ == "__main__":
  asyncio.run(parsersss())