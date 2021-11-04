# encoding=utf-8
"""in response to https://superuser.com/questions/1412875"""
from Npp import *

def su1412882_OnOpen_callback(kwargs):
    """this is the function that will be called when a new file is opened"""
    notepad.activateBufferID(kwargs['bufferID'])
    notepad.closeAllButCurrent()

def register_OnOpen_callback():
    """Registers the OnOpen callback"""
    unregister_OnOpen_callback()    # starts by making sure there are none registered
    notepad.callback(su1412882_OnOpen_callback, [NOTIFICATION.FILEOPENED])

def unregister_OnOpen_callback():
    """Unregisters the OnOpen callback - used to make sure that running the script twice doesn't register two instances of the same callback"""
    notepad.clearCallbacks(su1412882_OnOpen_callback)

if __name__ == '__main__': register_OnOpen_callback()