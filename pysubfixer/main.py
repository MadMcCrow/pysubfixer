# the main command :
from ffmpeg import delay_subs, remove_subs, embed_subs, FfmpegError
from sys import exit

def main(command : dict ) :
    try:
        newsubs = delay_subs(command["subs"], command["delay"])
        nosubs = remove_subs(command["source"])
        embed_subs(nosubs, newsubs)
        exit(0)
    except FfmpegError as e:
        errors = str(e).splitlines()
        error_lines = min(len(errors), 10)
        print(f'there were errors running ffmpeg : (last {error_lines} lines) :')
        print('\n'.join(errors[-error_lines:]))
        exit(1)
