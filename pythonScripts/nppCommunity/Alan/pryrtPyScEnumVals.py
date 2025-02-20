# encoding=utf-8
"""in response to Alan chat message
"""
from Npp import *

prev = None

for l1 in range(editor1.getLineCount()):
    orig = editor1.getLine(l1)
    isFound = False
    prevL2 = None
    for l2 in range(editor2.getLineCount()):
        str2 = editor2.getLine(l2)
        isFound |= (orig == str2)
        if prevL2 is None and prev == str2:
            prevL2 = l2
            # this indicates where I will want to add it
    if not isFound:
        console.write("Need to add '{}' after line#{}\n".format(orig.strip(), prevL2))
        if prevL2 is None:
            # insert at end
            editor2.appendText(orig)
        else:
            # insert after prevL2
            p = editor2.positionFromLine(prevL2+1)  # start of _next_ line
            editor2.insertText(p, orig)
    prev = orig
