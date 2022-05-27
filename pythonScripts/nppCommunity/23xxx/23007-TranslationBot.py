# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23007/

This will set up a translation dictionary, where the key is the "from" and the value is the "to".
The r'' notation will be used so that you can use regex metacharacters in either the key or value

Define your translation regular expressions here:
"""
translation = {
    r'"JJIS number:"':              r'"د JJIS شمیره:"',
    r'"Choose one"':                r'"یو يې غوره کړئ"',
    r'"Social Security number:"':   r'"د ټولنیز مصؤنیت لمبر:"',
    r'"State ID \(SID\):"':         r'"د ایالت ID \(SID\):"'
}

from Npp import editor,notepad,console

class TranslationBot(object):
    def go(self):
        global translation
        editor.beginUndoAction()
        for srch, repl in translation.items():
            editor.rereplace( srch, repl )
        editor.endUndoAction()

TranslationBot().go()

"""
//+ Condition1: ListField("$Node1","textselected","JJIS number:")
//+ Condition1: ListField("$Node1","textselected","Choose one")
//+ Condition1: ListField("$Node1","textselected","Social Security number:")
//+ Condition1: ListField("$Node1","textselected","State ID (SID):")

"""