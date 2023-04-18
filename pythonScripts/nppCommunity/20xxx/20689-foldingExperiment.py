# encoding=utf-8
"""https://community.notepad-plus-plus.org/post/62503

Start by looking at current fold settings
"""
from Npp import *

console.show()

def inspectLine(contents, lineNumber, totalLines):
    f = editor.getFoldLevel(lineNumber)
    console.write("{}\t{:04x}\n".format(lineNumber, f))

editor.forEachLine(inspectLine)
