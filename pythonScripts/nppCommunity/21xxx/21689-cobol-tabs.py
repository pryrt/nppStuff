# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21689/"""
from Npp import *

cols = (7,8,12, 72)
pixperchar = 8

def set_tab_via_callback():
    for linenum in range(editor.getLineCount()):
        editor.clearTabStops(linenum)
        for tabcol in cols:
            editor.addTabStop(linenum, tabcol*pixperchar)

set_tab_via_callback()
