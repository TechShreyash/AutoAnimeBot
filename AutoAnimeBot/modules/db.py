from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI
from AutoAnimeBot.core.log import LOGGER

logger = LOGGER("Database")
logger.info("Starting Mongo DB Client")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime

animedb = db.animes
uploadsdb = db.uploads
channeldb = db.channel
votedb = db.votes
faileddb = db.failed

logger.info("Mongo DB Client Started Successfully")


async def get_animesdb():
    anime_list = []
    async for name in animedb.find().sort("pos", 1):
        anime_list.append(name)
    return anime_list


async def is_uploaded(name):
    data = await get_uploads()
    anime = []
    for i in data:
        anime.append(i["id"])
    if name in anime:
        return True
    else:
        return False


async def save_animedb(name, pos):
    await animedb.insert_one({"id": name, "pos": pos})


async def del_anime(name):
    await animedb.delete_one({"id": name})


async def get_uploads():
    anime_list = []
    async for name in uploadsdb.find().sort("pos", 1):
        anime_list.append(name)
    return anime_list


async def save_uploads(name, quality=None):
    if quality is None:
        await uploadsdb.update_one({"id": name}, upsert=True)
    else:
        q = await uploadsdb.find_one({"id": name})
        if q:
            q = q.get("q")
            q.append(quality)
        if not q:
            q = [quality]
        await uploadsdb.update_one({"id": name}, {"$set": {"q": q}}, upsert=True)
    return


async def is_quality_uploaded(name, q):
    data = await uploadsdb.find_one({"id": name})
    if data:
        if data.get("q"):
            if q in data["q"]:
                return True
    return False


# channel


async def get_channel(anilist):
    anilist = "a" + str(anilist)
    anime = await channeldb.find_one({"anilist": anilist})
    if anime is None:
        return 0, 0, 0
    msg = anime["msg"].replace("a", "")
    return int(msg), anime["episodes"], anime.get("post")


async def save_channel(anilist, post, dl_id, episodes=None):
    if episodes is None:
        episodes = []
    anilist = "a" + str(anilist)
    dl_id = "a" + str(dl_id)
    await channeldb.update_one(
        {
            "anilist": anilist,
        },
        {"$set": {"msg": dl_id, "episodes": episodes, "post": post}},
        upsert=True,
    )


# vote


async def is_voted(id, user):
    id = "a" + str(id)
    votes = await votedb.find_one({"id": id})
    if votes is None:
        return False
    if user not in votes["users"]:
        return False
    return True


async def save_vote(id, user):
    id = "a" + str(id)
    await votedb.update_one({"id": id}, {"$addToSet": {"users": user}}, upsert=True)


# failed


async def add_to_failed(name):
    await faileddb.update_one({"id": name}, {"$inc": {"count": 1}}, upsert=True)


async def is_failed(name):
    data = await faileddb.find_one({"id": name})
    if data:
        if data["count"] > 3:
            return True
    return False
