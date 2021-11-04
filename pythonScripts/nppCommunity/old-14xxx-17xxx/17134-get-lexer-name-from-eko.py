# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/16870/

other notes go here
"""
from Npp import *
import ctypes
import ctypes.wintypes as wintypes

user32 = wintypes.WinDLL('user32')
WM_USER = 1024
NPPMSG = WM_USER+1000
NPPM_GETLANGUAGEDESC = NPPMSG+84

def get_lexer_name(hwnd):
    ''' Returns the text which is shown in the first field of the statusbar

        original author:    @Eko-palypse aka @ekopalypse
        source url:         https://notepad-plus-plus.org/community/topic/17134/enhance-udl-lexer

        Normally one might use notepad.getLanguageName(notepad.getLangType())
        but because this resulted in some strange crashes on my environment ctypes is used.

        Args:
            None
        Returns:
            None
    '''
    if hwnd is None: hwnd = user32.FindWindowW(u'Notepad++', None)
    language = notepad.getLangType()
    length = user32.SendMessageW(hwnd, NPPM_GETLANGUAGEDESC, language, None)
    buffer = ctypes.create_unicode_buffer(u' ' * length)
    user32.SendMessageW(hwnd, NPPM_GETLANGUAGEDESC, language, ctypes.byref(buffer))
    #console.write(buffer.value+"\n")  # uncomment if unsure how the lexer name in configure should look like - npp restart needed
    return buffer.value

console.show()
console.clear()
npp_hwnd = user32.FindWindowW(u'Notepad++', None)
firstBufferID = notepad.getCurrentBufferID()
for (filename, bufferID, index, view) in notepad.getFiles():
    notepad.activateBufferID( bufferID )
    eko = get_lexer_name(npp_hwnd)
    ori = notepad.getLanguageName(notepad.getLangType())
    dsc = notepad.getLanguageDesc(notepad.getLangType())
    console.write("file='{}'\n\teko=|{}|\n\tori=|{}|\n\tdsc=|{}|\n".format(filename, eko,ori,dsc))
    xGetCurrentLang = notepad.getCurrentLang()  # LANGTYPE -- this is the one I used
    xGetLangType = notepad.getLangType()        # LANGTYPE -- this is the one eko referenced
    console.write("\tgcl={} glt={}\n".format(xGetCurrentLang, xGetLangType))

notepad.activateBufferID( firstBufferID )
