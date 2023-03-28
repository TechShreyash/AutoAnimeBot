from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AutoAnimeBot import app
from pyrogram import filters
from AutoAnimeBot.modules.db import is_voted, save_vote
from AutoAnimeBot.core.log import LOGGER

logger = LOGGER("Vote")


def get_vote_buttons(a, b, c):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"👍 {a}", callback_data="vote1"),
                InlineKeyboardButton(text=f"♥️ {b}", callback_data="vote2"),
                InlineKeyboardButton(text=f"👎 {c}", callback_data="vote3"),
            ]
        ]
    )
    return buttons


def strip_int(x):
    y = ""
    for i in x:
        if i.isnumeric():
            y += i
    return y


def button_formatter(buttons):
    x = str(buttons)
    y = []
    x.replace("♥️", "").replace("👍", "").replace("'👎", "")
    for i in range(3):
        a = x.find("text")
        z = x[a + 9 :]
        b = z.find('"')
        z = z[:b]
        y.append(strip_int(z.strip()))
        x = x[a + b + 10 :]
    return y


@app.on_callback_query(filters.regex("vote"))
async def votes_(_, query: CallbackQuery):
    try:
        id = query.message.id
        user = query.from_user.id
        vote = int(query.data.replace("vote", "").strip())

        if await is_voted(id, user):
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
    except Exception as e:
        logger.warning(str(e))
