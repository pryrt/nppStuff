# -*- coding: utf-8 -*-
'''
Makes lexilla's "hidden" lexers available for NPP.
- SAS
- Stata
- X12

The most recent version of this script is available at
https://raw.githubusercontent.com/pryrt/nppStuff/refs/heads/main/pythonScripts/dev/HiddenLexers.py

===========

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

A more generic version of 23275-enable-stata-lexer.py, which can be extended
as the framework for handling all of the hidden lexers, not just SAS and Stata

The post https://community.notepad-plus-plus.org/post/78579 helped update it for Notepad++ v8.4.3
'''

from Npp import notepad, editor, console, NOTIFICATION
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
import sys

class GenericLexer:
    _lexer_name = b"Generic"

    def __init__(self):
        tmp_name = self._lexer_name
        if sys.version_info.major==3: tmp_name = self._lexer_name.decode("utf-8")
        self.lexer_name = create_unicode_buffer(tmp_name)

    def announce(self, lexintf):
        return # comment out this line to announce each HiddenLexer enablement
        tmp_name = self._lexer_name
        if sys.version_info.major==3: tmp_name = self._lexer_name.decode("utf-8")
        console.write("I will colorize {} from {}\n".format(tmp_name, str(lexintf)))
        pass

    def colorize(self, lexintf):
        raise NotImplementedError("You should be calling colorize() on a specific lexer, not on the {} parent class".format(__class__))

# specific lexer subclasses
class SasLexer(GenericLexer):
    """
        SAS is another language

        %let
        %do
        also        cards        class
        data        input        model
        ods        proc        var
        where
        %printz
        %blah
        %peterfake
        where        run
        * ... comment style 1;
        run
        // ... comment style 2;
        run
        /* comment style 3 */
        5 + 7 = 9
        one
    """

    _lexer_name = b"sas"
    SCE_SAS_DEFAULT                                        = 0
    SCE_SAS_COMMENT                                        = 1
    SCE_SAS_COMMENTLINE                                    = 2
    SCE_SAS_COMMENTBLOCK                                   = 3
    SCE_SAS_NUMBER                                         = 4
    SCE_SAS_OPERATOR                                       = 5
    SCE_SAS_IDENTIFIER                                     = 6
    SCE_SAS_STRING                                         = 7
    SCE_SAS_TYPE                                           = 8
    SCE_SAS_WORD                                           = 9
    SCE_SAS_GLOBAL_MACRO                                   = 10
    SCE_SAS_MACRO                                          = 11
    SCE_SAS_MACRO_KEYWORD                                  = 12
    SCE_SAS_BLOCK_KEYWORD                                  = 13
    SCE_SAS_MACRO_FUNCTION                                 = 14
    SCE_SAS_STATEMENT                                      = 15


    def colorize(self, lexintf):
        self.announce(lexintf)

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
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "%let %do")
        editor.setKeyWords(1, "also cards class data input model ods proc var where")
        editor.setKeyWords(2, "%printz")
        editor.setKeyWords(3, "run")

class StataLexer(GenericLexer):
    """
        Stata is a statistics language

        * http://galton.uchicago.edu/~eichler/stat22000/Handouts/stata-commands.html

        anova by ci clear correlate ...
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
    """

    _lexer_name = b"stata"
    SCE_STATA_DEFAULT                                  = 0
    SCE_STATA_COMMENT                                  = 1
    SCE_STATA_COMMENTLINE                              = 2
    SCE_STATA_COMMENTBLOCK                             = 3
    SCE_STATA_NUMBER                                   = 4
    SCE_STATA_OPERATOR                                 = 5
    SCE_STATA_IDENTIFIER                               = 6
    SCE_STATA_STRING                                   = 7
    SCE_STATA_TYPE                                     = 8
    SCE_STATA_WORD                                     = 9
    SCE_STATA_GLOBAL_MACRO                             = 10
    SCE_STATA_MACRO                                    = 11

    def colorize(self, lexintf):
        self.announce(lexintf)

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

        #### TODO: this block needs to move inside .colorize(), so needs to be reworked to be relative
        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "anova by ci clear correlate describe diagplot drop edit exit gen generate graph help if infile input list log lookup oneway pcorr plot predict qnorm regress replace save sebarr set sort stem summ summarize tab tabulate test ttest use")   # keywords SAS: %let %do
        editor.setKeyWords(1, "byte int long float double strL str") # types # SAS: also cards

