from main.utils.downloader import downloader
from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from main.wall import generate_logo

START = """
**🔮 Hello There, You Can Use Me To Download HD Wallpapers...**

__High Quality Wallpapers From (http://wall.alphacoders.com) And (http://unsplash.com)__

➤ Click /help Or The Button Below To Know How To Use Me
"""

HELP = """
**🖼 How To Use Me ?**

**To Download Wallpapers -** `/wall <search>`
**To Download Wallpapers From Unsplash - ** `/unsplash <search>`

**♻️ Example:** 
`/wall anime`
`/unsplash cat`
"""

# Commands
@app.on_message(filters.command("start"))
async def start(bot, message: Message):
  # await message.reply_photo("https://telegra.ph/file/7a98ead33e7b99fd82cc7.jpg",caption=START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="help_menu"), InlineKeyboardButton(text="Repo", url="https://github.com/TechShreyash/TechZ-Logo-Maker-Bot")]]))
  await message.reply_text(START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="help_menu"), InlineKeyboardButton(text="Repo", url="https://github.com/TechShreyash/TechZ-Logo-Maker-Bot")]]))

@app.on_message(filters.command("help"))
async def help(bot, message: Message):
  # await message.reply_photo("https://telegra.ph/file/7a98ead33e7b99fd82cc7.jpg",caption=HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="start_menu")]]))
  await message.reply_text(HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="start_menu")]]))

@app.on_message(filters.command("leech") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message: Message):
  return await downloader(bot,message)
  

if __name__ == "__main__":
  print("==================================")
  print("[INFO]: WALLPAPER BOT STARTED BOT SUCCESSFULLY")
  print("==========JOIN @TECHZBOTS=========")

  idle()
  print("[INFO]: WALLPAPER BOT STOPPED")