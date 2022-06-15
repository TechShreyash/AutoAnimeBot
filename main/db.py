from main import db

animedb = db.animes

async def get_animes(): 
    anime_list = []
    async for name in animedb.find():
        anime_list.append(name)
    return anime_list

async def save_anime(name,data): 
    data = await animedb.insert_one({"name": name, "data": data})
    return
  
async def del_anime(name): 
    data = await animedb.delete_one({"name": name})
    return