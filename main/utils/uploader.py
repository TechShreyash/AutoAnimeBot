from os.path import isfile

async def upload_video(file):
    fuk = isfile(file)
    if fuk:
        c_time = time.time()
        z = await r.reply_document(
        document=trgt,
        caption=os.path.basename(trgt),
        progress=progress_for_pyrogram,
        progress_args=(
            f"STARTING TO UPLOAD {os.path.basename(trgt)}...",
            r,
            c_time
        )
        )
        os.remove(trgt)
    
    try:
        await r.delete()
        os.remove(trgt)
    except:
        return
    return