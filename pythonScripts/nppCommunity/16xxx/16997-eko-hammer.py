# encoding=utf-8
"""code from https://notepad-plus-plus.org/community/topic/16997/ #11 by Eko-palypse:

Try to "hammer" NPP with many calls to the getLanguageDesc and getCurrentLang
"""
import random
from Npp import editor, notepad, NOTIFICATION, MENUCOMMAND
import time

def on_lang_changed(args):
    x = notepad.getCurrentLang()
    z = ''
    z = notepad.getLanguageDesc(x)
    y = editor.getLexerLanguage()
    print '{:<20} {:<40} {}'.format(y, z, time.localtime())
    #console.write(y+"\n")

notepad.clearCallbacks([NOTIFICATION.LANGCHANGED])
notepad.callback(on_lang_changed, [NOTIFICATION.LANGCHANGED])

LANGUAGES = [eval('MENUCOMMAND.{}'.format(x)) for x in dir(MENUCOMMAND) if x.startswith('LANG_') and not x.startswith('LANG_USER')]
COUNTS = len(LANGUAGES)
for i in range(1,1000+1):
    #console.write('#{:<8} {}\n'.format(i, time.localtime()))
    notepad.menuCommand(LANGUAGES[random.randint(0,COUNTS-1)])
    time.sleep(0.01)
    #console.write('#{:<8} {}\t'.format(i, time.localtime()))
    notepad.menuCommand(MENUCOMMAND.LANG_PYTHON)
    time.sleep(0.01)

"""
CURSOR ON NEXT LINE:

"""