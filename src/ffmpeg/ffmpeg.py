#! /usr/env python
# ffmpeg/ffmpeg.py : FFMpeg controls written in a pythonic way

# python
import os
import asyncio
import shlex
import shutil
import sys
from datetime import datetime
from typing import List, Callable

from .ffcmd import FFcmd


class FFmpeg(FFcmd) :
    """
        class to represent an instance of ffmpeg running in the background
    """
    
    def __init__(self, arguments) :
        """
            create ffmpeg process and start async task
        """
        # the ffmpeg binary name changes depending on platform
        command = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
        self._execute(command)
