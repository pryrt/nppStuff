# encoding=utf-8
"""
Derived from 22890-simplest.py, in response to https://community.notepad-plus-plus.org/topic/22890/

This is the simplest paradigm for converting a stream (normal) selection to rectangular (column):
1) Click or arrow to where you want to start selecting
2) Shift+Click or Shift+arrow to get to the end of the selection (ie, do a normal selection)
3) Run this script to convert the selection from STREAM to rectangle and refresh the screen automatically to see it
"""
from Npp import notepad, editor, SELECTIONMODE, STATUSBARSECTION
editor.setSelectionMode( SELECTIONMODE.RECTANGLE )
notepad.activateFile(notepad.getCurrentFilename()) # use the activateFile() command to refresh UI; otherwise, it doesn't _look_ like column/rectangle select)
