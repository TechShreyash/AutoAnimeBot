import asyncio
from AutoAnimeBot.core.log import LOGGER
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from AutoAnimeBot.modules.uploader import upload_video
import os
from AutoAnimeBot.modules.db import (
    add_to_failed,
    del_anime,
    get_channel,
    is_failed,
    is_quality_uploaded,
    save_channel,
    save_uploads,
    is_voted,
    save_vote,
    is_uploaded,
)
from AutoAnimeBot.modules.downloader import downloader
from AutoAnimeBot.modules.anilist import get_anilist_data, get_anime_img, get_anime_name
from config import (
    INDEX_CHANNEL_USERNAME,
    UPLOADS_CHANNEL_USERNAME,
    SLEEP_TIME,
)
from pyrogram.errors import FloodWait
from pyrogram import filters
from AutoAnimeBot.inline import button1
from techzapi.api import TechZApi
from pyrogram.client import Client

logger = LOGGER("TgHandler")
app = Client


async def tg_handler(appp, TECHZ_API_KEY):
    global app
    app = appp
    queue = app.queue
    Gogo = TechZApi.Gogo(TECHZ_API_KEY)
    Gogo.base = "https://api.techzbots.live"

    while True:
        if len(queue) != 0:
            try:
                i = queue[0]
                logger.info("Processing : " + i)

                try:
                    data = Gogo.episode(i, lang="any")
                except Exception as e:
                    logger.warning("Unable To Fetch Links : " + str(e))
                    await add_to_failed(i)
                    queue.pop(0)
                    continue

                for q, l in data["dlinks"].items():  # q = quality, l = link
                    if await is_quality_uploaded(i, q):
                        continue
                    if await is_failed(f"{i}-{q}"):
                        continue

                    video_id, anime_id, name, ep_num = await start_uploading(
                        app, q, l, i
                    )

                    await app.update_status(
                        f"Adding Links To Index Channel ({INDEX_CHANNEL_USERNAME})..."
                    )
                    await channel_handler(video_id, anime_id, name, ep_num, q)
                    await save_uploads(i, q)
                    await app.update_status(f"Sleeping for {SLEEP_TIME} seconds")
                    await asyncio.sleep(SLEEP_TIME)

                for q in ["360p", "480p", "720p", "1080p"]:
                    if q not in data["dlinks"]:
                        await save_uploads(i, q)

                await del_anime(i)
                queue.pop(0)
            except Exception as e:
                logger.warning(str(e))
                await del_anime(i)
                await add_to_failed(f"{i}-{q}")
                queue.pop(0)
        else:
            if "Idle..." not in app.status.text:
                await app.update_status("Idle...")
                await asyncio.sleep(SLEEP_TIME)
            else:
                await asyncio.sleep(SLEEP_TIME)


async def start_uploading(app, q, l, eid):
    try:
        title = eid.replace("-", " ").title().strip() + f" - {q}"
        file_name = f"{title} [@{UPLOADS_CHANNEL_USERNAME}].mp4"

        anime = eid.split("-episode-")[0].replace("-", " ").title().strip()
        id, img, tit = await get_anime_img(anime)
        msg = await app.send_photo(app.UPLOADS_CHANNEL_ID, photo=img, caption=title)

        await app.update_status(f"Downloading {title}")
        file = await downloader(msg, l, title, file_name)

        await app.update_status(f"Uploading {title}")
        video_id = await upload_video(app, msg, file, id, tit, title, eid)

        return video_id, id, tit, eid.split("-episode-")[1]
    except Exception as e:
        logger.warning(str(e))
        try:
            await msg.delete()
        except:
            pass


VOTE_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👍", callback_data="vote1"),
            InlineKeyboardButton(text="♥️", callback_data="vote2"),
            InlineKeyboardButton(text="👎", callback_data="vote3"),
        ]
    ]
)

EPITEXT = """
🔰 **Episodes :**

{}
"""


async def channel_handler(video_id, anime_id, name, ep_num, quality):
    try:
        dl_id, episodes, post = await get_channel(anime_id)

        if dl_id == 0:
            img, caption = await get_anilist_data(name)
            main = await app.send_photo(
                app.INDEX_CHANNEL_ID,
                photo=img,
                caption=caption,
                reply_markup=VOTE_MARKUP,
            )
            link = f"➤ **Episode {ep_num}** : [{quality}](https://t.me/{UPLOADS_CHANNEL_USERNAME}/{video_id})"

            dl = await app.send_message(
                app.INDEX_CHANNEL_ID,
                EPITEXT.format(link),
                disable_web_page_preview=True,
            )
            await app.send_sticker(
                app.INDEX_CHANNEL_ID,
                "CAACAgUAAxkBAAEUmDtkHHayrNb6EFmmlzQlF3wR03QY2AACGgYAApROQVYbFOqQoyJzAy8E",
            )

            dl_id = int(dl.id)
            post = int(main.id)

            caption += f"\n📥 **Download -** [{name}](https://t.me/{INDEX_CHANNEL_USERNAME}/{dl_id})"
            await main.edit_caption(caption, reply_markup=VOTE_MARKUP)
            episode = {ep_num: [(quality, video_id)]}
            await save_channel(anime_id, post=post, dl_id=dl_id, episodes=episode)

        else:
            episodes[ep_num].append((quality, video_id))
            await save_channel(anime_id, post, dl_id, episodes)

            text = ""
            for ep, data in episodes.items():
                line = f"➤ **Episode {ep}** : "
                for q, v in data:
                    line += f"[{q}](https://t.me/{UPLOADS_CHANNEL_USERNAME}/{v}) | "

                x = line[:-3] + "\n"

                if len(x) + len(text) > 4000:
                    dl = await app.send_message(
                        app.INDEX_CHANNEL_ID,
                        EPITEXT.format(x),
                        disable_web_page_preview=True,
                        reply_to_message_id=post,
                    )
                    dl_id = int(dl.id)
                    await save_channel(anime_id, post, dl_id, {ep: data})

                else:
                    text += x
                    await app.edit_message_text(
                        app.INDEX_CHANNEL_ID,
                        dl_id,
                        EPITEXT.format(text),
                        disable_web_page_preview=True,
                    )

        main_id = dl_id
        info_id = main_id - 1
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Info",
                        url=f"https://t.me/{INDEX_CHANNEL_USERNAME}/{info_id}",
                    ),
                    InlineKeyboardButton(
                        text="Comments",
                        url=f"https://t.me/{INDEX_CHANNEL_USERNAME}/{main_id}?thread={main_id}",
                    ),
                ]
            ]
        )
        await app.edit_message_reply_markup(
            app.UPLOADS_CHANNEL_ID, video_id, reply_markup=buttons
        )
    except Exception as e:
        logger.warning(str(e))
