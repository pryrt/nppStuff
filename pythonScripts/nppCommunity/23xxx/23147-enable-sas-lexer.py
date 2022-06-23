# -*- coding: utf-8 -*-
'''
    Makes the builtin SAS lexer available for NPP.

    To toggle the escape characters on/off one can
    create another script with these two lines of code.

    sas_lexer.show_escape_chars = not sas_lexer.show_escape_chars
    editor.styleSetVisible(sas_lexer.SCE_ERR_ESCSEQ, sas_lexer.show_escape_chars)

'''
"""
Peter trying to adapt https://raw.githubusercontent.com/Ekopalypse/NppPythonScripts/master/npp/error_list_lexer_support2.py
based on Eko's comments https://community.notepad-plus-plus.org/topic/23147/missing-lexers-from-lexilla/7
"""

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE
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
        #self.show_escape_chars = False
        #self.separate_path_and_line_number = '0'
        #self.interpret_escape_sequences = '1'
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
        editor.styleSetFore(self.SCE_SAS_MACRO                 , (0xCC,0x66,0xFF))
        editor.styleSetFore(self.SCE_SAS_MACRO_KEYWORD         , (0xCC,0x66,0xFF))
        editor.styleSetFore(self.SCE_SAS_BLOCK_KEYWORD         , (0,0,0x80))
        editor.styleSetFore(self.SCE_SAS_MACRO_FUNCTION        , (0xFF,0x66,0xFF))
        editor.styleSetFore(self.SCE_SAS_STATEMENT             , (0xAA,0,0))

        # ordering is important
        self.ilexer_ptr = self.create_lexer_func(b'sas')
        editor_hwnd = self.editor1_hwnd if notepad.getCurrentView() == 0 else self.editor2_hwnd
        self.user32.SendMessageW(editor_hwnd, self.SCI_SETILEXER, 0, self.ilexer_ptr)
        #editor.setProperty('lexer.sas.value.separate', self.separate_path_and_line_number)
        #editor.setProperty('lexer.sas.escape.sequences', self.interpret_escape_sequences)

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
        console.write("check_lexers: {}\n".format(has_no_lexer_assigned))


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