# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25699/

other notes go here
"""
from Npp import editor,notepad,console

def gotoLineCentered_25699():
    whichLine = int(notepad.prompt("Which Line? ","Goto Line (Centered)")) - 1          # notepad.prompt()...
    editor.gotoLine(whichLine);
    # in an ideal world, I would get the height of the visible window, but
    #   while editor.getFirstVisibleLine() will show the top, I cannot (yet) find the height or bottom
    f = whichLine - 10
    if f<0: f = 0
    s = whichLine + 10
    if s>editor.getLineCount(): s = editor.getLineCount()
    pf = editor.positionFromLine(f)
    ps = editor.positionFromLine(s)
    #console.write("{} {} {}\n".format(f, pf, ps))
    #editor.setFirstVisibleLine(f)
    editor.scrollRange(ps, pf)

gotoLineCentered_25699()
del(gotoLineCentered_25699)
