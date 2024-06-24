# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25902/"""
from Npp import notepad,console,editor

def _doit():
    #console.clear()
    #console.show()
    MARK_BOOKMARK = 20

    def bookmarkIfMatched(pattern, contents, lineNumber, totalLines):
        if pattern in contents:
            #console.write("found '{}' on line {}: '{}'\n".format(pattern, lineNumber+1, contents.rstrip()))
            editor.markerAdd(lineNumber, MARK_BOOKMARK)

    mySelection = editor.getSelText()
    if mySelection != '':
        editor.forEachLine(lambda c,l,t: bookmarkIfMatched(mySelection, c, l, t))


_doit()
del(_doit)
