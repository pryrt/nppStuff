# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/22919/

this is an example of registering a NOTIFICATION.SHUTDOWN callback
    the example just writes to c:\temp\onShutdown.txt with the date/time
    and the arguments passed
"""
from Npp import *
from datetime import datetime

def myOnShutdown_22919(kwargs):
    with open("c:\\temp\\onShutdown.txt", 'a') as f:
        f.write("{}\tshutdown args: {}\n".format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'), ', '.join(["{}=>{}".format(k,kwargs[k]) for k in kwargs])))
        pass

notepad.callback(myOnShutdown_22919, [NOTIFICATION.SHUTDOWN])
console.write("registered [NOTIFICATION.SHUTDOWN] = myOnShutdown_22919\n")
with open("c:\\temp\\onShutdown.txt", 'a') as f:
    f.write("{}\tregistered myOnShutdown_22919\n".format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S')))
