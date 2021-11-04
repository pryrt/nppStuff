# encoding=utf-8
"""in response to https://superuser.com/questions/1395356/open-a-session-file-and-show-the-last-document-lines-at-the-top-of-the-window"""
from Npp import *

def su1395356_ScrollToEnd_Callback(args):
    """this will scroll to the end of the current file"""
    b = args['bufferID']
    notepad.activateBufferID(b)
    #editor.documentEnd()
    #console.write("scroll to end: {} => '{}'\n".format(b, notepad.getBufferFilename(b)))
    su1395356_AlternateScrollToLastNLines()

def su1395356_EndCallback():
    notepad.clearCallbacks(su1395356_ScrollToEnd_Callback)
    console.write("cleared callbacks end\n")

def su1395356_AlternateScrollToLastNLines():
    """will scroll the last n, assuming **Settings | Preferences | Editing | Enable scrolling beyond last line** enabled"""
    n = 16
    editor.scrollToEnd()
    for i in range(n-1):        # use n-1 because one row is already visible
        editor.lineScrollUp()

if __name__ == '__main__':
    console.show()
    console.clear()
    su1395356_EndCallback()
    notepad.callback(su1395356_ScrollToEnd_Callback, [NOTIFICATION.FILEOPENED])
    console.write("done initializing callbacks\n")


"""
If you have [PythonScript](https://github.com/bruderstein/PythonScript/), you can run the following script:

<!-- language: lang-py -->

    ...

Every file you open should go to the end of the buffer when you open it.

To stop this callback, **Plugins > PythonScript > Show Console**, then run `su1395356_EndCallback()` from the immediate-line.

If you restart NPP, the callback won't be active any more, so you'll need to run the script again.  Or, you might want to import this script from your `startup.py`, with **Plugins > Python Script > Configuration...** setting "Initialisation" to "ATSTARTUP", which will make it automatically start

If you don't have it in `startup.py`, you might want to use the **Configuration...** dialog to add it to the **Menu Items** list; once that's done and NPP is restarted, you can use **Settings > Shortcut Mapper** to assign a keyboard shortcut.
"""