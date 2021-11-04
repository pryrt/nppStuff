# -*- coding: utf-8 -*-
'''
use PythonScript instead of gui to remove empty lines
'''
import sys
from Npp import *

def delTrulyEmpty(contents, lineNumber, totalLines):
    if contents.strip('\r\n') == "":
        editor.deleteLine(lineNumber)

editor.beginUndoAction()
editor.forEachLine(delTrulyEmpty)
editor.endUndoAction()
