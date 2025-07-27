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
        pycall.run(cmd, on_end_f = self.on_finished)
        self.is_running = True

    def on_finished(self, return_code) :
        print("finished running cmd")
        self.is_running = False
        pass

    async def wait(self) :
        idx = 0
        characters = ['.  ', '.. ', '...']
        while self.is_running :
            idx = idx % len(characters)
            print("please wait" + characters[idx], end='\r')
            await asyncio.sleep(0.2)
            idx += 1