#! /usr/bin/env python
# Simple install script for installing the GUI on windows

# basic import
from os import name as osname
from os.path import abspath
from subprocess import check_call
from sys import executable, exit
from shutil import copy2 as cp
import argparse

_src = "pysubfixer"
_target = "gui"

def dependencies() : 
    try :
        if osname == 'nt':
            print ("installing PyQt6 ...")
            check_call([executable, '-m', 'pip', 'install', 'PyQt6'])
            print ("installing pyinstaller ...")
            check_call([executable, '-m', 'pip', 'install', 'pyinstaller'])
        else :
            raise NotImplementedError("This installer only supports windows")
    except Exception as E :
        print(f'failed to install dependencies : {E}')
        raise Exception()

def build() :
    try : 
        import PyInstaller.__main__ as installer
        build = installer.run([
            f'{_src}/{_target}.py',
            '--clean',
            '--noconfirm',
            '--noupx',
            '--onedir',
            '--onefile',
            '--windowed',
            '--collect-all',
            'PyQt6.sip',
        ])
    except Exception as E :
        print(f'Failed to build with pyinstaller :{E}')
        raise Exception

def parse_args() :
    """parse command line arguments and/or generate errors for the user"""
    parser = argparse.ArgumentParser(description="Installer script for pysubfixer GUI")
    parser.add_argument("install_dir", help="where to install the final binary")
    parser.add_argument("--skip", action="store_true", help="skip the pip install commands")
    args = parser.parse_args()
    return {
        "out"  : args.install_dir,
        "deps" : not args.skip
    }

def install(path) : 
    print(f"installing to target directory : {path}")
    cp(f'./dist/{_target}', f'{abspath(path)}/{_target}.exe')


def main() :
    opts = parse_args()
    if opts['deps'] :
        dependencies()
    build()
    install(opts['out'])

if __name__ == "__main__":
    try : 
        main()
        exit(0)
    except:
        exit(1)