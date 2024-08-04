# -*- coding: utf-8 -*-
'''
Makes lexilla's "SubStyles" feature available for each of the lexers defined

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

As far as I can tell, as of Scintilla 5.5.1 / Notepad++ v8.6.9, there are only a handful
of languages in the Lexilla bundle that allow substyling, and those have specific styles
that allow substyles.

- LexBASH
    - languages: BASH
    - styles: SCE_SH_IDENTIFIER=8, SCE_SH_SCALAR=9
- LexCPP
    - languages: C, CPP, JAVA, JS, RC, CS, FLASH, SWIFT, TYPESCRIPT
    - styles: SCE_C_IDENTIFIER=11, SCE_C_COMMENTDOCKEYWORD=17
- LexGDScript
    - languages: GDScript
    - styles: SCE_GD_IDENTIFIER=11
- LexHTML
    - languages: HTML, XML, PHP, ASP, JSP
    - styles: SCE_H_TAG=1, SCE_H_ATTRIBUTE=3, SCE_HJ_WORD=46, SCE_HJA_WORD=61, SCE_HB_WORD=74, SCE_HP_WORD=96, SCE_HPHP_WORD=121
- LexLua
    - languages: LUA
    - styles: SCE_LUA_IDENTIFIER=11
- LexPython
    - languages: PYTHON
    - styles: SCE_P_IDENTIFIER=11
- LexVerilog
    - languages: Verilog
    - styles: <none>
    - comment: no, I don't know why the LexVerilog enables the substyles feature, but doesn't have them for any styles

You can have up to 64 substyles per lexer, split among the N languages used by that lexer.

To implement your own word list with your own colors for a given language+style, you can
go to that given language, look for "INSTRUCTIONS", and follow those instructions.

Every style is pre-populated with a keyword list of "pryrt" (my frequent online username,
and a word you aren't likely to have in your source code), or "pryrtN" where N is a number,
with the color of foreground=BLUE and background=YELLOW.
You should change the wordlist(s) and colors to match your needs and theme, and add
more rows similar to the examples if you want more than one substyle for a given style

If any of your keywords were in the main Notepad++ keyword list for a given Language's style,
you will have to remove those keywords from the `langs.xml`, because Lexilla gives priority
to the main style's keyword list before it tries to check the substyle keyword list(s)

Based on Eko's original EnhanceAnyLexer and my HiddenLexers scripts, plus
    https://community.notepad-plus-plus.org/topic/25980/highlighting-with-self-created-words-in-langs-xml-does-not-work
'''

from Npp import notepad, editor, NOTIFICATION

class SubstyleLexerInterface:
    def __str__(self):
        return "<" + self.__class__.__name__ + ">"

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # map each language name (getCurrentLang) to an instance of the right class
        # the PHP class is an example of how to do it for other lexers (because PHP is the class used for 25980)
        self.map_languages = dict()
        self.map_languages['BASH']          = BASH_SubstyleLexer()
        self.map_languages['C']             = C_SubstyleLexer()
        self.map_languages['CPP']           = CPP_SubstyleLexer()
        self.map_languages['JAVA']          = JAVA_SubstyleLexer()
        self.map_languages['JAVASCRIPT']    = JS_SubstyleLexer()
        self.map_languages['RC']            = RC_SubstyleLexer()
        self.map_languages['CS']            = CS_SubstyleLexer()
        self.map_languages['FLASH']         = FLASH_SubstyleLexer()
        self.map_languages['SWIFT']         = SWIFT_SubstyleLexer()
        self.map_languages['TYPESCRIPT']    = TYPESCRIPT_SubstyleLexer()
        self.map_languages['GDSCRIPT']      = GDSCRIPT_SubstyleLexer()
        self.map_languages['HTML']          = HTML_SubstyleLexer()
        self.map_languages['XML']           = XML_SubstyleLexer()
        self.map_languages['PHP']           = PHP_SubstyleLexer()
        self.map_languages['ASP']           = ASP_SubstyleLexer()
        self.map_languages['JSP']           = JSP_SubstyleLexer()
        self.map_languages['LUA']           = LUA_SubstyleLexer()
        self.map_languages['PYTHON']        = PYTHON_SubstyleLexer()
        self.map_languages['VERILOG']       = VERILOG_SubstyleLexer()
        #console.write("At Creation: self MapContents: {}\n".format(", ".join(self.map_languages.keys())))
        #console.write("create: self.map = {}\n".format(self.map_languages))
        #console.write("create: PHP in Map = {}\n".format('PHP' in self.map_languages))

        # create the callbacks
        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        self.enabled = False

        console.write("Initialized {}\n".format(self.__class__.__name__))

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

    def check_lexers(self):
        '''
            Checks if the current document is of interest, and initializes.

            Args:
                None
            Returns:
                None
        '''
        #console.write("\ncheck_lexers()\n")
        #console.write("At Check: self MapContents: {}\n".format(", ".join(self.map_languages.keys())))
        #console.write("At Check: PHP in Map = {}\n".format('PHP' in self.map_languages))

        langType = str(notepad.getCurrentLang())
        #console.write("At Check: checking '{}' inMap={}\n".format(langType, langType in self.map_languages))
        #console.write("SubStylesForLexer: active file uses \"{}\" lexer, enabled={}, inMap={}\n".format(langType, self.enabled, langType in self.map_languages))

        if self.enabled:
            if langType in self.map_languages:
                #console.write("Going to use \"{}\" SubStyles lexer\n".format(langType))
                self.map_languages[langType].colorize()

    def toggle(self):
        ''' Toggles between enabled and disabled '''
        self.enabled = not self.enabled
        if self.enabled:
            console.write("Enabled SubStyle Lexers\n")
        else:
            console.write("Disabled SubStyle Lexers\n")
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

