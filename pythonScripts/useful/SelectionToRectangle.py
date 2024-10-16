# encoding=utf-8
"""
Derived from 22890-simplest.py, in response to https://community.notepad-plus-plus.org/topic/22890/

2022-Oct-06: modify based on https://community.notepad-plus-plus.org/topic/23564 to convert either stream selection (old behavior) or multi-selection (new behavior) to a single column selection

This is the simplest paradigm for converting a stream (normal) selection to rectangular (column):
1) Click or arrow to where you want to start selecting
2) Shift+Click or Shift+arrow to get to the end of the selection (ie, do a normal selection)
3) Run this script to convert the selection from STREAM to rectangle and refresh the screen automatically to see it

You can also start with a Multi-Selection (multiple Ctrl+Clicks) and convert it, with the start of the column at the lowest selection-start, and the end of the selection at the highest selection-end
"""
from Npp import notepad, editor, SELECTIONMODE, STATUSBARSECTION

if editor.getSelectionMode()==SELECTIONMODE.THIN:    # this is the mode after making an edit in rectangle(column) mode
    ss,se = editor.getSelectionStart(), editor.getSelectionEnd()
    editor.setSelection(ss,se)

if editor.getSelectionMode()==SELECTIONMODE.STREAM and editor.getSelections()>1:    # this is multi-selection mode
    ss = None
    se = None

    for si in range(0, editor.getSelections()):
        s0 = editor.getSelectionNStart(si)
        s1 = editor.getSelectionNEnd(si)
        if ss is None or s0 < ss: ss = s0
        if se is None or s1 > se: se = s1

    editor.setSelection(ss,se)

if editor.getSelectionMode()!=SELECTIONMODE.RECTANGLE:
    editor.setSelectionMode( SELECTIONMODE.RECTANGLE )
    notepad.activateFile(notepad.getCurrentFilename()) # use the activateFile() command to refresh UI; otherwise, it doesn't _look_ like column/rectangle select)

"""
Test:
    one
    two
    three
    four
"""
