# encoding=utf-8
from Npp import console
console.show()
console.clear()
console.write( u'SMILE: ☺\n' )
console.write( u"क़" )

"""
if the first line is `# encoding =utf-8` instead, it will give an error:

    File "C:\Users\peter.jones\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\NppForumPythonScripts\16899-encoding-sscce.py", line 5
    SyntaxError: Non-ASCII character '\xe2' in file C:\Users\peter.jones\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\NppForumPythonScripts\16899-encoding-sscce.py on line 5, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
"""