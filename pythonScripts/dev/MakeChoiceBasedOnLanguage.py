# seeing if I can make a choice based on the language
#   notepad.getCurrentLang() returns a LANGTYPE
#       * Unfortunately, 1.0.8 helpfile doesn't describe the LANGTYPE enum
#       * Some googling eventually found
#           `enum LangType` at https://github.com/bruderstein/PythonScript/blob/25939fedd2080d1aefc577379664350c343ec13d/NppPlugin/include/Notepad_plus_msgs.h
#         and
#           `boost::python::enum_<LangType>("LANGTYPE")` at https://github.com/bruderstein/PythonScript/blob/master/PythonScript/src/NotepadPython.cpp
#       * Some experimenting showed I can convert that to a string in python using str( notepad.getCurrentLang() )
enumLang = notepad.getCurrentLang()
strLang = str(enumLang)
if enumLang == LANGTYPE.PYTHON:
    msg = "Python!"
elif enumLang == LANGTYPE.HTML:
    msg = "HTML should be renderable"
elif enumLang == LANGTYPE.USER:
    msg = "User Defined Language!"
else:
    msg = "other language: '" + strLang + "'"
notepad.messageBox("'"+strLang+"': " + msg)
console.show()
console.write(strLang+ "\n")
# at this point, I should be able to figure out how to launch a pre-processor or send the HTML directly to a browser
console.run(r'cmd.exe /c echo command echo ' + "'"+strLang+"': " + msg)
editor.documentEnd()
#console.run(r'cmd.exe /c echo #command echo INTO THIS DOCUMENT: ' + "'"+strLang+"': " + msg, editor)
console.run(r'cmd.exe /c start cmd /k echo "' + notepad.getCurrentFilename() + '"')
#### so console.run() is the accepted way of launching a new process from inside PythonScript; that's obviously how I'd have to launch pre-processors, and again how I'd load the result with the browser

# 1.3.0.0 updates: helpfile does describe LANGTYPE
#   also, I see .getLanguageDesc and .getLanguageName: let's try those out on a UDL file
console.write('getLanguageName = {}\n'.format(notepad.getLanguageName(enumLang)) )
console.write('getLanguageDesc = {}\n'.format(notepad.getLanguageDesc(enumLang)) )
    # for MARKDOWN file:
    #   getLanguageName = udf - Markdown
    #   getLanguageDesc = User Defined language file - Markdown
    # for PYTHON file:
    #   getLanguageName = Python
    #   getLanguageDesc = Python file

