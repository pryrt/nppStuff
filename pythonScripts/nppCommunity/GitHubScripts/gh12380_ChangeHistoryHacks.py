# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/12380
#  https://www.scintilla.org/ScintillaDoc.html#ChangeHistory
#  https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/scintilla/include/Scintilla.h

from Npp import *

from ctypes import (CFUNCTYPE)
from ctypes.wintypes import (HWND, UINT, WPARAM, LPARAM)
LRESULT = LPARAM

#-------------------------------------------------------------------------------

# from scintilla.h:
SC_CHANGE_HISTORY_DISABLED = 0
SC_CHANGE_HISTORY_ENABLED = 1
SC_CHANGE_HISTORY_MARKERS = 2
SC_CHANGE_HISTORY_INDICATORS = 4
SCI_SETCHANGEHISTORY = 2780
SCI_INDICSETSTYLE = 2080
INDICATOR_HISTORY_REVERTED_TO_ORIGIN_INSERTION = 36
INDICATOR_HISTORY_REVERTED_TO_ORIGIN_DELETION = 37
INDICATOR_HISTORY_SAVED_INSERTION = 38
INDICATOR_HISTORY_SAVED_DELETION = 39
INDICATOR_HISTORY_MODIFIED_INSERTION = 40
INDICATOR_HISTORY_MODIFIED_DELETION = 41
INDICATOR_HISTORY_REVERTED_TO_MODIFIED_INSERTION = 42
INDICATOR_HISTORY_REVERTED_TO_MODIFIED_DELETION = 43
INDIC_PLAIN = 0
INDIC_SQUIGGLE = 1
INDIC_TT = 2
INDIC_DIAGONAL = 3
INDIC_STRIKE = 4
INDIC_HIDDEN = 5
INDIC_BOX = 6
INDIC_ROUNDBOX = 7
INDIC_STRAIGHTBOX = 8
INDIC_CONTAINER = 8
INDIC_DASH = 9
INDIC_DOTS = 10
INDIC_SQUIGGLELOW = 11
INDIC_DOTBOX = 12
INDIC_SQUIGGLEPIXMAP = 13
INDIC_COMPOSITIONTHICK = 14
INDIC_COMPOSITIONTHIN = 15
INDIC_FULLBOX = 16
INDIC_TEXTFORE = 17
INDIC_POINT = 18
INDIC_POINTCHARACTER = 19
INDIC_GRADIENT = 20
INDIC_GRADIENTCENTRE = 21
INDIC_POINT_TOP = 22
INDIC_EXPLORERLINK = 23
INDIC_IME = 32

#-------------------------------------------------------------------------------

class CHH(object):

    def __init__(self):
        notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])
        self.bufferactivated_callback(None)  # call immediately so changes affect currently active file without switching tabs
        console.write("ChangeHistoryHacks Registered\n")

    def bufferactivated_callback(self, args):
        function_type = CFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
        scintilla_direct_function = function_type(editor.getDirectFunction())
        scintilla_direct_pointer = editor.getDirectPointer()
        ch_enable_setting = SC_CHANGE_HISTORY_ENABLED | SC_CHANGE_HISTORY_MARKERS | SC_CHANGE_HISTORY_INDICATORS
        scintilla_direct_function(scintilla_direct_pointer, SCI_SETCHANGEHISTORY, ch_enable_setting, 0)
        scintilla_direct_function(scintilla_direct_pointer, SCI_INDICSETSTYLE, INDICATOR_HISTORY_MODIFIED_INSERTION, INDIC_GRADIENTCENTRE)  # INDIC_ROUNDBOX)
        scintilla_direct_function(scintilla_direct_pointer, SCI_INDICSETSTYLE, INDICATOR_HISTORY_SAVED_INSERTION, INDIC_HIDDEN)
        scintilla_direct_function(scintilla_direct_pointer, SCI_INDICSETSTYLE, INDICATOR_HISTORY_SAVED_DELETION, INDIC_HIDDEN)

#-------------------------------------------------------------------------------

if __name__ == '__main__': CHH()
