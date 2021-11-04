# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21225/

Written by @PeterJones

Searches for keywordText multiple times, and replaces it with the next element of replacementList
"""
from Npp import *

keywordText = 'TYPEE'
replacementList = [ 'CANADA', 'MEXICO', 'COSTA RICA' ]

counter = -1

def nextReplacement(m):
    global counter
    counter += 1
    return replacementList[counter] if counter < len(replacementList) else m.group(0)

editor.beginUndoAction()
editor.replace(keywordText, nextReplacement)
editor.endUndoAction()
