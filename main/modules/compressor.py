import asyncio
from main.modules.utils import get_progress_text
import os
import re
import math

async def compress_video(total_time, message, name):
  try:
    video = "video.mkv"
    out = "out.mkv" 
    prog = "progressaa.txt"

    with open(prog, 'w') as f:
      pass
    
    cmd = [
      "ffmpeg",
      "-hide_banner",
      "-loglevel",
      "quiet",
      "-progress",
      prog,
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
    print(27273)
    process = await asyncio.create_subprocess_exec(
        *cmd,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print("started")
    while True:
      print("x")
      with open(prog, 'r+') as file:
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
          
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    if os.path.lexists(out):
        return out
    else:
        return "None"
  except Exception as e:
    print(e)
