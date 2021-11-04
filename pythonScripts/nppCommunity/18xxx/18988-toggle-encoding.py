from Npp import notepad, MENUCOMMAND

try:
    toggle = 1 - toggle
except NameError:
    toggle = 0

notepad.menuCommand( (MENUCOMMAND.FORMAT_AS_UTF_8, MENUCOMMAND.FORMAT_ANSI)[toggle] )
