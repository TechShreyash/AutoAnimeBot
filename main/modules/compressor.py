import asyncio
from math import floor
import os
import time
import re
import json

async def compress_video(video_file,total_time, message):
    x = video_file.split(".")
    fname = video_file.replace(x[-1],'').strip() + "_compressed" + x[-1].strip()  
    out = fname  
    video_file = '"' + video_file + '"'
    fname = '"' + fname + '"'
    
    progress = "progress.txt"
    with open(progress, 'w') as f:
      pass
    
    file_genertor_command = [
      "ffmpeg",
    "-i",
    video_file,
    "-preset",
    "ultrafast",
    "-c:v",
    "libx265",
    "-crf",
    "27",
    "-map",
    "0:v",
    "-c:a",
    "aac",
    "-map",
    "0:a",
    "-c:s",
    "copy",
    "-map",
    "0:s?",
    fname,
    "-y"
    ]

    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    while process.returncode != 0:
      await asyncio.sleep(3)
      with open("progressaa.txt", 'r+') as file:
        text = file.read()
        time_in_us=re.findall("out_time_ms=(\d+)", text)
        progress=re.findall("progress=(\w+)", text)
        speed=re.findall("speed=(\d+\.?\d*)", text)

        if len(speed):
          speed = speed[-1]
        else:
          speed = 1
        if len(time_in_us):
          time_in_us = time_in_us[-1]
        else:
          time_in_us = 1
        if len(progress):
          if progress[-1] == "end":
            break

        time_done = floor(time_in_us/1000000) # time of video that is completed compressing in seconds
        remaining = floor(int(total_time)-time_done)

        ETA = floor(remaining/float(speed))
    try:
        os.remove(video_file)
    except:
        pass
    return out