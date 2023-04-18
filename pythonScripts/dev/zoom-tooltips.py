# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/16858/

the goals I want to learn:
1. how to use the ctypes.windll.user32 or appropriate sub-module to do a tooltip
2. gain access to the scintilla zoom level, and use the zoom event

I haven't yet been able to find easy example of setting a tooltip/popup... but searching the forum for ctypes, I found scott's
    https://notepad-plus-plus.org/community/topic/15698/last-modified-date-in-status-bar/15
which shows a way to grab the existing statusbar text for a given entry...
"""
from Npp import *
import ctypes

def dzt_register():
    """this will register a function to the ZOOM event"""
    editor.callback(dzt_ZoomCallback, [SCINTILLANOTIFICATION.ZOOM])

def dzt_unregister():
    """this will register a function to the ZOOM event"""
    editor.clearCallbacks([SCINTILLANOTIFICATION.ZOOM])

def dzt_ZoomCallback(args):
    """this is the ZOOM callback function"""
    z = editor.getZoom()
    s = editor.styleGetSize(0)  # get the default size for this language/filetype
    zp = 100. * (1+float(z)/float(s))
    console.write("zoomCallback() -> zoom = {}/{} = {}%\n".format(z, s, zp))
    #for sbs in [STATUSBARSECTION.CURPOS,STATUSBARSECTION.DOCSIZE,STATUSBARSECTION.DOCTYPE,STATUSBARSECTION.EOFFORMAT,STATUSBARSECTION.TYPINGMODE,STATUSBARSECTION.UNICODETYPE]:
    #    console.write('\tsection({}) = {}\n'.format(sbs, npp_get_statusbar(sbs)))

import ctypes
from ctypes.wintypes import BOOL, HWND, LPARAM

def npp_get_statusbar(statusbar_item_number):

    WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    FindWindow = ctypes.windll.user32.FindWindowW
    SendMessage = ctypes.windll.user32.SendMessageW
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
        retcode = SendMessage(npp_get_statusbar.STATUSBAR_HANDLE, SB_GETTEXTW, statusbar_item_number, text_buffer)
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

def dzt_exploreTooltips():
    return None # don't do anything... crashing NPP
    """https://docs.microsoft.com/en-us/windows/desktop/Controls/create-a-tooltip-for-a-control"""
    #from ctypes.windll.commctrl import *
    # from commctrl import (TOOLTIPS_CLASS, TTS_ALWAYSTIP, TTS_NOPREFIX, TTM_ADDTOOL, TTM_SETMAXTIPWIDTH)
    TOOLTIPS_CLASS  = u'tooltips_class32'   # commctrl.h    : if _W, use u'' else ''
    TTS_ALWAYSTIP   = 0x1                   # commctrl.h
    TTS_BALLOON     = 0x40                  # commctrl.h
    WS_POPUP        = 0x80000000            # winuser.h
    CW_USEDEFAULT   = 0x80000000            # winuser.h
    WM_USER         = 0x400
    TTM_ADDTOOLW    = WM_USER + 50

    hWnd = ctypes.windll.user32.FindWindowW(u"Notepad++", None)
    g_hInst = None # global instance handle (from docs.ms) -- don't know what it should be
    hwndTip = ctypes.windll.user32.CreateWindowExW(None, TOOLTIPS_CLASS, None,
        WS_POPUP |TTS_ALWAYSTIP | TTS_BALLOON,
        CW_USEDEFAULT, CW_USEDEFAULT,
        CW_USEDEFAULT, CW_USEDEFAULT,
        hWnd, None,
        g_hInst, None);
    console.write('hmph {}'.format(hwndTip))
    ctypes.windll.user32.SendMessageW(hwndTip , TTM_ADDTOOLW , 0, None )



if __name__ == '__main__':
    console.show()
    console.clear()
    console.write(__file__ + "::" + __name__ + "\n")
    dzt_unregister()
    dzt_register()
    dzt_ZoomCallback(dzt_ZoomCallback)
    dzt_exploreTooltips()
