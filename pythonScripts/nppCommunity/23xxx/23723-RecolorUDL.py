# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23723/

My idea is to look at the HiddenLexers, especially the Colorize method,
and try to see if I can live-edit the UDL colors
"""
from Npp import editor,notepad,console
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
from time import sleep

windll.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
windll.user32.SendMessageW.restype  = LPARAM

class ThisIsTheClass(object):
    _lexer_name = b"Markdown (preinstalled)"
    _lexer_unic = create_unicode_buffer(_lexer_name)
    notepad_hwnd = windll.user32.FindWindowW(u'Notepad++', None)
    editor1_hwnd = windll.user32.FindWindowExW(notepad_hwnd, None, u"Scintilla", None)
    editor2_hwnd = windll.user32.FindWindowExW(notepad_hwnd, editor1_hwnd, u"Scintilla", None)

    # https://github.com/notepad-plus-plus/notepad-plus-plus/blob/b502266e8d70a5dc9069e13d2d18ef071aea5578/lexilla/include/SciLexer.h#L209-L233
    SCE_USER_STYLE_DEFAULT              = 0
    SCE_USER_STYLE_COMMENT              = 1
    SCE_USER_STYLE_COMMENTLINE          = 2
    SCE_USER_STYLE_NUMBER               = 3
    SCE_USER_STYLE_KEYWORD1             = 4
    SCE_USER_STYLE_KEYWORD2             = 5
    SCE_USER_STYLE_KEYWORD3             = 6
    SCE_USER_STYLE_KEYWORD4             = 7
    SCE_USER_STYLE_KEYWORD5             = 8
    SCE_USER_STYLE_KEYWORD6             = 9
    SCE_USER_STYLE_KEYWORD7             = 10
    SCE_USER_STYLE_KEYWORD8             = 11
    SCE_USER_STYLE_OPERATOR             = 12
    SCE_USER_STYLE_FOLDER_IN_CODE1      = 13
    SCE_USER_STYLE_FOLDER_IN_CODE2      = 14
    SCE_USER_STYLE_FOLDER_IN_COMMENT    = 15
    SCE_USER_STYLE_DELIMITER1           = 16
    SCE_USER_STYLE_DELIMITER2           = 17
    SCE_USER_STYLE_DELIMITER3           = 18
    SCE_USER_STYLE_DELIMITER4           = 19
    SCE_USER_STYLE_DELIMITER5           = 20
    SCE_USER_STYLE_DELIMITER6           = 21
    SCE_USER_STYLE_DELIMITER7           = 22
    SCE_USER_STYLE_DELIMITER8           = 23
    SCE_USER_STYLE_IDENTIFIER           = 24

    def __init__(self):

        console.show()
        console.clear()
        console.write("NPPv{}\ttxt:'{}' uni:'{}'\n".format(self.nppver(), self._lexer_name, self._lexer_unic))
        #if self.nppver() < 8.410:
        #    raise ValueError("NPP v{} is too old; upgrade to at least NPP v8.4.1".format(self.nppver()))
        #
        #self.ilexer_ptr = windll.user32.SendMessageW(self.notepad_hwnd, self.NPPM_CREATELEXER, 0, addressof(self._lexer_unic))


    def nppver(self):
        self.NPPM_GETNPPVERSION = 1024 + 1000 + 50
        nppv = windll.user32.SendMessageW(self.notepad_hwnd, self.NPPM_GETNPPVERSION, 1, 0 )
        # for v8.4.1 and newer, this will pad it as 8<<16 + 410 for easy comparison
        # v8.4 will be under old scheme of 8<<16 + 4, v8.3.3 is 8<<16 + 33
        ver = nppv >> 16    # major version
        mnr = nppv & 0xFFFF # minor version
        if (ver <= 8) and (mnr < 10):
            ver += mnr/10.
        elif (ver <= 8) and (mnr < 100):
            ver += mnr/100.
        elif (ver>8) or (mnr>99):
            ver += mnr/1000.

        return ver

    def go(self):
        #console.write("pass")
        #console.write("Current View = {}\nCurrent File:\n\t{}\n\t{}\n\t== {}\n".format(notepad.getCurrentView(), notepad.getCurrentFilename(), __file__, notepad.getCurrentFilename().lower() == __file__.lower()))
        #if notepad.getCurrentView()==0 and notepad.getCurrentFilename().lower() == __file__.lower():
        #    # if the current file is the script in view#0, move the script to the alternate view
        #    notepad.menuCommand(MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW)
        #    view0index = notepad.getCurrentDocIndex(0)
        #    notepad.activateIndex(0, view0index)

        # create a new file in the main view, and change it to UDL
        notepad.new()
        default_bg = editor.styleGetBack(0)

        notepad.runMenuCommand('Language', self._lexer_name)
        editor.setText("""# Hello World

This is it

- Bullet 1
- Bullet 2

1. Ordered
2. List

_italic_
**bold**

5 + 6
"""
        )
        editor.gotoPos(0xFFFF)
        for s in range(0,25):
            fg, bg = editor.styleGetFore(s), editor.styleGetBack(s)
            sfg = str(fg)
            sbg = str(bg)
            console.write("style#{}\tfg = ({}), bg = ({})\n".format(int(s),sfg,sbg))
        editor.setSavePoint() # fake save point

        editor.styleSetBack(self.SCE_USER_STYLE_COMMENTLINE, (0,255,255))
        notepad.activateFile(notepad.getCurrentFilename()) # refresh UI
        sleep(2)
        editor.styleSetBack(self.SCE_USER_STYLE_COMMENTLINE, (255,255,255))
        notepad.activateFile(notepad.getCurrentFilename()) # refresh UI
        sleep(2)
        notepad.close()
        pass

ThisIsTheClass().go()
