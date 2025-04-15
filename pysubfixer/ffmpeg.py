#! /usr/env python

# global variable
class FfmpegError(Exception):
    """simple error class to avoid abusing python's builtins"""

def ffmpeg_command(inputfiles : list, outputfile : str, inputoptions = '', outputoptions = '' ) :
    """run a ffmpeg command"""
    from subprocess import run
    from shlex import split
    command = ' '.join(['ffmpeg', inputoptions, ' '.join(map(lambda x: f'-i {x}', inputfiles)), outputoptions, outputfile])
    simulate = globals()["simulate"] if "simulate" in globals() else False
    if simulate :
        print(f'would run : {command}')
        return
    else : 
        result = run(split(command), capture_output=True, text=True)
    errors = result.stderr
    if errors :
        raise FfmpegError(errors)


def delay_subs(inputfile, seconds, simulate = False) -> str :
    """delay a srt file"""
    if seconds == 0 :
        return inputfile
    from os.path import splitext
    name, extension = splitext(inputfile)
    output = f'{name}-delayed{seconds}s{extension}'
    ffmpeg_command( 
        inputfiles = [inputfile],
        inputoptions = f'-itsoffset {seconds}',
        outputfile= output,
        outputoptions = '-c copy',
    )
    return output
        
def remove_subs(inputfile) :
    """remove all subs from a file"""
    from os.path import splitext
    name, extension = splitext(inputfile)
    output = f'{name}-no_subs{extension}'
    ffmpeg_command( 
        inputfiles = [inputfile],
        outputoptions = '-map 0 -c copy -sn',
        outputfile= output)
    return output

def embed_subs(video, srt) :
    """embed an srt file in your video"""
    from os.path import splitext
    name, extension = splitext(video)
    output = f'{name}-embedded{extension}'
    ffmpeg_command( 
        inputfiles = [video, srt],
        outputoptions = '-c copy -c:s mov_text',
        outputfile= output)
    return output

def parse_args() :
    """parse command line arguments and/or generate errors for the user"""
    import argparse
    parser = argparse.ArgumentParser(description="Fix your subtitles with this amazing script !")
    parser.add_argument("video_file", help="input video file")
    parser.add_argument("subtitle_file", help="input subtitle file")
    parser.add_argument("-d", "--delay", type=int, help="delay amount in seconds")
    parser.add_argument("-s", "--simulate", action="store_true", help="Enable simulate mode")
    args = parser.parse_args()
    global simulate
    simulate = args.simulate
    # return a dict
    return {
        "source": args.video_file,
        "subs"  : args.subtitle_file,
        "delay" : args.delay if args.delay is not None else 0,
     }
