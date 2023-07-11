# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://community.notepad-plus-plus.org/topic/24687
# author: @Alan-Kilborn

from Npp import *

output_line_list = []
for obj_str in [ 'editor', 'notepad' ]:
    for item in dir(eval(obj_str)):
        obj_plus_item_str = obj_str + '.' + item
        if not item.startswith('_') and 'bound method' in str(eval(obj_plus_item_str)):
            output_line_list.append(obj_plus_item_str)
notepad.new()
eol = [ '\r\n', '\n', '\r' ][ editor.getEOLMode() ]
editor.appendText(eol.join(output_line_list))
