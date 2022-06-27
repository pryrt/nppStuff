# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23171/horizontal-line-question/29

This will prompt for a number, and then run a regex to hardwrap after that column
"""
from Npp import editor,notepad,console

colstr = notepad.prompt("Column", "Hard Wrap at Column", 80)
srch = r'^.{' + colstr + '}'
editor.rereplace(srch, r'$0\r\n')
