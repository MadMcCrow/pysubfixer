#! /usr/env python
# gui/main.py : run as pyQt App
from sys import argv
from PyQt6.QtWidgets import QApplication
from mainwidget import MainWidget
from ffmpeg import delay_subs, remove_subs, embed_subs

def cmd(command : dict) :
    """
    execute the ffmpeg command
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
def main() :
    """
    Main GUI function
    """
    myApp = QApplication(argv)
    widget = MainWidget(runcmd=cmd)
    widget.show()
    myApp.exec()

# execute !
if __name__ == "__main__":
    main()

