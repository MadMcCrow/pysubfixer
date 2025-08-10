#! /usr/env python
# ffmpeg/ffprobe.py :run ffprobe more snakily

# python
import os

# ours
from .ffcmd import FFcmd


class FFprobe(FFcmd) :
    """
        class to represent an instance of ffprobe running in the background
    """
    
    cmd : str = "ffprobe.exe" if os.name == 'nt' else "ffprobe"

    def __init__(self, arguments) :
        """
            create ffprobe process and start async task
        """
        self._execute()
