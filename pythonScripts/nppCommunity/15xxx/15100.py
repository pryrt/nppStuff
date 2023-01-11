# https://notepad-plus-plus.org/community/topic/15100/regex-rounding-numbers
#   version 1

#console.clear()
#console.show()

editor.documentEnd()
end = editor.getCurrentPos()
start = 0
#console.write("start:{}\n".format(start))
#console.write("end:  {}\n".format(end))
#editor.documentStart()

while start < end:
    position = editor.findText( FINDOPTION.REGEXP , start , end , "-*\d+\.\d{4,}")    # find any that are at more than 3 digits after the decimal point

    # error handling
    if position is None:
        #console.writeError("editor.position is NONE => not found.\n")
        break

    # grab the matched text
    #console.write("editor: findText @ " + str(position[0]) + ":" + str(position[1]) + "\n")
    text = editor.getTextRange(position[0], position[1])
    #console.write(text + "\n")

    # round it=
    rounded = round( float(text) , 3 )
    text = "{:0.3f}".format(rounded)
    #console.write(text + "\n" )

    # replace it with rounded
    editor.setSel(position[0], position[1])
    editor.replaceSel(text)

    # next
    start = position[1]
    # 2020-Mar-06: for long-enough original values (like 16.14999999999), it
    #   would have likely skipped match on next line
    #   Change to getSelectionEnd instead
    start = editor.getSelectionEnd()

#console.writeError("DONE\n")