# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/20485/

The goal is to register a handler which will see whether the active file is the right RouterOS UDL,
and, if so, try to alter the global background color.

Unfortunately, while I found notepad.getEditorDefaultBackgroundColor(), there isn't a set equivalent
"""
from Npp import *

def check_and_modify():
    current_language = notepad.getLanguageName(notepad.getLangType()).replace('udf - ','')
    console.write("{}\n".format(notepad.getEditorDefaultBackgroundColor()))
    if 'RouterOS' == current_language:
        console.write("Good\n")
    else:
        console.write("no match\n")

check_and_modify()