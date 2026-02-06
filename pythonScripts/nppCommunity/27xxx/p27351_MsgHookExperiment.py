# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27351/

Experimenting with hooking into the main message loop to look for WM_SIZE
based on @Alan-Kilborn's MsgHooker.py and the example script
found at <https://community.notepad-plus-plus.org/post/100127>
"""
from Npp import *
from MsgHooker import MH as MsgHook
WM_SIZE = 0x0005

def cb( hwnd, msg, wParam, lParam):
    console.write(f"cb(h:{hwnd}, m:{msg}, w:{wParam}, l:{lParam})\n")
    return False

mhe = MsgHook([ editor1.hwnd, editor2.hwnd ], cb, [WM_SIZE])

######################## the code below works
###
###     from Npp import *
###     from ctypes import WinDLL
###     from MsgHooker import MH as MsgHook
###
###     WM_SIZE = 0x0005
###     WM_MOUSEWHEEL = 0x020A
###     WM_SYSCOMMAND = 0x0112
###     SC_KEYMENU = 0xF100
###     VK_MENU = 0x12
###
###     def HIWORD(value): return (value >> 16) & 0xFFFF
###     def LOWORD(value): return value & 0xFFFF
###
###     user32 = WinDLL('user32')
###
###     def alt_held():
###         return (user32.GetAsyncKeyState(VK_MENU) & 0x8000) != 0
###
###     class MWHD(object):
###
###         def __init__(self):
###
###             # these must be assigned to "self" variables so that they aren't garbage collected!
###             self.mh1 = None #self.mh1 = MsgHook([ editor1.hwnd, editor2.hwnd ], self.editor_hook_func, [ WM_MOUSEWHEEL ])
###             self.mh2 = None #self.mh2 = MsgHook([ notepad.hwnd ], self.notepad_hook_func, [ WM_SYSCOMMAND ])
###             self.mh3 = MsgHook([ editor1.hwnd, editor2.hwnd ], self.editor_resize_hook, [ WM_SIZE ])
###
###         def __del__(self):
###             self.unhook()
###
###         def unhook(self):
###             if(self.mh1):
###                 self.mh1.unhook()
###                 self.mh1 = None
###             if(self.mh2):
###                 self.mh2.unhook()
###                 self.mh2 = None
###             if(self.mh3):
###                 self.mh3.unhook()
###                 self.mh3 = None
###             del self
###
###         def editor_hook_func(self, hwnd, msg, wParam, lParam):
###             wheel_delta = HIWORD(wParam)
###             if wheel_delta > 0x7FFF: wheel_delta -= 0x1_0000
###             keys_down = LOWORD(wParam)
###             alt_down = alt_held()
###             e = 'editor1' if hwnd == editor1.hwnd else 'editor2'
###             console.write(f"Editor Hook({e}:{hwnd:08x}, {msg:04x}, {wParam:08x}, {lParam:08x}): wheel_delta={wheel_delta}, alt_down={alt_down}, keys_down={keys_down}\n")
###             if alt_down and keys_down == 0:
###                 notepad.menuCommand(MENUCOMMAND.SEARCH_GOTONEXTFOUND if wheel_delta < 0 else MENUCOMMAND.SEARCH_GOTOPREVFOUND)
###                 return False
###             return True
###
###         # https://stackoverflow.com/questions/352270/how-to-cancel-the-system-key-down-state-in-windows
###         def notepad_hook_func(self, hwnd, msg, wParam, lParam):
###             e = 'editor1' if hwnd == editor1.hwnd else 'editor2'
###             console.write(f"NotepadHook({e}:{hwnd:08x}, {msg:04x}, {wParam:08x}, {lParam:08x}): {wParam & 0xFFF0:04x} vs {SC_KEYMENU:04x}\n")
###             if (wParam & 0xFFF0) == SC_KEYMENU and lParam == 0: return False
###             return True
###
###         def editor_resize_hook(self, hwnd, msg, wParam, lParam):
###             e = 'editor1' if hwnd == editor1.hwnd else 'editor2'
###             console.write(f"Resize Hook({e}:{hwnd:08x}, {msg:04x}, {wParam:08x}, {lParam:08x}) => width:{LOWORD(lParam)} x height:{HIWORD(lParam)}\n")
###             return False
###
###
###     MOUSE_WHEEL_HOOK_DEMO = MWHD()
###
###     """
###     MOUSE_WHEEL_HOOK_DEMO.unhook(); del MOUSE_WHEEL_HOOK_DEMO
###     """
###     import gc
###     gc.collect()
