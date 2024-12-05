# encoding=utf-8
"""in response to https://github.com/bruderstein/PythonScript/issues/36#issuecomment-2517921387

"""
from Npp import editor1,editor2,notepad,console,BUFFERENCODING,MENUCOMMAND
import ctypes   # .windll, .addressof, .create_string_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
import sys

SendMessageW = ctypes.windll.user32.SendMessageW
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageW.restype = LPARAM

SCI_GETTEXT = 2182

notepad.new()
notepad.setEncoding(BUFFERENCODING.UTF8)
editor.setText("ÄÑ×Ø UTF8")
editor.setSavePoint()   # pretend it's saved
idUTF8 = notepad.getCurrentBufferID()

notepad.new()
notepad.setEncoding(BUFFERENCODING.ANSI)
editor.setText("ÄÑ×Ø ANSI".encode("iso8859-1"))
editor.setSavePoint()   # pretend it's saved
idANSI = notepad.getCurrentBufferID()
notepad.menuCommand(MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW)

notepad.activateBufferID(idUTF8)
txt = editor.getText()
console.write(txt)

notepad.activateBufferID(idANSI)
txt = editor.getText()
console.write(txt)
