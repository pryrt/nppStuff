# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23883/

It won't do _exactly_ what the person wants.  But I think I could count each word,
and then maybe eventually do some highlighting of the most frequent words

Search forum for frequency:
- https://community.notepad-plus-plus.org/post/61801 => Alan

Unfortunately, despite following the formula from EnhanceAnyLexer,
I cannot get the indicators to consistently color what I want.

"""
from Npp import editor,notepad,console, INDICATORSTYLE, INDICFLAG, INDICVALUE
from random import randint

class FrequentHighlighter(object):
    INDICATOR_ID = 0

    stopwords = ['the', 'and', 'or', 'self', 'is']
    def match_found(self, m):
        self.word_matches.append(editor.getTextRange(m.span(0)[0], m.span(0)[1]).lower())

    def go(self):
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

        output_list = []
        for k in sorted(self.histogram_dict, key=self.histogram_dict.get, reverse=True):
            if self.histogram_dict[k] > 1:
                output_list.append('{}={}'.format(k, self.histogram_dict[k]))

        #output_list.sort()
        console.write('\r\n'.join(output_list))

        # TODO: do the coloring
        editor.research('[[:alpha:]]{3,}', self.match_colorize)


    def match_colorize(self, m):
        a,b = m.span(0)
        word = editor.getTextRange(m.span(0)[0], m.span(0)[1]).lower()
        if word in self.histogram_dict:
            editor.setIndicatorCurrent(self.INDICATOR_ID)
            editor.setIndicatorValue(randint(0,255))
            editor.indicatorFillRange(a, b-a)


FrequentHighlighter().go()
