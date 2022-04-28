"""
This is example text
That
The
Other
blah
"""
from Npp import editor, notepad, SELECTIONMODE, MENUCOMMAND
from time import sleep

notepad.messageBox("Column selection, then trigger UPDATEUI with activateFile")
editor.setSel(5, 48)
console.write("{}:{}:{} -- {}..{}\n".format(
    editor.getSelectionMode(), SELECTIONMODE.values[editor.getSelectionMode()],editor.selectionIsRectangle(),
    editor.getSelectionStart(),editor.getSelectionEnd(),
))
editor.setSelectionMode(SELECTIONMODE.RECTANGLE)
console.write("{}:{}:{} -- {}..{}\n".format(
    editor.getSelectionMode(),SELECTIONMODE.values[editor.getSelectionMode()],editor.selectionIsRectangle(),
    editor.getSelectionStart(),editor.getSelectionEnd(),
))
sleep(5)
notepad.activateFile(notepad.getCurrentFilename())
sleep(5)

notepad.messageBox("Column selection, then trigger UPDATEUI with changing tabs twice")
editor.setSel(6, 47)
console.write("{}:{}:{} -- {}..{}\n".format(
    editor.getSelectionMode(), SELECTIONMODE.values[editor.getSelectionMode()],editor.selectionIsRectangle(),
    editor.getSelectionStart(),editor.getSelectionEnd(),
))
editor.setSelectionMode(SELECTIONMODE.RECTANGLE)
console.write("{}:{}:{} -- {}..{}\n".format(
    editor.getSelectionMode(),SELECTIONMODE.values[editor.getSelectionMode()],editor.selectionIsRectangle(),
    editor.getSelectionStart(),editor.getSelectionEnd(),
))
notepad.menuCommand(MENUCOMMAND.VIEW_TAB_NEXT)
notepad.menuCommand(MENUCOMMAND.VIEW_TAB_PREV)
sleep(5)

"""
editor.setSelectionMode(SELECTIONMODE.RECTANGLE)
notepad.activateFile(notepad.getCurrentFilename())
"""