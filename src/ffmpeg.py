#! /usr/env python
# ffmpeg/ffmpeg.py : FFMpeg controls written in a pythonic way

# python
import os
import asyncio
import shlex
import shutil
import sys
from typing import List, Callable


class FFmpeg() :
    """
        class to represent an instance of ffmpeg running in the background
    """
    
    # the ffmpeg binary name changes depending on platform
    command = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"


    class Exception(Exception):
        """simple error class to avoid abusing python's builtins"""


    class Input() :
        """
            class to represent an input for ffmpeg
            TODO : check that you can actually have multiple options for inputs
        """

        def __init__(self, filepath : str, options : str = "") :
            self._p = filepath
            self._o = options

        def __str__(self) -> str :
            """get the string that needs to be sent to ffmpeg"""
            return f"{self._o} -i '{self.path()}'"

        def path(self) -> str: 

            """return the path only"""
            return os.path.abspath(self._p)
        def exists(self) -> bool :

            """check input validity"""
            return os.path.exists(self.path())


    class Arguments() :
        """
            class to represent an ffmpeg command
            TODO : expand and improve
        """
        def __init__(self, inputs : list , outputfile : str, outputoptions = '') : 
            self.__in = inputs
            self.__out = os.path.abspath(outputfile)
            self.__outopts = outputoptions

        def __str__(self) -> str : 
            instr = " ".join(map(str, self.inputs))
            outstr = f"{self.__outopts} {self.__out}"
            return f"{instr} {outstr}"

        def to_shargs(self) :
            return shlex.split(str(self))

        def input_files(self) ->List[str] :
            return [x.path() for x in self.inputs]

        @property
        def inputs(self) :
            return self.__in

        @inputs.setter
        def inputs(self, paths : list) :
            self.__in = []
            for x in paths : 
                if isinstance(x, str)  :
                    x = FFmpegInput(x)
                if x.exists() :
                    self.__in.append(x)
                else :
                    raise FileNotFoundError(f"file {x.path()} does not exists !")


    class  Output() :
        """
            class to handle stdout and stderr of ffmpeg
        """
        @staticmethod
        def _time() :
            return time.now()

        def __init__(self, args : str, name = None) -> None:
            self.name = name
            self.__cmd = ' '.join(args)
            self.__start = _time()
            self.__end = None
            self.__out = {}
            self.__err = {}

        def stdout(self, instr : str) -> None :
            self.__out[_time()] = instr
        def stderr(self, instr : str) -> None :
            self.__err[_time()] = instr
        def __str__(self) -> str:   
            res = ""
            for (k,v) in self.__out.items() :
                res += v + '\n'
            return res
        def log(self) -> str :
            """
                write as a log
            """
            l = []
            for (k,v) in self.__out.items() :
                l.append(f'<{k}> - {v}')
            for (k,v) in self.__err.items() :
                l.append(f'<{k}> - ERROR : {v}')
            l.sort()
            l.insert(0, f"'{self.__cmd}' started at {self.__start}")
            l.append(f'execution took {self.duration()}')
            return '\n'.join(l)
        def close(self, fut) :
            self.__end = _time()
        def duration(self) :
            if self.__end is not None :
                return self.__end - self.__start 
            return _time() - self.__start


    @staticmethod
    def check_file(filepath : str) :
        """
            make sure file exist
        """
        if not path.exists(path.abspath(filepath)) :
            raise FileNotFoundError(f"{filepath} does not exists")

    @staticmethod
    def check_FFmpeg() :
        """
            make sure ffmpeg is installed
        """
        pathbin = shutil.which(self.command)
        if not os.path.exists(pathbin) :
            raise EnvironmentError(f"{command} is not available")
   
    def __init__(self, arguments :  Arguments,  on_finished : Callable| None = None) :
        """
            create ffmpeg process and start async task
        """
        # copy to our object
        self.args = arguments
        self._cb = on_finished
        # check ffmpeg is available :
        check_FFmpeg()
        # check that all files exists :
        [check_file(x) for x in arguments.input_files()]
        # if we're in a simulation, print and exit :
        try : 
            if globals()["simulate"] :
                print(self.args)
                sys.exit(0)
        except :
            pass
        # else start the process :
        loop = asyncio.get_running_loop()
        self._out = FFmpegStdio()
        self._task = loop.create_task(_execute, name="ffmpeg")
        self._task.add_done_callback(on_finished)

    def is_running(self) -> bool :
        """
            returns true if ffmpeg is running in the background
        """
        try:
            if self._task.cancelled() or self._task.done() :
                return False
        except :
            return False
        finally :
            return True

    async def _execute(self) :
        """
            async method running the actual subprocess
        """
        _pipe = asyncio.subprocess.PIPE
        ps = await asyncio.create_subprocess_exec(self.command, self.args.to_shargs(), stdin =_pipe, stdout=_pipe)
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.__read_stream(ps.stdout, self._out.stdout ))
            tg.create_task(self.__read_stream(ps.stderr, self._out.stderr ))
        rc = await ps.wait()
        return self._out

    def _on_finish(self, fut) :
        """
            called on task completion
        """
        if self._cb is not None :
            self._cb()

    async def __read_stream(self, stream, cb):
        """
            read stream, non-blocking
        """
        while True:
            line = await stream.readline()
            if line:
                cb(line.decode(locale.getencoding()))
            else:
                break