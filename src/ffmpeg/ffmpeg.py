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

    def __init__(self, *inputs, output, options : List | str | None = None ) :
        """ create ffmpeg process and start async task """
        self.outfile = output
        self.args = [ f"-i {self.checkfile(x, True)}" for x in inputs]
        if isinstance(options, str) :
            self.args.append(options)
        elif isinstance(options,list) :
            self.args += [str(x) for x in options]
        self.args.append(self.checkfile(output, False))
        # run
        self._execute()

    def output(self) :
        return self.checkfile(self.outfile, None)
