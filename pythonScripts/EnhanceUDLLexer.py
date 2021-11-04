# -*- coding: utf-8 -*-

from Npp import editor, editor1, editor2, notepad, NOTIFICATION, SCINTILLANOTIFICATION, INDICATORSTYLE
import ctypes
import ctypes.wintypes as wintypes

from collections import OrderedDict
regexes = OrderedDict()

# ------------------------------------------------- configuration area ---------------------------------------------------
#
# Define the lexer name exactly as it can be found in the Language menu
lexer_name = 'DNATest'

# Definition of colors and regular expressions
#   Note, the order in which regular expressions will be processed
#   is determined by its creation, that is, the first definition is processed first, then the 2nd, and so on
#
#   The basic structure always looks like this
#
#   regexes[(a, b)] = (c, d)
#
#   regexes = an ordered dictionary which ensures that the regular expressions are always processed in the same order
#   a = a unique number - suggestion, start with 0 and always increase by one
#   b = color in the form of (r,g,b) such as (255,0,0) for the color red
#   c = raw byte string, describes the regular expression. Example r'\w+'
#   d = number of the match group to be used


# Examples:
#   All found words which may consist of letter, numbers and the underscore,
#   with the exception of those that begin with fn, are displayed in a blue-like color.
#   The results from match group 1 should be used for this.
#regexes[(0, (79, 175, 239))] = (r'fn\w+\$|(\w+\$)', 1)

#   All numbers are to be displayed in an orange-like color, the results from
#   matchgroup 0, the standard matchgroup, should be used for this.
#regexes[(1, (252, 173, 67))] = (r'\d', 0)

regexes[(0, (252, 173, 67))] = (r'[Aa]', 0)
regexes[(1, (152, 73, 167))] = (r'[Gg]', 0)
regexes[(2, (52, 37, 176))] = (r'[Cc]', 0)
regexes[(3, (25, 17, 77))] = (r'[Tt]', 0)

#regexes[(4, (127, 0, 0))] = (r'a', 0)   # A:red
#regexes[(5, (0, 127, 0))] = (r'c', 0)   # C:green
#regexes[(6, (0, 0, 127))] = (r't', 0)   # T:blue
#regexes[(7, (127,127,0))] = (r'g', 0)   # G:yellow

# Definition of which area should not be styled
# 1 = comment style
# 2 = comment line style
# 16 = delimiter1
# ...
# 23 = delimiter8
excluded_styles = [1, 2, 16, 17, 18, 19, 20, 21, 22, 23]

# ------------------------------------------------ /configuration area ---------------------------------------------------

try:
    EnhanceUDLLexer().main()
