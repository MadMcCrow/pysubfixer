#! /usr/env python
# cli/exception.py : handle ffmpeg errors 

# global variable
class FFmpegException(Exception):
    """simple error class to avoid abusing python's builtins"""
