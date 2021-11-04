#!/usr/bin/python
# -*- coding: utf-8 -*-

#################################################################################
## automate find dialog
import ctypes
from ctypes.wintypes import BOOL, HWND, LPARAM

WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)

FindWindow = ctypes.windll.user32.FindWindowW
FindWindowEx = ctypes.windll.user32.FindWindowExW
SendMessage = ctypes.windll.user32.SendMessageW
EnumChildWindows = ctypes.windll.user32.EnumChildWindows
GetClassName = ctypes.windll.user32.GetClassNameW
create_unicode_buffer = ctypes.create_unicode_buffer


BM_CLICK = 0x00F5
SBT_OWNERDRAW = 0x1000
WM_USER = 0x400

SB_GETTEXTLENGTHW = WM_USER + 12
SB_GETTEXTW = WM_USER + 13

STATUSBAR_HANDLE = None

def on_press(window_handle, button_text):
    button_handle = FindWindowEx(window_handle, 0, u"Button", button_text)
    SendMessage(button_handle, BM_CLICK, 0, 0)

def get_result_from_statusbar(statusbar_item):
    retcode = SendMessage(STATUSBAR_HANDLE, SB_GETTEXTLENGTHW, statusbar_item, 0)
    length = retcode & 0xFFFF
    type = (retcode >> 16) & 0xFFFF
    _text = ''

    if type == SBT_OWNERDRAW:
        retcode = SendMessage(STATUSBAR_HANDLE, SB_GETTEXTW, statusbar_item, 0)
        _text =  'SBT_OWNERDRAW:{}'.format(ctypes.wstring_at(retcode))
    else: # not sure if this gets called at all
        text_buffer = create_unicode_buffer(length)
        retcode = SendMessage(STATUSBAR_HANDLE, SB_GETTEXTW, statusbar_item, text_buffer)
        _text = 'text_buffer:{}'.format(text_buffer[:length])

    return _text


def EnumCallback(hwnd, lparam):
    global STATUSBAR_HANDLE
    curr_class = create_unicode_buffer(256)
    GetClassName(hwnd, curr_class, 256)
    if curr_class.value.lower() == "msctls_statusbar32":
        STATUSBAR_HANDLE = hwnd
        return False
    return True

notepad.menuCommand(MENUCOMMAND.SEARCH_FIND)

find_hwnd = FindWindow(None, u'Find')
EnumChildWindows(find_hwnd, WNDENUMPROC(EnumCallback), 0)

if STATUSBAR_HANDLE:
    on_press(find_hwnd, u'Coun&t')
    console.write(get_result_from_statusbar(0) + '\n')
