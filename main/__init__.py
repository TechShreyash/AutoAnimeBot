import asyncio
from pyrogram import Client
from config import *
import libtorrent as lt
from qbittorrent import Client

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
  )
app.start()

print("[INFO]: STARTING Lib Torrent CLIENT")
ses = lt.session()
ses.listen_on(6881, 6891)

qb = Client('http://127.0.0.1:8080/')
qb.login()

queue = []

status = app.send_message(CHANNEL_ID,"Bot Started")
try:
  app.pin_chat_message(CHANNEL_ID,status.message_id)
except:
  pass