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

# define new notepad-object method to return config directory relative to notepad.getPluginConfigDir()
Notepad.getConfigDirectory = lambda self: os.path.dirname(os.path.dirname(notepad.getPluginConfigDir()))

# import a python script from that folder to run it every time the program loads
# import doubleclickExtra

# https://community.notepad-plus-plus.org/topic/20340/perl-subroutine-calltips-with-pythonscript
# look up the my ($args,$other) = @_ from the first line of a sub definition,
# and use it for tooltips when calling ... = fn(|) with cursor at |
##USE LSP INSTEAD## from perl_ide_ps154 import PerlIDE
##USE LSP INSTEAD## __plide = PerlIDE()
##USE LSP INSTEAD## __plide.initialize()

# see nppOnSaveSyntaxCheck.py for references
##USE LSP INSTEAD##from nppOnSaveSyntaxCheck import _SINGLETON_CHECKER
##USE LSP INSTEAD##_SINGLETON_CHECKER.toggle_OnSave_callback()
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

# ZoomLevelKeepBothViewsSynched
import ZoomLevelKeepBothViewsSynched
zlkbvs = ZoomLevelKeepBothViewsSynched.ZLKBVS()


##
#import ctypes
#FindWindow = ctypes.windll.user32.FindWindowW
#SendMessage = ctypes.windll.user32.SendMessageW
#notepad.hwnd = FindWindow(u"Notepad++", None)
#console.write("hwnd = 0x{:08x} = {}\n".format(notepad.hwnd,notepad.hwnd))
#winv = SendMessage(notepad.hwnd, 1024+1000+42,0,0)
#console.write("Win v{}\n".format(winv))
#nppv = SendMessage(notepad.hwnd, 1024+1000+50,0,0)
#console.write("NPP v{}.{}\n".format(nppv>>16, nppv&0xFFFF))

######################

#### change EOL representation to the cool diagonal Control Pictures
####    => must be done every change of buffer, and doesn't honor the "normal text" or custom-color setting unless I change that setting after
####        probably other ps I could use to adjust the color/boxes after the fact, but at that point, it's too complicated for my needs.
#editor.setRepresentation(u'\u000A', u'\u240A')
#editor.setRepresentation(u'\u000D', u'\u240D')

######################
def CCB():
    notepad.clearCallbacks()
    editor.clearCallbacks()

console.write("END of user startup.py\n\n")
