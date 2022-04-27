# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/22890/ and 22919

alternate paradigm
"""
from Npp import notepad, editor, SELECTIONMODE, STATUSBARSECTION

try:
    columnSelectMode
    startPos
    endPos
except NameError:
    #console.show()
    console.write('initialize toggle mode for the first time\n')
    columnSelectMode = False
    startPos = None
    endPos = None

if not columnSelectMode:
    startPos = editor.getCurrentPos()
    endPos = startPos
    notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, "In Rectangle/Column Selection Mode")

else:
    endPos = editor.getCurrentPos()
    editor.setSel(startPos, endPos)
    editor.setSelectionMode( SELECTIONMODE.RECTANGLE )

    # this overrides the statusbar.. but the refresh UI will overwrite that with default
    notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, "")

    # use the upcoming activateFile to refresh UI
    #   otherwise, it doesn't _look_ like column/rectangle select)
    notepad.activateFile(notepad.getCurrentFilename())

columnSelectMode = not columnSelectMode

#console.show()
#console.write("toggle selection mode to {}: {} .. {}\n".format(columnSelectMode, startPos, endPos))
