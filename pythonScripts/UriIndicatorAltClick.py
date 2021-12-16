# -*- coding: utf-8 -*-

from Npp import *
import os
import re

class UIAC(object):

    def __init__(self):
        self.URL_INDIC = 8  # URL_INDIC is used in N++ source code
        self.ALT_MODIFIER = 4
        self.backslash = '\\' ; self.two_backslashes = self.backslash * 2
        self.alt_held_at_click = False
        self.installed = False
        self.install()

    def install(self):
        if not self.installed:
            # https://www.scintilla.org/ScintillaDoc.html#SCN_INDICATORCLICK
            editor.callback(self.indicator_click_callback, [SCINTILLANOTIFICATION.INDICATORCLICK])
            # https://www.scintilla.org/ScintillaDoc.html#SCN_INDICATORRELEASE
            editor.callback(self.indicator_release_callback, [SCINTILLANOTIFICATION.INDICATORRELEASE])
            self.installed = True

    def uninstall(self):
        if self.installed:
            editor.clearCallbacks(self.indicator_click_callback)
            editor.clearCallbacks(self.indicator_release_callback)
            self.installed = False

    def is_installed(self):
        return self.installed

    def mb(self, msg, flags=0, title=''):
        return notepad.messageBox(msg, title, flags)

    def get_indicator_range(self, indic_number):
        # similar to ScintillaEditView::getIndicatorRange() in N++ source
        # https://github.com/notepad-plus-plus/notepad-plus-plus/blob/8f38707d33d869a5b8f5014dbb18619b166486a0/PowerEditor/src/ScitillaComponent/ScintillaEditView.h#L562
        curr_pos = editor.getCurrentPos()
        indic_mask = editor.indicatorAllOnFor(curr_pos)
        if (indic_mask & (1 << indic_number)) != 0:
            start_pos = editor.indicatorStart(indic_number, curr_pos)
            end_pos = editor.indicatorEnd(indic_number, curr_pos)
            if curr_pos >= start_pos and curr_pos <= end_pos:
                return (start_pos, end_pos)
        return (0, 0)

    def indicator_click_callback(self, args):
        # example: INDICATORCLICK: {'position': 12294, 'idFrom': 0, 'modifiers': 4, 'code': 2023, 'hwndFrom': 1577146}
        #print('UriIndicatorAltClick indicator click callback')
        self.alt_held_at_click = (args['modifiers'] & self.ALT_MODIFIER) != 0

    def indicator_release_callback(self, args):

        # example: INDICATORRELEASE: {'position': 12294, 'idFrom': 0, 'modifiers': 0, 'code': 2024, 'hwndFrom': 1577146}

        #print('UriIndicatorAltClick indicator release callback')

        if not self.alt_held_at_click: return
        self.alt_held_at_click = False

        (start_pos, end_pos) = self.get_indicator_range(self.URL_INDIC)
        if start_pos == end_pos:  return  # if click on indicator that is not URL_INDIC

        uri_text = editor.getTextRange(start_pos, end_pos)

        (uri_scheme, _, uri_path) = uri_text.partition(':')

        uri_path = uri_path.replace('%20', ' ').replace('%24', '$').replace('/', self.backslash)

        # check for optional syntax at end:   edit:....txt(L127,C12)
        goto_line = goto_col = 0
        m = re.search(r'\(L(-?\d+)(?:,C(\d+))?\)$', uri_path)
        if m:
            uri_path = uri_path[:-len(m.group())]
            goto_line = int(m.group(1))
            if m.group(2): goto_col = int(m.group(2))

        if not os.path.isfile(uri_path):
            # look for a relative path, relative to currently active document
            try:
                (valid_dir_of_active_doc, _) = notepad.getCurrentFilename().rsplit(os.sep, 1)
            except ValueError:
                # we started out in a "new 1" file, no path on that whatsoever
                self.mb('Cannot find file:\r\n\r\n{}'.format(uri_path))
                return
            test_path_in_active_doc_dir = valid_dir_of_active_doc + os.sep + uri_path
            if os.path.isfile(test_path_in_active_doc_dir):
                uri_path = test_path_in_active_doc_dir
            else:
                (test_dir, test_filename) = test_path_in_active_doc_dir.rsplit(os.sep, 1)
                if os.path.isdir(test_dir):
                    expanded_test_dir = os.path.abspath(test_dir)
                    if expanded_test_dir != test_dir:
                        self.mb('Cannot find file:\r\n\r\n{}\r\n\r\nLooked in this dir:\r\n\r\n{}'.format(test_filename, expanded_test_dir))
                        return
                self.mb('Cannot find file:\r\n\r\n{}'.format(uri_path))
                return

        notepad.open(uri_path)

        if goto_line != 0:
            if goto_line == -1: goto_line = editor.getLineCount()
            goto_line -= 1
            if goto_col != 0:
                goto_col_pos = editor.findColumn(goto_line, goto_col)
                editor.gotoPos(goto_col_pos)
            else:
                editor.gotoLine(goto_line)

if __name__ == '__main__':

    if 'uiac' not in globals():
        uiac = UIAC()  # will automatically "install" it
    else:
        # each running the script toggles install/uninstall:
        uiac.uninstall() if uiac.is_installed() else uiac.install()
        print('uiac installed?:', uiac.is_installed())
