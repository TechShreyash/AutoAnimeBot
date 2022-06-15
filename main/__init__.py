import asyncio
from main.utils.parser import auto_parser
from pyrogram import Client
from config import *
import libtorrent as lt
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

async def start():
  app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
  )

  print("[INFO]: STARTING BOT...")
  app.start()

  print("[INFO]: STARTING Lib Torrent CLIENT")
  ses = lt.session()
  ses.listen_on(6881, 6891)

  print("[INFO]: STARTING MONGO DB CLIENT")
  mongo_client = MongoClient(MONGO_DB_URI)
  db = mongo_client.autoanime

  print("Creating Parse task")
  asyncio.create_task(auto_parser())

asyncio.run(start())