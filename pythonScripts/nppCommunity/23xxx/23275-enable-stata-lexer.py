# -*- coding: utf-8 -*-
'''
    Makes lexilla's builtin Stata lexer available for NPP.

    To toggle the escape characters on/off one can
    create another script with these two lines of code.

    stata_lexer.show_escape_chars = not stata_lexer.show_escape_chars
    editor.styleSetVisible(stata_lexer.SCE_ERR_ESCSEQ, stata_lexer.show_escape_chars)

'''
"""
Peter trying to adapt https://raw.githubusercontent.com/Ekopalypse/NppPythonScripts/master/npp/error_list_lexer_support2.py
based on Eko's comments https://community.notepad-plus-plus.org/topic/23147/missing-lexers-from-lexilla/7
Converted the Stata from https://community.notepad-plus-plus.org/post/77802 to Stata
"""

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE
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

        self.kernel32 = windll.kernel32
        self.user32 = windll.user32

        notepad_hwnd = self.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = self.user32.FindWindowExW(notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = self.user32.FindWindowExW(notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)

        self.kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = HMODULE
        self.kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
        self.kernel32.GetProcAddress.restype = LPVOID
        handle = self.kernel32.GetModuleHandleW(None)
        create_lexer_ptr = self.kernel32.GetProcAddress(handle, b'CreateLexer')

        CL_FUNCTYPE = WINFUNCTYPE(LPVOID, LPCSTR)
        self.create_lexer_func = CL_FUNCTYPE(create_lexer_ptr)

        self.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]

        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        self.SCI_SETILEXER                                          = 4033

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
        self.ilexer_ptr = self.create_lexer_func(b'stata')
        editor_hwnd = self.editor1_hwnd if notepad.getCurrentView() == 0 else self.editor2_hwnd
        self.user32.SendMessageW(editor_hwnd, self.SCI_SETILEXER, 0, self.ilexer_ptr)
        # properties: fold.compact, fold.at.else
        editor.setKeyWords(0, "anova by ci clear correlate describe diagplot drop edit exit gen generate graph help if infile input list log lookup oneway pcorr plot predict qnorm regress replace save sebarr set sort stem summ summarize tab tabulate test ttest use")   # keywords SAS: %let %do
        editor.setKeyWords(1, "byte int long float double strL str") # types # SAS: also cards
        #editor.setKeyWords(2, "%printz")
        #editor.setKeyWords(3, "run")
        console.write("Stata lexer: set styles\n")

    def check_lexers(self):
        '''
            Checks if the current document is of interest.

            Args:
                None
            Returns:
                None
        '''

        has_no_lexer_assigned = editor.getLexerLanguage() == 'null'
        _, _, file_extension = notepad.getCurrentFilename().rpartition('.')
        if has_no_lexer_assigned and file_extension in self.known_extensions:
            self.init_lexer()
        console.write("check_lexers: {} {}\n".format(editor.getLexerLanguage(), has_no_lexer_assigned))


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
        console.write("on_bufferactivated\n")


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
        console.write("on_langchanged\n")


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
        self.on_bufferactivated(None)

console.show()
stata_lexer = StataLexer()
stata_lexer.main()

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
