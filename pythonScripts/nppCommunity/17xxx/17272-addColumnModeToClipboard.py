# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/17272/how-to-copy-columns-in-excel-and-paste-into-first-column-of-text-file-without-word-wrapping/3

The OP wanted to be able to paste a column of Excel data in column-paste mode.

My experiments with another tool showed that Notepad++ adds empty entries for 'MSDEVColumnSelect', 'Borland IDE Block Type' to indicate HTML mode.
I should be able to register those two, then add them in.  I think.

Unfortunately, pywin32 does not seem to be included with PythonScript, and asking someone to install those would be a big ask.
Might have to do it with individual ctypes win32 api calls, like eko used ain get_lexer_name, and I replicated in pyscFilteredViewerLibrary

Good news: user32 from wintypes.WinDLL('user32') does seem to be able to access it.
* translating algorithms from https://metacpan.org/source/JDB/Win32-Clipboard-0.58/Clipboard.xs

taking inspiration from
* https://github.com/mandubian/play/blob/master/python/Lib/site-packages/pyreadline/clipboard/win32_clipboard.py
* https://github.com/vsajip/pywinauto/blob/3f08937c2b7eed1d0c5c791d796fee20df41413e/pywinauto/clipboard.py
"""
from Npp import *
console.show()
console.clear()

import ctypes
from ctypes import *
user32 = ctypes.windll.user32
CF_COLUMN_SELECT = user32.RegisterClipboardFormatA('MSDEVColumnSelect')
console.write('Registered {} as #{}\n'.format('MSDEVColumnSelect',CF_COLUMN_SELECT))
CF_BORLAND_BLOCK = user32.RegisterClipboardFormatA('Borland IDE Block Type')
console.write('Registered {} as #{}\n'.format('Borland IDE Block Type',CF_BORLAND_BLOCK))

GetClipboardFormatName = windll.user32.GetClipboardFormatNameA
GetClipboardFormatName.argtypes=[c_uint,c_char_p,c_int]

GlobalLock = windll.kernel32.GlobalLock
GlobalAlloc = windll.kernel32.GlobalAlloc
GlobalUnlock = windll.kernel32.GlobalUnlock
memcpy = cdll.msvcrt.memcpy

GlobalAlloc.argtypes=[c_int, c_int]
GlobalLock.argtypes=[c_int]
GlobalUnlock.argtypes=[c_int]


GPTR=64
GHND=66

def clipboard_EnumClipboardFormats():
    if not( user32.OpenClipboard(None) ): raise Exception('user32.OpenClipboard failed!')

    #console.write("Opened clipboard\n")

    formatList = []
    prevFormat = 0
    nextFormat = user32.EnumClipboardFormats(prevFormat)
    while nextFormat != 0:
        formatList.append(nextFormat)
        #console.write("EnumClipboardFormats({}) = {}\n".format(prevFormat, nextFormat))
        prevFormat = nextFormat
        nextFormat = user32.EnumClipboardFormats(prevFormat)

    user32.CloseClipboard()
    #console.write("Final formatList = {}\n".format(formatList))
    return formatList

def clipboard_getClipboardFormatName(formatID):
    """grabs the clipboard format name

    follows logic of https://perlmonks.org/?node_id=1197101, with it's pre-allocated string and the call to the user32 api function
    """
    raise Exception("Cannot GetClipboardFormatName")
    bufferA = ctypes.create_string_buffer("___", 128)
    if not( user32.OpenClipboard(None) ): raise Exception('user32.OpenClipboard failed!')
    r = GetClipboardFormatName( formatID, bufferA, 128)
        # TODO = debugging; using https://github.com/mandubian/play/blob/master/python/Lib/site-packages/pyreadline/clipboard/win32_clipboard.py as an example of someone who used ctypes to access the clipboard
    user32.CloseClipboard()
    if r==0: raise WinError()
    console.write("GetClipboardFormatName({}) = #{}# '{}'".format(formatID, r, repr(bufferA.raw)))
    return bufferA

def clipboard_setClipboardValue(formatID, value):
    """sets the formatID entry of the clipboard to what's contained in the value"""
    console.write("setClipboardValue({}, {})\n".format(formatID, repr(value)))
    return None

