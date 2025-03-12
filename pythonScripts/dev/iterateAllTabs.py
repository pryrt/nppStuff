# encoding=utf-8
"""iterate through all tabs, looking for just SQL files

try to figure out why C++ version of NPPM_INTERNAL_SQLBACKSLASHESCAPE https://github.com/notepad-plus-plus/notepad-plus-plus/pull/16258/files
wasn't working when tried with NPPM_GETBUFFERLANGTYPE

"""
from Npp import notepad, editor

import ctypes
from ctypes.wintypes import BOOL, HWND, WPARAM, LPARAM, UINT
LRESULT = LPARAM

FindWindow = ctypes.windll.user32.FindWindowW
SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.restype = LRESULT
SendMessage.argtypes = [ HWND, UINT, WPARAM, LPARAM ]
WM_USER = 1024
NPPMSG = WM_USER + 1000
NPPM_GETNBOPENFILES = NPPMSG + 7
NPPM_GETBUFFERIDFROMPOS = NPPMSG + 59
NPPM_GETBUFFERLANGTYPE = NPPMSG + 64


currentView = notepad.getCurrentView()
console.write("View: {}\n".format(currentView))
currentDoc = (
    notepad.getCurrentDocIndex(0),
    notepad.getCurrentDocIndex(1)
)
ed = (editor1, editor2)
console.write("currentDocIndex: {}\n".format(currentDoc))
for viewIndex in range(2):
    #nOpenInThisView = notepad.getNbOpenFiles
    nOpenInThisView = SendMessage(notepad.hwnd, NPPM_GETNBOPENFILES, 0, viewIndex+1)
    console.write("nOpen[{}] = {}\n".format(viewIndex, nOpenInThisView))

    for docIndex in range(nOpenInThisView):
        bufferID = SendMessage(notepad.hwnd, NPPM_GETBUFFERIDFROMPOS, docIndex, viewIndex)
        langType = SendMessage(notepad.hwnd, NPPM_GETBUFFERLANGTYPE, bufferID, 0)
        if LANGTYPE.values[langType] == LANGTYPE.SQL:
            console.write("buferID[{}][{}] = 0x{:016x}\n".format(viewIndex, docIndex, bufferID))
            console.write("langType[0x{:016x}] = {}\n".format(bufferID, langType))
            console.write("-- SQL\n")
            notepad.activateIndex(viewIndex, docIndex)
            ed[viewIndex].setProperty("sql.backslash.escapes", "0")
            notepad.activateIndex(currentView, currentDoc[currentView])
