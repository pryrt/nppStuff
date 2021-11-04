# encoding=utf-8
"""from ekopalypse's  https://notepad-plus-plus.org/community/topic/17992/how-to-get-the-scintilla-view0-view1-hwnds/8"""
from Npp import *
import ctypes, ctypes.wintypes

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                     ctypes.wintypes.HWND,
                                     ctypes.wintypes.LPARAM)

user32 = ctypes.WinDLL('user32', use_last_error=True)
scintilla_hwnd = {0:None, 1:None}

def find_scintilla_windows(npp_handle):

    def foreach_window(hwnd, lParam):
        curr_class = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, curr_class, 256)

        if curr_class.value == 'Scintilla':
            if user32.GetParent(hwnd) == npp_handle:
                if scintilla_hwnd[0] is None:
                    scintilla_hwnd[0] = hwnd
                elif scintilla_hwnd[1] is None:
                    scintilla_hwnd[1] = hwnd
                    console.write("type(scintilla_hwnd)={}, len()={}\n".format(scintilla_hwnd, len(scintilla_hwnd)))
                    #return False
                else:
                    scintilla_hwnd[ len(scintilla_hwnd) ] = hwnd
        return len(scintilla_hwnd)>=1

    return not user32.EnumChildWindows(npp_handle,
                                       EnumWindowsProc(foreach_window),
                                       None)

console.show()
console.clear()
find_scintilla_windows(user32.FindWindowW(u'Notepad++', None))
console.write("{}".format(scintilla_hwnd))