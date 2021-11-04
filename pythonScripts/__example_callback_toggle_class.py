"""explore registering instance method as callback"""

from Npp import *

class DummyClass:
    def __init__(self):
        """Constructor"""
        self._is_registered = False
        console.write("Initializing self = {}\n".format(self))

    def __del__(self):
        """Destructor -- not called as often as I would hope"""
        self.reset()
        console.write("True Destructor! {}\n".format(self))

    def reset(self):
        console.write("Resetting self = {}\n".format(self))
        self.toggle_callback(False)
        del(self)

    def onSave_callback(self, kwargs):
        console.write("self={}, kwargs={}\n".format(self, kwargs))

    def toggle_callback(self, flag=False):
        console.write("notepad.clearCallbacks(...)\n")
        #        notepad.clearCallbacks(self.onSave_callback)
        #        notepad.clearCallbacks([NOTIFICATION.FILEBEFORESAVE])
        notepad.clearCallbacks(self.onSave_callback, [NOTIFICATION.FILEBEFORESAVE])
        if flag or not self._is_registered:
            console.write("notepad.callback(...) registered\n")
            notepad.callback(self.onSave_callback, [NOTIFICATION.FILEBEFORESAVE])
        self._is_registered = not self._is_registered

def simple_callback(kwargs):
    console.write("simple kwargs={}".format(kwargs))

global SINGLETON

def _delete_singleton():
    global SINGLETON
    notepad.clear_callbacks()
    del(SINGLETON)

if __name__ == '__main__':
    try:
        SINGLETON
    except NameError:
        SINGLETON = DummyClass()

    SINGLETON.toggle_callback()


