[this forum post](https://community.notepad-plus-plus.org/topic/24228/can-t-make-default-c-style-to-highlight-custom-macros) shows a user who wants additional C++ keyword category.

I went looking through LexCPP.cpp and associated, and ran some PythonScript experiments:
```py
# encoding=utf-8
"""allows me to go through the first 32 styles, and see which keyword list goes with each style"""
from Npp import editor,notepad,console
from time import sleep

class findStylesToKeyWordSet(object):
    def go(self):
        console.clear()
        console.show()
        for s in range(32): # (0,5,11,16,19): # range(32):
            fg = editor.styleGetFore(s);
            editor.styleSetFore(s, (255,255,0))
            console.write("style #{}\n".format(s))
            for kws in range(9):
                editor.setKeyWords(kws, "set{}".format(kws))
            sleep(2)
            editor.styleSetFore(s,fg)
            sleep(0)

findStylesToKeyWordSet().go()
```

Running that for C++, the StyleID="19" (SCE_C_GLOBALCLASS) is associated with index3 for `editor.setKeyWords()`

So if in PythonScript I set that list using `editor.setKeywords(3, "word1 word2 ...")`, and either use PythonScript or stylers.xml to setSstyleID="19" to CYAN,
then the words I listed will show up highlighted CYAN.  However, I cannot find any of instre1, instre2, type1 ... type7 (those are the 9 available stylers.xml:`<WordsStyle ... keywordClass="xxx">` <=>  langs.xml:`<Keywords name="xxx">` mapping strings, per [Parameters.cpp::getKwClassFromName()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/c8e4e671dad405d60e95ba483991a4b3b77bf2c2/PowerEditor/src/Parameters.cpp#L590), which is called during [AddStyler()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/c8e4e671dad405d60e95ba483991a4b3b77bf2c2/PowerEditor/src/Parameters.cpp#L3963) and [feedKeyWordsParameters()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/c8e4e671dad405d60e95ba483991a4b3b77bf2c2/PowerEditor/src/Parameters.cpp#L4454)

So I don't know how to figure out how Notepad++ decides whether to populate the keywords based on a given stylers.xml+langs.xml combination.
