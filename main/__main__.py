import asyncio
from config import CHANNEL_ID
from main.modules.parser import auto_parser
from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  await message.reply_text("I am working fine :)")

async def start_():
  asyncio.create_task(auto_parser())

if __name__ == "__main__":
  print("==================================")
  print("[INFO]: BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  print("Creating Parse task")
  asyncio.run(start_())

  app.send_message(CHANNEL_ID,text="Bot Started")
  app.send_video("downloads/mp4.mp4")
  idle()

  print("[INFO]: BOT STOPPED")
  for task in asyncio.Task.all_tasks():
        task.cancel()