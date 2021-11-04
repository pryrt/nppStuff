# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/16870/

exploring editor.setProperty() and related

additional experiments: moved to 19486-propertiesForEachLexer.py
"""
from Npp import *
from time import sleep

console.show()
console.clear()

notepad.new()
editor.addText("/* json comment */\r\n[1,2,3] // tail comment\r\n{ \"key\": 5 }\r\n");
editor.setSavePoint() # no longer marked "dirty"
notepad.setLangType(LANGTYPE.JSON)
console.write(editor.propertyNames() + "\n")

sleep(1)
editor.setProperty("lexer.json.allow.comments",1)
editor.addText("")
sleep(1)
editor.setProperty("lexer.json.allow.comments",0)
editor.addText("")
sleep(1)
editor.setProperty("lexer.json.allow.comments",1)
editor.addText("")
sleep(1)

