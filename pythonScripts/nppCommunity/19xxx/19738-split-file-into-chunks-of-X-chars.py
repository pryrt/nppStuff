# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/19738/ , the 2022-May-10 add-on

set nChars to be the maximum "chunk" size, then run this script.
"""
from Npp import editor, notepad
import os.path

nChars = 9000

regex = r'(?s).{1,' + str(nChars) + r'}(\R|\z)'

counter = 0
originalFullname = notepad.getCurrentFilename()
originalPath, originalFile = os.path.split( originalFullname )
originalBase, originalExt = os.path.splitext( originalFile )

def withChunk(m):
    global counter
    counter += 1
    newPath = "{}\\{}_{:03d}{}".format(originalPath, originalBase, counter, originalExt)
    #console.write( "{}\tlength={}".format(newPath, len(m.group(0)))+"\n")

    notepad.new()
    editor.setText(m.group(0))
    notepad.saveAs(newPath)
    notepad.close()
    notepad.activateFile(originalFullname)

editor.research(regex, withChunk)
