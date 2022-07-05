import asyncio
from main.modules.utils import get_progress_text
import os
import time
import re
import json
import subprocess
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def task(video,out):
  await asyncio.create_subprocess_exec(
        "ffmpeg",
      "-hide_banner",
      "-loglevel",
      "quiet",
      "-progress",
      "progressaa.txt",
      "-i",
      video,
      "-preset", 
      "fast",
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
      out,
      "-y",
    )

async def compress_video(video,total_time, message, name):
    out = "out.mkv" 
    progress = "progressaa.txt"
    with open(progress, 'w') as f:
      pass

    print("started")
    asyncio.create_task(task(video,out))

    while True:
      with open(progress, 'r+') as file:
        text = file.read()
        frame = re.findall("frame=(\d+)", text)
        time_in_us=re.findall("out_time_ms=(\d+)", text)
        progress=re.findall("progress=(\w+)", text)
        speed=re.findall("speed=(\d+\.?\d*)", text)
        if len(frame):
          frame = int(frame[-1])
        else:
          frame = 1
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
        
        time_done = math.floor(int(time_in_us)/1000000)
        
        progress_str = get_progress_text(name,"Encoding",time_done,str(speed),total_time,enco=True)
        print(time_done)
        try:
          await message.edit(progress_str)
        except:
            pass
      await asyncio.sleep(5)
      
    if os.path.lexists(out):
        return out
    else:
        return None