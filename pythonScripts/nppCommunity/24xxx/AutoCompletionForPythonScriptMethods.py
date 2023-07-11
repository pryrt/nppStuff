# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24687/

Auto-completion for PythonScript methods (complete-on-dot) when a dot is entered.

Derived from https://github.com/bruderstein/PythonScript/issues/275#issuecomment-1383132656 as starting point

Installation Instructions:
- call it `AutoCompletionForPythonScriptMethods.py`
- see FAQ for instructions: https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript

"""
import Npp
from Npp import editor,notepad,console,SCINTILLANOTIFICATION

class ACFPSM(object):
    """AutoCompletionForPythonScriptMethods (ACFPSM)
    When toggled on, it will add a custom autoCompletion popup when '.' is typed

    It auto-populates the autoCompletion list from the PythonScript object methods and enumeration members
    """

    # populate the class dictionary when class is created
    aclists = dict()
    for obj_str in dir(Npp):
        """
        @Alan-Kilborn posted this alogrithm in https://community.notepad-plus-plus.org/post/87757
        and I expanded it to work on enums w/ elements, not just objects w/ methods
        """
        if obj_str.startswith('_'): continue
        if obj_str not in aclists: aclists[obj_str] = []
        for item in dir(eval(obj_str)):
            if item.startswith('_') or item.startswith(tuple(str(d) for d in range(10))): continue
            obj_plus_item_str = obj_str + '.' + item
            if 'bound method' in str(eval(obj_plus_item_str)) or hasattr(eval(obj_plus_item_str), 'values'):
                aclists[obj_str].append(item)


    def __init__(self):
        """Constructor: Registers the callback"""
        console.write("Registered AutoCompletionForPythonScriptMethods.py callbacks\n")
        editor.callback(self.on_charadded, [SCINTILLANOTIFICATION.CHARADDED])
        self.active = True
        self.bufferIDs = []

    def toggle(self):
        """Toggles whether or not the PythonScript autoCompletion is active"""
        self.active = not self.active
        console.write("AutoCompletionForPythonScriptMethods.py callbacks are {}\n".format('active' if self.active else 'inactive'))

    def get_current_dotted_words(self, p):
        """used by on_charadded to get a sequence of word-characters-or-dot as the active 'word'"""
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
        """this is the callback function that will be run when you add a new character in scintilla"""
        if not self.active:
            return

        if args['ch'] == ord('.'):
            word = self.get_current_dotted_words(editor.getCurrentPos())
            clist = None
            if word[:-1] in self.aclists:
                clist = ';'.join(self.aclists[word[:-1]])

            if clist is not None:
                editor.autoCSetSeparator(ord(';'))
                editor.autoCShow(0, clist)

if __name__ == '__main__':
    """
    if this script is run manually (rather than from startup.py),
    it will create an instance, or if the instance exists, it will toggle the autoCompletion state
    """
    try:
        _ACFPSM.toggle()
    except NameError:
        _ACFPSM = ACFPSM()
