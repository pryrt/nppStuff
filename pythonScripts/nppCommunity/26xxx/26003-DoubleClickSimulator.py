# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26003/

Simulate the word-doubleclick in PythonScript
"""
from Npp import editor
p = editor.getCurrentPos()
if editor.wordStartPosition(p,True) < p:
    editor.wordLeft()
editor.wordRightExtend()
