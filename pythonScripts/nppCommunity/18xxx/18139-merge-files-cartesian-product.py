# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/18139/

You can merge two files using the cartesian product <https://en.wikipedia.org/wiki/Cartesian_product>,
which is implemented in itertools.product() <https://docs.python.org/2/library/itertools.html#itertools.product>

assumes:
* your file1.txt (names) is in the primary notepad++ view,
* your file2.txt (numbers) is in the secondary notepad++ view (you can RClick on the title tab and Move to Other View)
* you want the merged file to end up in file1.txt
* you want to be able to undo if something goes wrong
"""
from Npp import *
import itertools

def allLinesNoEOL(scint = editor):
    """a generator to yield all the lines of a given scintilla instance,

    All lines have trailing whitespace removed (ie, end-of-lines)

    scint defaults to the active editor if not supplied
    """
    for n in range(scint.getLineCount()):
        yield scint.getLine(n).rstrip()

# thanks to @Ekopalypse and @Alan-Kilborn for https://notepad-plus-plus.org/community/topic/18133/regex-rounding-numbers-python-script-does-not-run-properly/24
try:
    hidden
except NameError:
    hidden = notepad.createScintilla()

# iterate through the cartesian product of the two files, storing in the temporary "hidden" scintilla
hidden.setText("")
for p in itertools.product(allLinesNoEOL(editor1), allLinesNoEOL(editor2)):
    hidden.addText(p[0]+p[1]+"\n")

# copy the results
editor1.beginUndoAction()
editor1.setText(hidden.getText())
editor1.endUndoAction()

# "do not destroy!" -- don't use notepad.destroyScintilla(hidden)
# but still clear the text itself
hidden.setText("")

# since we don't need the overhead of scintilla operations, hidden could be replaced by a simple string