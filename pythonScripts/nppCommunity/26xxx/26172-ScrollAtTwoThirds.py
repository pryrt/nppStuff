from Npp import editor, console, SCINTILLANOTIFICATION
import datetime

def scrollThirdIfBottomThird(args):
    p = editor.getCurrentPos()
    l = editor.lineFromPosition(p)
    v = editor.getFirstVisibleLine()
    h = editor.linesOnScreen()
    console.write("t:{} pos:{} line:{} first:{} height:{} l-v:{} 2/3h: {} DoScroll?:{}\n".format(datetime.datetime.now(), p,l,v,h,l-v, 2/3*h, (l-v) > 2/3*h))
    if (l-v) > 2/3*h:
        editor.lineScroll(0, round(h/3))

console.show()
editor.callback(scrollThirdIfBottomThird, [SCINTILLANOTIFICATION.CHARADDED])
console.write("Registered CHARADDED=>scrollThirdIfBottomThird() callback\n")

"""
1. Run Script to register callback; verify it gives the message in the console.
2. Edit this file by hitting ENTER in the blank section, until about 2/3 through the screen,
   and watch it scroll when I make it below 2/3













"""
