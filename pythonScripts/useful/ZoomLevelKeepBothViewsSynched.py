# -*- coding: utf-8 -*-
from __future__ import print_function

#########################################
#
#  ZoomLevelKeepBothViewsSynched (ZLKBVS)
#
#########################################
# Author: Alan Kilborn
# references:
#  https://community.notepad-plus-plus.org/topic/25844
#  for newbie info on PythonScripts, see https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript

#-------------------------------------------------------------------------------

from Npp import *

#-------------------------------------------------------------------------------

try:
    editor1.hwnd
except AttributeError:
    # running PS2
    import ctypes
    user32 = ctypes.WinDLL('user32')
    notepad.hwnd = user32.FindWindowW(u'Notepad++', None)
    editor1.hwnd = user32.FindWindowExW(notepad.hwnd, None, u'Scintilla', None)

assert editor1.hwnd

#-------------------------------------------------------------------------------

class ZLKBVS(object):

    def __init__(self):
        editor.callback(self.zoom_callback, [SCINTILLANOTIFICATION.ZOOM])
        self.zoom_callback( { 'hwndFrom' : editor } )

    def zoom_callback(self, args):
        if not notepad.isSingleView():
            other_editor = editor2 if args['hwndFrom'] == editor1.hwnd else editor1
            this_editor = editor2 if other_editor == editor1 else editor1
            other_editor.setZoom(this_editor.getZoom())

#-------------------------------------------------------------------------------

# to run via another file, e.g., (user) startup.py, put these lines (uncommented and unindented) in that file:
#  import ZoomLevelKeepBothViewsSynched
#  zlkbvs = ZoomLevelKeepBothViewsSynched.ZLKBVS()
# also note: need to make sure that "Initialisation" for "Python Script Configuration" is set to "ATSTARTUP" and not "LAZY".

if __name__ == '__main__':
    try:
        zlkbvs
    except NameError:
        zlkbvs = ZLKBVS()
