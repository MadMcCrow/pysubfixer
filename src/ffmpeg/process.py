#! /usr/env python
# cli/process.py : call ffmpeg

from subprocess import run
from shlex import split
from exception import FfmpegException

def ffmpeg_process(inputfiles : list, outputfile : str, inputoptions = '', outputoptions = '' ) :
    """
    run a ffmpeg command
    """
    command = ' '.join(['ffmpeg', inputoptions, ' '.join(map(lambda x: f'-i {x}', inputfiles)), outputoptions, outputfile])
    simulate = globals()["simulate"] if "simulate" in globals() else False
    if simulate :
        print(f'would run : {command}')
        return
    else : 
        result = run(split(command), capture_output=True, text=True)
    errors = result.stderr
    if errors :
        raise FfmpegException(errors)

