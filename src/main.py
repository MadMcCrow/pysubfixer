# main.py :
# main application
# imports :
from sys import exit
from argparse import ArgumentParser
from ffmpeg import delay_subs, remove_subs, embed_subs
from gui import runApplication
try :
    from rich import print
except:
    from builtins import print


# global variable
_simulate = False

def print_command(cmd : dict) :
    """
    print what will be done
    """
    text = f'adding {cmd["subs"]} to {cmd["source"]}'
    if cmd["delay"] != 0 :
        print(f'{text}, delayed by {cmd["delay"]} seconds')
    else :
        print(text)


def parse_args() :
    """
    parse command line arguments and/or generate errors for the user
    """
    parser = ArgumentParser(description="Fix your subtitles with this amazing script !")
    subparsers = parser.add_subparsers(description='available subcommands')
    #TODO allow for asking for GUI
    parser_main = subparsers.add_parser('<main_command_name>')
    #parser.add_argument("video_file", help="input video file")
    parser_main.add_argument("video_file", help="input video file")
    parser_main.add_argument("subtitle_file", help="input subtitle file")
    parser_main.add_argument("-d", "--delay", type=int, help="delay amount in seconds")
    parser_main.add_argument("-s", "--simulate", action="store_true", help="Enable simulate mode")
    args = parser.parse_args()
    global _simulate
    _simulate = args.simulate
    # return a dict
    return {
        "source": args.video_file,
        "subs"  : args.subtitle_file,
        "delay" : args.delay if args.delay is not None else 0,
     }

def cmd(command : dict) :
    """
    Execute ffmpeg command to embed the sub
    """
    try:
        newsubs = delay_subs(command["subs"], command["delay"])
        nosubs = remove_subs(command["source"])
        embed_subs(nosubs, newsubs)
        exit(0)
    except Exception as e:
        errors = str(e).splitlines()
        error_lines = min(len(errors), 10)
        print(f'there were errors running ffmpeg : (last {error_lines} lines) :')
        print('\n'.join(errors[-error_lines:]))
        exit(1)

def cli() :
    """
    call the CLI app
    """
    command = parse_args()
    cmd(command)
    


def gui() :
    """
    call the gui app !
    """
    runApplication(cmd)
    

# execute !
if __name__ == "__main__":
    gui()

