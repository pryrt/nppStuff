# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/19015/feature-request-md5-in-the-context-menu

Installation:
1) Install PythonScript using Plugins Admin or manually
2) **PythonScript > New Script**, `npp_selection_filenames_md5.py`

Instructions
1) Select a list of filenames in Notepad++, one filename per line
2) Run this script: **PythonScript > Scripts > `npp_selection_filenames_md5`**
3) The digests will be printed to the PythonScript console

select these two lines:
C:\usr\local\apps\notepad++\plugins\Config\PythonScript\scripts\19015-md5-on-filename-list.py
C:\usr\local\share\PassThru\perl\nppCommunity\19015-md5-on-list-of-files.pl

example output:
f798a465f8019eec4f06287dbeb2f7f8  C:\usr\local\apps\notepad++\plugins\Config\PythonScript\scripts\19015-md5-on-filename-list.py
1908fff7063f4dcf46866367adcd14c2  C:\usr\local\share\PassThru\perl\nppCommunity\19015-md5-on-list-of-files.pl

"""
from Npp import *
import hashlib

def forum_post19015_FunctionName():
    """this is the function's doc string"""
    console.show()
    console.clear()

    eol_tuple = ("\r\n", "\r", "\n")
    eol = eol_tuple[editor.getEOLMode()]

    txt = editor.getSelText()

    if txt == "\0" or len(txt)<1:
        console.writeError("\nusage: make a selection of filename-per-line in Notepad++, then run this script\n\n")
        return

    lines = txt.split(eol)
    for filename in lines:
        if len(filename)>0:
            md5str = hashlib.md5(open(filename,"rb").read()).hexdigest()
            console.write("{}  {}\n".format(md5str, filename))

if __name__ == '__main__': forum_post19015_FunctionName()

