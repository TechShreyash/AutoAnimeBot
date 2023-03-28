from math import floor
import os
import cv2
from string import ascii_letters, ascii_uppercase, digits
from pyrogram.types import MessageEntity


def get_duration(file):
    data = cv2.VideoCapture(file)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    seconds = int(frames / fps)
    return seconds


def get_filesize(file):
    x = os.path.getsize(file)
    x = round(x / (1024 * 1024))
    if x > 1024:
        x = str(round(x / 1024, 2)) + " GB"
    else:
        x = str(x) + " MB"

    return x


def format_time(time):
    min = floor(time / 60)
    sec = round(time - (min * 60))

    time = str(min) + ":" + str(sec)
    return time


def format_text(text):
    ftext = ""
    for x in text:
        if x in ascii_letters or x == " " or x in digits:
            ftext += x
        else:
            ftext += " "

    while "  " in ftext:
        ftext = ftext.replace("  ", " ")
    return ftext


def tags_generator(title):
    x = "#" + title.replace(" ", "_")

    while x[-1] == "_":
        x = x[:-1]
    return x
