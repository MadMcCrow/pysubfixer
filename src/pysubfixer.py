#! /usr/env python
# application :

# python
from argparse import ArgumentParser
from typing import Callable
import os, sys
# rich printing
try :
    from rich import print
except:
    from builtins import print

# pycall
import pycall

# ours :
from ffmpeg import FFmpeg


def fix_subs( subs : str, video : str , delay : int, output : str, on_finished : Callable) :
    """
        main command of pysubfixer
    """
    sn = "{}.sn{}".format(*os.path.splitext(video)) 
    if os.path.exists(sn) :
        os.remove(sn)
    deletesubs = FFmpeg( inputs = video, output=sn, options="-c:v copy -c:a copy -sn")
    sd = "{0}.{2}{1}".format(*(os.path.splitext(subs) + (delay,)))
    if os.path.exists(sd) :
        os.remove(sd)
    movesubs = FFmpeg(f"{subs} -itsoffset {delay} {sd}")
    pycall.wait(deletesubs, movesubs)
    on_finished()


def cli() :
    """
        command line tool : parse command line arguments and/or generate errors for the user
    """
    parser = ArgumentParser(description="Fix your subtitles with this amazing script !")
    #subparsers = parser.add_subparsers(description='available subcommands')
    parser.add_argument("video_file", help="input video file")
    parser.add_argument("subtitle_file", help="input subtitle file")
    parser.add_argument("-d", "--delay", type=int, help="delay amount in seconds", default=0)
    parser.add_argument("-o", "--output", help="output file", default=None)
    parser.add_argument("-s", "--simulate", action="store_true", help="Enable simulate mode")
    args = parser.parse_args(sys.argv[1:])
    global _simulate
    _simulate = args.simulate
    # make sure to have a good output file name :
    output = args.output if args.output is not None else "{0}.pysubfix-{2}.{1}".format(*(os.path.splitext(args.video_file) + (args.delay,)))
    fix_subs(
        subs  = args.subtitle_file,
        video = args.video_file,
        delay = args.delay, 
        output= output, 
        on_finished=sys.exit )
     

def gui() :
    """
    import and run the qt app
    """
    from gui import qt_app
    qt_app()
    
# prefer GUI
if __name__ == "__main__":
    gui()


