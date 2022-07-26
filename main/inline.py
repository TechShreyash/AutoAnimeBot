from config import INDEX_USERNAME, SCHEDULE_ID, STATUS_ID, UPLOADS_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button1 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="❤️‍ Anime Schedule ❤️‍", url= f"https://t.me/{UPLOADS_USERNAME}/{SCHEDULE_ID}")
            ],
           
                [
                InlineKeyboardButton(text="🔰 Index", url= f"https://t.me/{INDEX_USERNAME}"),
                InlineKeyboardButton(text="⚡️ Network ⚡️", url= f"https://t.me/AnimeSigma_Network"),
                InlineKeyboardButton(text="💠 Group", url= f"https://t.me/Anime_Sigma")
            ],
               [
                       
                InlineKeyboardButton(text="➤ Our Main Channel", url= f"https://t.me/AnimeSigma")
            ]
        ]
    )

button2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Queued List ✔", url= f"https://t.me/{UPLOADS_USERNAME}/{STATUS_ID}")
            ],
               
                 [
                InlineKeyboardButton(text="Owner 👀", url= f"https://t.me/Vedant_Vn"),
                InlineKeyboardButton(text="Ongoing Sigma✨", url= f"https://t.me/Anime_List_Index_Sigma/210")
                 ],
                
               [        
                InlineKeyboardButton(text="➤ Our Anime Group", url= f"https://t.me/Anime_Sigma")
            ],
        ]
    )
