#! /usr/env python
# ffmpeg/ffmpeg.py : FFMpeg controls written in a pythonic way

# python
import os
from time import sleep
from typing import List, Optional
import re

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
        self.args = [
            "-progress pipe:1",  # make sure to send progress to stdout, and never wait for 'y'
            "-y",
            "-nostdin"]
        self.args += [ f"-i {self.checkfile(x, True)}" for x in inputs]
        if isinstance(options, str) :
            self.args.append(options)
        elif isinstance(options,list) :
            self.args += [str(x) for x in options]
        self.args.append(self.checkfile(output, False))
        # run
        self._execute()

    def output(self) :
        return self.checkfile(self.outfile, None)

    def stdout(self, stream : str) :
        """
            progress looks like this :

            bitrate=1491.6kbits/s
            total_size=144965676
            out_time_us=777527528
            out_time_ms=777527528
            out_time=00:12:57.527528
            dup_frames=0
            drop_frames=0
            speed=1.56e+03x
            progress=continue
        """
        super().stdout(stream)
        try :
            m = re.match(r"out_time=(.*)", stream.strip())
            self.time = self.parse_time(m.groups()[0])
        except AttributeError :
            pass
        else :
            print(stream.strip())
            self.daemon.progress = self.progress()


    def progress(self) -> Optional[float] :
        try :
            return self.time / self.duration
        except AttributeError:
            return None


    def est_remaining(self) :
        if self.progress() is not None :
            return self.daemon.duration() * (1.0 - self.progress())
        return None
