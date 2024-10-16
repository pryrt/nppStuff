# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26203/

Running this script will _insert_ the clipboard instead of _pasting_ the clipboard, so the typing caret won't move
"""
from Npp import editor
import ctypes

def get_clipboard_text():
    """https://stackoverflow.com/a/23285159/5508606"""
    CF_TEXT = 1

    kernel32 = ctypes.windll.kernel32
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32 = ctypes.windll.user32
    user32.GetClipboardData.restype = ctypes.c_void_p

    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value
    finally:
        user32.CloseClipboard()

editor.insertText(editor.getCurrentPos(), get_clipboard_text())
