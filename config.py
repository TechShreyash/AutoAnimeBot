from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_DB_URI = getenv("MONGO_DB_URI")

INDEX_ID = int(getenv("INDEX_ID"))
UPLOADS_ID = int(getenv("UPLOADS_ID"))

STATUS_ID = int(getenv("STATUS_ID"))
SCHEDULE_ID = int(getenv("SCHEDULE_ID"))

CHANNEL_TITLE = getenv("CHANNEL_TITLE")
INDEX_USERNAME = getenv("INDEX_USERNAME")
UPLOADS_USERNAME = getenv("UPLOADS_USERNAME")