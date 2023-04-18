# encoding=utf-8
"""
PythonScript replacement of TextFX>Edit>Rewrap
https://community.notepad-plus-plus.org/post/78177
Author: @Ekopalypse , with input from @PeterJones

also saved as 23203-TextFXRewrap-Equivalent.py
"""
from Npp import editor, notepad
from textwrap import wrap
import re

def rewrap(text, pos, eol):
    paragraphed = re.sub(eol+eol, u'\u00B6', text)
    joined = re.sub(r'\h*(\r\n|\r|\n)', " ", paragraphed)
    unparagraphed = re.sub(u'\u00B6', eol+eol, joined)
    retlist = []
    for linetext in unparagraphed.splitlines():
        if linetext == '':
            retlist.append('')

        for partial in wrap(linetext, pos, expand_tabs=False, replace_whitespace=False, break_on_hyphens=False):
            retlist.append(partial)

    return retlist

def main():
    pos = int(notepad.prompt('Wrap at position:', 'ReWrap', '72'))
    if pos < 8 or pos > 2048:
        pos = 72

    start, end = editor.getUserLineSelection()
    start_pos = editor.positionFromLine(start)
    end_pos = editor.getLineEndPosition(end)

    eol = {0:'\r\n', 1:'\r', 2:'\n'}[editor.getEOLMode()]
    rewrapped = rewrap(editor.getRangePointer(start_pos, end_pos-start_pos), pos, eol)
    editor.setTarget(start_pos, end_pos)
    editor.beginUndoAction()
    editor.replaceTarget(eol.join(rewrapped))
    editor.endUndoAction()

main()
