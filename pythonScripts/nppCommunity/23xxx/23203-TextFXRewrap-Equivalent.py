# encoding=utf-8
"""
PythonScript replacement of TextFX>Edit>Rewrap
https://community.notepad-plus-plus.org/post/78161
Author: @Ekopalypse , with input from @PeterJones
"""
from Npp import editor, notepad
from textwrap import wrap
import re

def rewrap(text, pos):
	joined = re.sub(r'\h*(\r\n|\r|\n)', " ", text)
	return wrap(joined, pos, expand_tabs=False, replace_whitespace=True, break_on_hyphens=False)

def main():
	pos = int(notepad.prompt('Wrap at position:', 'ReWrap', '72'))
	if pos < 8 or pos > 2048:
		pos = 72

	start, end = editor.getUserLineSelection()
	start_pos = editor.positionFromLine(start)
	end_pos = editor.getLineEndPosition(end)

	rewrapped = rewrap(editor.getRangePointer(start_pos, end_pos-start_pos), pos)
	eol = {0:'\r\n', 1:'\r', 2:'\n'}[editor.getEOLMode()]
	editor.setTarget(start_pos, end_pos)
	editor.beginUndoAction()
	editor.replaceTarget(eol.join(rewrapped))
	editor.endUndoAction()

main()
