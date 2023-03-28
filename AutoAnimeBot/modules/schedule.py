import requests
import math
from AutoAnimeBot.core.log import LOGGER
from AutoAnimeBot.inline import button2
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageNotModified

logger = LOGGER("Schedule")


def change_tz(gmt):
    i, y = gmt.split(":")
    i = int(i)
    y = int(y)

    time = (i * 60) + y
    time = time + 330

    i = math.floor(time / 60)
    y = time - (i * 60)
    if y == 0:
        y = "00"

    return i, y


def get_scheduled_animes():
    url = "https://subsplease.org/api/?f=schedule&h=true&tz=$"
    res = requests.get(url).json()["schedule"]

    animes = []
    for i in res:
        x = {}
        x["title"] = i["title"]
        x["link"] = "https://subsplease.org/shows/" + i["page"]
        t = i["time"]

        hh, mm = change_tz(t)

        if int(hh) < 24:
            x["time"] = str(hh) + ":" + str(mm)
            animes.append(x)

    return animes


async def update_schedule(app):
    schedule: Message = app.schedule
    try:
        logger.info("Updating Schedule...")
        animes = get_scheduled_animes()
        text = "<b>📆 Today's Schedule</b> \n\n"

        for i in animes:
            text += '<b>[</b><code>{}</code><b>] - 📌 <a href="{}">{}</a></b>\n'.format(
                i["time"], i["link"], i["title"]
            )

        text += "\n<b>⏰ Current TimeZone :</b> <code>IST (UTC +5:30)</code>"
        text += "\n\n<b>❗️ Note :</b> This is not when episodes will be uploaded on channel, it's when they will be released by subsplease"

        try:
            await schedule.edit(text, reply_markup=button2, parse_mode=ParseMode.HTML)
        except:
            pass
    except MessageNotModified:
        pass
    except Exception as e:
        logger.warning(str(e))
