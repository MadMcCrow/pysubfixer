#! /usr/env python
# ffmpeg/command : a wrapper around calling ffmpeg, ffprobe or ffplay with python

import os
import asyncio
from pathlib import Path
from typing import Optional
from datetime import timedelta
import re


import pycall


class FFcmd() :
    """
        A class to launch ffmpeg commands, including ffplay and ffprobe
    """

    daemon : Optional[pycall.Daemon] = None

    def _execute(self) :
        shellcmd = f"{self.cmd} {' '.join(self.args)}"
        print(f"execute : {shellcmd}")
        self.daemon = pycall.run(shellcmd,
        # callbacks 
        on_end_f = self._on_finished, 
        stdout_f = self.stdout, 
        stderr_f = self.stderr,
        name = self.cmd)

    def _on_finished(self, out : pycall.Output) :
        pass


    def stdout(self, stream : str) :
        self.parse_input(stream)


    def stderr(self, stream : str) :
        self.parse_input(stream)


    @classmethod
    def checkfile(cls, file : str, should_exist : Optional) -> str :
        """
            used to make sure inputs exist, and outputs don't 
            this method can will call an handler for conflicts if it exists
        """
        truepath = Path(file.strip('\''))
        try :
            if truepath.is_dir() :
                raise IsADirectoryError(f"{file} is a directory !")
            if should_exist is not None :
                if truepath.exists() != should_exist:
                        if should_exist :
                            raise FileNotFoundError(file)
                        else :
                            raise FileExistsError(file)  
        except Exception as E:
            truepath = cls.conflict_handler(file, E)
        finally :
            return f"'{str(truepath)}'"

    
    def parse_input(self, line) :
        """
            Duration line may look like : 
            > Duration: 01:54:58.90, start: 0.000000, bitrate: 1938 kb/s
        """
        try :
            l = line.strip()
            if l.startswith("Duration") :
                m = re.match(r"Duration: (\d+:\d+:\d+\.\d+),\W+start: (\d+\.\d+),\W+bitrate: (\d+\.?\d*) ([km]+b/s)", l)
                v = list(m.groups())
                self.duration = self.parse_time(str(v[0]))
                self.start = float(v[1])
                self.bitrate = float(v[2])
                self.btunit = v[3]
        except :
            pass

    @staticmethod
    def parse_time( timestr : str) -> timedelta :
        try :
            m = re.match(r"(\d+):(\d+):(\d+\.\d+)", timestr)
            v = list(m.groups())
            return timedelta(hours=int(v[0]),minutes=int(v[1]),seconds=float(v[2]))
        except :
            return timedelta()


    def is_running(self) -> bool : 
        return self.daemon.is_running()
