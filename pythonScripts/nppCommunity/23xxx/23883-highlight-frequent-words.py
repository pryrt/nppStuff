# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23883/

When run, this script will count all the words (except for stopwords),
and assign a color to each word in the list of Top N Colors

Edit the contents of the stopwords variable to change which words are ignored
    - the default stopwords are some linking verbs, conjunctions, articles, and prepositions
    - words of 1 or two characters are automatically annoyed

Edit the list of appended colors in createPalette() to change the color palette
    - you can change the colors to your liking
    - you can or remove colors to change the nu
    - the default color list is based on mspaint.exe's palette on my laptop

Based heavily on these:
- @Alan-Kilborn     https://community.notepad-plus-plus.org/post/61801
- @Ekopalypse       https://github.com/Ekopalypse/NppPythonScripts/blob/master/npp/EnhanceAnyLexer.py


"""
from Npp import editor,notepad,console, INDICATORSTYLE, INDICFLAG, INDICVALUE
from random import randint

class FrequentHighlighter(object):
    INDICATOR_ID = 0

    stopwords = """
    be am are is was were been has have
    and but or nor for yet so
    the an
    aboard about above across after against along amid among around as at before behind below beneath beside between beyond but by concerning considering despite down during except following for from in inside into like minus near next of off on onto opposite out outside over past per plus regarding round save since than through till to toward under underneath unlike until up upon versus via with within without
    """.split()

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

    def match_found(self, m):
        self.word_matches.append(editor.getTextRange(m.span(0)[0], m.span(0)[1]).lower())

    def createPalette(self):
        self.palette = []
        self.palette.append(self.rgb(237,28,36))
        self.palette.append(self.rgb(255,174,201))
        self.palette.append(self.rgb(255,127,39))
        self.palette.append(self.rgb(255,201,14))
        self.palette.append(self.rgb(255,242,0))
        self.palette.append(self.rgb(239,228,176))
        self.palette.append(self.rgb(34,177,76))
        self.palette.append(self.rgb(181,230,29))
        self.palette.append(self.rgb(0,162,232))
        self.palette.append(self.rgb(153,217,234))
        self.palette.append(self.rgb(63,72,204))
        self.palette.append(self.rgb(112,146,190))
        self.palette.append(self.rgb(163,73,164))
        self.palette.append(self.rgb(200,191,231))

        self.word_palette = {}  # word palette will be populated later

    def go(self):
        self.createPalette()
        editor.indicSetStyle(self.INDICATOR_ID, INDICATORSTYLE.TEXTFORE)
        editor.indicSetFlags(self.INDICATOR_ID, INDICFLAG.VALUEFORE)
        self.word_matches = []
        self.histogram_dict = {}
        editor.research('[[:alpha:]]{3,}', self.match_found)
        for word in self.word_matches:
            if word not in self.histogram_dict:
                self.histogram_dict[word] = 1
            elif word not in self.stopwords:
                self.histogram_dict[word] += 1
            elif word in self.stopwords:
                if word in self.histogram_dict: del self.histogram_dict[word]

        output_list = []
        for word in sorted(self.histogram_dict, key=self.histogram_dict.get, reverse=True):
            if len(self.palette) > 0:
                self.word_palette[word] = self.palette.pop(0)   # equivalent to perl's shift, where pop() without argument is perl's pop
                output_list.append('{}={} [0x{:06x}]'.format(word, self.histogram_dict[word], self.word_palette[word]))
            elif self.histogram_dict[word] > 1:
                output_list.append('{}={}'.format(word, self.histogram_dict[word]))

        #console.write('\r\n'.join(output_list) + "\r\n\r\n")

        # do the coloring
        self.colored = 0
        editor.research('[[:alpha:]]{3,}', self.match_colorize)


    def match_colorize(self, m):
        a,b = m.span(0)
        word = editor.getTextRange(m.span(0)[0], m.span(0)[1]).lower()

        if word in self.histogram_dict:
            if not word in self.word_palette: return
            # console.write("{:<3d} => 0x{:06x}\tword='{}'[{}] from {}..{} = len:{}\n".format(self.colored, self.word_palette[word], word, self.histogram_dict[word],a,b,b-a))
            editor.setIndicatorCurrent(self.INDICATOR_ID)
            editor.setIndicatorValue(self.word_palette[word])
            editor.indicatorFillRange(a, b-a)
            self.colored = self.colored + 1


FrequentHighlighter().go()
