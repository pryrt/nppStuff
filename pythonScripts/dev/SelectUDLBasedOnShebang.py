# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24921/alternative-method-of-udl-association-that-file-suffix-possible

If the extension is right, and the shebang line is right, set to a specific UDL

INSTALLATION
1. Follow the instructions https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript
    to install PythonScript Plugin and save this script as `SelectUDLBasedOnShebang.py`
2. You will want to follow the "Starutp script" instructions in that FAQ as well, with the following two lines

import SelectUDLBasedOnShebang
selectUDLBasedOnShebang = SelectUDLBasedOnShebang.SelectUDLBasedOnShebang()


CONFIGURE:
Go to the line with "CONFIG =" and edit the contents
    - the extension should include the dot in the quotes
    - the firstLineText is the text that should match the "shebang" line (the first line of your file)
    - the NameOfUDL must match the name of your UDL exactly
Save
Run the script (Plugins > Python Script > Scripts > SelectUDLBasedOnShebang) or restart Notepad++

From now on (including after restart), anytime you activate the buffer of a file
ending with a known extension (one of the extensions in CONFIG), it will
look at the first line, and if the first line exactly matches one of the
firstLineText strings in the CONFIG table, then it will activate the UDL
that has exactly the NameOfUdl
"""
from Npp import editor,notepad,console,NOTIFICATION
import os

class SelectUdlBasedOnShebang(object):
    CONFIG = {
        ".mscript" : {                      # the extension, including the .
            "#UDL!mscript1": "mscript1",    # firstLineText : NameOfUDL
            "#UDL!mscript2": "mscript2",    # firstLineText : NameOfUDL
        },
        ".ext" : {                          # the extension, including the .
            "#UDL!ext1": "ext1",            # firstLineText : NameOfUDL
            "#UDL!ext2": "ext2",            # firstLineText : NameOfUDL
        },
    }
    def __init__(self):
        '''Initialize the new instance'''
        current_version = notepad.getPluginVersion()
        if current_version < '2.0.0.0':
            notepad.messageBox('It is needed to run PythonScript version 2.0.0.0 or higher',
                               'Unsupported PythonScript verion: {}'.format(current_version))
            return

        # setup callbacks
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])
        console.write("Registered on_bufferactivated callback for SelectUdlBasedOnShebang\n" )

        # run the initial check
        self.check_for_udl(notepad.getCurrentBufferID())


    def on_bufferactivated(self, args):
        '''
            This callback called every time document is switched.
            Triggers the check if the document is of interest.

            Args: provided by notepad object; the args of interest:
                args['bufferID']:   ID for the activated buffer
            Return:
                Nothing

        '''
        self.check_for_udl(args['bufferID'])

    def check_for_udl(self, bufferID):
        '''
            Check if the active buffer has a known extension for shebang processing
            If so, trigger the UDL-change

            Args:
                bufferID:   ID for the buffer of interest
            Return:
                Nothing
        '''
        filename = notepad.getBufferFilename(bufferID)
        (_,ext) = os.path.splitext(filename)
        if ext in self.CONFIG:
            self.check_shebang( self.CONFIG[ext] )

    def check_shebang(self, shebangs):
        '''
            Check if the active buffer has the right shebang
            If so, set teh UDL

            Args:
                shebangs:   dict mapping shebang to corresponding UDL name
            Return:
                Nothing
        '''
        firstLine = editor.getLine(0).rstrip();
        if firstLine in shebangs:
            found = shebangs[firstLine]
            notepad.runMenuCommand('Language', found)


if __name__ == '__main__':
    selectUdlBasedOnShebang = SelectUdlBasedOnShebang()

"""
Development Notes:
- see https://github.com/Ekopalypse/NppPythonScripts/blob/master/npp/EnhanceAnyLexer.py
- set UDL using notepad.runMenuCommand('Language', NAME_OF_UDL)

"""
