# -*- coding: utf-8 -*-
'''
    Makes the builtin SAS lexer available for NPP.
'''
"""
Peter trying to adapt https://raw.githubusercontent.com/Ekopalypse/NppPythonScripts/master/npp/error_list_lexer_support2.py
based on Eko's comments https://community.notepad-plus-plus.org/topic/23147/missing-lexers-from-lexilla/7
updated based on https://community.notepad-plus-plus.org/post/78579 for Notepad++ v8.4.3
"""

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID


class SasLexer:

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # **************** configuration area ****************
        # files with these extensions and a null lexer,
        # aka normal text, assigned do get handled
        self.known_extensions = ['sas']
        #
        # ****************************************************
        self.SCE_SAS_DEFAULT                                        = 0
        self.SCE_SAS_COMMENT                                        = 1
        self.SCE_SAS_COMMENTLINE                                    = 2
        self.SCE_SAS_COMMENTBLOCK                                   = 3
        self.SCE_SAS_NUMBER                                         = 4
        self.SCE_SAS_OPERATOR                                       = 5
        self.SCE_SAS_IDENTIFIER                                     = 6
        self.SCE_SAS_STRING                                         = 7
        self.SCE_SAS_TYPE                                           = 8
        self.SCE_SAS_WORD                                           = 9
        self.SCE_SAS_GLOBAL_MACRO                                   = 10
        self.SCE_SAS_MACRO                                          = 11
        self.SCE_SAS_MACRO_KEYWORD                                  = 12
        self.SCE_SAS_BLOCK_KEYWORD                                  = 13
        self.SCE_SAS_MACRO_FUNCTION                                 = 14
        self.SCE_SAS_STATEMENT                                      = 15

        self.NPPM_CREATELEXER                                       = (1024 + 1000 + 110)
        self.SCI_SETILEXER                                          = 4033

        self.user32 = windll.user32

        self.notepad_hwnd = self.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = self.user32.FindWindowExW(self.notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = self.user32.FindWindowExW(self.notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)

        self.lexer_name = create_unicode_buffer('SAS')

        self.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
        self.user32.SendMessageW.restype = LPARAM

        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])


        console.write("Initialized SAS lexer\n")

    def __del__(self):
        '''
            Destructor (kind of)
        '''
        console.write("Clear SAS lexer callbacks...\n")
        notepad.clearCallbacks(self.on_langchanged)
        notepad.clearCallbacks(self.on_bufferactivated)
        console.write("Destroyed SAS lexer\n")

    def init_lexer(self):
        '''
            Initializes the lexer and its properties
            Args:
                None
            Returns:
                None
        '''
        editor.styleSetFore(self.SCE_SAS_DEFAULT               , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_SAS_COMMENT               , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_COMMENTLINE           , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_COMMENTBLOCK          , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_NUMBER                , (255,0,0))
        editor.styleSetFore(self.SCE_SAS_OPERATOR              , (128,64,0))
        editor.styleSetFore(self.SCE_SAS_IDENTIFIER            , (64,64,64))
        editor.styleSetFore(self.SCE_SAS_STRING                , (128,128,128))
        editor.styleSetFore(self.SCE_SAS_TYPE                  , (128,0,255))       # not implemented
        editor.styleSetFore(self.SCE_SAS_WORD                  , (255,128,0))       # not implemented
        editor.styleSetFore(self.SCE_SAS_GLOBAL_MACRO          , (255,255,0))       # not implemented
        editor.styleSetFore(self.SCE_SAS_MACRO                 , (0,0,255))         # start with %
        editor.styleSetFore(self.SCE_SAS_MACRO_KEYWORD         , (0,255,255))       # keywords/keywords1
        editor.styleSetFore(self.SCE_SAS_BLOCK_KEYWORD         , (0,0,127))         # keywords2
        editor.styleSetFore(self.SCE_SAS_MACRO_FUNCTION        , (0,127,127))       # keywords3
        editor.styleSetFore(self.SCE_SAS_STATEMENT             , (0xAA,0,0))        # keywords4

        # ordering is important
        ilexer_ptr = self.user32.SendMessageW(self.notepad_hwnd, self.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
        editor_hwnd = self.editor1_hwnd if notepad.getCurrentView() == 0 else self.editor2_hwnd
        self.user32.SendMessageW(editor_hwnd, self.SCI_SETILEXER, 0, ilexer_ptr)


        editor.setKeyWords(0, "%let %do")
        editor.setKeyWords(1, "also cards class data input model ods proc var where")
        editor.setKeyWords(2, "%printz")
        editor.setKeyWords(3, "run")
        console.write("SAS lexer: set styles\n")

    def check_lexers(self):
        '''
            Checks if the current document is of interest.

            Args:
                None
            Returns:
                None
        '''

        has_no_lexer_assigned = (editor.getLexerLanguage() == 'null') or (editor.getLexerLanguage() == '')
        _, _, file_extension = notepad.getCurrentFilename().rpartition('.')
        console.write("check_lexers: lex='{}' nolex={} ext='{}'\n".format(editor.getLexerLanguage(), has_no_lexer_assigned, file_extension))
        if has_no_lexer_assigned and file_extension in self.known_extensions:
            self.init_lexer()


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
sas_lexer = SasLexer()
sas_lexer.main()


""" example junk SAS (just lists some of the keywords):

%let

%do

also

cards
class
data
input
model
ods
proc
var
where

%printz

run

* ... comment style 1;

run

// ... comment style 2;

run

/* comment style 3 */

5 + 7 = 9

one

blech


"""
