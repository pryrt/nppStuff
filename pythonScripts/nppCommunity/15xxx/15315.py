# remove duplicate lines (assumes lines already sorted, so only compares to previous line)

console.clear()
console.show()

prev = "should not match previous"
lineNumber = 0

while lineNumber < editor.getLineCount():
    editor.gotoLine(lineNumber)
    contents = editor.getLine(lineNumber)

    console.write( "#" + str(lineNumber) + "/" + str(editor.getLineCount()) )
    console.write( "#[" + str(len(contents)) + "]\t" + contents)

    if contents == prev:
        console.write( "\tdeleting\n" )
        editor.deleteLine(lineNumber)
    else:
        console.write( "\tno match\n" )
        lineNumber = lineNumber + 1

    prev = contents

# line 1
# this matches
# this matches
# line 3
