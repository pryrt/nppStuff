# -*- coding: utf-8 -*-
"""
By: Alan Kilborn
https://community.notepad-plus-plus.org/post/71772

Edited: Peter added a way to stop the jiggling: add a boolean to the instance, and if
"""

from Npp import console
import ctypes
from ctypes import Structure, c_uint, sizeof, byref, POINTER, c_int
from ctypes.wintypes import DWORD, LONG
import threading
import time

ULONG_PTR = ctypes.POINTER(DWORD)

INPUT_MOUSE          = 0
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE     = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ('dx', LONG),
        ('dy', LONG),
        ('mouseData', DWORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ULONG_PTR)
        )

class _INPUTunion(ctypes.Union):
    _fields_ = (
        ('mi', MOUSEINPUT),
        )

def MouseInput(flags, x, y, data): return MOUSEINPUT(x, y, data, flags, 0, None)
def Input(structure): return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
def Mouse(flags, x=0, y=0, data=0): return Input(MouseInput(flags, x, y, data))

class INPUT(ctypes.Structure):
    _fields_ = (
        ('type', DWORD),
        ('union', _INPUTunion)
        )

def sendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

def sendMouseMoveDeltaXY(x, y):
    flags = MOUSEEVENTF_MOVE
    event = Mouse(flags, x, y, 0)
    return sendInput(event)

class MJD(object):

    def __init__(self):
        self.jiggling = True
        self.jiggle_thread = threading.Thread(target=self.jiggle_thread_function, args=(1,))
        self.jiggle_thread.daemon = True  # thread won't stop until parent ends
        self.jiggle_thread.start()

    def jiggle_thread_function(self, name):
        multiplier = 1
        while self.jiggling:
            sendMouseMoveDeltaXY(multiplier, multiplier)
            multiplier *= -1
            #console.write("jiggled\n")
            time.sleep(0.1)  # use this so we don't continuously use CPU time
            sendMouseMoveDeltaXY(multiplier, multiplier)
            multiplier *= -1
            #console.write("jiggled\n")
            time.sleep(15.0)  # use this so we don't continuously use CPU time

if __name__ == "__main__":
    try:
        mjd
        mjd.jiggling = False
        del mjd
        console.write("stopped the MouseJiggleDaemon\n")
    except NameError:
        mjd = MJD()
        console.write("starting MouseJiggleDaemon\n")