class X12Lexer(GenericLexer):
    """
        X12 EDI is a language for business-to-business transaction software

        * https://x12.org/

        * example: https://iwayinfocenter.informationbuilders.com/TLs/TL_soa_ebiz_edix12/source/sample_docs49.htm
            ISA*00*          *01*          *ZZ*NOTP           *ZZ*NOTP           *050108*0954*U*00501*000000001*0*P*>
            GS*IN*NOTP*NOTP*20050108*0954*1*X*004010
            ST*810*0001
            BIG*20021119*184*20021015*BMB
            REF*IA*040682
            N1*BT*WALGREEN*92*0000
            ITD*02**1.000**30**31*****1% 30 NET 31
            FOB*CC
            PID*S**VI*FL
            IT1*0001*267*CA*53.52**IN*859067
            PID*F*08*VI**BARBIE SING W/ME DISC GRL CD PLYR
            TDS*1421839*1428984
            CAD*T***CFWY*CONSOLIDATED FREIGHTWAYS
            SAC*A*D240***7145**********FREIGHT CHARGE
            ISS*267*CA
            CTT*1
            SE*15*0001
            GE*1*1
            IEA*1*000000001

        Looking at LexX12.cxx, does not appear to have any keyword lists.
    """

    _lexer_name = b"x12"
    SCE_X12_DEFAULT                                    = 0
    SCE_X12_BAD                                        = 1
    SCE_X12_ENVELOPE                                   = 2
    SCE_X12_FUNCTIONGROUP                              = 3
    SCE_X12_TRANSACTIONSET                             = 4
    SCE_X12_SEGMENTHEADER                              = 5
    SCE_X12_SEGMENTEND                                 = 6
    SCE_X12_SEP_ELEMENT                                = 7
    SCE_X12_SEP_SUBELEMENT                             = 8

    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_X12_DEFAULT                 , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_X12_BAD                     , (255,0,0))
        editor.styleSetFore(self.SCE_X12_ENVELOPE                , (255,0,255))
        editor.styleSetFore(self.SCE_X12_FUNCTIONGROUP           , (0,204,0))
        editor.styleSetFore(self.SCE_X12_TRANSACTIONSET          , (0,0,204))
        editor.styleSetFore(self.SCE_X12_SEGMENTHEADER           , (64,64,64))
        editor.styleSetFore(self.SCE_X12_SEGMENTEND              , (128,128,128))
        editor.styleSetFore(self.SCE_X12_SEP_ELEMENT             , (255,0,0))
        editor.styleSetFore(self.SCE_X12_SEP_SUBELEMENT          , (255,127,255))

        editor.styleSetBack(self.SCE_X12_BAD                     , (255,255,0))
        editor.styleSetBack(self.SCE_X12_SEP_ELEMENT             , (237,237,237))
        editor.styleSetBack(self.SCE_X12_SEP_SUBELEMENT          , (237,237,237))

        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        # LexX12.cxx only defines one property; I want to enable folding
        editor.setProperty("fold", "1")
        editor.setMarginWidthN(3,14)    # MARGIN3 = FOLD, WIDTH=14px (standard width in NPP)

        # if I am wrong about keyword lists, each would go here...
        #editor.setKeyWords(0, "word1 word2")
        #editor.setKeyWords(1, "word11 word12")

class HiddenLexerInterface:
    NPPM_CREATELEXER                                   = (1024 + 1000 + 110)
    SCI_SETILEXER                                      = 4033

    def __str__(self):
        return "<" + self.__class__.__name__ + ">"

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # **************** configuration area ****************
        """
        files with these extensions and a null lexer (that is, normal text), will be processed by the listed extension

        Examples:
            self.map_extensions['oneext'] = OneFileLexer()                              # *.oneext will be processed by a OneFileLexer instance
            self.map_extensions['notc'] = self.map_extensions['noth'] = NotCLexer()     # *.notc and *.noth will be processed by the same NotCLexer instance
        """
        self.map_extensions = {}
        self.map_extensions['do'] = self.map_extensions['stata'] = StataLexer()
        self.map_extensions['sas'] = SasLexer()
        self.map_extensions['x12'] = X12Lexer()

        # initialize win32 interface info
        self.notepad_hwnd = windll.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = windll.user32.FindWindowExW(self.notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = windll.user32.FindWindowExW(self.notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)
        windll.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
        windll.user32.SendMessageW.restype  = LPARAM

        # if it's older then v8.4.1, need to make an old CreateLexer; if it's v8.4.2-or-newer, don't need to go searching for the function
        if self.nppver() < 8.410:
            windll.kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
            windll.kernel32.GetModuleHandleW.restype = HMODULE
            windll.kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
            windll.kernel32.GetProcAddress.restype = LPVOID
            handle = windll.kernel32.GetModuleHandleW(None)
            create_lexer_ptr = windll.kernel32.GetProcAddress(handle, b'CreateLexer')

            CL_FUNCTYPE = WINFUNCTYPE(LPVOID, LPCSTR)
            self.create_lexer_func = CL_FUNCTYPE(create_lexer_ptr)
        else:
            pass


        # create the callbacks
        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        self.enabled = False

        console.write("Initialized {}\n".format(self.__class__.__name__))

    def init_lexer(self, ext):
        '''
            Initializes the lexer and its properties
            Args:
                None
            Returns:
                None
        '''
        if ext in self.map_extensions:
            self.map_extensions[ext].colorize(self)
            self.lexer_name = self.map_extensions[ext].lexer_name

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
        if has_no_lexer_assigned and file_extension in self.map_extensions:
            if self.enabled:
                self.init_lexer(file_extension)
        #console.write("check_lexers: old:{} lex:{} hasnt:{} oldlang:{} newlang:{} << \"{}\" \n".format(
        #    old_lexer, editor.getLexerLanguage(), has_no_lexer_assigned,
        #    old_langtype, notepad.getCurrentLang(), notepad.getCurrentFilename()
        #))


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


try:
    lexer_interface.toggle()
    if True:
        notepad.clearCallbacks(lexer_interface.on_langchanged)
        notepad.clearCallbacks(lexer_interface.on_bufferactivated)
        del lexer_interface
        console.write("deleted callbacks and lexer_interface\n")
except NameError:
    lexer_interface = HiddenLexerInterface()
    lexer_interface.main()
