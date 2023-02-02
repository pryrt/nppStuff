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
# _SINGLETON_CHECKER.toggle_OnSave_callback(); del(_SINGLETON_CHECKER); del(nppOnSaveSyntaxCheck.nppOnSaveSyntaxCheck);

# https://community.notepad-plus-plus.org/post/59148
# make the full-line selection extend to right margin instead of just to EOL marker
editor.setSelEOLFilled(True)

# see https://community.notepad-plus-plus.org/topic/22274/linked-text-to-open-other-files-into-notepad
import UriIndicatorAltClick
uiac = UriIndicatorAltClick.UIAC()

# see https://community.notepad-plus-plus.org/post/71772
#import MouseJiggleDaemon
#mjd = MouseJiggleDaemon.MJD()

# alan's Change-History hack script, which allows adding coloring to the text itself, not just the border
#   He used a rounded box around it' I changed to a gradient-from-center...
#   but it seems to sometimes use a triangle, sometimes not... and I don't like that triangle,
#   and I don't find the inline change marker as helpful to me, so I'm disabling it for now
#import gh12380_ChangeHistoryHacks
#chh_instance = gh12380_ChangeHistoryHacks.CHH()

console.write("END of user startup.py\n\n")