def SetClipboardText(text):
    buffer = c_buffer(text)
    console.write(str(buffer)+"\n")
    bufferSize = sizeof(buffer)
    console.write(str(bufferSize)+"\n")
    hGlobalMem = GlobalAlloc(GHND, bufferSize) # GHND, bufferSize
    GlobalLock.restype = c_void_p
    lpGlobalMem = GlobalLock(hGlobalMem)
    console.write(str(lpGlobalMem)+"\n")
    memcpy(lpGlobalMem, addressof(buffer), c_int(bufferSize))
    GlobalUnlock(c_int(hGlobalMem))
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(c_int(CF_TEXT), c_int(hGlobalMem))
        CloseClipboard()


lst = clipboard_EnumClipboardFormats()
console.write("Final formatList = {}\n".format(lst))
# str = clipboard_getClipboardFormatName( lst[0] )
#clipboard_setClipboardValue( 1 , "This is the clipboard" )      # CF_TEXT
SetClipboardText("HI3")



# def forum_postNNNNN_FunctionName():
#     """this is the function's doc string"""
#     console.show()
#     console.clear()
#     console.write(__file__ + "::" + __name__ + "\n")
#     if forum_postNNNNN_FunctionName.__module__:
#         console.write("module: " + forum_postNNNNN_FunctionName.__module__ + "\n")
#     console.write("function docstring: ''" + forum_postNNNNN_FunctionName.__doc__ + "''\n")
#     console.write("file     docstring: ''" + __doc__.rstrip() + "''\n")
#
# if __name__ == '__main__': forum_postNNNNN_FunctionName()

"""
Access to clipboard:
    * https://stackoverflow.com/questions/101128/how-do-i-read-text-from-the-windows-clipboard-from-python | answer: https://stackoverflow.com/a/101167/5508606
        => uses pywin32's win32clipboard module to access
    * https://notepad-plus-plus.org/community/topic/17272/how-to-copy-columns-in-excel-and-paste-into-first-column-of-text-file-without-word-wrapping/3 => alan mentioned registering
        * win32clipboard.RegisterClipboardFormat() can be used to allow new format names
        * http://timgolden.me.uk/pywin32-docs/win32clipboard.html
        * https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-registerclipboardformata  and https://docs.microsoft.com/en-us/windows/desktop/dataxchg/clipboard-formats
        * need to browse source for other uses of those strings, so I can see how @DonHo _uses_ those formats, not just _registers_ those formats
    * I don't see how to do a column-copy or column-paste from PythonScript editor object
    * Perl:
        * clpExcelNpp.pl in my svn repo shows an example of how to use that.
        * https://perlmonks.org/?node_id=1197101 => shows how to mix Win32::API and Win32::Clipboard...

"""
""" @ekopalypse reply
import ctypes

def custom_paste():
    if ctypes.windll.user32.OpenClipboard(None):
        try:
            clipboard_handle = ctypes.windll.user32.GetClipboardData(1)
            if clipboard_handle:
                pointer_to_content = ctypes.windll.kernel32.GlobalLock(clipboard_handle)
                clipboard_data = ctypes.c_char_p(pointer_to_content).value
                ctypes.windll.kernel32.GlobalUnlock(clipboard_handle)
            else:
                raise ValueError('Invalid clipboard handle')
        except Exception as e:
            print('Error', e.message)
            return
        finally:
            # ensures that clipboard will be closed even in case of an exception
            ctypes.windll.user32.CloseClipboard()

        # there was no exception - start replacing targets
        lines = clipboard_data.splitlines()
        if len(lines) == editor.getSelections():
            for i, line in enumerate(lines):
                editor.setTarget(editor.getSelectionNStart(i), editor.getSelectionNEnd(i))
                editor.replaceTarget(line)
    else:
        print('Unable to open the clipboard - try again later')

custom_paste()
"""