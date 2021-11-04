"""https://community.notepad-plus-plus.org/topic/20296"""
from Npp import *
notepad.menuCommand(MENUCOMMAND.EDIT_CLEARREADONLY)   # clears the Windows attribute
if editor.getReadOnly():
    notepad.menuCommand(MENUCOMMAND.EDIT_SETREADONLY)   # toggles the Notepad++ menu, but only if it's needed
notepad.runPluginCommand('XML Tools', 'Pretty Print')
