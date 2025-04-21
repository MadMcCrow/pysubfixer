#! /usr/env python
# ffmpeg.py : various ffmpeg command functions

# import our runner
from .process import ffmpeg_process


def delay_subs(inputfile, seconds) -> str :
    """
    delay a srt file by x seconds
    """
    if seconds == 0 :
        return inputfile
    from os.path import splitext
    name, extension = splitext(inputfile)
    output = f'{name}-delayed{seconds}s{extension}'
    ffmpeg_process( 
        inputfiles = [inputfile],
        inputoptions = f'-itsoffset {seconds}',
        outputfile= output,
        outputoptions = '-c copy',
    )
    return output
        
def remove_subs(inputfile) :
    """
    remove all subs from a file
    """
    from os.path import splitext
    name, extension = splitext(inputfile)
    output = f'{name}-no_subs{extension}'
    ffmpeg_process( 
        inputfiles = [inputfile],
        outputoptions = '-map 0 -c copy -sn',
        outputfile= output)
    return output

def embed_subs(video, srt) :
    """
    embed an srt file in your video
    """
    from os.path import splitext
    name, extension = splitext(video)
    output = f'{name}-embedded{extension}'
    ffmpeg_process( 
        inputfiles = [video, srt],
        outputoptions = '-c copy -c:s mov_text',
        outputfile= output)
    return output

