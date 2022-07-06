import asyncio
from main.modules.compressor import compress_video
from main.modules.utils import episode_linker, get_duration, get_epnum, status_text
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main.modules.uploader import upload_video
import os
from main.modules.db import del_anime, get_channel, save_channel, save_uploads, is_voted, save_vote
from main.modules.downloader import downloader
from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name
from config import CHANNEL_ID, MAIN
from main import app, queue, status
from pyrogram.errors import FloodWait
from pyrogram import filters

status: Message
async def tg_handler():
    while True:
        try:
            if len(queue) != 0:
                i = queue[0]                
                queue.remove(i)
                val, id, name, ep_num, video = await start_uploading(i)
                
                await del_anime(i["title"])
                await save_uploads(i["title"])
                if val != "err":
                    await status.edit(await status_text("Adding Links To Main Channel..."))
                    await channel_handler(val,id,name,ep_num, video)
                await status.edit(await status_text("Sleeping For 5 Minutes..."))
                await asyncio.sleep(300)
            else:                
                if "Idle..." in status.text:
                    try:
                        await status.edit(await status_text("Idle..."))
                    except:
                        pass
                await asyncio.sleep(1800)
                
        except FloodWait as e:
            flood_time = int(e.x) + 5
            try:
                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"))
            except:
                pass
            await asyncio.sleep(flood_time)
        except:
            pass
            

async def start_uploading(data):
    try:
        title = data["title"]
        link = data["link"]
        size = data["size"]

        name, ext = title.split(".")
        name += " [@AutoAiringAnimes]." + ext
        fpath = "downloads/" + name

        id, img, tit = await get_anime_img(get_anime_name(title))
        msg = await app.send_photo(CHANNEL_ID,photo=img,caption=title)

        print("Downloading --> ",name)
        await status.edit(await status_text(f"Downloading {name}"))
        file = await downloader(msg,link,size,title)
        await msg.edit(f"Download Complete : {name}")

        print("Encoding --> ",name)
        await status.edit(await status_text(f"Encoding {name}"))
        duration = get_duration(file)
        os.rename(file,"video.mkv")
        compressed = await compress_video(duration,msg,name)
        
        if compressed == "None" or compressed == None:
            print("Encoding Failed Uploading The Original File")
            os.rename("video.mkv",fpath)
        else:
            os.rename("out.mkv",fpath)

        print("Uploading --> ",name)
        await status.edit(await status_text(f"Uploading {name}"))
        message_id = int(msg.id) + 1
        name = name.replace(" [@AutoAiringAnimes].","").replace(ext,"").strip()
        video = await upload_video(msg,fpath,id,tit,name,size)        
    except FloodWait as e:
        flood_time = int(e.x) + 5
        try:
            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"))
        except:
            pass
        await asyncio.sleep(flood_time)
    except Exception as e:
        print(e)
    return message_id, id, tit, name, video

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
async def channel_handler(msg_id,id,name,ep_num,video):
    try:
        anilist = await get_channel(id)

        if anilist == 0:
            img, caption = await get_anilist_data(name)
            main = await app.send_photo(MAIN,photo=img,caption=caption,reply_markup=VOTE_MARKUP)

            link = f"[{ep_num}](https://t.me/AutoAiringAnimes/{video})"
            dl = await app.send_message(
                MAIN,
                EPITEXT.format(link),
                disable_web_page_preview=True
            )

            await app.send_sticker(MAIN,"CAACAgUAAx0CXbNEVgABATemYrg6dYZGimb4zx9Q1DAAARzJ_M_NAAI6BQAC7s_BVQFFcU052MmMHgQ")
            dl_id = dl.id
            caption += f"\n📥 **Download -** [{name}](https://t.me/Anime_Dex/{dl_id})"
            await main.edit_caption(caption,reply_markup=VOTE_MARKUP)
            dl_id = int(dl_id)
            # db
            await save_channel(id,dl_id)
        else:
            dl_id = await get_channel(id)
            dl_id = int(dl_id)
            
            dl_msg = await app.get_messages(MAIN,dl_id)
            text = dl_msg.text
            text += f"\n{ep_num}"

            ent = episode_linker(dl_msg.text,dl_msg.entities,ep_num,f"https://t.me/AutoAiringAnimes/{video}")            
            
            await app.edit_message_text(MAIN,dl_id,text,entities=ent,disable_web_page_preview=True)

        main_id = dl_id
        info_id = main_id-1
        buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Info", url=f"https://t.me/Anime_Dex/{info_id}"),
                    InlineKeyboardButton(text="Comments", url=f"https://t.me/Anime_Dex/{main_id}?thread={main_id}")
                ]
            ])
        await app.edit_message_reply_markup(CHANNEL_ID,video,reply_markup=buttons)

    except FloodWait as e:
        flood_time = int(e.x) + 5
        try:
            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"))
        except:
            pass
        await asyncio.sleep(flood_time)
    return

def get_vote_buttons(a,b,c):
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

    
@app.on_callback_query(filters.regex("vote"))
async def votes_(_,query: CallbackQuery):
    try:
        id = query.message.id
        user = query.from_user.id
        vote = int(query.data.replace("vote","").strip())

        is_vote = await is_voted(id,user)
        if is_vote == 1:
            return await query.answer("You Have Already Voted... You Can't Vote Again")
        await query.answer()

        x = query.message.reply_markup['inline_keyboard'][0]
        a = x[0]['text'].replace('👍','').strip()
        b = x[1]['text'].replace('♥️','').strip()
        c = x[2]['text'].replace('👎','').strip()

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
            buttons = get_vote_buttons(a,b,c)
            await query.message.edit_reply_markup(reply_markup=buttons)
        elif vote == 2:
            b = b + 1
            buttons = get_vote_buttons(a,b,c)
            await query.message.edit_reply_markup(reply_markup=buttons)
        elif vote == 3:
            c = c + 1
            buttons = get_vote_buttons(a,b,c)
            await query.message.edit_reply_markup(reply_markup=buttons)

        await save_vote(id,user)
    except FloodWait as e:
        flood_time = int(e.x) + 5
        try:
            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"))
        except:
            pass
        await asyncio.sleep(flood_time)
    return
