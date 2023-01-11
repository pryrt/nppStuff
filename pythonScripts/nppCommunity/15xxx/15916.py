# https://notepad-plus-plus.org/community/topic/15916/plugin-to-perform-proprietary-decryption-and-encryption-during-open-and-save/5
from Npp import notepad, console, NOTIFICATION
notepad.callback(lambda x: console.write('FILEBEFORELOAD: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFORELOAD])
notepad.callback(lambda x: console.write('FILEBEFOREOPEN: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFOREOPEN])
notepad.callback(lambda x: console.write('FILEOPENED: {}\r\n'.format(x)),[NOTIFICATION.FILEOPENED])
notepad.callback(lambda x: console.write('BUFFERACTIVATED: {}\r\n'.format(x)),[NOTIFICATION.BUFFERACTIVATED])
notepad.callback(lambda x: console.write('FILEBEFORESAVE: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFORESAVE])
notepad.callback(lambda x: console.write('FILEBEFORECLOSE: {}\r\n'.format(x)),[NOTIFICATION.FILEBEFORECLOSE])
notepad.callback(lambda x: console.write('FILECLOSED: {}\r\n'.format(x)),[NOTIFICATION.FILECLOSED])
# editor.callback
# https://docs.python.org/2/tutorial/controlflow.html#lambda-expressions -- single line anonymous subroutines