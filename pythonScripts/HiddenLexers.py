# -*- coding: utf-8 -*-
'''
Makes lexilla's "hidden" lexers available for NPP.

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

A more generic version of 23275-enable-stata-lexer.py, which will eventually
be a framework for handling all of the hidden lexers, not just SAS and Stata

The post https://community.notepad-plus-plus.org/post/78579 helped update it for Notepad++ v8.4.3
'''

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID

class StataLexer:

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # **************** configuration area ****************
        # files with these extensions and a null lexer,
        # aka normal text, assigned do get handled
        self.known_extensions = ['do', 'stata']
        #
        #self.show_escape_chars = False
        #self.separate_path_and_line_number = '0'
        #self.interpret_escape_sequences = '1'
        # ****************************************************
        self.SCE_STATA_DEFAULT                                  = 0
        self.SCE_STATA_COMMENT                                  = 1
        self.SCE_STATA_COMMENTLINE                              = 2
        self.SCE_STATA_COMMENTBLOCK                             = 3
        self.SCE_STATA_NUMBER                                   = 4
        self.SCE_STATA_OPERATOR                                 = 5
        self.SCE_STATA_IDENTIFIER                               = 6
        self.SCE_STATA_STRING                                   = 7
        self.SCE_STATA_TYPE                                     = 8
        self.SCE_STATA_WORD                                     = 9
        self.SCE_STATA_GLOBAL_MACRO                             = 10
        self.SCE_STATA_MACRO                                    = 11

        self.NPPM_CREATELEXER                                   = (1024 + 1000 + 110)
        self.SCI_SETILEXER                                      = 4033

        self.kernel32 = windll.kernel32
        self.user32 = windll.user32

        self.notepad_hwnd = self.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = self.user32.FindWindowExW(self.notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = self.user32.FindWindowExW(self.notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)

        self.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
        self.user32.SendMessageW.restype  = LPARAM

        #console.write( "npp version: {:05.3f}\n".format(self.nppver()) )

        if self.nppver() < 8.410:

            self.kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
            self.kernel32.GetModuleHandleW.restype = HMODULE
            self.kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
            self.kernel32.GetProcAddress.restype = LPVOID
            handle = self.kernel32.GetModuleHandleW(None)
            create_lexer_ptr = self.kernel32.GetProcAddress(handle, b'CreateLexer')

            CL_FUNCTYPE = WINFUNCTYPE(LPVOID, LPCSTR)
            self.create_lexer_func = CL_FUNCTYPE(create_lexer_ptr)

            #console.write("init the function the old way\n")

        else:
            #console.write("init the function the new way\n")
            pass


        self.lexer_name = create_unicode_buffer('stata')


        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        self.enabled = False

        console.write("Initialized Stata lexer\n")

    def __del__(self):
        '''
            Destructor (kind of)
        '''
        console.write("Clear Stata lexer callbacks...\n")
        notepad.clearCallbacks(self.on_langchanged)
        notepad.clearCallbacks(self.on_bufferactivated)
        console.write("Destroyed Stata lexer\n")

    def init_lexer(self):
        '''
            Initializes the lexer and its properties
            Args:
                None
            Returns:
                None
        '''
        editor.styleSetFore(self.SCE_STATA_DEFAULT               , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_STATA_COMMENT               , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_COMMENTLINE           , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_COMMENTBLOCK          , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_NUMBER                , (255,128,0))
        editor.styleSetFore(self.SCE_STATA_OPERATOR              , (0,0,128))
        editor.styleSetFore(self.SCE_STATA_IDENTIFIER            , (64,64,64))
        editor.styleSetFore(self.SCE_STATA_STRING                , (128,128,128))
        editor.styleSetFore(self.SCE_STATA_TYPE                  , (128,0,255))     # KeyWords(1)
        editor.styleSetFore(self.SCE_STATA_WORD                  , (0,128,255))     # KeyWords(0)
        editor.styleSetFore(self.SCE_STATA_GLOBAL_MACRO          , (255,255,0))     # not implemented that I can see in LexStata.cxx
        editor.styleSetFore(self.SCE_STATA_MACRO                 , (0,0,255))       # not implemented that I can see in LexStata.cxx

        # ordering is important
        if self.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(b'stata')
            #console.write("old: called create_lexer_func()\n")
        else:
            self.ilexer_ptr = self.user32.SendMessageW(self.notepad_hwnd, self.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = self.editor1_hwnd if notepad.getCurrentView() == 0 else self.editor2_hwnd
        self.user32.SendMessageW(editor_hwnd, self.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "anova by ci clear correlate describe diagplot drop edit exit gen generate graph help if infile input list log lookup oneway pcorr plot predict qnorm regress replace save sebarr set sort stem summ summarize tab tabulate test ttest use")   # keywords SAS: %let %do
        editor.setKeyWords(1, "byte int long float double strL str") # types # SAS: also cards

        #console.write("Stata lexer: set styles\n")

    def check_lexers(self):
        '''
            Checks if the current document is of interest.

            Args:
                None
            Returns:
                None
        '''

        old_lexer = editor.getLexerLanguage()
        old_langtype = "{}".format(notepad.getCurrentLang())
        has_no_lexer_assigned = editor.getLexerLanguage() == 'null'
        _, _, file_extension = notepad.getCurrentFilename().rpartition('.')
        if has_no_lexer_assigned and file_extension in self.known_extensions:
            if self.enabled:
                self.init_lexer()
        console.write("check_lexers: old:{} lex:{} hasnt:{} oldlang:{} newlang:{}\n".format(
            old_lexer, editor.getLexerLanguage(), has_no_lexer_assigned,
            old_langtype, notepad.getCurrentLang()
        ))


    def on_bufferactivated(self, args):
        '''
            Callback which gets called every time one switches a document.
            Triggers the check if the document is of interest.

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()
        #console.write("on_bufferactivated\n")


    def on_langchanged(self, args):
        '''
            Callback gets called every time one uses the Language menu to set a lexer
            Triggers the check if the document is of interest

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()
        #console.write("on_langchanged\n")

    def nppver(self):
        self.NPPM_GETNPPVERSION = 1024 + 1000 + 50
        nppv = self.user32.SendMessageW(self.notepad_hwnd, self.NPPM_GETNPPVERSION, 1, 0 )
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

    def toggle(self):
        ''' Toggles between enabled and disabled '''
        self.enabled = not self.enabled
        if self.enabled:
            console.write("Enabled Hidden Lexers\n")
        else:
            console.write("Disabled Hidden Lexers\n")
        self.on_bufferactivated(None)

    def main(self):
        '''
            Main function entry point.
            Simulates the buffer_activated event to enforce
            detection of current document and potential styling.

            Args:
                None
            Returns:
                None
        '''
        self.enabled = True
        self.on_bufferactivated(None)

console.show()
console.write("Run again\n")
try:
    stata_lexer.toggle()
except NameError:
    stata_lexer = StataLexer()
    stata_lexer.main()

""" notepad.clearCallbacks(); del stata_lexer; del StataLexer """

""" example junk Stata (just lists some of the keywords):

* http://galton.uchicago.edu/~eichler/stat22000/Handouts/stata-commands.html

anova by ci clear correlate describe diagplot drop edit exit gen generate
graph help if infile input list log lookup oneway pcorr plot predict qnorm
regress replace save sebarr set sort stem summ summarize tab tabulate test
ttest use

byte int long float double strL

local life_questions 42
display `life_questions'
foreach var in varlist yearmade-kwh {
  summarize `var'
}

-(x+y^(x-y))/(x*y)

"string" + "string"

"string" * 5

< > <= >= == != ~=

generate incgt10k=income>10000 if income<.

a & b | c & !d

sqrt(4)


"""
