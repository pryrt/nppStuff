from Npp import notepad, editor, NOTIFICATION

def callback_npp_FILEBEFORESAVE(args):
    # the editor.appendText will go to the _active_ buffer, whatever
    # file is currently being saved.  So to solve two birds with one
    # stone, save the active buffer ID, then switch to the buffer ID
    # for this instance of the callback -- now the editor has the
    # correct buffer active.
    oldActiveID = notepad.getCurrentBufferID()
    notepad.activateBufferID(args["bufferID"])

    line_ending = ['\r\n', '\r', '\n'][notepad.getFormatType()]
    doc_size = editor.getTextLength()
    if editor.getTextRange(doc_size - 1, doc_size) != line_ending[-1]:
        # fix Notepad++'s "broken" functionality and add a line-ending at end-of-file
        editor.appendText(line_ending)

    # now that you're done editing, go back to the originally-active buffer
    notepad.activateBufferID(oldActiveID)

notepad.callback(callback_npp_FILEBEFORESAVE, [NOTIFICATION.FILEBEFORESAVE])

"""
[thread](https://notepad-plus-plus.org/community/topic/16785/remove-duplicate-numerical-lines/19) anymore, I'll continue the conversation here...

To continue with the hijack-tangent of this thread... :-)

@Scott-Sumner said,
> If people are interested in this script and have ideas about solving that particular problem, I'm interested in hearing them.

My first idea was that you could track the previous bufferID, and make sure you always activate the previous one.  While trying to see if that would help, I noticed that with the exact script you had posted, if all open files were missing EOL, it would save all files, but only fix the EOL on the active file.

That gave me the flash for the solution: in the callback, store the currently-active bufferID, activate the buffer for the argument to the callback (ie, the file being saved), make the changes to the now-active file, then re-activate the originally-active buffer.  The script below seemed to do it for me:

    from Npp import notepad, editor, NOTIFICATION

    def callback_npp_FILEBEFORESAVE(args):
        # the editor.appendText will go to the _active_ buffer, whatever
        # file is currently being saved.  So to solve two birds with one
        # stone, save the active buffer ID, then switch to the buffer ID
        # for this instance of the callback -- now the editor has the
        # correct buffer active.
        oldActiveID = notepad.getCurrentBufferID()
        notepad.activateBufferID(args["bufferID"])

        line_ending = ['\r\n', '\r', '\n'][notepad.getFormatType()]
        doc_size = editor.getTextLength()
        if editor.getTextRange(doc_size - 1, doc_size) != line_ending[-1]:
            # fix Notepad++'s "broken" functionality and add a line-ending at end-of-file
            editor.appendText(line_ending)

        # now that you're done editing, go back to the originally-active buffer
        notepad.activateBufferID(oldActiveID)

    notepad.callback(callback_npp_FILEBEFORESAVE, [NOTIFICATION.FILEBEFORESAVE])

I tested this with three open files: two in one view, one in other view; I tried various combinations of which ones needed to be saved, and which ones were missing EOL, and which was active, and it seemed to always do what I intended, but it's possible that other combinations won't work.

"""
"""
OLD DEBUG VERSION
console.show()
console.clear()

def callback_npp_FILEBEFORESAVE(args):
    # peter's debug
    console.show()
    console.write("\r\n")
    console.write("active ID(" + str(notepad.getCurrentBufferID()) + ") => " + notepad.getCurrentFilename() + "\r\n")
    #for k,v in args.iteritems():
    #    console.write(str(k) + " => " + str(v) + "\r\n")
    console.write("save   ID(" + str(args["bufferID"]) + ") => " + notepad.getBufferFilename(args["bufferID"]) + "\r\n")
    # /peter's debug

    oldActiveID = notepad.getCurrentBufferID()
    notepad.activateBufferID(args["bufferID"])

    line_ending = ['\r\n', '\r', '\n'][notepad.getFormatType()]
    doc_size = editor.getTextLength()
    if editor.getTextRange(doc_size - 1, doc_size) != line_ending[-1]:
        # fix Notepad++'s "broken" functionality and add a line-ending at end-of-file
        console.write("edit   ID(" + str(args["bufferID"]) + ") => " + notepad.getBufferFilename(args["bufferID"]) + "\r\n")
        editor.appendText(line_ending)

    notepad.activateBufferID(oldActiveID)

notepad.clearCallbacks(callback_npp_FILEBEFORESAVE)
notepad.callback(callback_npp_FILEBEFORESAVE, [NOTIFICATION.FILEBEFORESAVE])
"""
