# encoding=utf-8
"""allows me to go through the first 32 styles, and see which keyword list goes with each style"""
from Npp import editor,notepad,console
from time import sleep

class findStylesToKeyWordSet(object):
    def go(self):
        console.clear()
        console.show()
        for s in range(32): # (0,5,11,16,19): # range(32):
            fg = editor.styleGetFore(s);
            editor.styleSetFore(s, (255,255,0))
            console.write("style #{}\n".format(s))
            for kws in range(9):
                editor.setKeyWords(kws, "set{}".format(kws))
            sleep(2)
            editor.styleSetFore(s,fg)
            sleep(0)

findStylesToKeyWordSet().go()
