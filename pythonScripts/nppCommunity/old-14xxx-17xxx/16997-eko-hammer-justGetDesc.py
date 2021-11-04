# encoding=utf-8
"""code from https://notepad-plus-plus.org/community/topic/16997/ #12 by Eko-palypse:

Try to "hammer" NPP with many calls to the getLanguageDesc and getCurrentLang
"""
from Npp import notepad, LANGTYPE
import time

LANGUAGES = LANGTYPE.values.values()
console.write("START\n")
for i in range(1000+1):
  for language in LANGUAGES:
    x = notepad.getLanguageDesc(language)
    console.write("{:<7} {:<7} {:<40} {}\n".format(i,language,x,time.localtime()))
    time.sleep(0.001)
  console.write("\n")

console.write("DONE\n")