# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26689/

Example processing of NPPN_CMDLINEPLUGINMSG notification
"""
from Npp import notepad, console, NOTIFICATION
import ctypes
import sys

def usePluginMessageString(s):
    console.write(f"TODO: do something more interesting with -pluginMessage=\"{s}\"\n")

def getStringFromNotification(args):
    code = args['code'] if 'code' in args else None
    idFrom = args['idFrom'] if 'idFrom' in args else None
    hwndFrom = args['hwndFrom'] if 'hwndFrom' in args else None
    #console.write(f"notification(code:{code}, idFrom:{idFrom}, hwndFrom:{hwndFrom}) received\n")
    if idFrom is None: return
    s = ctypes.wstring_at(idFrom)
    #console.write(f"\tAdditional Info: str=\"{s}\"\n")
    usePluginMessageString(s)

def getStringFromCommandLine():
    for token in sys.argv:
        if len(token)>15 and token[0:15]=="-pluginMessage=":
            s = token[15:]
            #console.write(f"TODO: process {token} => \"{s}\"\n")
            usePluginMessageString(s)

notepad.callback(getStringFromNotification, [NOTIFICATION.CMDLINEPLUGINMSG])
console.write("Registered getStringFromNotification callback for CMDLINEPLUGINMSG\n")
getStringFromCommandLine()
