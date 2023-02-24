# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24173/

Enables the lexer.cpp.track.preprocessor property when it's a C/CPP file;
also needs to set a style for the appropriate StyleID (though I don't know what it is yet)

### === INSTRUCTIONS ===

1. Follow the [FAQ](https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript) to install PythonScript plugin and this script
2. Run it once normally (per the Usage section of the FAQ)
3. Go to a C/C++ file, and see that code like the following will have different colors for ELSEWHAT and THEREFORE
    ~~~
    #define XYZ
    #ifdef XYZ
    #define ELSEWHAT
    #else
    #define THEREFORE
    #endif
    ~~~
4. If you want this to run every time you run Notepad++,
    1. I assume you named the script PreProcessor24173.py
    2. Put the following lines in your "user startup" script (the FAQ explains how to find that)



"""
from Npp import editor, notepad, console, NOTIFICATION

class PreProcessor24173(object):
    SCE_C_DEFAULT = 0
    SCE_C_PREPROCESSOR = 9
    SCE_C_PREPROC_HIDDEN = 64 | SCE_C_PREPROCESSOR

    def __init__(self):
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED, NOTIFICATION.LANGCHANGED])
        self.on_bufferactivated(None)
        console.write("Registered PreProcessor24173 for C/C++ PREPROCESSOR #define tracking\n")

    def on_bufferactivated(self,args):
        lexer = editor.getLexerLanguage()
        langtype = "{}".format(notepad.getCurrentLang())
        if lexer == 'cpp':
            self.update_cpp()

    def update_cpp(self):
        editor.setProperty("lexer.cpp.track.preprocessor", 1)
        bg = editor.styleGetBack(self.SCE_C_PREPROCESSOR)
        fg = editor.styleGetFore(self.SCE_C_PREPROCESSOR)
        clr = ( (bg[0]+fg[0])//2, (bg[1]+fg[1])//2, (bg[2]+fg[2])//2 ) # halfway between FG and BG
        editor.styleSetFore(self.SCE_C_PREPROC_HIDDEN, clr)

if __name__ == '__main__':
    # notepad.clearCallbacks() # uncomment when debugging
    lexer_interface_24173 = PreProcessor24173()
