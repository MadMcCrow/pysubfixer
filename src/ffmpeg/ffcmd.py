#! /usr/env python
# ffmpeg/command : a wrapper around calling ffmpeg, ffprobe or ffplay with python

import os
import asyncio
from typing import List


import pycall


class FFcmd() :
    """
        A class to launch ffmpeg commands, including ffplay and ffprobe
    """ 


    cmd : str = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
    args = []

    def _execute(self) :
        shellcmd = f"{cmd} {' '.join(args)}"
        print(f"execute : {shellcmd}")
        return 
        self.daemon = pycall.run(shellcmd,
        # callbacks 
        on_end_f = self._on_finished, 
        stdout_f = self.stdout, 
        stderr_f = self.stderr)
      
    def _on_finished(self, out : pycall.Output) :
        pass

    def stdout(self, stream : str) :
        pass

    def stderr(self, stream : str) :
        pass