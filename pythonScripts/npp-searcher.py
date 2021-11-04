# editor1 is the PythonScript object instance for the first (left or top) document window in NPP
# editor2 is the instance for the second (right or bottom) document window

# Python's range(start, stop) operator will keep going while the index variable is LESS THAN stop, so it will never use stop: https://docs.python.org/2/library/functions.html#range
for lineNumber in range(0, editor1.getLineCount() ):
    # grab the nth line from File1 (exclude newline)
    editor1.gotoLine(lineNumber)
    newValue = editor1.getCurLine().rstrip()
    console.write("editor1: #" + str(lineNumber) + " = \"" + newValue + "\"\n")

    editor2.documentEnd()               # go to the last position
    end2 = editor2.getCurrentPos()      # record the position
    console.write("editor2.end = " + str(end2)+"\n")
    editor2.documentStart()             # back to the beginning
    start2 = editor2.getCurrentPos()    # record the position
    console.write("editor2.start = " + str(start2)+"\n")

    # want to replace two "xxx" entries in File2 with each line from File1
    for time in range(0, 2):
        console.write("time# " + str(time) + "!!!\n")

        # look for the first occurrence of 'xxx', starting at start2 and ending at end2
        #  position is a tuple with the start and end locations of the match
        position = editor2.findText( FINDOPTION.MATCHCASE, start2, end2, "xxx")
        if position is None:
            console.write("editor2.position is NONE, so skipping...\n")
            break                   # don't try to replace

        console.write("editor2: findText @ " + str(position[0]) + ":" + str(position[1]) + "\n")

        # select the "xxx"
        editor2.setSelectionStart(position[0])
        editor2.setSelectionEnd(position[1])

        # replace the selection with newValue
        editor2.replaceSel(newValue)

        # the cursor is now at the end of the replaced value, and we want to
        start2 = editor2.getCurrentPos()
        console.write("Start2: " + str(start2)+"\n")

    console.write("next source line...\n")