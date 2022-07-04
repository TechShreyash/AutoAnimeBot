import asyncio
from math import floor
import os
import time
import re
import json
from main.modules.utils import get_progress_text

async def compress_video(video_file,total_time, message, name):
  x = "." + video_file.split(".")[-1]
  fname = video_file.replace(x,'').strip() + "_compressed" + x
  out = fname  
  
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
    await asyncio.sleep(10)
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
      time_done = floor(int(time_in_us)/1000000) # time of video that is completed compressing in seconds      
    
    try:
      textt = get_progress_text(
        name,
        "Encoding",
        time_done,
        speed,
        total_time,
        enco=True
      )
      await message.edit(textt)
    except:
      pass
  try:
      os.remove(video_file)
  except:
      pass
  return out