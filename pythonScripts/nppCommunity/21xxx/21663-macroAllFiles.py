# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21663/

Run a macro on each open file
"""
from Npp import notepad

# store active tab in each View
keepBufferID = notepad.getCurrentBufferID()
docIndexes = [notepad.getCurrentDocIndex(v) for v in range(2)]

for filename, bufferID, index, view in notepad.getFiles():
    notepad.activateBufferID(bufferID)
    notepad.runMenuCommand("Macro", "DoNothing")

# restore active tab in each View
for v in range(2):
    notepad.activateIndex(v, docIndexes[v])
notepad.activateBufferID(keepBufferID)
