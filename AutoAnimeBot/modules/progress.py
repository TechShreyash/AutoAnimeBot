import time
from math import floor

t1 = 1
dcount = 1


async def upload_progress(current, total, title, message, logger):
    global t1, dcount

    t2 = time.time()
    done = floor(current / 1024)
    if t2 - t1 > 10:
        try:
            t1 = t2
            text = progress_text("Uploading", title, done, total / 1024, dcount)
            await message.edit_caption(text)
            dcount = done
        except Exception as e:
            logger.warning(str(e))


def progress_text(status, filename, current, total, dcounto):
    text = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}
ETA: {}
    """
    if total == 0:
        total = 1
    percent = round((current / total) * 100, 2)

    size_downloaded = round(current / 1024, 2)  # in MB
    if size_downloaded > 1024:
        size_downloaded = str(round(size_downloaded / 1024, 2)) + " GB"
    else:
        size_downloaded = str(size_downloaded) + " MB"

    total_size = round(total / 1024, 2)
    if total_size > 1024:
        total_size = str(round(total_size / 1024, 2)) + " GB"
    else:
        total_size = str(total_size) + " MB"

    fill = "▪️"
    blank = "▫️"
    bar = fill * floor(percent / 10)
    bar += blank * (int(((20 - len(bar)) / 2)))

    speed = round((current - dcounto) / 10, 2)  # in KB/s
    if speed == 0:
        speed = 1

    if speed > 1024 * 1024:
        stext = str(round(speed / 1024 * 1024, 2)) + " GB/s"
    elif speed > 1024:
        stext = str(round(speed / 1024, 2)) + " MB/s"
    else:
        stext = str(speed) + " KB/s"

    eta = round((total - current) / (speed))
    if eta > 3600:
        eta = str(round((eta / 3600), 2)) + " hours"
    elif eta > 60:
        eta = str(round((eta / 60))) + " minutes"
    else:
        eta = str(eta) + " seconds"

    return text.format(
        filename, status, percent, bar, size_downloaded, total_size, stext, eta
    )
