from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI

print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime

animedb = db.animes
uploadsdb = db.uploads

async def get_animesdb(): 
    anime_list = []
    async for name in animedb.find():
        anime_list.append(name)
    return anime_list

async def save_animedb(name,data): 
    data = await animedb.insert_one({"name": name, "data": data})
    return
  
async def del_anime(name): 
    data = await animedb.delete_one({"name": name})
    return

async def get_uploads(): 
    anime_list = []
    async for name in uploadsdb.find():
        anime_list.append(name)
    return anime_list

async def save_uploads(name): 
    data = await uploadsdb.insert_one({"name": name})
    return