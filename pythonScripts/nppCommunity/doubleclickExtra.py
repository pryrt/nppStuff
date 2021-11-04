""" doubleclickExtra.py

https://community.notepad-plus-plus.org/topic/19879/double-clicking-over-a-word-function-works-great-but-it-can-be-much-greater-than-ever

Highjacks the double-click action:
* saves current selection location
* runs Ctrl+F3 (Select and Find Next) to get the current selection into the search buffer
* goes back to the original position
* searches backward once and forward once to re-activate any smartmatches
* At this point, the active selection is in the search buffer and F3 will take you to the next instance.

To run it every time, put it in your user scripts folder as "doubleclickExtra.py", and add the following to your user startup.py:
~~~
from Npp import *
import sys
d = notepad.getPluginConfigDir() + r'\PythonScript\Scripts'
if not d in sys.path:
    sys.path.append(d)

import doubleclickExtra
~~~

"""
from Npp import *

def doubleclick_extra(args):
    ss = editor.getSelectionStart()
    se = editor.getSelectionEnd()
    notepad.menuCommand(MENUCOMMAND.SEARCH_SETANDFINDNEXT)
    editor.gotoPos(se)
    editor.setSelection(ss,se)
    notepad.menuCommand(MENUCOMMAND.SEARCH_FINDPREV)
    notepad.menuCommand(MENUCOMMAND.SEARCH_FINDNEXT)


editor.callback(doubleclick_extra, [SCINTILLANOTIFICATION.DOUBLECLICK])

# use editor.clearCallbacks([SCINTILLANOTIFICATION.DOUBLECLICK]) before re-running this script during debug
