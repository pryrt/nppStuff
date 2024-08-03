# -*- coding: utf-8 -*-
'''
Makes lexilla's "SubStyles" feature available for each of the lexers defined

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

Based on Eko's original EnhanceAnyLexer and my HiddenLexers scripts, plus
    https://community.notepad-plus-plus.org/topic/25980/highlighting-with-self-created-words-in-langs-xml-does-not-work
'''

from Npp import notepad, editor, NOTIFICATION

class Generic_SubstyleLexer:
    _lexer_name = "Generic"

    def __init__(self):
        pass

    def announce(self, lexintf):
        console.write("I will colorize {} from {}\n".format(self._lexer_name, str(lexintf)))
        pass

    def colorize(self):
        raise NotImplementedError("You should be calling colorize() on a specific lexer, not on the {} parent class".format(__class__))

class PHP_SubstyleLexer(Generic_SubstyleLexer):
    _lexer_name = "PHP"
    _style = dict()

    # INSTRUCTIONS: define style constants for any styles that allow substyles
    #   SCE_CONSTANT_NAME = StyleID_integer
    SCE_HPHP_WORD = 121

    # INSTUCTIONS: then, for each of those, create a dummy list
    #   _style[SCE_CONSTANT_NAME] = []
    _style[SCE_HPHP_WORD] = []

    # INSTRUCTIONS: if you want N substyles for a given parent style,
    #   then for each substyle [0] to [N-1], define a dict
    #   which includes fg, bg, and keywords, such as
    #       _style[SCE_CONSTANT_NAME][0] = dict(fg=(255,255,255), bg=(0,0,0), keywords="first second third")
    #       _style[SCE_CONSTANT_NAME][1] = dict(fg=(255,255,255), bg=(255,255,0), keywords="black on yellow")
    _style[SCE_HPHP_WORD][0] = dict(fg=(255,255,255), bg=(0,0,0), keywords="decrypt encrypt")

    def colorize(self):
        self.announce(self._lexer_name)

        for parentStyle in editor.getSubStyleBases().encode():
            console.write("Want to allocate substyles for parentStyle={}\n".format(parentStyle))


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
        self.map_languages['PHP'] = PHP_SubstyleLexer()
        console.write("At Creation: self MapContents: {}\n".format(", ".join(self.map_languages.keys())))
        console.write("create: self.map = {}\n".format(self.map_languages))
        console.write("create: PHP in Map = {}\n".format('PHP' in self.map_languages))

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
        console.write("\ncheck_lexers()\n")
        console.write("At Check: self MapContents: {}\n".format(", ".join(self.map_languages.keys())))
        console.write("At Check: PHP in Map = {}\n".format('PHP' in self.map_languages))

        langType = str(notepad.getCurrentLang())
        console.write("At Check: checking '{}' inMap={}\n".format(langType, langType in self.map_languages))
        console.write("SubStylesForLexer: active file uses \"{}\" lexer, enabled={}, inMap={}\n".format(langType, self.enabled, langType in self.map_languages))

        if self.enabled:
            if langType in self.map_languages:
                console.write("Going to use \"{}\" SubStyles lexer\n".format(langType))
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

try:
    substyle_lexer_interface.toggle()
    if True:
        notepad.clearCallbacks()
        del substyle_lexer_interface
        #console.clear()
        console.write("\ndeleted callbacks and substyle_lexer_interface\n============================\n\n")
except NameError:
    substyle_lexer_interface = SubstyleLexerInterface()
    substyle_lexer_interface.main()
