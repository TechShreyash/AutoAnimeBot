import os
import subprocess

async def convert_to_mp4(file):
    try:
        cmd = f'! ffmpeg -safe 0 -f concat -i {file} -c copy -bsf:a aac_adtstoasc downloads/video.mp4'  
        subprocess.Popen(cmd,shell=True)
        os.rmdir('downloads/ts_files')
        return 'downloads/video.mp4'
    except:
        pass