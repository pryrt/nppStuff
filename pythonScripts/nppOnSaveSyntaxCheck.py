# encoding=utf-8
""" Set up a Notepad++ OnSave Event

Run `perl -c` on the active perl file
Run `compile()` on the active pythonscript file

Inspired by @Alan-Kilborn's https://community.notepad-plus-plus.org/post/71021
and the https://dail8859.github.io/LuaScript/examples/luasyntaxchecker.lua.html that he linked to

Starting with just Perl, but might eventually do others
"""

import subprocess
import os.path
import re
from Npp import (
    editor, notepad, console,
    SCINTILLANOTIFICATION, NOTIFICATION, LANGTYPE, ANNOTATIONVISIBLE
    )

class NppOnSaveSyntaxCheck:

    def __init__(self):
        """initialize the instance"""
        self._is_registered = False

    def __del__(self):
        """destroy the instance: need to clear callbacks"""
        self.unregister_OnSave_callback()

    def annotatePerlErrors(self, fname):
        """clears existing annotations and sets new annotations if perl syntax errors occur"""
        if fname[-3:] != '.pl': return
        editor.annotationClearAll()
        try:
            d = os.path.dirname( notepad.getCurrentFilename() )
            optI = "-I" + d
            subprocess.check_output(['wperl', optI, '-c', notepad.getCurrentFilename()], shell=False, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            #editor.annotationSetText(0, e.output)
            results = dict()
            regex = re.compile(r"^(.*?) at (.*?) line (\d+)", re.IGNORECASE | re.MULTILINE)
            for m in regex.finditer(e.output):
                #console.write("blah = |{}|\n".format(m.group()))
                msg, fn, ln = m.groups()
                #console.write("line = {}\n".format(ln))
                #console.write("\tfile = {}\n".format(fn))
                #console.write("\tmessage = |{}|\n".format(msg))
                if ln in results:
                    results[ln] += "\n" + m.group()
                else:
                    results[ln] = m.group()
            if len(results)>0:
                editor.annotationSetVisible(ANNOTATIONVISIBLE.BOXED)
                for key, value in results.items():
                    #console.write("line({}) => |{}|\n".format(key, value))
                    editor.annotationSetStyle(int(key)-1, 4)    # style#4 = NUMBER (red)
                    editor.annotationSetText(int(key)-1, value)
                    editor.gotoLine(int(key)-1)
                #editor.annotationSetText(editor.getLineCount()-1, e.output)

    def annotatePythonScriptErrors(self, fname):
        """runs compile() on a PythonScript file and uses results to annotate"""
        if fname[-3:] != '.py': return
        editor.annotationClearAll()
        try:
            compile(editor.getText(), "<python script:{}>".format(fname), 'exec')
            #console.writeError("\n\nClean\n\n")
        except SyntaxError as e:
            eo = e.offset
            if eo is None:
                caret = "^"
            elif eo<2:
                caret =  "^"
            else:
                caret = " "*(int(eo)-1) + "^"

            el = int(e.lineno)-1
            annotation = caret + "\n" + e.msg
            editor.annotationSetVisible(ANNOTATIONVISIBLE.BOXED)
            editor.annotationSetStyle(el, 2)    # style#2 = NUMBER (red)
            editor.annotationSetText(el, annotation)
            editor.gotoLine(el)

            #console.writeError("\n")
            #console.writeError("filename            {}\n".format(e.filename             ))
            #console.writeError("lineno              {}\n".format(e.lineno               ))
            #console.writeError("msg                 {}\n".format(e.msg                  ))
            #console.writeError("offset              {}\n".format(e.offset               ))
            #console.writeError("print_file_and_line {}\n".format(e.print_file_and_line  ))
            #console.writeError("text                {}\n".format(e.text                 ))
            #console.writeError("caret               {}\n".format(caret                 ))
            ##console.writeError("args                {}\n".format(e.args                 ))
            ##console.writeError("message             {}\n".format(e.message              ))
            #console.writeError("\n")

    def syntaxCheckOnSave(self,kwargs):
        """This is the function that gets called whenever a file is saved
        kwargs['bufferID'] includes the correct ID
        """
        fname = notepad.getBufferFilename(kwargs['bufferID'])
        if fname[-3:] == '.pl':
            self.annotatePerlErrors(fname)
        elif fname[-3:] == '.py':
            self.annotatePythonScriptErrors(fname)
        else:
            pass

    def register_OnSave_callback(self):
        """registers the OnSave callback"""
        notepad.clearCallbacks(self.syntaxCheckOnSave, [NOTIFICATION.FILESAVED])
        notepad.callback(self.syntaxCheckOnSave, [NOTIFICATION.FILESAVED])
        self._is_registered = True
        console.write("NppOnSaveSyntaxCheck Registered\n")

    def unregister_OnSave_callback(self):
        """unregisters the OnSave callback"""
        notepad.clearCallbacks(self.syntaxCheckOnSave, [NOTIFICATION.FILESAVED])
        self._is_registered = False
        console.write("NppOnSaveSyntaxCheck Unregistered\n")

    def toggle_OnSave_callback(self, flag=False):
        """toggles the OnSave callback"""
        if not self._is_registered or flag:
            self.register_OnSave_callback()
        else:
            self.unregister_OnSave_callback()

global _SINGLETON_CHECKER
try:
    _SINGLETON_CHECKER
except NameError:
    _SINGLETON_CHECKER = NppOnSaveSyntaxCheck()

def _delete_singleton_checker():
    """use this when debugging, to get it to re-initialize the object
        since it's for debugging, it's safe to just clear all callbacks
    """
    global _SINGLETON_CHECKER
    _SINGLETON_CHECKER.unregister_OnSave_callback()
    notepad.clearCallbacks() # ALL!
    del(_SINGLETON_CHECKER)

if __name__ == '__main__':
    _SINGLETON_CHECKER.toggle_OnSave_callback()
