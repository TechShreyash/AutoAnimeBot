import asyncio
from config import CHANNEL_ID
from main.modules.parser import auto_parser
from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import importlib
import glob
from os.path import dirname, basename, isfile, join


modules = glob.glob(join(dirname("main/modules/"), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

for module in __all__: 
  imported_module = importlib.import_module("main.modules." + module)

@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  await message.reply_text("I am working fine :)")
  
async def parsersss():
  print("Creating Parse task")
  asyncio.create_task(auto_parser())

  print("==================================")
  print("[INFO]: BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  await app.send_message(CHANNEL_ID,text="Bot Started")
  await idle()
  print("[INFO]: BOT STOPPED")
  for task in asyncio.Task.all_tasks():
        task.cancel()

if __name__ == "__main__":
  asyncio.run(parsersss())
