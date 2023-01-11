# encoding=utf-8
""" https://notepad-plus-plus.org/community/topic/17005/
eko posted this code at 2019-01-25T20:30:52.026Z
"""
from Npp import *

def change_format(m):
    parts = m.group(0).split(':')
    min = int(parts[0])
    if min > 59:                # my fix
        real_minute = min % 60
        hours = min / 60
        return '{:02}:{:02}:{}'.format(hours, real_minute, parts[1])
    else:
        return '{}:{}'.format(*parts[:])

editor.rereplace('\d+:\d+\.\d+',change_format) # eko's
#editor.rereplace('(?<![:\d])\d+:\d+\.\d+',change_format) # mine


"""
1:00.000
11:11.111
22:22.222
33:33.333
40:00.000
50:00.000
60:00.000
70:00.000
80:00.000
90:00.000
100:00.000
129:00.000
1:15:00.000

And running a test with `1:15:00.000`, even with eko's simpler expression, works correctly (ie, doesn't try to change it) -- ahh, that's because the minutes are less than 60.
"""