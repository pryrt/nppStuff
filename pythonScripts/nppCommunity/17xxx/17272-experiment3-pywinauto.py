# https://github.com/vsajip/pywinauto/blob/3f08937c2b7eed1d0c5c791d796fee20df41413e/pywinauto/clipboard.py

console.show()
console.clear()

import ctypes
from ctypes import *

user32 = ctypes.windll.user32
GetClipboardData = ctypes.windll.user32.GetClipboardData
OpenClipboard    = ctypes.windll.user32.OpenClipboard
EmptyClipboard   = ctypes.windll.user32.EmptyClipboard
CloseClipboard   = ctypes.windll.user32.CloseClipboard
CountClipboardFormats  = ctypes.windll.user32.CountClipboardFormats
EnumClipboardFormats   = ctypes.windll.user32.EnumClipboardFormats
GetClipboardFormatName = ctypes.windll.user32.GetClipboardFormatNameW

_standard_formats = {
    1: 'CF_TEXT',
    2: 'CF_BITMAP',
    3: 'CF_METAFILEPICT',
    4: 'CF_SYLK',
    5: 'CF_DIF',
    6: 'CF_TIFF',
    7: 'CF_OEMTEXT',
    8: 'CF_DIB',
    9: 'CF_PALETTE',
    10: 'CF_PENDATA',
    11: 'CF_RIFF',
    12: 'CF_WAVE',
    13: 'CF_UNICODETEXT',
    14: 'CF_ENHMETAFILE',
    15: 'CF_HDROP',
    16: 'CF_LOCALE',
}

console.write("{}\n".format(1 in _standard_formats))
console.write("{}\n".format(17 in _standard_formats))

def clipboard_EnumClipboardFormats():
    if not( user32.OpenClipboard(None) ): raise Exception('user32.OpenClipboard failed!')

    console.write("Opened clipboard\n")

    formatList = []
    prevFormat = 0
    nextFormat = user32.EnumClipboardFormats(prevFormat)
    while nextFormat != 0:
        formatList.append(nextFormat)
        console.write("EnumClipboardFormats({}) = {}\n".format(prevFormat, nextFormat))
        prevFormat = nextFormat
        nextFormat = user32.EnumClipboardFormats(prevFormat)

    user32.CloseClipboard()
    console.write("Final formatList = {}\n".format(formatList))
    return formatList

def GetFormatName(format):
    "Get the string name for a format value"

    # standard formats should not be passed to GetClipboardFormatName
    if format in _standard_formats:
        return _standard_formats[format]

    if not OpenClipboard(None):
        raise WinError()

    max_size = 500
    buffer_ = ctypes.create_unicode_buffer(max_size+1)

    ret = GetClipboardFormatName(format, ctypes.byref(buffer_), max_size)
    console.write("GetClipboardFormatName ret={}\n".format(ret))

#    if not ret:
#        raise WinError()
#        #raise RuntimeError("test")

    CloseClipboard()

    return buffer_.value

clipboard_EnumClipboardFormats()
rng = range(1,17)
rng.append(55)
for nu in rng:
    nm = GetFormatName(nu)
    console.write("Name({}) = _{}_\n".format(nu,nm))

