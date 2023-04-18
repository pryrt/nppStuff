# encoding=utf-8
"""
I am going to take from dev-zoom-tooltips and Win32::Mechanize::NotepadPlusPlus/#65
and see if I can force my extra toolbar section to be listed all the time...

https://github.com/pryrt/Win32-Mechanize-NotepadPlusPlus/issues/65#issuecomment-904112745

"""

from Npp import *
import ctypes

from ctypes.wintypes import BOOL, HWND, LPARAM
WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
FindWindow = ctypes.windll.user32.FindWindowW
SendMessage = ctypes.windll.user32.SendMessageW
EnumChildWindows = ctypes.windll.user32.EnumChildWindows
GetClassName = ctypes.windll.user32.GetClassNameW
create_unicode_buffer = ctypes.create_unicode_buffer
create_string_buffer = ctypes.create_string_buffer
WM_USER = 0x400
SB_SETPARTS = WM_USER + 4;
SB_GETPARTS = WM_USER + 6;
SB_SETTEXTA = WM_USER + 1
SB_SETTEXTW = WM_USER + 11
SB_GETTEXTA = WM_USER + 2
SB_GETTEXTW = WM_USER + 13
SB_GETTEXTLENGTHA = WM_USER + 3
SB_GETTEXTLENGTHW = WM_USER + 12

def get_sb_handle():
    get_sb_handle.HANDLE = None

    def EnumCallback(hwnd, lparam):
        curr_class = create_unicode_buffer(256)
        GetClassName(hwnd, curr_class, 256)
        if curr_class.value.lower() == "msctls_statusbar32":
            get_sb_handle.HANDLE = hwnd
            #console.write("\t{:8s}0x{:08x}\n".format("sbWnd:", hwnd))
            return False
        return True

    EnumChildWindows(APP_HANDLE, WNDENUMPROC(EnumCallback), 0)

    return get_sb_handle.HANDLE

# editor.setStatusBar

console.show()
console.write(__file__ + "::" + __name__ + "\n")
APP_HANDLE = FindWindow(u"Notepad++", None)
console.write("\t{:32s}0x{:08x}\n".format("Notepad++ hWnd:", APP_HANDLE))
STATUSBAR_HANDLE = get_sb_handle()
console.write("\t{:32s}0x{:08x}\n".format("StatusBar hWnd:", STATUSBAR_HANDLE))
for sec in range(6):
    ret = SendMessage(STATUSBAR_HANDLE, 0x040c, sec, 0)
    console.write("\tSendMessage(0x{:08x}, 0x{:04x}, {}, {}) => {}\n".format(STATUSBAR_HANDLE, 0x040c, sec, 0, ret))

print SendMessage(STATUSBAR_HANDLE, 0x040c, 0, 0)
print SendMessage(STATUSBAR_HANDLE, 0x040c, 1, 0)
print SendMessage(STATUSBAR_HANDLE, 0x040c, 2, 0)
print SendMessage(STATUSBAR_HANDLE, 0x040c, 3, 0)
print SendMessage(STATUSBAR_HANDLE, 0x040c, 4, 0)
print SendMessage(STATUSBAR_HANDLE, 0x040c, 5, 0)
print SendMessage
# print SendMessage(0x001e0b22, 0x040c, 0, 0)
