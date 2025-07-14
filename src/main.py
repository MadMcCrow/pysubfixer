#! /usr/env python
# main.py :
# main function entry point for apps


# global variable
_simulate = False

def cli() :
    """
    call the CLI app
    """
    from cli import cli_app
    cli_app()
    
def gui() :
    """
    call the gui app !
    """
    from gui import qt_app
    qt_app()
    
# execute !
if __name__ == "__main__":
    gui()

