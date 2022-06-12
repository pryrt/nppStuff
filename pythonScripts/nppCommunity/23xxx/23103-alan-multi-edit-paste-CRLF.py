# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------

class MSCAD(object):

    def __init__(self):
        preferred_delimiter = '\r\n'
        if editor.getSelections() == 1 or editor.selectionIsRectangle(): return  # not our purview
        sel_text_list = []
        for n in range(editor.getSelections()):
            (s, e) = (editor.getSelectionNStart(n), editor.getSelectionNEnd(n))
            t = editor.getTextRange(s, e)
            sel_text_list.append(t)
        editor.copyText(preferred_delimiter.join(sel_text_list) + '\r\n')

#-------------------------------------------------------------------------------

if __name__ == '__main__': MSCAD()
