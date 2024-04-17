# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25699/

Alternative to **Search > Goto... > Line** , but attempts to center the new active line in the display

INSTALLATION INSTRUCTIONS:
See https://community.notepad-plus-plus.org/topic/23039/faq-how-to-install-and-run-a-script-in-pythonscript
You may want to give it a shortcut, per the instructions in the FAQ.  If you pick `Ctrl+G`, you will need
to use Shortcut Mapper to CLEAR the shortcut for "Goto..." in the SEARCH category of the MAIN tab of the Shortcut Mapper.
"""
from Npp import editor,notepad,console

def gotoLineCentered_25699():
    whichLine = int(notepad.prompt("Which Line? ","Goto Line (Centered)")) - 1          # notepad.prompt()...
    pc = editor.getCurrentPos()
    c = editor.lineFromPosition(pc)
    editor.gotoLine(whichLine)
    editor.scrollCaret()

    # this is counting >1 for a wrapped line, whereas the "Line" commands are logical line, but close enough
    h = editor.linesOnScreen()

    if whichLine > c:
        editor.lineScroll(0,h/2)
    elif whichLine < c:
        editor.lineScroll(0, -h/2)

    return

    # I had originally used something like below, but when moving up and down, it didn't always
    # center it, despite the scrollRange.  So I switched to the above sequence, where I just scroll to the caret,
    # then either half-height above or below depending on which direction I scrolled
    #####OLD##### # half the height above the new line
    #####OLD##### f = whichLine - h/2
    #####OLD##### if f<0: f = 0
    #####OLD##### pf = editor.positionFromLine(f)
    #####OLD#####
    #####OLD##### # half the height below the new line
    #####OLD##### s = whichLine + h/2
    #####OLD##### if s>editor.getLineCount():
    #####OLD#####     s = editor.getLineCount()
    #####OLD#####     editor.scrollToEnd()
    #####OLD#####     editor.lineScroll(0, -h/2)
    #####OLD#####
    #####OLD##### ps = editor.positionFromLine(s)
    #####OLD#####
    #####OLD##### console.write("{} {} {}\n".format(f, pf, ps))
    #####OLD##### #editor.setFirstVisibleLine(f)
    #####OLD##### editor.scrollRange(ps, pf)
    #####OLD##### editor.scrollCaret()

gotoLineCentered_25699()
del(gotoLineCentered_25699)
