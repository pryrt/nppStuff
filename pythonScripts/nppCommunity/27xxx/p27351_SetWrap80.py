# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27351/

Trying to implement @Coises idea for setting the wrap to exactly 80
"""
from Npp import *
import ctypes
from ctypes import wintypes
from MsgHooker import MH as MsgHook
WM_SIZE = 0x0005

# Define the RECT structure to match Win32 API
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

def pysc_setWrap80(ed=editor):
    #console.write("ed={}\n".format(ed))

    WRAPCHARS = 80

    # Setup the Win32 function prototype
    user32 = ctypes.windll.user32
    user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
    user32.GetClientRect.restype = wintypes.BOOL

    def get_window_size(hwnd):
        # 2. Instantiate the RECT structure
        rect = RECT()

        # 3. Call GetClientRect passing the rect by reference
        if user32.GetClientRect(hwnd, ctypes.byref(rect)):
            # 4. Parse the results
            # Client coordinates: top-left is always (0,0)
            return rect
        else:
            raise Exception("GetClientRect failed")

    sz = get_window_size(ed.hwnd)
    #console.write("{} => {}\n".format(ed.hwnd, {"width": sz.width(), "height": sz.height()}))

    usableWidth = sz.width()
    for m in range(0, 1+ed.getMargins()):
        w = ed.getMarginWidthN(m)
        usableWidth -= w
        #console.write("m#{}: {} => usableWidth: {}\n".format(m, w, usableWidth))

    widthWrappedChars = ed.textWidth(0,"_"*WRAPCHARS)+1 # one extra pixel to be able to show the VerticalEdge indicator line
    wantMargin = usableWidth - widthWrappedChars
    if wantMargin < 1:
        wantMargin = 0
    #console.write("{}\n".format({"windowWidth": sz.width(), "usableWidth": usableWidth, "pixelsFor80Char": widthWrappedChars, "wantMargin": wantMargin}))
    ed.setMarginRight(wantMargin)
    ed.setMarginLeft(0)

def HIWORD(value): return (value >> 16) & 0xFFFF
def LOWORD(value): return value & 0xFFFF

def pysc_size_callback( hwnd, msg, wParam, lParam):
    #console.write(f"cb(h:{hwnd}, m:{msg}, w:{wParam}, l:{lParam}) => {LOWORD(lParam)} x {HIWORD(lParam)}\n")
    if hwnd == editor1.hwnd:
        pysc_setWrap80(editor1)
    elif hwnd == editor2.hwnd:
        pysc_setWrap80(editor2)
    return True

pysc_setWrap80(editor1)
pysc_setWrap80(editor2)
pysc_size_hook = MsgHook([ editor1.hwnd, editor2.hwnd ], pysc_size_callback, [WM_SIZE])
console.write("SetWrap80 registered WM_SIZE callback\n")

def pysc_unsetWrap80(args=None):
    """
    To stop
    pysc_unsetWrap80()
    """
    editor1.setMarginRight(0)
    editor2.setMarginRight(0)
    global pysc_size_hook
    if pysc_size_hook:
        pysc_size_hook.unhook()
    del pysc_size_hook

# use the following in the console (no #) to stop it from always wrapping at 80
#
# pysc_unsetWrap80()

