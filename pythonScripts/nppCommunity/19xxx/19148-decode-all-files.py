# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/19148/
"""
from Npp import *
from time import sleep

bufferID = notepad.getCurrentBufferID()
for t in notepad.getFiles():
    notepad.activateIndex(t[3], t[2])
    sleep(0.5)
    editor.beginUndoAction()
    keep_pos = editor.getCurrentPos()
    editor.selectAll()
    sleep(0.5)
    notepad.runPluginCommand('MIME Tools', 'URL Decode')
    sleep(1)
    editor.setEmptySelection(keep_pos)
    editor.endUndoAction()
    sleep(0.5)


notepad.activateBufferID(bufferID)
"""
https://example/search?encode%3Dblah!!!!
https://example/search?encode%3Dblah!!!!
https://example/search?encode%3Dblah!!!!
other stuff "%55" hi
https://example/search?encode%3Dblah%20%21%22%23
https://example/search?encode%3Dblah%20%21%22%23+ABC
"""