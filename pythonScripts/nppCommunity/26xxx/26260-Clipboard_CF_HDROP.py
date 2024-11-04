# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26260/copying-file-itself-into-clipboard-in-notepad

Perl's Win32::Clipboard::GetFiles() just looks at the CF_HDROP...
    XS Source: https://metacpan.org/release/JDB/Win32-Clipboard-0.58/source/Clipboard.xs#L472-502
    - DragQueryFileA(): https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-dragqueryfilea
        - this is how you extract the Ith file from the HDROP list
    
But I think, despite assertions to the contrary, that 

- GetClipboardData(): https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboarddata
- SetClipboardData(): https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclipboarddata

Will eventually want to go through and enumerate them (see XS::EnumFormats for the wrapper), 
    look at the data structure for the HDROP handle contents
    ... would eventually need to allocate memory for the HDROP 



"""
from Npp import editor,notepad,console

import ctypes

c = ctypes.windll.user32.CountClipboardFormats()

class ThisIsTheClass(object):
    def go(self):
        #console.write("pass")
        pass

ThisIsTheClass().go()