class Generic_SubstyleLexer:
    _lexer_name = "Generic"

    def __init__(self):
        pass

    def announce(self, lexintf):
        #console.write("I will colorize {} from {}\n".format(self._lexer_name, str(lexintf)))
        pass

    def do_the_work(self):
        for parentStyle in editor.getSubStyleBases().encode():
            if parentStyle in self._style:
                numSubStyles = len(self._style[parentStyle])
                #console.write("Want to allocate {} substyle{} for parentStyle={}\n".format(numSubStyles, "s" if numSubStyles>1 else "", parentStyle))
                rStart = editor.allocateSubStyles(parentStyle, numSubStyles)
                #console.write("... coloring numSubStyles={} from rStart={}\n".format(numSubStyles, rStart))
                for idx in range(numSubStyles):
                    subStyle = rStart + idx
                    #console.write("... coloring idx={} subStyle={}\n".format(idx, subStyle))
                    editor.styleSetFore(subStyle, self._style[parentStyle][idx]['fg'])
                    editor.styleSetBack(subStyle, self._style[parentStyle][idx]['bg'])
                    editor.setIdentifiers(subStyle, self._style[parentStyle][idx]['keywords'])

    def colorize(self):
        raise NotImplementedError("You should be calling colorize() on a specific lexer, not on the {} parent class".format(__class__))

