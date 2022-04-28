# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/22890/

This is the simplest paradigm:
1) Click or arrow to where you want to start selecting
2) Shift+Click or Shift+arrow to get to the end of the selection (ie, do a normal selection)
3) Run this script to convert the selection from STREAM to rectangle and refresh the screen automatically to see it
"""
from Npp import notepad, editor, SELECTIONMODE, STATUSBARSECTION
editor.setSelectionMode( SELECTIONMODE.RECTANGLE )

# use the upcoming activateFile to refresh UI
#   otherwise, it doesn't _look_ like column/rectangle select)
notepad.activateFile(notepad.getCurrentFilename())
