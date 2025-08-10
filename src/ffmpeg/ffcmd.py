#! /usr/env python
# ffmpeg/command : a wrapper around calling ffmpeg, ffprobe or ffplay with python

import os
import asyncio
from typing import Optional


import pycall


class FFcmd() :
    """
        A class to launch ffmpeg commands, including ffplay and ffprobe
    """

    def _execute(self) :
        shellcmd = f"{self.cmd} {' '.join(self.args)}"
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

    @classmethod
    def checkfile(cls, file, should_exist : Optional) -> str :
        """
            used to make sure inputs exist, and outputs don't 
            this method can will call an handler for conflicts if it exists
        """
        truepath = os.path.relpath(os.path.realpath(file)) # shorter true version of path
        if should_exist is not None :
            if os.path.exists(truepath) != should_exist :
                try :
                    cls.conflict_handler(file, should_exist)
                except :
                    if should_exist :
                        raise FileNotFoundError(file)
                    else :
                        raise FileExistsError(file)
        return str(truepath)