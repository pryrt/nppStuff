# encoding=utf-8
"""https://community.notepad-plus-plus.org/topic/23149/find-and-replace-with-increments/4

This will start by matching text from `{` at the beginnig of a line to `}` or `},` at the beginning of a line

Inside those groups, it will replace all "zone_#" or "zone #" with the value of the counter
The counter will increment between `{...}` groups
"""
from Npp import *
import re

counter = 1

def replace_group(m):
    global counter
    out = re.sub(r'(?<=zone[ _])\d+', str(counter), m.group(0))
    counter = counter + 1
    return out

console.clear()
editor.beginUndoAction()
editor.rereplace(r'(?s)^{\h*$.*?^},?\h*$', replace_group)
editor.endUndoAction()
