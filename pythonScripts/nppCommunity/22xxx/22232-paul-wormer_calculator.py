"""
    -- Simple calculator for use under Notepad++.

    Select text that contains a valid Python arithmetic expression
    and execute this script.

    Result is inserted between selected text and text following it.

    I assigned the script to the key combination: `Alt+Num +`

    Sample expression: (-(1.0 + 2) * 3 + 55.0) / 8 = 5.75
"""
from Npp import *
expression = editor.getSelText()
try:
    answer = str(eval(expression))
    editor.addText(' = ' + answer)
except SyntaxError as err:
    console.write(err.args[0]+": "+err.args[1][3]+"\r\n")
    editor.addText(' *Error* ')
"""
(-(1.0 + 2) * 3 + 55.0) / 8
(-(1.0 + 2) * 3 + 55.0) / 8 = 5.75
(-(1.0 + 2) * 3 + 55.0) / 8
(-(1.0 + 2) * 3 + 55.0) / 8

 = 5.75
"""
