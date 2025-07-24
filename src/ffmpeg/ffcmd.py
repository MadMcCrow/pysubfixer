#! /usr/env python
# ffmpeg/command : a wrapper around calling ffmpeg, ffprobe or ffplay with python

import os

from typing import List

import pycall


class FFcmd() :
    """
        A class to launch ffmpeg commands, including ffplay and ffprobe
    """ 

    def __init__(self) :
        pass

    def _execute(self, cmd) :
        self.__runner = pycall.run(cmd)
        




    