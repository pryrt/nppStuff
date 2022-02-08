# -*- coding: utf-8 -*-
'''
If you want to have customized foldering characteristics
on a per-language basis, look no further (or, at least, try this out)

    See https://www.scintilla.org/ScintillaDoc.html#SCI_SETFOLDFLAGS for more information on that topic

'''
import sys
from Npp import (notepad, editor, editor1, editor2,
                 NOTIFICATION, SCINTILLANOTIFICATION,
                 INDICATORSTYLE, INDICFLAG, INDICVALUE)

if sys.version_info[0] == 2:
    from collections import OrderedDict as _dict
else:
    _dict = dict


class FoldingFormatter:
    def __init__(self):
        self.langs = dict()

    def add(self, langName):
        self.langs[langName] = FoldingFormatter.LanguageFoldingFormatter(langName)

    def get(self, langName):
        return self.langs[langName]

    class LanguageFoldingFormatter:
        def __init__(self, langName):
            self.name = langName

        def __str__(self):
            return "<<name:'{}'>>".format(self.name)

try:
    del _folding_formatter
    #console.writeError("deleted _folding_formatter\n")
except:
    #console.writeError("no _folding_formatter to begin with\n")
    pass # I want to delete it if it exists; I don't care if it didn't exist previously

_folding_formatter = FoldingFormatter()
_folding_formatter.add('vb')
console.write("look at {}\n".format(str(_folding_formatter.get('vb'))))

"""
what I want to do is create a callback which will look up the current file type,
and if it's in the dictionary, apply that specific folding setup, otherwise apply the default

__init__ should register the callback
__del__ (destructor) should unregister

script itself should destroy the FoldingFormatter instance every time script is run
(so that old callbacks will be unregistered)
"""
