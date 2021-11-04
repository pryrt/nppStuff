#https://notepad-plus-plus.org/community/topic/15971/sorting-multiple-chunks-of-non-connected-text/4
# works on active view / file
import sys
from Npp import *

console.clear()
#console.show()

# for debug, change view and document index
#i = notepad.getCurrentDocIndex(1)
#notepad.activateIndex(1,i)

keepGoing = True

editor.documentEnd()               # go to the last position
end2 = editor.getCurrentPos()      # record the position
#console.write("editor.end = " + str(end2)+"\n")
editor.documentStart()             # back to the beginning
start2 = editor.getCurrentPos()    # record the position
#console.write("editor.start = " + str(start2)+"\n")

while keepGoing:
    # find the group:\R prefix
    position = editor.findText( FINDOPTION.REGEXP, start2, end2, "groups:$")
    if position is None:
        break
    #console.write("editor: findText @ " + str(position[0]) + ":" + str(position[1]) + "\n")

    # find ___ (or EOF)
    underscore = editor.findText( FINDOPTION.REGEXP, position[1], end2, "^_+$")
    if underscore is None:
        keepGoing = False
        underscore = (end2, end2)

    # select the text
    #console.write("editor: findText @ " + str(underscore[0]) + ":" + str(underscore[1]) + "\n")
    editor.setSelectionStart(position[1]+2)    # start after the newline
    editor.setSelectionEnd(underscore[0]-2)    # end before the newline

    # okay, now the first match is highlighted... need to run the Edit > Line Operations > Sort Lines Lexicographically Ascending...
    # maybe notepad.menuCommand() or notepad.runMenuCommand()
    notepad.menuCommand(42059)  # got from https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/installer/nativeLang/english.xml
    #console.write(str(keepGoing))

    # start at the end of the last group
    start2 = underscore[0]

# want nothing selected at end
editor.clearSelections()