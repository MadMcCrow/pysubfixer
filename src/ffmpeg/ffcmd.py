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

    def __init__(self) :
        self.is_running = False

    def _execute(self, cmd) :
        self._cmd = cmd
        self.daemon = pycall.run(self._cmd, on_end_f = self.on_finished)

    def on_finished(self, return_code) :
        print("finished running cmd")
        self.is_running = False
        pass

    def wait(self) :
        pycall.wait(self.daemon)


