#! /usr/env python
# application :

# python
from argparse import ArgumentParser
from typing import Callable
import os
import sys

# rich printing
try :
    from rich import print
except:
    from builtins import print

# ours :
from .ffmpeg import FFmpeg


def fix_subs( subs : str, video : str , delay : int, output : str, on_finished : Callable) :
    """
        main command of pysubfixer
    """
    name, ext = os.path.splitext(video)
    deletesubs = FFmpeg(FFmpeg.Arguments([FFmpeg.Input(video)], f"{name}.sn.{ext}", "-c copy -sn"))
    name, ext = os.path.splitext(subs)
    movesubs = FFmpeg(FFmpeg.Arguments([FFmpeg.Input(subs, f"-itsoffset {delay}")], f"{name}.{delay}.{ext}"))
    while deletesubs.is_running() and movesubs.is_running() :
        time.sleep(0.1)
        print("please wait !")
    on_finished()


def cli() :
    """
        command line tool : parse command line arguments and/or generate errors for the user
    """
    parser = ArgumentParser(description="Fix your subtitles with this amazing script !")
    subparsers = parser.add_subparsers(description='available subcommands')
    #TODO allow for asking for GUI
    parser_main = subparsers.add_parser('<main_command_name>')
    #parser.add_argument("video_file", help="input video file")
    parser_main.add_argument("video_file", help="input video file")
    parser_main.add_argument("subtitle_file", help="input subtitle file")
    parser_main.add_argument("-d", "--delay", type=int, help="delay amount in seconds", default=0)
    parser_main.add_argument("-o", "--output", help="output file", default=None)
    parser_main.add_argument("-s", "--simulate", action="store_true", help="Enable simulate mode")
    args = parser.parse_args()
    global _simulate
    _simulate = args.simulate
    # make sure to have a good output file name :
    v, e = os.path.splitext(args.output)
    output = args.output if args.output is not None else f"{v}.pysubfix-{args.delay}.{e}"
    fix_subs(
        subs  = args.subtitle_file,
        video = args.video_file,
        delay = args.delay, 
        output= output)
     

def gui() :
    """
    import and run the qt app
    """
    from gui import qt_app
    qt_app()
    
# prefer GUI
if __name__ == "__main__":
    gui()


