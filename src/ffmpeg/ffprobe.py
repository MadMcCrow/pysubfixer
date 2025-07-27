
#! /usr/env python
# ffmpeg/ffprobe.py :run ffprobe more snakily

# python
import os

# ours
from .ffcmd import FFcmd


class FFprobe(FFcmd) :
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
