# encoding=utf-8
"""Permutes the non-EOL characters of the current line, and duplicates it to the lines below

Usage example:
- I know there are letters NTH somewhere, and letter I in the second position, and there is one unknown char left
  so I want to permute the non-I characters (including unknowns), then insert the I, then try things out:
  1. Input nth_ as the only line in a file: use lowercase, so that DSpellCheck will work later
  2. PythonScript > scripts > permuteCurrentLine => there will now be 4!=24 lines (in a different example, might be 5!=120)
  3. insert i as the second character in all the lines
  4. if there are letters that I know cannot go in certain slots, remove those
  5. There will likely be less than a dozen letters left as possibilities, so for each letter (including the ones that are already used elsewhere, in case of duplicates)
     a. REPLACE( _ => x ), where x is the letter
     b. look for spellcheck results -- save any that are possible
     c. UNDO
     d. that should give a smaller list of words -- maybe even just one word
"""
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
