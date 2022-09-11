from pyrogram import Client
from config import *

app = Client(
    "AutoAnimeBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
  )
app.start()
queue = []
status = app.get_messages(UPLOADS_ID,STATUS_ID)
schedule = app.get_messages(UPLOADS_ID,SCHEDULE_ID)