# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25396/

Finds the first line _number_ in the active View.
Scrolls the other View to have that same line number as the first visible line.
"""
from Npp import editor,editor1,editor2

class SynchronizeBothViewsByLineNumber(object):
    def __init__(self):
        a = editor.getFirstVisibleLine()
        b = editor1.getFirstVisibleLine()
        c = editor2.getFirstVisibleLine()
        console.write("{} {} {}\n".format(a,b,c))
        editor1.setFirstVisibleLine(a)
        editor2.setFirstVisibleLine(a)

SynchronizeBothViewsByLineNumber()
