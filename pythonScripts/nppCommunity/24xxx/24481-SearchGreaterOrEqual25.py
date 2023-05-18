# encoding=utf-8
"""https://community.notepad-plus-plus.org/post/86443

Bookmark any line that starts with an integer greater than
or equal to 25.

"""
from Npp import editor, notepad, MENUCOMMAND
import re  # to be able to use Python's regular expression library

def custom_match_func(m):
    i = int(m.group(0))
    if i >= 25:
        editor.setSel( m.start(0), m.end(0) )
        notepad.menuCommand(MENUCOMMAND.SEARCH_TOGGLE_BOOKMARK)
        # really should check bookmark status first, and have it
        # only toggle if it's not already bookmarked
        # but that goes beyond the scope of this FAQ

# notepad.menuCommand(MENUCOMMAND.SEARCH_CLEAR_BOOKMARKS) # optionally clear bookmarks before this search
editor.research(r'^\b\d+\b', custom_match_func)

"""
Here is example data to test it on:
1. Here
Here is 25
25 here         This line should match
Yep
99999 is OK     So should this one

"""
