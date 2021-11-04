# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/17550"""
from Npp import *

console.show()
console.clear()

keyword = notepad.prompt('Enter keyword to search for:', '', 'permit')
find_what = notepad.prompt('Enter text to find:', '', 'log')

if find_what != None and len(find_what) > 0 and keyword != None and len(keyword)>0:
    replace_with = notepad.prompt('Enter replacement text:', '', '')

    if replace_with != None:

        editor.beginUndoAction()
        nLines = editor.getLineCount()

        for line_nbr in range(0, nLines):
            start_pos = editor.positionFromLine(line_nbr)
            str = editor.getLine(line_nbr)
            end_pos = start_pos + len(str) - 1
            if keyword in str:
                editor.rereplace(find_what, replace_with, 0, start_pos, end_pos)

        editor.endUndoAction()

"""
# Alan-Kilborn's original code
bookmark_mask = 1 << 24

if editor.markerNext(0, bookmark_mask) == -1:

    notepad.messageBox('To use this, need to have at least one bookmarked line; you have zero', '')

else:

    find_what = notepad.prompt('Enter text to find:', '', '')

    if find_what != None and len(find_what) > 0:

        replace_with = notepad.prompt('Enter replacement text:', '', '')

        if replace_with != None:

            editor.beginUndoAction()

            line_nbr = editor.markerNext(0, bookmark_mask)
            while line_nbr != -1:
                start_pos = editor.positionFromLine(line_nbr)
                end_pos = start_pos + len(editor.getLine(line_nbr)) - 1
                editor.rereplace(find_what, replace_with, 0, start_pos, end_pos)
                line_nbr = editor.markerNext(line_nbr + 1, bookmark_mask)

            editor.endUndoAction()
"""

"""
@Alan-Kilborn said:
> here’s a Pythonscript that fulfills the title of this thread;

Nice.

I'm not sure that "run a regex to bookmark, then run a PythonScript to edit" is any less confusing to the typical user than "run these 2-3 regex in sequence"... but that's still a good alternative.

Really, with one more prompt at the beginning of your script ("Enter the keyword, such as 'permit': "), and using PythonScript to set the bookmarks rather than making the user manually bookmark, PythonScript could be made to handle it.  (Or, skipping bookmarks, just wrap the `editor.rereplace` inside of the `while` loop with pseudocode `if line contains KEYWORD then editor.rereplace`.)
"""
