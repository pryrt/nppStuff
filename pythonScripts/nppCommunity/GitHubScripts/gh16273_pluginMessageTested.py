# encoding=utf-8
from Npp import notepad, console, NOTIFICATION
import ctypes

def myFunction(args):
    code = args['code'] if 'code' in args else None
    idFrom = args['idFrom'] if 'idFrom' in args else None
    hwndFrom = args['hwndFrom'] if 'hwndFrom' in args else None
    console.write("notification(code:{}, idFrom:{}, hwndFrom:{}) received\n".format(code, idFrom, hwndFrom))
    if code==NOTIFICATION.CMDLINEPLUGINMSG:
        if idFrom is None: return
        str = ctypes.wstring_at(idFrom)
        console.write("\tAdditional Info: str=\"{}\"\n".format(str))

notepad.callback(myFunction, [NOTIFICATION.CMDLINEPLUGINMSG])
