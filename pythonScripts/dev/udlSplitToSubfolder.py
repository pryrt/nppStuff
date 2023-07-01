# encoding=utf-8
"""
eventually, this will want to read the "common UDL" file <configDir>\userDefineLang.xml ,
and if there are any, split those out into `<configDir>\userDefineLangs\` folder.

Make use of a NOTIFICATION.shutdown, and maybe spawn a background process to do the action
"""
from Npp import notepad, NOTIFICATION
import os, subprocess

# notepad.callback(my_callback. [NOTIFICATION.SHUTDOWN])

class udlSplitToSubfolder():
    TEMPDIR = os.environ['TEMP']    # I originally thought I might need to create and run %TEMP%\blah.bat,
                                    # but maybe not
    def __init__(self):
        notepad.callback(self.example_background_process, [NOTIFICATION.SHUTDOWN])
        console.write("registered\n")
        console.show()

    def example_background_process(self, args):
        #https://stackoverflow.com/questions/1196074/how-to-start-a-background-process-in-python
        #notepad.messageBox(str(args), "title")
        subprocess.Popen(['cmd', '/c', 'echo', 'hello', '&', 'pause']) # shows multi-command as well

if __name__ == '__main__':
    udlSplitToSubfolder()
