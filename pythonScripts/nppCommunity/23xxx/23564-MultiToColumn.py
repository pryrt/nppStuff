# encoding=utf-8
"""
Derived from SelectionToRectangle.py from 22890-simplest.py, in response to https://community.notepad-plus-plus.org/topic/23564,
which had (accidentally) changed a Column Selection to a Multi-Selection instead. This converts a multi-selection to a column-selection
"""
from Npp import notepad, editor, SELECTIONMODE, STATUSBARSECTION

#console.clear()
#console.write("PRE:  {}..{} R:{} M:{}\n".format(editor.getSelectionStart(), editor.getSelectionEnd(), editor.selectionIsRectangle(), editor.getMultipleSelection()))

if not(editor.selectionIsRectangle()) and (editor.getMultipleSelection()):
    ss,se = editor.getSelectionStart(), editor.getSelectionEnd()
    #console.write("GET:  {}..{} R:{} M:{}\n".format(editor.getSelectionStart(), editor.getSelectionEnd(), editor.selectionIsRectangle(), editor.getMultipleSelection()))
    editor.setSelection(ss,se)
    #console.write("SET:  {}..{} R:{} M:{}\n".format(editor.getSelectionStart(), editor.getSelectionEnd(), editor.selectionIsRectangle(), editor.getMultipleSelection()))
    editor.setSelectionMode( SELECTIONMODE.RECTANGLE )
    #console.write("RECT: {}..{} R:{} M:{}\n".format(editor.getSelectionStart(), editor.getSelectionEnd(), editor.selectionIsRectangle(), editor.getMultipleSelection()))

notepad.activateFile(notepad.getCurrentFilename()) # use the activateFile() command to refresh UI; otherwise, it doesn't _look_ like column/rectangle select)
#console.write("POST: {}..{} R:{} M:{}\n".format(editor.getSelectionStart(), editor.getSelectionEnd(), editor.selectionIsRectangle(), editor.getMultipleSelection()))

"""
Notes:
Alan reminded me about [PythonScript Toggleable Script?](https://community.notepad-plus-plus.org/topic/22890/pythonscript-toggleable-script/31), where I developed SelectionToRectangle.py, which converted a normal stream selection to a column (rectangle) selection.

Using the concepts from that, I saw that after Guy's manipulation (above) the selection converts from a rectangle selection to a multi-selection.  If I _just_ ran the SelectionToRectangle, the modes _claim_ to be a rectangular selection again... but looking at the selection start/end, it's a one-row rectangle, so not very columnar.  However, before doing that, the multi-selection still has the original extents for the beginning and end of selection.  So using those values to create a new stream selection and convert to rectangular, I think it works as desired:

    one
    two
    three
    four

Instructions:
0. Save this script, and optionally assign it a keyboard shortcut
1. use the one...four text above, do a column selection between the fourth space and the letters
2. type " then backspace to replicate Guy's issue
3. Edit > Line Operations > Sort Lines Lexicographically Ascending -- order should still be one, two, three, four, because it doesn't sort because of multi-selection
4. run this script
5. Edit > Line Operations > Sort Lines Lexicographically Ascending -- order should now be four, one, three, two, because it went back to column/rectangle-selection
"""
