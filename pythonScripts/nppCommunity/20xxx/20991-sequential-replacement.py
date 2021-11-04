# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/20991/find-and-replace-automation-in-python
"""
from Npp import *

editor.beginUndoAction()

r = int( notepad.prompt("number", "Replace starting at", 1) )

for s in range(1,19):
    srch = "{:04d}".format(s)   # you showed 4-digit leading zeros
    repl = "{:04d}".format(r)   # assumed replacement also 4-digit leading zeros
    #console.write("s/{}/{}/\r\n".format(srch,repl))    # for debugging
    editor.replace(srch,repl)   # do the replacement on the first match found
    r = r + 1                   # move to next replacement integer

editor.endUndoAction()  # allows a single undo to undo all 18 replacements
