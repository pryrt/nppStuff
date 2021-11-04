'''
https://community.notepad-plus-plus.org/topic/12576/list-of-all-assigned-keyboard-shortcuts/18
By @Ekopalypse

(imported after re-mentioned in https://community.notepad-plus-plus.org/topic/21213/)
'''
import ctypes
import ctypes.wintypes as wintypes
from threading import Thread
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

def start_sk_dialog():
    notepad.menuCommand(MENUCOMMAND.SETTING_SHORTCUT_MAPPER)


sk_mapper = Thread(target=start_sk_dialog)
sk_mapper.start()
time.sleep(1)

WM_USER = 1024
WM_CLOSE = 16

TCM_FIRST = 4864
TCM_GETITEMCOUNT = (TCM_FIRST + 4)
TCM_SETCURSEL = (TCM_FIRST + 12)

BABYGRID_USER = (WM_USER + 7000)
BGM_GETCELLDATA  = BABYGRID_USER + 4
BGM_GETROWS  = BABYGRID_USER + 23

class BGCELL(ctypes.Structure):
    _fields_ = [('row', wintypes.INT),
                ('col', wintypes.INT)]

cell_buffer = ctypes.create_unicode_buffer(1000)

bgcell = BGCELL()

sk_mapper_hwnd = user32.FindWindowW(None, u'Shortcut mapper')
sys_tab_hwnd = user32.FindWindowExW(sk_mapper_hwnd, None, u'SysTabControl32',None)
item_count = user32.SendMessageW(sys_tab_hwnd, TCM_GETITEMCOUNT, 0, 0)
babygrid = user32.FindWindowExW(sk_mapper_hwnd, None, u'BABYGRID',None)

shortcuts = []
for tab in range(item_count):
    rows = user32.SendMessageW(babygrid, BGM_GETROWS, 0, 0)
    print 'rows', rows

    for i in range(1, rows+1):
        shortcut = []
        for j in range(1,3):
            bgcell.row = i
            bgcell.col = j
            res = user32.SendMessageW(babygrid,
                              BGM_GETCELLDATA,
                              ctypes.byref(bgcell),
                              cell_buffer)
            shortcut.append(cell_buffer.value)
        shortcuts.append(shortcut)

    user32.SetForegroundWindow(sk_mapper_hwnd)
    user32.SendMessageW(sys_tab_hwnd, TCM_SETCURSEL, tab, 0)
    user32.keybd_event(0x27,0,0,0)
    user32.keybd_event(0x27,0,2,0)
    time.sleep(.1) # suggested on Aug 15, 2019

user32.SendMessageW(sk_mapper_hwnd, WM_CLOSE, 0, 0)

_max_length = len(max([x[0] for x in shortcuts if x[1]], key=len))
notepad.new()
editor.setText('\r\n'.join(['{0:<{2}} : {1}'.format(x[0], x[1], _max_length) for x in shortcuts if x[1]]))
