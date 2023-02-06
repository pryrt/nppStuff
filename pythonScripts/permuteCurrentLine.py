# encoding=utf-8
"""Permutes the non-EOL characters of the current line, and duplicates it to the lines below"""
from Npp import editor,notepad,console
from itertools import permutations

class PermuteCurrentLine(object):
    def eol(self):
        return ("\r\n", "\r", "\n")[editor.getEOLMode()]

    def go(self):
        linetext = editor.getCurLine().rstrip()
        linenum  = editor.lineFromPosition(editor.getCurrentPos())
        startpos = editor.positionFromLine(linenum)
        endpos   = editor.getLineEndPosition(linenum)
        #console.write("#{}\t'{}' @ {}..{}{}".format(linenum, linetext, startpos, endpos, self.eol()))

        editor.beginUndoAction()

        for x in permutations(linetext):
            txt = "".join(x) + self.eol()
            #console.write("\t#{}\t{}".format(linenum, txt))
            editor.replaceLine(linenum, txt)
            linenum = linenum + 1

        editor.endUndoAction()

PermuteCurrentLine().go()
