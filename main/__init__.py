import aiohttp
from pyrogram import Client
from config import *
import libtorrent as lt

app = Client(
  "bot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)

print("[INFO]: STARTING BOT...")
app.start()

print("[INFO]: STARTING AIOHTTP CLIENT")
session = aiohttp.ClientSession()

print("[INFO]: STARTING Lib Torrent CLIENT")
lib = lt.session()
lib.listen_on(6881, 6891)