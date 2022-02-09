# -*- coding: utf-8 -*-
'''
If you want to have customized foldering characteristics
on a per-language basis, look no further (or, at least, try this out)

    See https://www.scintilla.org/ScintillaDoc.html#SCI_SETFOLDFLAGS for more information on that topic

'''
import sys
from Npp import (notepad, editor, editor1, editor2,
                 NOTIFICATION, SCINTILLANOTIFICATION,
                 FOLDFLAG)

class FoldingFormatter:
    def __init__(self):
        self.langs = dict()
        self.registerFoldingCallback()
        self.add('__DefaultFolding__', FOLDFLAG.LINEAFTER_CONTRACTED)
        self._is_interesting = False

    def add(self, langName, foldFlags=FOLDFLAG.LINEAFTER_CONTRACTED):
        #console.write("adding '{}' to {}\n".format(langName, self.langs))
        self.langs[langName] = FoldingFormatter.LanguageFoldingFormatter(langName, foldFlags)

    def get(self, langName):
        #console.write("getting '{}' from {}\n".format(langName, self.langs))
        return self.langs[langName]

    def applyFolding(self):
        active_language = notepad.getLanguageName(notepad.getLangType()).replace('udf - ','').lower()
        self._is_interesting = active_language in self.langs
        #console.write("applyFolding({}) {}\n\t{}\n".format(active_language, '[interesting]' if self._is_interesting else '', self.langs))
        #console.write("\tinteresting = {}\n".format(self._is_interesting))
        if self._is_interesting:
            # apply this language's FOLD settings
            editor.setFoldFlags(self.langs[active_language].foldFlags)
            pass
        else:
            # apply default FOLD settings
            editor.setFoldFlags(self.langs['__DefaultFolding__'].foldFlags)
            pass

    def foldingCallback(self, args):
        """
            This processes the callback arguments, then runs the applyFolding method
        """
        #console.write("callback args {}\n".format(str(args)))
        self.applyFolding()
        pass

    def registerFoldingCallback(self):
        #console.write("Registering FoldingFormatter callback\n")
        # editor.callbackSync(self.on_updateui, [SCINTILLANOTIFICATION.UPDATEUI])
        # editor.callbackSync(self.on_marginclick, [SCINTILLANOTIFICATION.MARGINCLICK])
        notepad.callback(self.foldingCallback, [NOTIFICATION.LANGCHANGED, NOTIFICATION.BUFFERACTIVATED])

    def __del__(self):
        #console.write("FoldingFormatter being deleted:\n")
        editor1.setFoldFlags(self.langs['__DefaultFolding__'].foldFlags)
        editor2.setFoldFlags(self.langs['__DefaultFolding__'].foldFlags)
        for k in self.langs.keys():
            del self.langs[k]
            #console.write("\t... {} deleted\n".format(k))
        #console.write("... Unregister callback\n")
        notepad.clearCallbacks(self.foldingCallback)

    class LanguageFoldingFormatter:
        def __init__(self, langName, foldFlags):
            self.name = langName
            self.foldFlags = foldFlags

        def __del__(self):
            #console.write("\tLanguageFoldingFormatter[{}] is being deleted\n".format(self.name))
            pass

        def __str__(self):
            return "<<folder for '{}'>>".format(self.name)

try:
    # I want to delete it if it exists, because if I'm running the script again,
    #   I may have updated the callback code and thus need to delete the old callback before defining a new one
    #console.clear()
    #console.write("deleting old\n")
    global _folding_formatter
    del _folding_formatter
except:
    # I don't care if it didn't exist previously
    pass

_folding_formatter = FoldingFormatter()
_folding_formatter.add('visual basic', foldFlags=FOLDFLAG.LINEBEFORE_EXPANDED|FOLDFLAG.LINEAFTER_CONTRACTED)

"""
what I want to do is create a callback which will look up the current file type,
and if it's in the dictionary, apply that specific folding setup, otherwise apply the default

__init__ should register the callback
__del__ (destructor) should unregister

script itself should destroy the FoldingFormatter instance every time script is run
(so that old callbacks will be unregistered)
"""
