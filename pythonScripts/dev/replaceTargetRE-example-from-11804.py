# encoding=utf-8
""" https://community.notepad-plus-plus.org/topic/19217/working-use-case-for-sci_replacetargetre

I am working on implementing editor.replaceTargetRE in Win32::Mechanize::NotepadPlusPlus::Editor,
but it's currently not working.

Found https://notepad-plus-plus.org/community/topic/11804/ with LuaScript/PythonScript examples that _should_ work
"""
from Npp import *
from time import sleep

console.show()
#console.clear()

tWait = 0.007
N = 10
right = 0
srctxt = """This is a not selected line !!!
This is line one !!!
Today is a beautiful day !!!
This is line three !!!
This is a not selected line !!!
"""
cmptxt = """This is a not selected line !!!
This is line one !!!
Today is a great day !!!
This is line three !!!
This is a not selected line !!!
"""

for x in range(N):
    notepad.new()
    editor.setText(srctxt)
    sleep(tWait)

    editor.setTargetRange(32,105)

    editor.setSearchFlags(FINDOPTION.REGEXP)
    editor.searchInTarget(r'beautiful')

    editor.replaceTargetRE('great')

    if editor.getText() == cmptxt:
        right = right + 1

    editor.setSavePoint()
    notepad.close()

console.write("Final Score: tWait={} gave {}/{} right!\n".format(tWait,right,N))

def my_indent(text, indentation):
    retval = '';
    return ''.join(indentation+line for line in text.splitlines(True))

# debug print version
if True:
    notepad.new()
    editor.setText(srctxt)
    sleep(0.5)

    # set and verify the initial range
    editor.setTargetRange(32,105)
    console.writeError( "range = ({},{})\n".format( editor.getTargetStart(), editor.getTargetEnd() ) )
    console.writeError( "{}\n".format( my_indent( editor.getTargetText(), "\t") ) )

    # set the option
    editor.setSearchFlags(FINDOPTION.REGEXP)
    console.writeError( "SCFIND_REGEXP = 0x{:08x}\n".format(FINDOPTION.REGEXP) )
    console.writeError( "getSearchFlags() = '0x{:08x}'\n".format(editor.getSearchFlags()) )

    # do the search and check retval
    searchret = editor.searchInTarget('beautiful')
    console.writeError( "searchInTarget('beautiful')={}\n".format(searchret))
    # here, perl returned 32, but pythonscript returns 64

    # do the replacement
    editor.replaceTargetRE('great')
    console.writeError( "range = ({},{})\n".format( editor.getTargetStart(), editor.getTargetEnd() ) )
    console.writeError( "{}\n".format( my_indent( editor.getTargetText(), "\t") ) )

    # get the final whole text
    got = editor.getText()
    console.writeError( "range = ({},{})\n".format( editor.getTargetStart(), editor.getTargetEnd() ) )
    console.writeError( "{}\n".format( my_indent( got, "\t") ) )


    sleep(2.5)
    editor.setSavePoint()
    notepad.close()
