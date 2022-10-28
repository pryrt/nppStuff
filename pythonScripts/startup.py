from Npp import *
import sys

console.write("Start of user startup.py\n")

# add scripts folder to the path
#d = notepad.getPluginConfigDir() + r'\PythonScript\Scripts\nppCommunity'
#if not d in sys.path:
#    sys.path.append(d)
# updated to https://community.notepad-plus-plus.org/topic/22299/convenience-technique-when-organizing-pythonscripts-into-folders
import os
for (root, dirs, files) in os.walk(notepad.getPluginConfigDir() + r'\PythonScript\scripts', topdown=False):
    if root not in sys.path:
        sys.path.append(root)

# import a python script from that folder to run it every time the program loads
# import doubleclickExtra

# https://community.notepad-plus-plus.org/topic/20340/perl-subroutine-calltips-with-pythonscript
# look up the my ($args,$other) = @_ from the first line of a sub definition,
# and use it for tooltips when calling ... = fn(|) with cursor at |
from perl_ide_ps154 import PerlIDE
__plide = PerlIDE()
__plide.initialize()

# see nppOnSaveSyntaxCheck.py for references
from nppOnSaveSyntaxCheck import _SINGLETON_CHECKER
_SINGLETON_CHECKER.toggle_OnSave_callback()

# https://community.notepad-plus-plus.org/post/59148
# make the full-line selection extend to right margin instead of just to EOL marker
editor.setSelEOLFilled(True)

# see https://community.notepad-plus-plus.org/topic/22274/linked-text-to-open-other-files-into-notepad
import UriIndicatorAltClick
uiac = UriIndicatorAltClick.UIAC()

# see https://community.notepad-plus-plus.org/post/71772
#import MouseJiggleDaemon
#mjd = MouseJiggleDaemon.MJD()

console.write("END of user startup.py\n\n")
