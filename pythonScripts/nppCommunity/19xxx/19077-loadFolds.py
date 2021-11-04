# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/19077/

Loads current fold state

"""
from Npp import *

console.show()
console.clear()

currentID = notepad.getCurrentBufferID()

notepad.messageBox("About to load the folding file\nPlease enter appropriate path/filename in Open dialog")
notepad.menuCommand(MENUCOMMAND.FILE_OPEN)
#notepad.menuCommand(MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW) # toggle to other view

foldList = dict()

def readFoldingLevel(contents, lineNumber, totalLines):
    global foldList
    #console.write(contents)
    if contents.strip():    # if it's not a blank line
        lstr, fstr, fbool = contents.strip().split(',')
        #console.write("{}/{}/{}\n".format(lstr,fstr,fbool))
        foldList[ int(lstr) ] = (fbool == 'True')

editor.forEachLine(readFoldingLevel)
notepad.close()
#print(foldList)
notepad.activateBufferID(currentID)

def applyFoldingLevel(contents, lineNumber, totalLines):
    global foldList
    #key = "{}".format(lineNumber)
    if lineNumber in foldList:  # make sure it exists
        state = foldList[ lineNumber ]
        editor.setFoldExpanded(lineNumber, state)

editor.forEachLine(applyFoldingLevel)
