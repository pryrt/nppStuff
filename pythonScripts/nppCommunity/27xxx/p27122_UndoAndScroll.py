# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27122/

This does the UNDO then tries to scroll to approximate center
"""
from Npp import editor

# undo
editor.undo()

# find location after undo
pc = editor.getCurrentPos()
c = editor.lineFromPosition(pc)
editor.gotoLine(1)
editor.gotoLine(c)
editor.setCurrentPos(pc)

# try to center it
# this is counting >1 for a wrapped line, whereas the "Line" commands are logical line, but close enough
h = editor.linesOnScreen()
f = editor.getFirstVisibleLine()
s = int(c - h/2)

#console.write(f"h={h}, f={f}, c={c}, s={s}\n")
editor.lineScroll(0, s)

del(pc)
del(c)
del(h)
del(f)
del(s)
