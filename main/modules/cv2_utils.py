import os
import cv2, random
from string import ascii_uppercase, hexdigits

def get_duration(file):
    data = cv2.VideoCapture(file)
  
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    seconds = int(frames / fps)
    return seconds


def get_screenshot(file):
    cap = cv2.VideoCapture(file)
    name = "./" + "".join(random.choices(ascii_uppercase + hexdigits,k = 10)) + ".jpg"

    total_frames = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    frame_num = random.randint(0,total_frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num-1)
    res, frame = cap.read()

    cv2.imwrite(name, frame)
    cap.release()
    #cv2.destroyAllWindows()
    return name

def get_filesize(file):
    x = os.path.getsize(file)
    x = round(x/(1024*1024))
    if x > 1024:
        x = str(round(x/1024,2)) + " GB"
    else:
        x = str(x) + " MB"

    return x

def get_epnum(name):
    x = name.split("-")[1].strip()
    x, y = x.split(" ")
    x = x.strip()
    return x

def format_time(time):
    min = round(time/60)
    sec = round(time-(min*60))

    time = str(min) + ":" + str(sec)
    return time