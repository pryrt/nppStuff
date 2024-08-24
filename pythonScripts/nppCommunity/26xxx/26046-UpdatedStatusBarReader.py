# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26046/
derived from https://community.notepad-plus-plus.org/post/32089
    and added the .restype, .argtypes, and ctypes.addressof(text_buffer) to make it work in v8.6.9-64bit
"""
from Npp import *

import ctypes
from ctypes.wintypes import BOOL, HWND, WPARAM, LPARAM, UINT

def npp_get_statusbar(statusbar_item_number):
    LRESULT = LPARAM
    WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    FindWindow = ctypes.windll.user32.FindWindowW
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage.restype = LRESULT
    SendMessage.argtypes = [ HWND, UINT, WPARAM, LPARAM ]
    EnumChildWindows = ctypes.windll.user32.EnumChildWindows
    GetClassName = ctypes.windll.user32.GetClassNameW
    create_unicode_buffer = ctypes.create_unicode_buffer
    WM_USER = 0x400; SB_GETTEXTLENGTHW = WM_USER + 12; SB_GETTEXTW = WM_USER + 13

    npp_get_statusbar.STATUSBAR_HANDLE = None

    def get_data_from_statusbar(statusbar_item_number):
        retcode = SendMessage(npp_get_statusbar.STATUSBAR_HANDLE, SB_GETTEXTLENGTHW, statusbar_item_number, 0)
        length = retcode & 0xFFFF
        type = (retcode >> 16) & 0xFFFF
        text_buffer = create_unicode_buffer(length)
        retcode = SendMessage(npp_get_statusbar.STATUSBAR_HANDLE, SB_GETTEXTW, statusbar_item_number, ctypes.addressof(text_buffer))
        retval = '{}'.format(text_buffer[:length])
        return retval

    def EnumCallback(hwnd, lparam):
        curr_class = create_unicode_buffer(256)
        GetClassName(hwnd, curr_class, 256)
        if curr_class.value.lower() == "msctls_statusbar32":
            npp_get_statusbar.STATUSBAR_HANDLE = hwnd
            return False
        return True

    EnumChildWindows(FindWindow(u"Notepad++", None), WNDENUMPROC(EnumCallback), 0)

    return get_data_from_statusbar(statusbar_item_number) if npp_get_statusbar.STATUSBAR_HANDLE else None

