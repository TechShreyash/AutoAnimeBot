from config import (
    INDEX_CHANNEL_USERNAME,
    SCHEDULE_MSG_ID,
    STATUS_MSG_ID,
    UPLOADS_CHANNEL_USERNAME,
    COMMENTS_GROUP_LINK,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="View Schedule",
                url=f"https://t.me/{UPLOADS_CHANNEL_USERNAME}/{SCHEDULE_MSG_ID}",
            )
        ],
        [
            InlineKeyboardButton(
                text="Index Channel", url=f"https://t.me/{INDEX_CHANNEL_USERNAME}"
            ),
            InlineKeyboardButton(text="Discussion Group", url=COMMENTS_GROUP_LINK),
        ],
    ]
)

button2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Check Queue",
                url=f"https://t.me/{UPLOADS_CHANNEL_USERNAME}/{STATUS_MSG_ID}",
            )
        ]
    ]
)