class BASH_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "PHP"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_SH_IDENTIFIER = 8
        SCE_SH_SCALAR = 9

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_SH_IDENTIFIER] = []
        self._style[SCE_SH_SCALAR] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_SH_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_SH_SCALAR].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class C_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "C"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class CPP_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "CPP"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class JAVA_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "JAVA"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class JS_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "JAVASCRIPT"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class RC_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "RC"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class CS_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "CS"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class FLASH_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "FLASH"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class SWIFT_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "SWIFT"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class TYPESCRIPT_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "TYPESCRIPT"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_C_IDENTIFIER = 11
        SCE_C_COMMENTDOCKEYWORD = 17

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_C_IDENTIFIER] = []
        self._style[SCE_C_COMMENTDOCKEYWORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_C_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_C_COMMENTDOCKEYWORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class GDSCRIPT_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "GDSCRIPT"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_GD_IDENTIFIER = 11

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_GD_IDENTIFIER] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_GD_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class HTML_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "HTML"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_H_TAG = 1
        SCE_H_ATTRIBUTE = 3
        SCE_HJ_WORD = 46
        SCE_HJA_WORD = 61
        SCE_HB_WORD = 74
        SCE_HP_WORD = 96
        SCE_HPHP_WORD = 121

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_H_TAG] = []
        self._style[SCE_H_ATTRIBUTE] = []
        self._style[SCE_HJ_WORD] = []
        self._style[SCE_HJA_WORD] = []
        self._style[SCE_HB_WORD] = []
        self._style[SCE_HP_WORD] = []
        self._style[SCE_HPHP_WORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_H_TAG].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_H_ATTRIBUTE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))
        self._style[SCE_HJ_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt3"))
        self._style[SCE_HJA_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt4"))
        self._style[SCE_HB_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt5"))
        self._style[SCE_HP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt6"))
        self._style[SCE_HPHP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt7"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class XML_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "XML"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_H_TAG = 1
        SCE_H_ATTRIBUTE = 3
        SCE_HJ_WORD = 46
        SCE_HJA_WORD = 61
        SCE_HB_WORD = 74
        SCE_HP_WORD = 96
        SCE_HPHP_WORD = 121

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_H_TAG] = []
        self._style[SCE_H_ATTRIBUTE] = []
        self._style[SCE_HJ_WORD] = []
        self._style[SCE_HJA_WORD] = []
        self._style[SCE_HB_WORD] = []
        self._style[SCE_HP_WORD] = []
        self._style[SCE_HPHP_WORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_H_TAG].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_H_ATTRIBUTE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))
        self._style[SCE_HJ_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt3"))
        self._style[SCE_HJA_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt4"))
        self._style[SCE_HB_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt5"))
        self._style[SCE_HP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt6"))
        self._style[SCE_HPHP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt7"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class PHP_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "PHP"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_H_TAG = 1
        SCE_H_ATTRIBUTE = 3
        SCE_HJ_WORD = 46
        SCE_HJA_WORD = 61
        SCE_HB_WORD = 74
        SCE_HP_WORD = 96
        SCE_HPHP_WORD = 121

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_H_TAG] = []
        self._style[SCE_H_ATTRIBUTE] = []
        self._style[SCE_HJ_WORD] = []
        self._style[SCE_HJA_WORD] = []
        self._style[SCE_HB_WORD] = []
        self._style[SCE_HP_WORD] = []
        self._style[SCE_HPHP_WORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_H_TAG].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt1"))
        self._style[SCE_H_ATTRIBUTE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))
        self._style[SCE_HJ_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt3"))
        self._style[SCE_HJA_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt4"))
        self._style[SCE_HB_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt5"))
        self._style[SCE_HP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt6"))
        self._style[SCE_HPHP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class ASP_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "ASP"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_H_TAG = 1
        SCE_H_ATTRIBUTE = 3
        SCE_HJ_WORD = 46
        SCE_HJA_WORD = 61
        SCE_HB_WORD = 74
        SCE_HP_WORD = 96
        SCE_HPHP_WORD = 121

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_H_TAG] = []
        self._style[SCE_H_ATTRIBUTE] = []
        self._style[SCE_HJ_WORD] = []
        self._style[SCE_HJA_WORD] = []
        self._style[SCE_HB_WORD] = []
        self._style[SCE_HP_WORD] = []
        self._style[SCE_HPHP_WORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_H_TAG].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_H_ATTRIBUTE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))
        self._style[SCE_HJ_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt3"))
        self._style[SCE_HJA_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt4"))
        self._style[SCE_HB_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt5"))
        self._style[SCE_HP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt6"))
        self._style[SCE_HPHP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt7"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class JSP_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "JSP"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_H_TAG = 1
        SCE_H_ATTRIBUTE = 3
        SCE_HJ_WORD = 46
        SCE_HJA_WORD = 61
        SCE_HB_WORD = 74
        SCE_HP_WORD = 96
        SCE_HPHP_WORD = 121

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_H_TAG] = []
        self._style[SCE_H_ATTRIBUTE] = []
        self._style[SCE_HJ_WORD] = []
        self._style[SCE_HJA_WORD] = []
        self._style[SCE_HB_WORD] = []
        self._style[SCE_HP_WORD] = []
        self._style[SCE_HPHP_WORD] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_H_TAG].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))
        self._style[SCE_H_ATTRIBUTE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt2"))
        self._style[SCE_HJ_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt3"))
        self._style[SCE_HJA_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt4"))
        self._style[SCE_HB_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt5"))
        self._style[SCE_HP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt6"))
        self._style[SCE_HPHP_WORD].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt7"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class LUA_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "LUA"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_LUA_IDENTIFIER = 11

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_LUA_IDENTIFIER] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_LUA_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class PYTHON_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "PYTHON"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_P_IDENTIFIER = 11

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        self._style[SCE_P_IDENTIFIER] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        self._style[SCE_P_IDENTIFIER].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

class VERILOG_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "VERILOG"
    _style = dict()

    def colorize(self):
        # define style constants for any styles that allow substyles
        #   SCE_CONSTANT_NAME = StyleID_integer
        SCE_VERILOG_NONE = -1

        # then, for each of those, create a dummy list
        #   _style[SCE_CONSTANT_NAME] = []
        #self._style[SCE_VERILOG_NONE] = []

        # INSTRUCTIONS: if you want N substyles for a given parent style,
        #   then for each substyle, append a dict which includes fg, bg, and keywords, such as:
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third"))
        #       self._style[SCE_CONSTANT_NAME].append(dict(fg=(0,0,0), bg=(255,255,0), keywords="black on yellow"))
        #self._style[SCE_VERILOG_NONE].append(dict(fg=(0,0,255), bg=(255,255,0), keywords="pryrt"))

        # this does the work
        self.announce(self._lexer_name)
        self.do_the_work()

try:
    substyle_lexer_interface.toggle()
    if False:
        notepad.clearCallbacks()
        del substyle_lexer_interface
        #console.clear()
        console.write("Deleted callbacks and substyle_lexer_interface\n\n\n")
except NameError:
    substyle_lexer_interface = SubstyleLexerInterface()
    substyle_lexer_interface.main()
