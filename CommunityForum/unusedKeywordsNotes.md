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

...

Tracing the logic through, the `findKeyWordsParameters()` linked above seems to be where it's going from the langs.xml to populating those word lists.  The indexName string comes from the `<Keywords name="..." ...>` attribute, as I expected.  Based on the `getKwClassFromName()`, instre1 will return 0, instre2 will return 1, type1=2, and so on through type7=8.  then it calls `_langList[_nbLang]->setWords(keyWordsString, kw_integer)` where  `_langList[_nbLang]` is a new instance of class Lang (called a `struct Lang final`).  The Lang::setWords method will pass the keyWordsString into the kw_integer-th index of `_langKeyWordList`, which is an element of the class/struct.  Nothing else accesses that except Lang methods, including `getWords()`.  `pLang->getWords(typeIndex)` is called by `NppParameters::getWordList(langID,typeIndex)`.  

Everything I am reading is saying to me that if I want to set the keyword list equivalently to `editor.setKeywords(3,"...")`, it should be `->setWords("...",3)` which should come from `type2`=3.  But type2 in C++ should be the type2 list that's already there.  Why is this not matching expectations?

Hmm, when I google the c++ type2 terms, they often are coming up as "doxygen" => yes, the list at [doxygen.nl](https://www.doxygen.nl/manual/commands.html) is nearly verbatim the type2 list from langs.xml.  But doxygen should be set2, which would be type1.  But type1 is the bool/char/class, which seems to be correctly working, even though it's set1.  It seems there's an off-by-one or a swap-by-one somewhere in my understanding of what's happening.

Let's try something: go to a new 8.5 unzip.  Open a .cpp and give it some example doxygen from [here](https://www.doxygen.nl/manual/docblocks.html) -- ooh, that works.  The doxygen block (`/*! ... */`) shows up as the COMMENT DOC color as styleID="3", and a keyword like `\brief` (where `brief` _is_ in the langs.xml::cpp::type2) shows up as COMMENT DOC KEYWORD (styleID="17").  If I add `keywordClass="type2"` to the COMMENT DOC KEYWORD and restart, Style Configurator now shows the type2 keyword list with the COMMENT DOC KEYWORD entry.  variable `keywords3` is used for SCE_C_COMMENTDOCKEYWORD, and keywords3 comes from case2, which.... ugh

Hmm, is my mental off-by-one caused because there's a keywords and keywords2 variable, but no keywords1 variable?  No, because keywords3 is mapped to case2.  

Well, wait, maybe that means that set3=case3: is the 4th entry _for c++_, which is type3.  I thought I had tried it.  But let's try again.  Nope.  Try from type7 down to type1, then instre2 and instre1.  When I get to type2, so there are two instances of that name, it just does doxygen based on the second instance.  When I do type1, then the int/class/etc gets overwritten and it only does the second instance.  And instre2 doesn't work.  and instre1 overwrites the `if` and other such syntax. :-(

Anyway, back to tracing.  it sure looks like setWords is based on the NPP definitions of 0-8.  move on to `getWords`, which is only called in `NppParameters::getWordList(langID,typeIndex)`, as I said above.  In the setXmlLexer, it calls generic=getWordList(L_HTML, LANG_INDEX_INSTR); in setCppLexer, it calls doxygenKeyWords=getWordList(L_CPP, LANG_INDEX_TYPE2) -- and then executes SCI_SETKEYWORDS,2,doxygenKeyWords.  Moving out of there (but _will_ be back): setJsLexer calls doxygen=(L_CPP, LANG_INDEX_TYPE2); so does setObjClexer; and setTypeScriptLexer.  Then there is getCompleteKeywordList(string kwl, langType, keywordIndex), which wraps around getWordList(langType, keywordIndex), and then adds space and then converts from CODEPAGE; then it returns the c-string .

Back to setCppLexer(): after it does the non-wrapped for doxygen, if it found doxygen, it will do the same conversion that's in the wrapper (I don't know why they didn't just use the wrapper to begin with).  But doxygen goes to SCI_SETKEYWORDS(2,list).  then it runs makeStyle(language,array), which appears to be what takes the user-defined list from styler.xml and if there are any user-defined keywords, it prepends them to the instre1 string.  Then it uses the wrapper to grab the hardcoded(instre1) list, and saves as cppInstrs.  Then similarly for user-defined and hardcoded type1 into cppTypes.  Then it sets SCI_SETKEYWORDS(0,cppInstrs) and SCI_SETKEYWORDS(1,cppTypes).  Hence, it never does a SCI_SETKEYWORDS(3,...), so that is why nothing I define will get propagated, and why none of my experiments worked.  So the only way around it would be using a language callback from pythonscript.
