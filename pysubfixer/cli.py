#! /usr/env python

# global variable
simulate = False

from main import main
try :
    from rich import print
except:
    from builtins import print


# TODO :
# - add auto detect subtitles and remove them 

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

def print_command(cmd : dict) :
    """print what will be done"""
    text = f'adding {cmd["subs"]} to {cmd["source"]}'
    if cmd["delay"] != 0 :
        print(f'{text}, delayed by {cmd["delay"]} seconds')
    else :
        print(text)


def cli() :
    command = parse_args()
    main(command)

# execute !
if __name__ == "__main__":
    cli()