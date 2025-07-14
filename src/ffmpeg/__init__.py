#! /usr/env python
# simplified function

#python :
from typing import Callable
import os
import time

# ours :
from .ffmpeg import FFmpeg

def fix_subs( subs : str, video : str , delay : int, output : str, on_finished : Callable) :
    name, ext = os.path.splitext(video)
    deletesubs = FFmpeg(FFmpeg.Arguments([FFmpeg.Input(video)], f"{name}.sn.{ext}", "-c copy -sn"))
    name, ext = os.path.splitext(subs)
    movesubs = FFmpeg(FFmpeg.Arguments([FFmpeg.Input(subs, f"-itsoffset {delay}")], f"{name}.{delay}.{ext}"))
    while deletesubs.is_running() and movesubs.is_running() :
        time.sleep(0.1)
        print("please wait !")
    on_finished()