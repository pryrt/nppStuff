# encoding=utf-8
""" published by @ekopalypse in https://notepad-plus-plus.org/community/topic/17552/change-menu-text-for-remove-consecutive-duplicate-lines/16
"""

def remove_duplicates():
    """ removes duplicate lines from the active file

    grabs the whole document into an enumerated sequence of line_num,line_text
    if line_text isn't in the set of unique lines, add it.  (set is an unordered mutable container, which can only hold one of any given element; it's basically the "key" side of a perl hash)
    else add the line_num to the list of duplicates

    I modified it to include .beginUndoAction()/.endUndoAction() pair, because if I want a bulk action, I also want bulk-undo
    """

    editor.beginUndoAction()   # pcj

    unique_lines = set()
    duplicates = []
    for line_num, line in enumerate(editor.getCharacterPointer().splitlines()):
        if line not in unique_lines:
            unique_lines.add(line)
        else:
            duplicates.append(line_num)

    for line_num in reversed(duplicates):
        editor.deleteLine(line_num)

    editor.endUndoAction() # pcj

remove_duplicates()