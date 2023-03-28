print("AutoAnimeBot Config Generator\n")

config = ""

for i in [
    "API_ID",
    "API_HASH",
    "BOT_TOKEN",
    "MONGO_DB_URI",
    "STATUS_MSG_ID",
    "SCHEDULE_MSG_ID",
    "INDEX_CHANNEL_USERNAME",
    "UPLOADS_CHANNEL_USERNAME",
    "TECHZ_API_KEY",
    "COMMENTS_GROUP_LINK",
    "CHANNEL_TITLE"
]:
    x = input(f"Enter {i}: ")
    config += f'{i} = "{x}"\n'

with open("config.env", "w") as f:
    f.write(config)
