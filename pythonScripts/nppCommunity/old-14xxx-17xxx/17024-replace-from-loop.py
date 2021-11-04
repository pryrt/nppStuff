# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/17024/

This will take the next item from a list (er, immutable tuple, really)

This is based on the `editor.replace()` example in pythonscript docs.
"""
from Npp import *
import re

counter = 0
search_for_string = 'text0'
loopy_replacements = ('iteration1', 'other text', '3rd text chain')

def forum_post17024_select_replacement(m):
    """this will select the next item from the loopy_replacements"""
    global counter
    global loopy_replacements
    l = len(loopy_replacements)

    chosen = loopy_replacements[counter % l]
    counter = counter + 1

    return chosen

editor.replace( search_for_string , forum_post17024_select_replacement , re.IGNORECASE )
#editor.replace( 'text0' , get_counter , re.IGNORECASE )