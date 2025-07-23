#! /usr/env python
# ffmpeg/ffmpeg.py : FFMpeg controls written in a pythonic way

# python
import os
import asyncio
import shlex
import shutil
import sys
from datetime import datetime
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
            self.inputs = inputs
            self.__out = os.path.abspath(outputfile)
            self.__outopts = outputoptions

        def __str__(self) -> str : 
            instr = " ".join(map(str, self.inputs))
            outstr = f"{self.__outopts} '{self.__out}'"
            return f"{instr} {outstr}"

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
                    x = FFmpeg.Input(x)
                if x.exists() :
                    self.__in.append(x)
                else :
                    raise FileNotFoundError(f"file {x.path()} does not exists !")

        def __iter__(self) : 
            for elem in self.inputs :
                yield str(elem)


    @staticmethod
    def check_file(filepath : str) :
        """
            make sure file exist
        """
        if not os.path.exists(os.path.abspath(filepath)) :
            raise FileNotFoundError(f"{filepath} does not exists")

    classmethod
    def check_FFmpeg(cls) :
        """
            make sure ffmpeg is installed
        """
        pathbin = shutil.which(cls.command)
        if not os.path.exists(pathbin) :
            raise EnvironmentError(f"{command} is not available")
   
    def __init__(self, arguments :  Arguments | tuple,  on_finished : Callable| None = None) :
        """
            create ffmpeg process and start async task
            #TODO : move to kwargs to arguments
        """
        # copy to our object
        if isinstance(arguments, tuple) :
            arguments = FFmpeg.Arguments(*arguments)
        self.args = arguments
        self._cb = on_finished
        # check ffmpeg is available :
        self.check_FFmpeg()
        # check that all files exists :
        [self.check_file(x) for x in arguments.input_files()]
        # if we're in a simulation, print and exit :
        try : 
            if globals()["simulate"] :
                print(self.args)
                sys.exit(0)
        except :
            pass
        self._task = None
    
    async def start(self) :
        self._out = FFmpeg.Output()
        await self._execute()
        async for stdout, stderr in self._stream():
            if stdout:
                self._out.stdout(stdout)
            if stderr:
                self._out.stderr(stderr)
        rc = await self.wait()

    async def wait(self) :
        if self.ps is None:
            return None
        rc = await self.ps.wait()
       
 
                
    async def _execute(self) :
        """
            async method running the actual subprocess
        """
        spl = shlex.split(f"{self.command} {str(self.args)}")
        print(f"CMD = {self.command} {str(self.args)}")
        print(f"SPL = {spl}")
        sys.exit()
        self.ps = await asyncio.create_subprocess_exec(spl[0], *spl[1:], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    def _on_finish(self, fut) :
        """
            called on task completion
        """
        if self._cb is not None :
            self._cb()


    async def _stream(self):
        """
            read stream, non-blocking
        """
        while True:
            if self.ps.stdout.at_eof() and self.ps.stderr.at_eof():
                break
            stdout = await self.ps.stdout.readline()
            stderr = await self.ps.stderr.readline()
            yield stdout.decode(), stderr.decode()
            await asyncio.sleep(0.1) # TODO store in variable

    def get_progress(self) :
        pass