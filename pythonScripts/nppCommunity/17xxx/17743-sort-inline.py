# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/17743/"""
from Npp import *

def forum_post17743_FunctionName():
    """
    split each line into tokens; sort those tokens; replace the existing line
    """
    #console.show()
    #console.clear()

    # sort within each line of numeric tokens
    editor.beginUndoAction()
    for lnum in range(editor.getLineCount()):
        editor.gotoLine(lnum)
        txt = editor.getCurLine().rstrip()
        vals = sorted([int(x) for x in txt.split()])
        repl = " ".join([str(x) for x in vals])
        #console.write("[{}] => [{}]\n".format(txt, repl))
        editor.replaceLine(lnum, repl)
    editor.endUndoAction()

if __name__ == '__main__': forum_post17743_FunctionName()
