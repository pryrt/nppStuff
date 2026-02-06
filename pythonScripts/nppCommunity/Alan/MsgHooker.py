# -*- coding: utf-8 -*-
# original author: @Alan-Kilborn
# reference: https://community.notepad-plus-plus.org/post/100127
# modified by: @PeterJones
#   - updated to add the .unhook() and .__del__() methods

import platform
from ctypes import (WinDLL, WINFUNCTYPE)
from ctypes.wintypes import (HWND, INT, LPARAM, UINT, WPARAM)

user32 = WinDLL('user32')

GWL_WNDPROC = -4  # used to set a new address for the window procedure

LRESULT = LPARAM

WndProcType = WINFUNCTYPE(
    LRESULT,  # return type
    HWND, UINT, WPARAM, LPARAM  # function arguments
    )

running_32bit = platform.architecture()[0] == '32bit'
SetWindowLong = user32.SetWindowLongW if running_32bit else user32.SetWindowLongPtrW
SetWindowLong.restype = WndProcType
SetWindowLong.argtypes = [ HWND, INT, WndProcType ]

class MH(object):

    def __init__(self,
            hwnd_to_hook_list,
            hook_function,  # supplied hook_function must have args:  hwnd, msg, wparam, lparam
                            #  and must return True/False (False means the function handled the msg)
            msgs_to_hook_list=None,  # None means ALL msgs
            ):
        self.users_hook_fn = hook_function
        self.msg_list = msgs_to_hook_list if msgs_to_hook_list is not None else []
        self.new_wnd_proc_hook_for_SetWindowLong = WndProcType(self._new_wnd_proc_hook)  # the result of this call must be a self.xxx variable!
        self.orig_wnd_proc_by_hwnd_dict = {}
        for h in hwnd_to_hook_list:
            self.orig_wnd_proc_by_hwnd_dict[h] = SetWindowLong(h, GWL_WNDPROC, self.new_wnd_proc_hook_for_SetWindowLong)
            v = self.orig_wnd_proc_by_hwnd_dict[h]
            #print(f"add {h:08x} => {v}")

    def __del__(self):
        self.unhook()

    def unhook(self):
        #print(f"unhook: self:{self} => <{self.orig_wnd_proc_by_hwnd_dict}>");
        mykeys = []
        for h in self.orig_wnd_proc_by_hwnd_dict.keys():
            orig = self.orig_wnd_proc_by_hwnd_dict[h]
            print(f"\tdel {h:08x} => {orig}")
            SetWindowLong(h, GWL_WNDPROC, orig)
            mykeys.append(h)
        for h in mykeys:
            del self.orig_wnd_proc_by_hwnd_dict[h]

    def _new_wnd_proc_hook(self, hwnd, msg, wParam, lParam):
        retval = True  # assume that this message will go unhandled (by us)
        need_to_call_orig_proc = True
        if len(self.msg_list) == 0 or msg in self.msg_list:
            retval = self.users_hook_fn(hwnd, msg, wParam, lParam)
            if not retval: need_to_call_orig_proc = False
        if need_to_call_orig_proc:
            retval = self.orig_wnd_proc_by_hwnd_dict[hwnd](hwnd, msg, wParam, lParam)

        return retval

