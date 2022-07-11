from main.modules.utils import get_progress_text
import time

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start,
    ttl
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff

        try:
            percentage = round(percentage/100,2)
            await message.edit(
                text=get_progress_text(
                    ud_type,
                    "Uploading",
                    percentage,
                    speed,
                    ttl
                )
            )
        except:            
            pass