# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/16997/ #8,#10 by Eko-palypse:

Try to "hammer" NPP with many calls to the getLanguageDesc and getCurrentLang
"""
from Npp import *

console.show()
console.clear()
console.write(__file__ + "::" + __name__ + "\n")
for i in range(1000000):
    x = notepad.getLanguageDesc(notepad.getCurrentLang())
    console.write( '#{:-8} => {}\n'.format( i, x ) )

