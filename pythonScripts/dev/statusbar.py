# encoding=utf-8
"""StatusBar Manipulation

published as https://community.notepad-plus-plus.org/post/69314

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! USER WARNING: STATUS BAR MAY FLASH DURING UPDATE !!!
!!! FLASH-SENSITIVE USERS SHOULD NOT USE THIS SCRIPT !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Complete example:
* implements a class for StatusBar manipulation
* includes a method which adds an extra StatusBar section
* includes an example callback to force it to a particular string
    (this could be changed so the callback puts some piece of particular
    info into the status bar)
* shows a 10sec example of it being used; note, because Notepad++ resets
    the status bar every time it changes tabs, you can see it flashing
    frequently
"""

from Npp import *
import ctypes
from ctypes.wintypes import BOOL, HWND, WPARAM, LPARAM, UINT
from struct import pack, unpack
from time import sleep

class _SB(object):
    """refer to these values as _SB.xxxx elsewhere"""
    LRESULT = LPARAM
    WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    WM_USER = 0x400
    SB_SETPARTS = WM_USER + 4
    SB_GETPARTS = WM_USER + 6
    SB_SETTEXTA = WM_USER + 1
    SB_SETTEXTW = WM_USER + 11
    SB_GETTEXTA = WM_USER + 2
    SB_GETTEXTW = WM_USER + 13
    SB_GETTEXTLENGTHA = WM_USER + 3
    SB_GETTEXTLENGTHW = WM_USER + 12
    SBT_OWNERDRAW = 0x1000
    ctypes.windll.user32.SendMessageW.restype = LRESULT
    ctypes.windll.user32.SendMessageW.argtypes = [ HWND, UINT, WPARAM, LPARAM ]

_SB() # call it to initialize


class NppStatusBar(object):
    """implement a class wrapper around the status bar"""

    def __init__(self):
        self._APP = None
        self._HANDLE = None

        def EnumCallback(hwnd, lparam):
            curr_class = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, curr_class, 256)
            if curr_class.value.lower() == "msctls_statusbar32":
                self._HANDLE = hwnd
                #console.write("\t{:32s}0x{:08x}\n".format("sbWnd:", hwnd))
                return False
            return True

        # console.write("\n" + __file__ + "::" + str(self.__class__) + "\n")
        self._APP = ctypes.windll.user32.FindWindowW(u"Notepad++", None)
        # console.write("\t{:32s}0x{:08x}\n".format("Notepad++ hWnd:", self._APP))
        ctypes.windll.user32.EnumChildWindows(self._APP, _SB.WNDENUMPROC(EnumCallback), 0)
        # console.write("\t{:32s}0x{:08x}\n".format("StatusBar hWnd:", self._HANDLE))

        self.__debugStatusBarSections()

    def __debugStatusBarSections(self):
        for sec in [STATUSBARSECTION.DOCTYPE,STATUSBARSECTION.DOCSIZE,STATUSBARSECTION.CURPOS,STATUSBARSECTION.EOFFORMAT,STATUSBARSECTION.UNICODETYPE,STATUSBARSECTION.TYPINGMODE]:
            self.getStatusBarText(sec)

    def getStatusBarText(self, sec):
        section = int(sec)
        retcode = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_GETTEXTLENGTHW, section, 0)
        length = retcode & 0xFFFF
        sbtype = (retcode>>16) & 0xFFFF
        assert (sbtype != _SB.SBT_OWNERDRAW)
        text_buffer = ctypes.create_unicode_buffer(length)
        retcode = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_GETTEXTW, section, ctypes.addressof(text_buffer))
        text = '{}'.format(text_buffer[:length])
        del text_buffer
        # console.write("\tSendMessage(0x{:08x}, 0x{:04x}, {:d}, {:d}) => 0x{:04x} 0x{:04x} \"{:s}\"\n".format(self._HANDLE, _SB.SB_GETTEXTLENGTHW, section, 0, sbtype, length, text))
        return text

    def setStatusBarText(self, sec, txt):
        section = int(sec)
        if section <= 5:
            notepad.setStatusBar(STATUSBARSECTION.values[sec], txt)
        else:
            nChars = len(txt)
            text_buffer = ctypes.create_unicode_buffer(nChars)
            text_buffer[:nChars] = txt[:nChars]
            # console.write(repr(text_buffer))
            retcode = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_SETTEXTW, section, ctypes.addressof(text_buffer))
            del text_buffer
            # console.write("\t...\n")
            # sleep(1)
            # console.write("\t... done\n")

    def getStatusBarNumberOfSections(self):
        nParts = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_GETPARTS, 0, 0)
        return nParts & 0xFFFF

    def getStatusBarParts(self):
        nParts = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_GETPARTS, 0, 0)
        # console.write("getStatusBarParts() -> nParts = {}\n".format(nParts))
        nBytes = 4 * nParts
        buf = ctypes.create_string_buffer(nBytes)
        retcode = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_GETPARTS, nParts, ctypes.addressof(buf))
        #retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, nParts, buf)
        # console.write("\tretcode = {}\n".format(retcode))
        ints = unpack('i'*nParts, buf[:nBytes])
        # console.write("\tbuf = {:s} = {:s}\n".format(repr(buf[:nBytes]), ints))
        del buf
        return ints

    def setStatusBarParts(self, *args):
        # console.write("setStatusBarParts({:s})\n".format(args))
        nParts = len(args)
        nBytes = 4 * nParts
        buf = ctypes.create_string_buffer(nBytes)
        buf[:nBytes] = pack('i'*nParts, *args)
        # console.write("\tedit buf = {:s} = {:s}\n".format(repr(buf[:nBytes]), unpack('i'*nParts, buf[:nBytes]) ))
        retcode = ctypes.windll.user32.SendMessageW(self._HANDLE, _SB.SB_SETPARTS, nParts, ctypes.addressof(buf))
        # console.write("\tretcode = {}\n".format(retcode))

    def addStatusBarSection(self, text, width):
        # console.write("addStatusBarSection({:s})\n".format(text))
        oldParts = self.getStatusBarParts()
        nParts = len(oldParts)
        subtract = int(width / nParts)
        scaled = map(lambda x: x-subtract, oldParts)
        scaled.append( oldParts[-1] )
        self.setStatusBarParts( *scaled )
        self.setStatusBarText( nParts, text )

    def example_setSeventhSection(self, txt, width):
        """
        If there are 7 sections, update text;
        if less, add a section and
        """
        n = self.getStatusBarNumberOfSections()
        if n==7:
            self.setStatusBarText(n-1, txt)
        else:
            self.addStatusBarSection(txt, width)

def example_callback(args):
    sb.example_setSeventhSection("Example", 360)

console.show()
sb = NppStatusBar()
editor.callback(example_callback, [SCINTILLANOTIFICATION.UPDATEUI])
example_callback(None) # call it once to update the UI manually
console.write("For the next 10s, should say Example... \n")
console.write("... even if you UpdateUI (change tabs, etc)\n")
sleep(10)
editor.clearCallbacks(example_callback)
console.write("... DONE.  The next UpdateUI will clear it.\n")

