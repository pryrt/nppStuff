from Npp import notepad, console, NOTIFICATION
notepad.callback(lambda x: console.write('FILEBEFORELOAD: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFORELOAD])
notepad.callback(lambda x: console.write('FILEBEFOREOPEN: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFOREOPEN])
notepad.callback(lambda x: console.write('FILEOPENED: {}\r\n'.format(x)),[NOTIFICATION.FILEOPENED])
notepad.callback(lambda x: console.write('BUFFERACTIVATED: {}\r\n'.format(x)),[NOTIFICATION.BUFFERACTIVATED])
notepad.callback(lambda x: console.write('FILEBEFORECLOSE: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFORECLOSE])
notepad.callback(lambda x: console.write('FILECLOSED: {}\r\n'.format(x)),[NOTIFICATION.FILECLOSED])
'''
"""https://community.notepad-plus-plus.org/topic/20795"""
from Npp import editor, SCINTILLANOTIFICATION

def on_modified(args):
    if DO_ON_MODIFIED:
        if editor.getModify():
            console.write("Do something\n")
        else:
            console.write("Not modified\n")
    else:
        console.write("Do nothing.\n")

#try:
#    DO_ON_MODIFIED = not DO_ON_MODIFIED
#except NameError:
#    editor.callbackSync(on_char_added, [SCINTILLANOTIFICATION.CHARADDED])
#    DO_ON_MODIFIED = True

DO_ON_MODIFIED = True
on_modified('x')

def do_on_load(args):
    console.write("on_load({})\n".format((args)))

notepad.callback(do_on_load, [NOTIFICATION.FILEBEFORELOAD])

'''
