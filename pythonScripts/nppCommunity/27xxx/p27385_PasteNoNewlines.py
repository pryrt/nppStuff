# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27385/

This will paste the CF_TEXT plaintext from the clipboard, but will convert any series of newline characters into a single space before doing the paste.

Because this uses .insertText() instead of putting the modified text back into the clipboard and doing .paste(), it should avoid clobbering the clipboard.

(based on @alan-kilborn's clipboard script here:
<https://community.notepad-plus-plus.org/post/97132>)
"""
from Npp import *

try:
    editor3h  # third editor, hidden
except NameError:
    editor3h = notepad.createScintilla()

def get_clipboard_text_without_newlines():
    retval = ''
    editor3h.clearAll()
    editor3h.paste()
    if editor3h.getLength() > 0:
        editor3h.rereplace(r'[\r\n]+', ' ') # replace all newline seqeuences with a single space
        retval = editor3h.getText()
    return retval

editor.beginUndoAction()
editor.insertText(editor.getCurrentPos(), get_clipboard_text_without_newlines())
editor.endUndoAction()
