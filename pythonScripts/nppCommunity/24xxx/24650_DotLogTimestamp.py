# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24650/

- Call this from startup.py using
import DotLogTimestamp
_DLTS = DotLogTimestamp.DLTS()

- Make sure to set Plugins > PythonScript > Configuration > Initialisation to "ATSTARTUP" instead of "LAZY"

- installation instructions: see
    https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript

"""
from Npp import editor,notepad,console,NOTIFICATION
from datetime import datetime

class DLTS(object):
    def __init__(self):
        console.write("Registered DotLogTimestamp.py callbacks\n")
        notepad.callback(self.fileopened_callback, [NOTIFICATION.FILEOPENED])
        notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])
        self.active = True
        self.bufferIDs = []

    def toggle(self):
        self.active = not self.active
        console.write("DotLogTimestamp.py callbacks are {}\n".format('active' if self.active else 'inactive'))

    def fileopened_callback(self, args):
        if self.active:
            self.bufferIDs.append(args['bufferID'])

    def bufferactivated_callback(self, args):
        if self.active:
            if args['bufferID'] in self.bufferIDs:
                line = editor.getLine(0).strip()
                if line[0:4] == ".LOG":
                    editor.appendText("{}\n".format(datetime.now().strftime("%Y-%b-%d %H:%M:%S")))
                self.bufferIDs.remove(args['bufferID'])

if __name__ == '__main__':
    try:
        _DLTS.toggle()
    except NameError:
        _DLTS = DLTS()
