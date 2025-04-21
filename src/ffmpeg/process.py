#! /usr/env python
# cli/process.py : call ffmpeg

from os import path
from subprocess import run
from shlex import split
from .exception import FFmpegException

def checkFile(filepath : str) :
    """
    make sure file exist
    """
    print(f"target = {path.abspath(filepath)}")
    if not path.exists(path.abspath(filepath)) :
        raise FileNotFoundError(f"{filepath} does not exists")
    pass


def checkFFmpeg() :
    """
    make sure ffmpeg is installed
    """
    pass

def ffmpeg_process(inputfiles : list, outputfile : str, inputoptions = '', outputoptions = '' ) :
    """
    run a ffmpeg command
    """
    # perform checks :
    [checkFile(x) for x in inputfiles]
    # build command
    command = ' '.join(['ffmpeg', inputoptions, ' '.join(map(lambda x: f'-i {x}', inputfiles)), outputoptions, outputfile])
    simulate = globals()["simulate"] if "simulate" in globals() else False
    if simulate :
        print(f'would run : {command}')
        return
    else : 
        result = run(split(command), capture_output=True, text=True)
    errors = result.stderr
    if errors :
        raise FFmpegException(errors)



