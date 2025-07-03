# encoding=utf-8
# https://community.notepad-plus-plus.org/post/97676
import ctypes
from ctypes import wintypes
from Npp import notepad

CF_HDROP = 15
GHND = 66

OpenClipboard = ctypes.windll.user32.OpenClipboard
OpenClipboard.argtypes = [ wintypes.HWND ]
OpenClipboard.restype = wintypes.BOOL

EmptyClipboard = ctypes.windll.user32.EmptyClipboard
EmptyClipboard.argtypes = []
EmptyClipboard.restype = wintypes.BOOL

SetClipboardData = ctypes.windll.user32.SetClipboardData
SetClipboardData.argtypes = [ wintypes.UINT, wintypes.HANDLE ]
SetClipboardData.restype = wintypes.HANDLE

CloseClipboard = ctypes.windll.user32.CloseClipboard
CloseClipboard.argtypes = []
CloseClipboard.restype = wintypes.BOOL

GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalLock.argtypes = [ wintypes.HGLOBAL ]
GlobalLock.restype = wintypes.LPVOID

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
GlobalAlloc.restype = wintypes.HGLOBAL

GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalUnlock.argtypes = [ wintypes.HGLOBAL ]
GlobalUnlock.restype = wintypes.BOOL

memcpy = ctypes.cdll.msvcrt.memcpy
memcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]

addressof = ctypes.addressof

class POINT(ctypes.Structure):
    _fields_ = [
        ('x', wintypes.LONG),
        ('y', wintypes.LONG)
    ]

class DROPFILES(ctypes.Structure):
    _fields_ = [
        ('pFiles', wintypes.DWORD),
        ('pt', POINT),
        ('fNC', wintypes.BOOL),
        ('fWide', wintypes.BOOL),
    ]

def dump_mem(addr, size):
    mem = list((ctypes.c_ubyte * size).from_address(addr))
    print(mem)

def main():
    path = ctypes.create_unicode_buffer(notepad.getCurrentFilename())
    path_size = ctypes.sizeof(path)
    df_size = ctypes.sizeof(DROPFILES)
    total_size = df_size + path_size + 2  # The data that follows the structure is a double null-terminated list of file names.

    df = DROPFILES()
    df.pFiles = df_size
    df.fWide = True

    h_global_mem = GlobalAlloc(GHND, total_size)  # allocate enough memory to hold the df struct and the full path
    if h_global_mem:
        lp_global_mem = GlobalLock(h_global_mem)  # lock and get the pointer to the memory
        memcpy(lp_global_mem, addressof(df), df_size)  # first copy the df struct
        memcpy(lp_global_mem+df_size, addressof(path), path_size)  # now copy the full path name
        dump_mem(lp_global_mem, total_size)
        GlobalUnlock(h_global_mem)
        res = OpenClipboard(notepad.hwnd)  # but 0 should be fine as well
        if res:
            if not EmptyClipboard():
                print('ERROR EmptyClipboard failed')
            if SetClipboardData(CF_HDROP, h_global_mem) is None:
                print('ERROR SetClipboardData failed')
            CloseClipboard()
        else:
            print('ERROR OpenClipboard', res)
    else:
        print('ERROR GlobalAlloc', h_global_mem)

main()
