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

from struct import pack, unpack


def sb7_register():
    """this will register a function to the UPDATEUI event"""
    editor.callback(sb7_StatusBarCallback, [SCINTILLANOTIFICATION.UPDATEUI])

def sb7_unregister():
    """this will clear a function to the UIUPDATE event"""
    editor.clearCallbacks(sb7_StatusBarCallback)

def sb7_StatusBarCallback(args):
    """
    this is the UIUPDATE status bar callback

    1. count the existing statusbar sections;
    2. if only 6
        1. grab right edges using SB_GETPARTS
        2. scale or shift the right edges to the left
        3. SB_SETPARTS n+1
        4. my_sect = (n+1) - 1
       else
        1. my_sect = 6 (the 7th section, base 0)
    3. SB_SETTEXT(my_sect, "PCJ")


    references:
        create a mutable buffer (allocate virtual buffer):
            https://docs.python.org/2/library/ctypes.html?highlight=ctypes%20create_unicode_buffer#ctypes.create_string_buffer
        equivalent of perl unpack():
            https://docs.python.org/2/library/struct.html?highlight=struct#struct.unpack
    """
    console.write("{}\n".format(args))
    sb7_StatusBarCallback.APP_HANDLE = FindWindow(u"Notepad++", None)
    console.write("\t{:8s}0x{:08x}\n".format("hWnd:", sb7_StatusBarCallback.APP_HANDLE))
    sb7_StatusBarCallback.STATUSBAR_HANDLE = None

    def EnumCallback(hwnd, lparam):
        curr_class = create_unicode_buffer(256)
        GetClassName(hwnd, curr_class, 256)
        if curr_class.value.lower() == "msctls_statusbar32":
            sb7_StatusBarCallback.STATUSBAR_HANDLE = hwnd
            console.write("\t{:8s}0x{:08x}\n".format("sbWnd:", sb7_StatusBarCallback.STATUSBAR_HANDLE))
            return False
        return True

    EnumChildWindows(sb7_StatusBarCallback.APP_HANDLE, WNDENUMPROC(EnumCallback), 0)

    def sb_getparts():
        nParts = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, 0, 0)
        console.write("sb_getparts() -> nParts = {}\n".format(nParts))
        nBytes = 4 * nParts
        buf = create_string_buffer(nBytes)
        retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, nParts, buf)
        console.write("\tretcode = {}\n".format(retcode))
        ints = unpack('i'*nParts, buf[:nBytes])
        console.write("\tbuf = {:s} = {:s}\n".format(repr(buf[:nBytes]), ints))
        del buf
        return ints

    sb_getparts()

    def sb_gettext(sec):
        nChars = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETTEXTLENGTHW, int(sec), 0)
        console.write("sb_gettext({}) -> SendMessage(0x{:08x}, 0x{:04x}, {}, {}) => {}\n".format(sec, sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETTEXTLENGTHW, sec, 0, nChars))
        # it's using the same hwnd and messageid as my perl script with the same wparam and lparam values, but for some reason, it's (almost) always returning 0
        #   (one time, sb_gettext(0) returned 11, which is the length of "Python File")
        nBytes = 512
        buf = create_string_buffer(nBytes)
        nCharsGot = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETTEXTW, int(sec), buf)
        console.write("\tGETTEXTW = '{:s}' ({:d})\n".format(repr(buf[:nBytes]), nCharsGot))
        del buf

    for i in range(6):
        sb_gettext(i)

    def sb_setparts(*args):
        console.write("sb_setparts({:s})\n".format(args))
        nParts = len(args)
        nBytes = 4 * nParts
        buf = create_string_buffer(nBytes)
        buf[:nBytes] = pack('i'*nParts, *args)
        console.write("\tedit buf = {:s} = {:s}\n".format(repr(buf[:nBytes]), unpack('i'*nParts, buf[:nBytes]) ))
        retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_SETPARTS, nParts, buf)
        console.write("\tretcode = {}\n".format(retcode))

    sb_setparts((200,400,600,800,1000,1200))        # resize the six sections

    sb_setparts((200,400,600,800,1000,1200,1400))   # add a seventh section

    sb7_unregister()
    return

    nParts = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, 0, 0)
    console.write("\tnParts = {}\n".format(nParts))
    if nParts < 7:
        # grab the existing edges
        length = 4*nParts
        buf = create_string_buffer(length)
        retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, nParts, buf)
        console.write("\tretcode = {}\n".format(retcode))
        console.write("\tbuf = {:s}\n".format(repr(buf[:length])))
        ints = unpack('i'*nParts, buf[:length])
        console.write("\told ints = {:s}\n".format(ints))

        # try to just resize the existing sections
        buf[:length] = pack('iiiiii', 100,200,300,400,500,600)
        console.write("\tedit buf = {:s}\n".format(repr(buf[:length])))
        console.write("\tedit ints = {:s}\n".format(unpack('i'*nParts, buf[:length])))
        retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_SETPARTS, nParts, buf)
        console.write("\tretcode = {}\n".format(retcode))

        # try an extra section
        l2 = 4*(nParts+1)
        b2 = create_string_buffer(l2)
        b2[:l2] = pack('iiiiiii', 100, 200, 300, 400, 500, 600, 700)
        console.write("\tedit b2 = {:s}\n".format(repr(b2[:l2])))
        console.write("\tedit i2 = {:s}\n".format(unpack('i'*(1+nParts), b2[:l2])))
        retcode = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_SETPARTS, 1+nParts, b2)
        console.write("\tretcode = {}\n".format(retcode))

        # check my work
        nParts = SendMessage(sb7_StatusBarCallback.STATUSBAR_HANDLE, SB_GETPARTS, nParts+1, buf)
        console.write("\tnParts = {}\n".format(nParts))

    #endif nParts<7

    ##### my $str = "PCJ";
    ##### my $slen = length($str);
    ##### my $bytes = Encode::encode('ucs2-le', $str);
    ##### my $blen = length($bytes);
    ##### my $wbuf = Win32::GuiTest::AllocateVirtualBuffer( $hWnd, $blen );
    ##### Win32::GuiTest::WriteToVirtualBuffer($wbuf, $bytes);
    ##### my $settext = SendMessage($sbWnd, SB_SETTEXTW, $getparts, $wbuf->{ptr});
    ##### Win32::GuiTest::FreeVirtualBuffer($wbuf);
    wbytes = u"PCJ".encode('utf-16-le')
    wlen = len(wbytes)
    console.write("\tPCJ = {:d}:'{:s}'\n".format(wlen,repr(wbytes)))



if __name__ == '__main__':
    console.show()
    sb7_unregister()
    sb7_register()
