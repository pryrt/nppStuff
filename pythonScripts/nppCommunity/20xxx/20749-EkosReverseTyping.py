"""https://community.notepad-plus-plus.org/post/62959"""
from Npp import editor, SCINTILLANOTIFICATION

def on_char_added(args):
    if DO_REVERSE_TYPING:
        editor.gotoPos(editor.getCurrentPos()-1)

try:
    DO_REVERSE_TYPING = not DO_REVERSE_TYPING
except NameError:
    editor.callbackSync(on_char_added, [SCINTILLANOTIFICATION.CHARADDED])
    DO_REVERSE_TYPING = True
