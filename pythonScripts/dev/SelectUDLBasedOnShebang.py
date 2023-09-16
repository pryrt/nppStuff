# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24921/alternative-method-of-udl-association-that-file-suffix-possible

If the extension is right, and the shebang line is right, set to a specific UDL

INSTALLATION
1. Follow the instructions https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript
    to install PythonScript Plugin and save this script as `SelectUDLBasedOnShebang.py`
2. You will want to follow the "Starutp script" instructions in that FAQ as well, with the following two lines
TBD
TBD

CONFIGURE:
1. you will need to go to the line with "CONFIG ="
    - the extension should include the dot in the quotes
    - the firstLineText is the text that should match the "shebang" line (the first line of your file)
    - the NameOfUDL must match the name of your UDL exactly
2. save
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

        # delete from final version: for debug, I want it to clear callbacks before registering
        notepad.clearCallbacks()

        # setup callbacks
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])
        console.write("Registered on_bufferactivated callback for SelectUdlBasedOnShebang\n" )

    def on_bufferactivated(self, args):
        '''
            This callback called every time document is switched.
            Triggers the check if the document is of interest.

            Args: provided by notepad object; the args of interest:
                args['bufferID']:   ID for the activated buffer

        '''
        console.write("on_bufferactivated: "+str(args)+"\n")
        self.check_for_udl(args['bufferID'])

    def check_for_udl(self, bufferID):
        '''
            Check if the active buffer has a known extension for shebang processing
            If so, trigger the UDL-change

            Args:
                bufferID:   ID for the buffer of interest
        '''
        filename = notepad.getBufferFilename(bufferID)
        console.write("checking active buffer {}:{} for UDL\n".format(bufferID,filename))
        (_,ext) = os.path.splitext(filename)
        ext = ext.strip('.')
        console.write("\text = '{}'\n".format(ext))

    def main(self):
        console.write("pass\n")

selectUdlBasedOnShebang = SelectUdlBasedOnShebang()
selectUdlBasedOnShebang.main()

"""
Development Notes:
- see https://github.com/Ekopalypse/NppPythonScripts/blob/master/npp/EnhanceAnyLexer.py
- set UDL using notepad.runMenuCommand('Language', NAME_OF_UDL)

"""
