# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21446/ multi-selection request

the comments show my debug code, or alternative methods

this will loop through all N sections of the multi-selection
for each section:
* find the start and end locations
* grab the original text from that section
* replace the original by surrounding it with **

Notes:
* it allows a single undo for the whole group of replacements, but if you do UNDO,
    it will clear the multi-selection
* at the end of the replacement, the multi-selection goes down to a zero-length
    selection at the start of each of the original words;
        shift+arrows or shift+ctrl+arrow will allow you to extend the multi-selection again

"""
from Npp import *

editor.beginUndoAction()

for mSel in range(editor.getSelections()):
    selStart = editor.getSelectionNStart(mSel)
    selEnd = editor.getSelectionNEnd(mSel)
    orig = editor.getTextRange(selStart, selEnd)
    #console.write("loop #{}: {}..{} = \"{}\"\n".format(mSel,selStart,selEnd,orig))
    txt = "**" + orig + "**"
    editor.replace(orig,txt,0,selStart,selEnd)



editor.endUndoAction()
