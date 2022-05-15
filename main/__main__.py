from main.utils.downloader import downloader
from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  await message.reply_text("I am working fine :)")

@app.on_message(filters.command("up") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message: Message):
  return await downloader(bot,message)
  

if __name__ == "__main__":
  print("==================================")
  print("[INFO]: BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  idle()
  print("[INFO]: BOT STOPPED")