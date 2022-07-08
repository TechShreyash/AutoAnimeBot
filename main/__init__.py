from pyrogram import Client
from config import *
import libtorrent as lt

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

queue = []

status = app.get_messages(UPLOADS_ID,STATUS_ID)