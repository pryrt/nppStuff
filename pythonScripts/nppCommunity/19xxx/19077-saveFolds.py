# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/19077/

Saves current fold state

"""
from Npp import *

#console.show()
#console.clear()

foldstr = ""

def saveFoldingLevel(contents, lineNumber, totalLines):
    global foldstr
    if editor.getFoldLevel(lineNumber)>0:
        foldstr += "{},{},{}\n".format(
            lineNumber,
            editor.getFoldLevel(lineNumber),
            editor.getFoldExpanded(lineNumber)
        )
        #console.write("#{}/{}# foldLevel={} ({})\n".format(lineNumber, totalLines, editor.getFoldLevel(lineNumber)&FOLDLEVEL.NUMBERMASK-0x400, editor.getFoldLevel(lineNumber)))

editor.forEachLine(saveFoldingLevel)
#console.write(foldstr)

notepad.new()
editor.setText(foldstr)
notepad.messageBox("About to save the folding file\nPlease enter appropriate path/filename in SaveAs dialog")
notepad.menuCommand(MENUCOMMAND.FILE_SAVEAS)
notepad.close()