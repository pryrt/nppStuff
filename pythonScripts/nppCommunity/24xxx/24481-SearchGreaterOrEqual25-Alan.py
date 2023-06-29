# encoding=utf-8
"""https://community.notepad-plus-plus.org/post/86443

@Alan-Kilborn's alternative
"""
from Npp import *

def custom_match_func(m):
    if custom_match_func.stop: return
    i = int(m.group(0))
    if i >= 25:
        editor.setSel( m.start(0), m.end(0) )
        custom_match_func.stop = True

custom_match_func.stop = False
editor.research(r'^\b\d+\b', custom_match_func, 0, editor.getCurrentPos())

"""
Here is example data to test it on:
1. Here
Here is 25
25 here         This line should match
Yep
99999 is OK     So should this one

"""
