# -*- coding: utf-8 -*-
from __future__ import print_function

from Npp import *
import ctypes
from ctypes import wintypes
import platform

#-------------------------------------------------------------------------------

user32 = ctypes.WinDLL('user32')

notepad.hwnd = user32.FindWindowW(u'Notepad++', None)

LRESULT = wintypes.LPARAM

WndProcType = ctypes.WINFUNCTYPE(
    LRESULT,  # return type
    wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM  # arguments
    )

running_32bit = platform.architecture()[0] == '32bit'

SetWindowLong = user32.SetWindowLongW if running_32bit else user32.SetWindowLongPtrW
SetWindowLong.restype = WndProcType
SetWindowLong.argtypes = [wintypes.HWND, wintypes.INT, WndProcType]

SendMessageW = user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [ wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM ]

GWL_WNDPROC = -4

WM_CLOSE = 0x10
WM_SYSCOMMAND = 0x112
SC_MINIMIZE = 0xF020
VK_SHIFT = 0x10

#-------------------------------------------------------------------------------

class ENMTST(object):

    def __init__(self):
        self.new_npp_wnd_proc_hook_for_SetWindowLong = WndProcType(self.new_npp_wnd_proc_hook)
        self.orig_npp_wnd_proc = SetWindowLong(notepad.hwnd, GWL_WNDPROC, self.new_npp_wnd_proc_hook_for_SetWindowLong)

    def new_npp_wnd_proc_hook(self, hwnd, msg, wParam, lParam):
        retval = True
        if msg == WM_CLOSE and not self.shift_held():
            SendMessageW(hwnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
            retval = False  # set to False if we don't want further processing of this message
        if retval: retval = self.orig_npp_wnd_proc(hwnd, msg, wParam, lParam)
        return retval

    def shift_held(self):
        return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0

#-------------------------------------------------------------------------------

# to run from startup.py, put these lines (uncommented) in that file:
#import ExitNppMinimizesToSystemTray
#ExitNppMinimizesToSystemTray.ENMTST()

if __name__ == '__main__': ENMTST()