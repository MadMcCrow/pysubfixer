#! /usr/env python
# cli/subs : a wrapper around calling ffmpeg, ffprobe or ffplay with python

# python
import os
from typing import Callable
from concurrent.futures import ThreadPoolExecutor

import pycall

# ours 
from ffmpeg import FFmpeg

class CliHandler(FFmpeg) :
    @classmethod
    def conflict_handler(cls, file, is_input ) :
        if is_input :
            raise FileNotFoundError(file)
        else :
            # TODO : ask before deletion !
            print(f"{file} already exists: writing over !")
            os.remove(file)

class RemoveSubs(CliHandler) :
    def __init__(self, video) :
        output = "{}.sn{}".format(*os.path.splitext(video)) 
        super().__init__(video, output=output, options="-c:v copy -c:a copy -sn" )


class DelaySubs(CliHandler) :
    def __init__(self, subs, delay :int = 0) :
        output = "{0}.{2}{1}".format(*(os.path.splitext(subs) + (delay,)))
        super().__init__(subs, output=output, options=f"-itsoffset {delay}" )



def fix_subs( subs : str, video : str , delay : int, output : str, on_finished : Callable) :
    """
        main command of pysubfixer
    """

    remsub = RemoveSubs(video)
    delsub = DelaySubs(subs)
    with ThreadPoolExecutor(max_workers=4) as pool:
        pool.submit(pycall.wait(remsub.daemon, delsub.daemon))
    on_finished()
