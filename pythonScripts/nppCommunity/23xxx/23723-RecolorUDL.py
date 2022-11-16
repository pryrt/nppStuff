# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23723/

The user needs to update the list of dark_udls and light_udls a few lines down,
    where the names must exactly match the UDL name (as displayed in the Language menu)

Whenever you switch to a tab (or open a file in a new tab) and that tab has one of the
listed UDLs, it will do logic:
    if UDL is light and DarkMode is enabled, it will recolor the UDL
    if UDL id dark and DarkMode is not enabled, it will recolor the UDL
    otherwise, it will use the normal colors for the UDL

"""
from Npp import editor,notepad,console
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
from time import sleep
from math import sqrt, floor

windll.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
windll.user32.SendMessageW.restype  = LPARAM

class RecolorUDL(object):
    dark_udls = ["Markdown (preinstalled dark mode)"]
    light_udls = ["Markdown (preinstalled)"]
    all_udls = dark_udls + light_udls

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

    DEBUG = False
    VERSION = '1.0.0'

    def __init__(self):
        self.in_callback = False

        console.show()
        console.clear()
        console.write("RecolorUDL v{} in NPP v{} PythonScript v{}\n".format(self.VERSION, self.nppver(), notepad.getPluginVersion()))

        #self.example()

        ## register the callbacks, so that BufferActivated or LanguageChanged will trigger re-colorizing, as appropriate
        notepad.callback(self.callback, [NOTIFICATION.LANGCHANGED, NOTIFICATION.BUFFERACTIVATED])

        self.callback(None)
        return


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

    def example(self):
        self.DEBUG = True
        notepad.new()
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
        editor.setSavePoint() # fake save point
        editor.gotoPos(0xFFFFFFFF)
        sleep(1)

        if self.DEBUG: console.write("isDarkMode? {}\n".format(self.isDarkMode()))
        for udl in self.all_udls:
            if udl is not None:
                notepad.runMenuCommand('Language', udl)
            if self.DEBUG: console.write("set to UDL = '{}'\n".format(udl))
            sleep(2)
            self.callback(None)
            sleep(2)

        notepad.close()
        return

    def callback(self, args):
        if self.in_callback:
            return              # don't do a second callback if inside a first

        self.in_callback = True

        if self.DEBUG: console.write("callback called with args={}\n".format(args))
        ty = notepad.getLangType()
        if self.DEBUG: console.write("callback sees langtype={}\n".format(ty))
        if ty == LANGTYPE.USER:
            udl = (notepad.getLanguageName(ty))[6:]
            if self.DEBUG:
                console.write("DEBUG:\n\tgetLexerLanguage={}\n\tgetCurrentLanguage={}\n\tgetLanguageName={}\n\tgetLanguageDesc={}\n\tUDL = '{}'\n".format(
                    editor.getLexerLanguage(), notepad.getCurrentLang(),
                    notepad.getLanguageName(ty), notepad.getLanguageDesc(ty),
                    udl
                ))
            if udl in self.all_udls:
                self.recolorize(udl)

        self.in_callback = False

    def recolorize(self, udl):
        default_fg = editor.styleGetFore(0)
        default_bg = editor.styleGetBack(0)

        # If it's a DarkUDL and LightMode, it will invert; or if it's a LightUDL and DarkMode, but not if mode matches UDL
        darkUDLinLightMode = (udl in self.dark_udls) and (not self.isDarkMode())
        lightUDLinDarkMode = (udl in self.light_udls) and (self.isDarkMode())

        if darkUDLinLightMode or lightUDLinDarkMode:
            if self.DEBUG: console.write("RE-COLORIZING...\n")
            for sty in range(0,25):   # UDL has style numbers 0..24
                # only invert the foreground if it wasn't transparent/inherited or otherwise the same as the default fg
                fg = editor.styleGetFore(sty)
                if fg != default_fg:
                    hsl = self.rgb2hsl(fg)
                    hsl2 = (hsl[0], hsl[1], 1-hsl[2])   # invert the luminosity
                    rgb = self.hsl2rgb(hsl2)
                    if self.DEBUG: console.write("DEBUG: FG#{}\t{} = HSL:{} => HSL2:{} = rgb:{}\n".format(sty, fg, hsl, hsl2, rgb))
                    editor.styleSetFore(sty,tuple(rgb))

                # only invert the background if it wasn't transparent/inherited or otherwise the same as the default bg
                bg = editor.styleGetBack(sty)
                if bg != default_bg:
                    hsl = self.rgb2hsl(bg)
                    hsl2 = (hsl[0], hsl[1], 1-hsl[2])   # invert the luminosity
                    rgb = self.hsl2rgb(hsl2)
                    if self.DEBUG: console.write("DEBUG: BG#{}\t{} = HSL:{} => HSL2:{} = rgb:{}\n".format(sty, bg, hsl, hsl2, rgb))
                    editor.styleSetBack(sty,tuple(rgb))
        else:
            if self.DEBUG: console.write("NO INVERSION...\n")

        notepad.activateFile(notepad.getCurrentFilename()) # refresh UI

        return

    def isDarkMode(self):
        return 1L == windll.user32.SendMessageW(RecolorUDL.notepad_hwnd, 1024 + 1000 + 107, 0, 0)

    def rgb2hsl(self, rgb):
        """ rgb to fractional hsl tuple: "h" is H/60deg or H/40hue, so a number from 0 to 6, s and v are from 0 to 1, inclusive """
        # https://en.wikipedia.org/wiki/HSL_and_HSV
        # need to do a whole bunch of float conversion, because when I left it as integers from the RGB tuple, it did integer division,
        #   which caused saturation to be 0 or 1 all the time

        c = float(max(rgb) - min(rgb))
        l = 0.5*(max(rgb) + min(rgb))/255
        if c==0:
            h = 0
        elif max(rgb) == rgb[0]:
            h = float(rgb[1]-rgb[2])/c % 6.0
        elif max(rgb) == rgb[1]:
            h = float(rgb[2]-rgb[0])/c + 2.0
        elif max(rgb) == rgb[2]:
            h = float(rgb[0]-rgb[1])/c + 4.0
        else:
            raise ValueError("rgb2hsl(RGB={}) => c={}, max={}: max not found?!".format(rgb, c, max(rgb)))

        s = 0.0 if (l==0.0 or l==1.0) else (c/255.0) / (1.0 - abs(2.0*l - 1.0))

        #console.write("\tRGB:{} => c={} HSL:({:04.2f},{:06.2%},{:06.2%})\n".format(rgb, c, h, s, l))
        return (h,s,l)

    def hsl2rgb(self, hsl):
        """ fractional hsl back to rgb tuple """
        # https://en.wikipedia.org/wiki/HSL_and_HSV

        h,s,l = hsl
        c = (1.0 - abs(2.0 * l - 1.0)) * s * 255.0
        x = c*(1.0 - abs(h % 2.0 - 1.0))
        m = (l * 255.0 - c / 2.0)
        if h<1:
            rgb = ([int(floor(q+m)) for q in [c,x,0]])
        elif h<2:
            rgb = ([int(floor(q+m)) for q in [x,c,0]])
        elif h<3:
            rgb = ([int(floor(q+m)) for q in [0,c,x]])
        elif h<4:
            rgb = ([int(floor(q+m)) for q in [0,x,c]])
        elif h<5:
            rgb = ([int(floor(q+m)) for q in [x,0,c]])
        else:
            rgb = ([int(floor(q+m)) for q in [c,0,x]])

        return tuple(rgb)



RecolorUDL()

# use `notepad.clearCallbacks(); del(RecolorUDL)` in PythonScript console to reset everything during debug
