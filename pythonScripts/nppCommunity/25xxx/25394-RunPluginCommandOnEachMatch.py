# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25394/

Runs a plugin command on each match.
The RunPluginCommandOnEachMatch() call at the end takes three arguments:
- a r'' string containing the regex to use
- a plugin name (must match the menu spelling exactly)
- an action from that plugin's sub-menu (must match the menu spelling exactly)

Defaults to acting on what's in between <fieldMap>...</fieldMap>,
using the JsonTools > Pretty-print current JSON file action
Edit that call to get
"""
from Npp import editor,notepad,console
import re

class RunPluginCommandOnEachMatch(object):
    def cb(self, m):
        editor.setSel(m.start(0), m.end(0))
        notepad.runPluginCommand(self.strPlugin, self.strCommand)
        self.startPos = m.end(0)
        editor.setSel(self.startPos,self.startPos)

    def __init__(self, rawRE, strPlugin, strCommand):
        self.strPlugin = strPlugin
        self.strCommand = strCommand
        self.startPos = 0
        oldStart = editor.getSelectionStart()
        oldEnd = editor.getSelectionEnd()
        editor.beginUndoAction()
        while self.startPos < editor.getLength():
            editor.research(rawRE, self.cb, re.MULTILINE, self.startPos, -1, 1);
        editor.endUndoAction()

RunPluginCommandOnEachMatch(r'(?s)(?<=<fieldMap>).*?(?=</fieldMap>)', 'JsonTools', 'Pretty-print current JSON file')
