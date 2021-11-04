# -*- coding: utf-8 -*-
from __future__ import print_function

from Npp import *
import ctypes
from ctypes.wintypes import BOOL, HWND, WPARAM, LPARAM, UINT

def npp_get_statusbar(statusbar_item_number):

    WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    FindWindowW = ctypes.windll.user32.FindWindowW
    FindWindowExW = ctypes.windll.user32.FindWindowExW
    SendMessageW = ctypes.windll.user32.SendMessageW
    LRESULT = LPARAM
    SendMessageW.restype = LRESULT
    SendMessageW.argtypes = [ HWND, UINT, WPARAM, LPARAM ]
    EnumChildWindows = ctypes.windll.user32.EnumChildWindows
    GetClassNameW = ctypes.windll.user32.GetClassNameW
    create_unicode_buffer = ctypes.create_unicode_buffer

    SBT_OWNERDRAW = 0x1000
    WM_USER = 0x400; SB_GETTEXTLENGTHW = WM_USER + 12; SB_GETTEXTW = WM_USER + 13

    npp_get_statusbar.STATUSBAR_HANDLE = None

    def get_result_from_statusbar(statusbar_item_number):
        assert statusbar_item_number <= 5
        retcode = SendMessageW(npp_get_statusbar.STATUSBAR_HANDLE, SB_GETTEXTLENGTHW, statusbar_item_number, 0)
        length = retcode & 0xFFFF
        type = (retcode >> 16) & 0xFFFF
        assert (type != SBT_OWNERDRAW)
        text_buffer = create_unicode_buffer(length)
        retcode = SendMessageW(npp_get_statusbar.STATUSBAR_HANDLE, SB_GETTEXTW, statusbar_item_number, ctypes.addressof(text_buffer))
        retval = '{}'.format(text_buffer[:length])
        return retval

    def EnumCallback(hwnd, lparam):
        curr_class = create_unicode_buffer(256)
        GetClassNameW(hwnd, curr_class, 256)
        if curr_class.value.lower() == "msctls_statusbar32":
            npp_get_statusbar.STATUSBAR_HANDLE = hwnd
            return False  # stop the enumeration
        return True  # continue the enumeration

    npp_hwnd = FindWindowW(u"Notepad++", None)
    #print('npph:', npp_hwnd)
    EnumChildWindows(npp_hwnd, WNDENUMPROC(EnumCallback), 0)
    #print('sbh:', npp_get_statusbar.STATUSBAR_HANDLE)
    if npp_get_statusbar.STATUSBAR_HANDLE: return get_result_from_statusbar(statusbar_item_number)
    assert False

print(npp_get_statusbar(0))
print(npp_get_statusbar(1))
