# -*- coding: utf-8 -*-
'''
https://community.notepad-plus-plus.org/post/65373
'''

from Npp import editor, SCINTILLANOTIFICATION, MODIFICATIONFLAGS

MARK_BOOKMARK = 24  # from N++ source code

def callback_sci_MODIFIED(args):
    if args['modificationType'] & MODIFICATIONFLAGS.CHANGEMARKER:
        line = editor.lineFromPosition(args['position'])
        if editor.markerGet(line) & (1 << MARK_BOOKMARK):
            print('bookmark placed on line {}'.format(line + 1))
        else:
            print('bookmark removed on line {}'.format(line + 1))
editor.callback(callback_sci_MODIFIED, [SCINTILLANOTIFICATION.MODIFIED])
