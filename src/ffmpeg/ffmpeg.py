#! /usr/env python
# ffmpeg/ffmpeg.py : FFMpeg controls written in a pythonic way

# python
import os
from time import sleep
from typing import List, Optional

# ours
from .ffcmd import FFcmd


class FFmpeg(FFcmd) :
    """
        class to represent an instance of ffmpeg running in the background
    """
    
    cmd : str = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"

    def __init__(self, *inputs, options : Optional, output) :
        """ create ffmpeg process and start async task """
        self.args = [ f"-i {x}" for x in inputs] + options + [output]
        # the ffmpeg binary name changes depending on platform
        self._execute()