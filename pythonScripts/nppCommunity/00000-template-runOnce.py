# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/NNNNNN/

other notes go here
"""
from Npp import *

def forum_postNNNNN_FunctionName():
    """this is the function's doc string"""
    console.show()
    console.clear()
    console.write(__file__ + "::" + __name__ + "\n")
    if forum_postNNNNN_FunctionName.__module__:
        console.write("module: " + forum_postNNNNN_FunctionName.__module__ + "\n")
    console.write("function docstring: ''" + forum_postNNNNN_FunctionName.__doc__ + "''\n")
    console.write("file     docstring: ''" + __doc__.rstrip() + "''\n")

if __name__ == '__main__': forum_postNNNNN_FunctionName()
