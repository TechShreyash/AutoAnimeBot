import asyncio
from main.modules.utils import get_progress_text
import os
import time
import re
import json
import subprocess
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def compress_video(video,total_time, message, name):
    print(video,total_time, message, name)
    x = "." + video.split(".")[-1]
    out = video.replace(x,'').strip() + "_compressed" + x   
    progress = "progressaa.txt"
    with open(progress, 'w') as f:
      pass
    
    file_genertor_command = [
      "ffmpeg",
      "-hide_banner",
      "-loglevel",
      "quiet",
      "-progress",
      progress,
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
      "-y"      
    ]

    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    print("started")
    while process.returncode != 0:
      await asyncio.sleep(3)
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
          
    stdout, stderr = await process.communicate()

    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    if os.path.lexists(out):
        return out
    else:
        return None