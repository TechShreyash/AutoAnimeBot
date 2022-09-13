import os
import shutil


async def convert_to_mp4(file):
    try:
        os.remove('downloads/video.mp4')
    except:
        pass

    cmd = f'ffmpeg -safe 0 -f concat -i {file} -c copy -bsf:a aac_adtstoasc downloads/video.mp4'
    os.system(cmd)

    try:
        shutil.rmtree('downloads/ts_files')
    except:
        pass
    return 'downloads/video.mp4'