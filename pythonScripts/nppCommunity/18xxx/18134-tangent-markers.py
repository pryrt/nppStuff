# encoding=utf-8
"""as a tangent from the other 18134, look at scintilla markers (which are used as "bookmarks", not "mark #")
"""
from Npp import *
from time import sleep

console.clear()
console.show()
console.write("{:<4d} {:08x} {:032b}\n".format(3, editor.markerGet(3)&0xFFFFFFFF, editor.markerGet(3)&0xFFFFFFFF))

for m in range(32):
    editor.markerDefine(24, m)
    console.write("{} ".format(m))
    sleep(0.1)
console.write("\n")

editor.markerDefine(24, 30)
editor.rGBAImageSetWidth(32)

for m in range(32,128):
    editor.markerDefine(24, 10000+m)
    console.write("{} ".format(m))
    sleep(0.3)
console.write("\n")

editor.markerDefine(24, 30)
