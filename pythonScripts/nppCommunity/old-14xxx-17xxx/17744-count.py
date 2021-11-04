# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/17744/"""
from Npp import *
import zlib

console.clear()

def forum_post17744_FunctionName():
    """
    this uses a hash of each line as a key in a dictionary, to count how many entries;
    to preserve order, it will run through the file a second time
    (this saves memory of whole-line keys, and an array to hold order)
    """

    # initialize dictionary and ordered list
    count = dict()

    # parse the active editor's text
    for lnum in range(editor.getLineCount()):
        editor.gotoLine(lnum)
        key = zlib.crc32(editor.getCurLine().rstrip()) & 0xFFFFFFFF
        if key in count:
            count[key] = count[key] + 1
        else:
            count[key] = 1

    # make the changes:
    editor.beginUndoAction()
    lnum = 0
    while lnum < editor.getLineCount():     # use a while loop rather than for loop, so I can choose _not_ to advance lnum after i delete the row (because "next" row will have same lnum as the deleted row)
        editor.gotoLine(lnum)
        key = zlib.crc32(editor.getCurLine().rstrip()) & 0xFFFFFFFF
        if key in count:
            #console.write("{:010X}|{}|{}\n".format(key, editor.getCurLine().rstrip(), count[key]))
            editor.lineEnd()
            editor.addText(" {}".format(count[key]))
            del count[key]  # don't want to have duplicates, so remove the key to indicate I'm done
            lnum = lnum + 1
        else:
            #console.write("{:010X}|{}|{}\n".format(key, editor.getCurLine().rstrip(), "NEED TO DELETE LINE"))
            editor.lineDelete()
    editor.endUndoAction()

if __name__ == '__main__': forum_post17744_FunctionName()
