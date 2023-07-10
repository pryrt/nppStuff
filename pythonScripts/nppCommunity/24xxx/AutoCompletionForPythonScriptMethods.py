# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24687/

Auto-completion for PythonScript methods (complete-on-dot) when a dot is entered.

Derived from https://github.com/bruderstein/PythonScript/issues/275#issuecomment-1383132656 as starting point

"""
from Npp import editor,notepad,console,SCINTILLANOTIFICATION

class ACFPSM(object):
    sci_methods = ';'.join("""
        addRefDocument
        addSelection
        addStyledText
        addTabStop
        addText
        addUndoAction
        """.split())

    npp_methods = ';'.join("""
        activateBufferID
        activateFile
        activateIndex
        """.split())

    def __init__(self):
        console.write("Registered AutoCompletionForPythonScriptMethods.py callbacks\n")
        editor.callback(self.on_charadded, [SCINTILLANOTIFICATION.CHARADDED])
        self.active = True
        self.bufferIDs = []

    def toggle(self):
        self.active = not self.active
        console.write("AutoCompletionForPythonScriptMethods.py callbacks are {}\n".format('active' if self.active else 'inactive'))

    def get_current_dotted_words(self, p):
        end_p = p
        while p > 0:
            p -= 1
            c = editor.getCharAt(p)
            # . or _ is valid
            if c == ord('.') or c == ord('_'):
                continue
            # digit is valid
            if ord('0') <= c and c <= ord('9'):
                continue
            # uppercase is valid
            if ord('A') <= c and c <= ord('Z'):
                continue
            # lowercase is valid
            if ord('a') <= c and c <= ord('z'):
                continue

            # otherwise, not valid, so do not include this character in the string
            p+=1
            break

        return editor.getTextRange(p, end_p)


    def on_charadded(self, args):
        if not self.active:
            return

        if args['ch'] == ord('.'):
            word = self.get_current_dotted_words(editor.getCurrentPos())
            clist = None
            if word in ['editor.', 'editor1.', 'editor2.']:
                clist = self.sci_methods
            elif word == 'notepad.':
                clist = self.npp_methods

            if clist is not None:
                editor.autoCSetSeparator(ord(';'))
                editor.autoCShow(0, clist)

if __name__ == '__main__':
    try:
        _ACFPSM.toggle()
    except NameError:
        _ACFPSM = ACFPSM()
