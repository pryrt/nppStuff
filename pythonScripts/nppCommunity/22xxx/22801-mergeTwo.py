# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/22801/

Put FILE1.xml (the destination) in the left/main view.
Put FILE2.xml (the source with the lines to be copied) in the right/second view
    (View > Move/Clone Current Document > Move to Other View or
    Right Click on the title and Move to Other View)

"""
from Npp import editor1,editor2,notepad,MESSAGEBOXFLAGS

notepad.messageBox("Ensure that FILE1.xml destination is in view1\nand FILE2.xml source is in view2\nOK if good, CANCEL to stop the script", "Setup Views", MESSAGEBOXFLAGS.OKCANCEL)

def processLineInDestination(contents, lineNumber, totalLines):
    if contents.strip() != "":
        return 1

    srctxt = nextNonblankFromSource()
    if srctxt == None:
        return 1
    editor1.replaceLine(lineNumber, srctxt)
    return 1

def nextNonblankFromSource():
    myLine = ""
    while myLine.strip() == "":
        if nextNonblankFromSource.counter >= editor2.getLineCount():
            return None
        myLine = editor2.getLine(nextNonblankFromSource.counter).rstrip()
        nextNonblankFromSource.counter += 1

    return myLine

editor1.beginUndoAction()
nextNonblankFromSource.counter = 0
editor1.forEachLine(processLineInDestination)
editor1.endUndoAction()
