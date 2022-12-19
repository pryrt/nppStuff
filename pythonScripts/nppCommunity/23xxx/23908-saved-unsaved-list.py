# encoding=utf-8
"""quoted from Alan Kilborn: https://community.notepad-plus-plus.org/topic/23908/"""
from Npp import editor,notepad,console

if 1:
    import os
    for (pathname, buffer_id, index, view) in notepad.getFiles():
        notepad.activateFile(pathname)
        state = 'unsaved' if editor.getModify() else 'saved'
        print('on startup, activating a {st} "{fn}"'.format(st=state, fn=pathname.rsplit(os.sep, 1)[-1]))
