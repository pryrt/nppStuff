from ctypes import *
#http://pydoc.net/pyreadline/2.1/pyreadline.keysyms.winconstants/
CF_TEXT = 1
GPTR = 64
GHND = 66

console.show()
console.clear()

OpenClipboard = windll.user32.OpenClipboard
EmptyClipboard = windll.user32.EmptyClipboard
GetClipboardData = windll.user32.GetClipboardData
GetClipboardFormatName = windll.user32.GetClipboardFormatNameA
SetClipboardData = windll.user32.SetClipboardData
EnumClipboardFormats = windll.user32.EnumClipboardFormats
CloseClipboard = windll.user32.CloseClipboard
#OpenClipboard.argtypes=[c_int]
EnumClipboardFormats.argtypes=[c_int]
CloseClipboard.argtypes=[]
GetClipboardFormatName.argtypes=[c_uint,c_char_p,c_int]
GetClipboardData.argtypes=[c_int]
SetClipboardData.argtypes=[c_int,c_int]

GlobalLock = windll.kernel32.GlobalLock
GlobalAlloc = windll.kernel32.GlobalAlloc
GlobalUnlock = windll.kernel32.GlobalUnlock
GlobalLock.argtypes=[c_int]
GlobalUnlock.argtypes=[c_int]
memcpy = cdll.msvcrt.memcpy

def enum():
    OpenClipboard(None)
    q=EnumClipboardFormats(0)
    while q:
        print q,
        q=EnumClipboardFormats(q)
    CloseClipboard()

def getformatname(format):
    buffer = c_buffer(" "*100)
    bufferSize = sizeof(buffer)
    OpenClipboard(None)
    GetClipboardFormatName(format,buffer,bufferSize)
    CloseClipboard()
    return buffer.value

def GetClipboardText():
    console.writeError("entering GetClipboardText\n")
    text = ""
    if OpenClipboard(None):
        hClipMem = GetClipboardData(CF_TEXT)
        console.writeError("hClipMem={}\n".format(hClipMem))
        if hClipMem:
            GlobalLock.restype = c_char_p
            text = GlobalLock(hClipMem)
            GlobalUnlock(hClipMem)
        CloseClipboard()
    console.writeError("leaving GetClipboardText\n")
    return text

def SetClipboardText(text):
    buffer = c_buffer(text)
    bufferSize = sizeof(buffer)
    hGlobalMem = GlobalAlloc(c_int(GHND), c_int(bufferSize))
    GlobalLock.restype = c_void_p
    lpGlobalMem = GlobalLock(c_int(hGlobalMem))
    memcpy(lpGlobalMem, addressof(buffer), c_int(bufferSize))
    GlobalUnlock(c_int(hGlobalMem))
    if OpenClipboard(None):
        EmptyClipboard()
        SetClipboardData(c_int(CF_TEXT), c_int(hGlobalMem))
        CloseClipboard()

if __name__ == '__main__':
    txt=GetClipboardText()                            # display last text clipped
    console.write(repr(txt))