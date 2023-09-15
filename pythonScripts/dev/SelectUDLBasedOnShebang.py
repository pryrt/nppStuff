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
from Npp import editor,notepad,console

class ThisIsTheClass(object):
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
    def go(self):
        #console.write("pass")
        pass

ThisIsTheClass().go()
console.show()
console.write(str(ThisIsTheClass.CONFIG)+"\n")
