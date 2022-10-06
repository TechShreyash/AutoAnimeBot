import asyncio
from main.modules.ffmpeg import convert_to_mp4
from main.modules.api import AnimePahe
from main.modules.utils import episode_linker, status_text
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main.modules.uploader import upload_video
import os
from main.modules.db import del_anime, get_channel, save_channel, save_uploads, is_voted, save_vote, is_uploaded
from main.modules.downloader import downloader
from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name
from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID
from main import app, queue, status
from pyrogram.errors import FloodWait
from pyrogram import filters
from main.inline import button1

status: Message
is_bot_on = 0


async def tg_handler():
    while True:
        if len(queue) != 0:
            i = queue[0]
            queue.remove(i)
            data = AnimePahe.get_episode_links(i['ep_id'])
            if not data:
                await del_anime(i["title"])
                await save_uploads(i["title"])
                print('Links not found, skipping -->',i['title'])
                continue
            headers = data['headers']
            sources = []
            sources_qua = []

            for source in data['sources']:
                quality = source['quality']
                if quality not in sources_qua:
                    sources.append(source)
                    sources_qua.append(quality)

            for source in sources:
                try:
                    val, id, name, ep_num, video = await start_uploading(i, source, headers)
                except:
                    val = 'error'
                if val != 'error':
                    try:
                        await status.edit(await status_text(f"Adding Links To Index Channel ({INDEX_USERNAME})..."), reply_markup=button1)
                    except:
                        pass
                    await channel_handler(val, id, name, ep_num, video)
                    await asyncio.sleep(300)
            await del_anime(i["title"])
            await save_uploads(i["title"])
        else:
            if "Idle..." not in status.text:
                try:
                    await status.edit(await status_text("Idle..."), reply_markup=button1)
                except:
                    pass
            global is_bot_on
            if is_bot_on == 0:
                is_bot_on = 1
                await asyncio.sleep(30)
            else:
                await asyncio.sleep(600)


async def start_uploading(data, source, header):
    if await is_uploaded(data["title"]):
        return 'error', 1, 2, 3, 4
    
    title = data["title"] + f" ({source['quality']}p)"
    link = source['url']
    ep_id = data["ep_id"]
    total_size = source['size']
    name = f"{title} [@{UPLOADS_USERNAME}].mp4"
    fpath = "downloads/" + name

    oppp = get_anime_name(title)
    id, img, tit = await get_anime_img(oppp)
    msg = await app.send_photo(UPLOADS_ID, photo=img, caption=name)

    print("Downloading --> ", title)
    await status.edit(await status_text(f"Downloading {title}"), reply_markup=button1)
    text = await downloader(msg, link, header, fpath, total_size, title)
    await msg.edit(f"Encoding : {title}")

    file = await convert_to_mp4(text)

    print("Uploading --> ", title)
    await status.edit(await status_text(f"Uploading {title}"), reply_markup=button1)
    message_id = int(msg.id) + 1
    video = await upload_video(msg, file, id, tit, title, total_size)

    try:
        os.remove(file)
    except:
        pass
    try:
        os.remove(fpath)
    except:
        pass
    return message_id, id, oppp, title, video

VOTE_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👍", callback_data="vote1"),
            InlineKeyboardButton(text="♥️", callback_data="vote2"),
            InlineKeyboardButton(text="👎", callback_data="vote3")
        ]
    ]
)

EPITEXT = """
🔰 **Episodes :**

{}
"""


async def channel_handler(msg_id, id, name, ep_num, video):
    try:
        anilist, episodes = await get_channel(id)

        if anilist == 0:
            img, caption = await get_anilist_data(name)
            main = await app.send_photo(INDEX_ID, photo=img, caption=caption, reply_markup=VOTE_MARKUP)
            link = f"[{ep_num}](https://t.me/{UPLOADS_USERNAME}/{video})"

            dl = await app.send_message(
            INDEX_ID,
            EPITEXT.format(link),
            disable_web_page_preview=True
        )
            await app.send_sticker(INDEX_ID, "CAACAgUAAx0CXbNEVgABATemYrg6dYZGimb4zx9Q1DAAARzJ_M_NAAI6BQAC7s_BVQFFcU052MmMHgQ")

            dl_id = dl.id
            caption += f"\n📥 **Download -** [{name}](https://t.me/{INDEX_USERNAME}/{dl_id})"
            await main.edit_caption(caption, reply_markup=VOTE_MARKUP)
            dl_id = int(dl_id)
            episode = [link]
            await save_channel(id, dl_id, episode)

        else:
            link = f"[{ep_num}](https://t.me/{UPLOADS_USERNAME}/{video})"
            episodes.append(link)
            dl_id = anilist
            await save_channel(id, dl_id, episodes)
            print(episodes)
            text = ''
            for i in episodes:
                text += i + '\n'

            await app.edit_message_text(INDEX_ID, dl_id, text, disable_web_page_preview=True)

        main_id = dl_id
        info_id = main_id-1
        buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="Info", url=f"https://t.me/{INDEX_USERNAME}/{info_id}"),
            InlineKeyboardButton(
                text="Comments", url=f"https://t.me/{INDEX_USERNAME}/{main_id}?thread={main_id}")
        ]
    ])
        await app.edit_message_reply_markup(UPLOADS_ID, video, reply_markup=buttons)
    except:
        pass

def get_vote_buttons(a, b, c):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"👍 {a}", callback_data="vote1"),
                InlineKeyboardButton(text=f"♥️ {b}", callback_data="vote2"),
                InlineKeyboardButton(text=f"👎 {c}", callback_data="vote3")
            ]
        ]
    )
    return buttons


def button_formatter(buttons):
    x = str(buttons)
    y = x.find("text")
    x = x[y:]
    x = x.replace('text": "👍 ', '').strip()
    b = x.find('"')
    a1 = x[:b]

    y = x.find("text")
    x = x[y:]
    x = x.replace('text": "♥️ ', '').strip()
    b = x.find('"')
    a2 = x[:b]

    y = x.find("text")
    x = x[y:]
    x = x.replace('text": "👎 ', '').strip()
    b = x.find('"')
    a3 = x[:b]

    return a1, a2, a3


@app.on_callback_query(filters.regex("vote"))
async def votes_(_, query: CallbackQuery):
    try:
        id = query.message.id
        user = query.from_user.id
        vote = int(query.data.replace("vote", "").strip())

        is_vote = await is_voted(id, user)
        if is_vote == 1:
            return await query.answer("You Have Already Voted... You Can't Vote Again")
        await query.answer()

        x = query.message.reply_markup
        a, b, c = button_formatter(x)

        if a == "":
            a = 0
        if b == "":
            b = 0
        if c == "":
            c = 0

        a = int(a)
        b = int(b)
        c = int(c)

        if vote == 1:
            a = a + 1
            buttons = get_vote_buttons(a, b, c)
            await query.message.edit_reply_markup(reply_markup=buttons)
        elif vote == 2:
            b = b + 1
            buttons = get_vote_buttons(a, b, c)
            await query.message.edit_reply_markup(reply_markup=buttons)
        elif vote == 3:
            c = c + 1
            buttons = get_vote_buttons(a, b, c)
            await query.message.edit_reply_markup(reply_markup=buttons)

        await save_vote(id, user)
    except FloodWait as e:
        flood_time = int(e.x) + 5
        try:
            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"), reply_markup=button1)
        except Exception as e:
            print(e)
        await asyncio.sleep(flood_time)
    except:
        pass