except NameError:

    user32 = wintypes.WinDLL('user32')

    WM_USER = 1024
    NPPMSG = WM_USER+1000
    NPPM_GETLANGUAGEDESC = NPPMSG+84
    SC_INDICVALUEBIT = 0x1000000
    SC_INDICFLAG_VALUEFORE = 1


    class SingletonEnhanceUDLLexer(type):
        '''
            Ensures, more or less, that only one
            instance of the main class can be instantiated
        '''
        _instance = None
        def __call__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super(SingletonEnhanceUDLLexer, cls).__call__(*args, **kwargs)
            return cls._instance


    class EnhanceUDLLexer(object):
        '''
            Provides additional color options and should be used in conjunction with the built-in UDL function.
            An indicator is used to avoid style collisions.
            Although the Scintilla documentation states that indicators 0-7 are reserved for the lexers,
            indicator 0 is used because UDL uses none internally.

            Even when using more than one regex, it is not necessary to define more than one indicator
            because the class uses the flag SC_INDICFLAG_VALUEFORE.
            See https://www.scintilla.org/ScintillaDoc.html#Indicators for more information on that topic
        '''
        __metaclass__ = SingletonEnhanceUDLLexer

        def __init__(self):
            '''
                Instantiated the class,
                because of __metaclass__ = ... usage, is called once only.
            '''
            editor.callbackSync(self.on_updateui, [SCINTILLANOTIFICATION.UPDATEUI])
            notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
            notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])
            self.doc_is_of_interest = False
            self.lexer_name = None
            self.npp_hwnd = user32.FindWindowW(u'Notepad++', None)
            self.configure()


        @staticmethod
        def rgb(r, g, b):
            '''
                Helper function
                Retrieves rgb color triple and converts it
                into its integer representation

                Args:
                    r = integer, red color value in range of 0-255
                    g = integer, green color value in range of 0-255
                    b = integer, blue color value in range of 0-255
                Returns:
                    integer
            '''
            return (b << 16) + (g << 8) + r


        @staticmethod
        def paint_it(color, pos, length):
            '''
                This is where the actual coloring takes place.
                Color, the position of the first character and
                the length of the text to be colored must be provided.
                Coloring occurs only if the position is not within the excluded range.

                Args:
                    color = integer, expected in range of 0-16777215
                    pos = integer,  denotes the start position
                    length = integer, denotes how many chars need to be colored.
                Returns:
                    None
            '''
            if pos < 0 or editor.getStyleAt(pos) in excluded_styles:
                return
            editor.setIndicatorCurrent(0)
            editor.setIndicatorValue(color)
            editor.indicatorFillRange(pos, length)


        def style(self):
            '''
                Calculates the text area to be searched for in the current document.
                Calls up the regexes to find the position and
                calculates the length of the text to be colored.
                Deletes the old indicators before setting new ones.

                Args:
                    None
                Returns:
                    None
            '''
            start_line = editor.docLineFromVisible(editor.getFirstVisibleLine())
            end_line = editor.docLineFromVisible(start_line + editor.linesOnScreen())
            start_position = editor.positionFromLine(start_line)
            end_position = editor.getLineEndPosition(end_line)
            editor.setIndicatorCurrent(0)
            editor.indicatorClearRange(0, editor.getTextLength())
            for color, regex in self.regexes.items():
                editor.research(regex[0],
                                lambda m: self.paint_it(color[1],
                                                        m.span(regex[1])[0],
                                                        m.span(regex[1])[1] - m.span(regex[1])[0]),
                                0,
                                start_position,
                                end_position)


        def configure(self):
            '''
                Define basic indicator settings, the needed regexes as well as the lexer name.

                Args:
                    None
                Returns:
                    None
            '''
            editor1.indicSetStyle(0, INDICATORSTYLE.TEXTFORE)
            editor1.indicSetFlags(0, SC_INDICFLAG_VALUEFORE)
            editor2.indicSetStyle(0, INDICATORSTYLE.TEXTFORE)
            editor2.indicSetFlags(0, SC_INDICFLAG_VALUEFORE)
            self.regexes = OrderedDict([ ((k[0], self.rgb(*k[1]) | SC_INDICVALUEBIT), v) for k, v in regexes.items() ])
            self.lexer_name = u'User Defined language file - %s' % lexer_name


        def check_lexer(self):
            '''
                Checks if the current document is of interest
                and sets the flag accordingly

                Args:
                    None
                Returns:
                    None
            '''
            language = notepad.getLangType()
            length = user32.SendMessageW(self.npp_hwnd, NPPM_GETLANGUAGEDESC, language, None)
            buffer = ctypes.create_unicode_buffer(u' ' * length)
            user32.SendMessageW(self.npp_hwnd, NPPM_GETLANGUAGEDESC, language, ctypes.byref(buffer))
            self.doc_is_of_interest = True if buffer.value == self.lexer_name else False


        def on_bufferactivated(self, args):
            '''
                Callback which gets called every time one switches a document.
                Triggers the check if the document is of interest.

                Args:
                    provided by notepad object but none are of interest
                Returns:
                    None
            '''
            self.check_lexer()


        def on_updateui(self, args):
            '''
                Callback which gets called every time scintilla
                (aka the editor) changed something within the document.

                Triggers the styling function if the document is of interest.

                Args:
                    provided by scintilla but none are of interest
                Returns:
                    None
            '''
            if self.doc_is_of_interest:
                self.style()


        def on_langchanged(self, args):
            '''
                Callback gets called every time one uses the Language menu to set a lexer
                Triggers the check if the document is of interest

                Args:
                    provided by notepad object but none are of interest
                Returns:
                    None
            '''
            self.check_lexer()


        def main(self):
            '''
                Main function entry point.
                Simulates two events to enforce detection of current document
                and potential styling.

                Args:
                    None
                Returns:
                    None
            '''
            self.on_bufferactivated(None)
            self.on_updateui(None)

    EnhanceUDLLexer().main()