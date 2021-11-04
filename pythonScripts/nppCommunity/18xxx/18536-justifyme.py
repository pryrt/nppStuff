# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/18536/

Centers text based on PreferredWidth setting in script

If the cursor is on a line, just center that line.
If there is a multiline selection, center all the lines.

If a line to be centered is longer than PreferredWidth, it will just trim all leading and trailing spaces
"""
from Npp import *

PreferredWidth = 80

s0 = editor.getSelectionStart()
s1 = editor.getSelectionEnd()
l0 = editor.lineFromPosition(s0)
l1 = editor.lineFromPosition(s1)

if l1>l0 and s1==editor.positionFromLine(l1):
    # multiline selection ends at the beginning of a line
    #   going to assume that the final line isn't really part of the selection
    #   (ie, select from start of line1 to start of line3, you really just want 1-2 selected)
    l1 = l1 - 1

editor.beginUndoAction()

for myLine in range(l0,l1+1):
    # grab the current line, sans trailing and leading whitespace/newlines
    str = editor.getLine(myLine).rstrip().lstrip()

    # add appropriate leading spaces for centering
    if len(str) < PreferredWidth:
        nInsert = (PreferredWidth-len(str)) // 2
        str = (' ' * nInsert) + str
        #print('\t=>"{}"\n'.format(str))
        editor.replaceLine(myLine,str)  # this will keep the original EOL (CR,LF,CRLF,or EOF)

editor.endUndoAction()