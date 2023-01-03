# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://community.notepad-plus-plus.org/topic/23929 "Show only lines that contain a search term"
#  https://community.notepad-plus-plus.org/topic/20058 (see Dec 17, 2022 9:50AM posting)

from Npp import *
import inspect
import os
from ctypes import (WinDLL)

#-------------------------------------------------------------------------------

# N++'s redmarking indicator number:
SCE_UNIVERSAL_FOUND_STYLE = 31  # see https://github.com/notepad-plus-plus/notepad-plus-plus/search?q=SCE_UNIVERSAL_FOUND_STYLE

#-------------------------------------------------------------------------------

def editor_getWordAtCaretOrSelection():
    retval = ''
    (sel_start, sel_end) = (editor.getSelectionStart(), editor.getSelectionEnd())
    if editor.getSelections() == 1 and sel_start != sel_end:
        retval = editor.getTextRange(sel_start, sel_end)
    else:
        start_of_word_pos = editor.wordStartPosition(editor.getCurrentPos(), True)
        end_of_word_pos = editor.wordEndPosition(start_of_word_pos, True)
        if start_of_word_pos != end_of_word_pos:
            retval = editor.getTextRange(start_of_word_pos, end_of_word_pos)
            editor.setSelection(end_of_word_pos, start_of_word_pos)
    return retval

#-------------------------------------------------------------------------------

class LFVH1(object):

    def __init__(self):

        self.debug = True if 1 else False
        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]

        self.settings_by_viewfile_dict = {}

        LINE_NUMBER_MARGIN_DEFAULT_BACKGROUND_RGB = editor.styleGetBack(STYLESCOMMON.LINENUMBER)
        self.UNFILTERED_BACKGROUND_RGB = LINE_NUMBER_MARGIN_DEFAULT_BACKGROUND_RGB
        self.FILTERED_BACKGROUND_RGB = (255, 192, 203)  # pinkish margin color to indicate not all lines shown due to filtering

        # initialize for currently active tab when invoked for the first time
        view_plus_file = str(notepad.getCurrentView()) + notepad.getCurrentFilename()
        self.dprint('view_plus_file:', view_plus_file)
        if view_plus_file not in self.settings_by_viewfile_dict:
            self.reset_settings_for_active_tab(view_plus_file)

        notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])
        editor.callback(self.updateui_callback, [SCINTILLANOTIFICATION.UPDATEUI])

    def prompt_for_string_to_match(self):

        view_plus_file = str(notepad.getCurrentView()) + notepad.getCurrentFilename()
        self.dprint('view_plus_file:', view_plus_file)
        if view_plus_file not in self.settings_by_viewfile_dict:
            self.reset_settings_for_active_tab(view_plus_file)

        # determine what default text to put in the user prompt box:
        user_input = self.settings_by_viewfile_dict[view_plus_file]['previous_user_input']
        if editor.getSelectionEmpty():
            __ = editor_getWordAtCaretOrSelection()
            if len(__) > 0: user_input = __
        else:
            rect_sel_mode = editor.getSelectionMode() in [ SELECTIONMODE.RECTANGLE, SELECTIONMODE.THIN ]
            multi_sel_mode = editor.getSelections() > 1
            if not rect_sel_mode and not multi_sel_mode:
                stream_sel_contents = editor.getSelText()
                if '\r' not in stream_sel_contents and '\n' not in stream_sel_contents:
                    # we only want selected text if it is all one one line
                    user_input = stream_sel_contents

        prompt_str = '\r\n'.join([
            '          (Hold Shift while answering or leave box empty to restore showing of all lines)',
            'ENTER LITERAL SEARCH STRING to show only those lines that contain the string',
        ])
        user_input = self.prompt(prompt_str, user_input)
        restore_all_lines_to_shown = self.shift_held()
        if restore_all_lines_to_shown: user_input = ''
        if user_input is None: return  # user cancel

        if len(user_input) == 0:
            if len(self.settings_by_viewfile_dict[view_plus_file]['show_lines_tup_list']) > 0:
                # we currently have some hidden lines
                if restore_all_lines_to_shown or self.yes_no('Are you sure you want to show ALL lines?'):
                    self.settings_by_viewfile_dict[view_plus_file]['show_lines_tup_list'] = []  # empty list means to show all lines
                    self.freshen_user_view_of_active_tab()
            return

        # find the list of lines that should be shown:
        L = []
        editor.search(user_input, lambda m: L.append(m.span(0)))
        self.dprint('L:', L)

        if len(L) == 0:
            __ = user_input[:20]
            if __ != user_input: __ += '...'
            msg = '\r\n\r\n'.join([
                'No matches for "{}"'.format(__),
                'Leaving previously displayed lines unchanged.',
            ])
            self.mb(msg)
            return

        # remember current values:
        self.settings_by_viewfile_dict[view_plus_file]['show_lines_tup_list'] = L
        self.settings_by_viewfile_dict[view_plus_file]['previous_user_input'] = user_input

        self.freshen_user_view_of_active_tab()

    def bufferactivated_callback(self, args):

        self.dprint('BUFFERACTIVATED:', args)

        view_plus_file = str(notepad.getCurrentView()) + notepad.getCurrentFilename()
        self.dprint('view_plus_file:', view_plus_file)
        if view_plus_file not in self.settings_by_viewfile_dict:
            self.reset_settings_for_active_tab(view_plus_file)

        # refresh the hidden/shown state of the lines, because N++ will revert
        #  our previously hidden lines to shown when a tab is activated
        self.freshen_user_view_of_active_tab()

    def updateui_callback(self, args):

        # this is mainly for when user renames a file, or does a save-as;
        #  it might be our quickest route to detection of that

        #self.dprint('UPDATEUI:', args)  # would fire too often!

        view_plus_file = str(notepad.getCurrentView()) + notepad.getCurrentFilename()
        #self.dprint('view_plus_file:', view_plus_file)

        if view_plus_file not in self.settings_by_viewfile_dict:

            # the current tab is seen as never having been encountered before (from a rename or a save-as, e.g.)
            self.reset_settings_for_active_tab(view_plus_file)

            # only update when absolutely necessary, as UPDATEUI callback happens a lot!
            self.freshen_user_view_of_active_tab()

    def freshen_user_view_of_active_tab(self):

        view_plus_file = str(notepad.getCurrentView()) + notepad.getCurrentFilename()
        if view_plus_file not in self.settings_by_viewfile_dict:
            self.reset_settings_for_active_tab(view_plus_file)

        L = self.settings_by_viewfile_dict[view_plus_file]['show_lines_tup_list']

        show_all_not_hide_some = len(L) == 0

        editor.foldAll(FOLDACTION.EXPAND)

        editor.setIndicatorCurrent(SCE_UNIVERSAL_FOUND_STYLE)
        editor.indicatorClearRange(0, editor.getLength())

        if show_all_not_hide_some:

            self.show_all_lines()

            # set the background of the line number margin to normal
            #  to indicate that all lines are shown
            editor.styleSetBack(STYLESCOMMON.LINENUMBER, self.UNFILTERED_BACKGROUND_RGB)

        else:

            line_of_caret = editor.lineFromPosition(editor.getCurrentPos())

            # hide all lines first:
            self.show_all_lines(False)
            # show only lines with hits from the search based on user criterion:
            for (pos_start, pos_end) in L:
                editor.setIndicatorCurrent(SCE_UNIVERSAL_FOUND_STYLE)
                editor.indicatorFillRange(pos_start, pos_end - pos_start)
                line_start = editor.lineFromPosition(pos_start)
                line_end = editor.lineFromPosition(pos_end)
                editor.showLines(line_start, line_end)

            # make sure caret is not within a now-hidden region of lines:
            if not editor.getLineVisible(line_of_caret):
                # caret needs to be moved
                moved_caret = False
                # see if caret can be moved below its current position
                for new_loc in range(line_of_caret, editor.getLineCount()):
                    if editor.getLineVisible(new_loc):
                        editor.setEmptySelection(editor.positionFromLine(new_loc))
                        editor.chooseCaretX()
                        moved_caret = True
                        break
                if not moved_caret:
                    # see if caret can be moved above its current position
                    for new_loc in range(line_of_caret - 1, 0, -1):
                        if editor.getLineVisible(new_loc):
                            editor.setEmptySelection(editor.positionFromLine(new_loc))
                            editor.chooseCaretX()
                            moved_caret = True
                            break
                if not moved_caret:
                    # user line 1 is always shown, so punt and put caret there
                    editor.setEmptySelection(0)
                    editor.chooseCaretX()

            # set the background of the line number margin to a special color
            #  to indicate that some lines are not shown
            editor.styleSetBack(STYLESCOMMON.LINENUMBER, self.FILTERED_BACKGROUND_RGB)

    def reset_settings_for_active_tab(self, view_plus_file):
        if view_plus_file not in self.settings_by_viewfile_dict:
            self.settings_by_viewfile_dict[view_plus_file] = {
                'show_lines_tup_list' : [],  # empty list means to show all lines
                'previous_user_input' : '',
            }

    def show_all_lines(self, show_not_hide=True):
        f = editor.showLines if show_not_hide else editor.hideLines
        f(1, editor.getLineCount() - 1)  # can't hide user line 1 (Scintilla restriction)

    def shift_held(self):
        VK_SHIFT = 0x10
        user32 = WinDLL('user32')
        return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0

    def print(self, *args, **kwargs):
        try:
            self.print_first
        except AttributeError:
            self.print_first = True
        if self.print_first:
            console.show()      # this will put input focus in the PS console window, at the >>> prompt
            #console.clear()
            editor.grabFocus()  # put input focus back into the editor window
            self.print_first = False
        d_tag = '<DBG>' if 'debug' in kwargs else ''
        if 'debug' in kwargs: del kwargs['debug']
        print(self.__class__.__name__ + d_tag + ':', *args, **kwargs)

    def dprint(self, *args, **kwargs):  # debug print function
        if self.debug:
            kwargs['debug'] = True
            self.print(*args, **kwargs)

    def mb(self, msg, flags=0, title=''):  # a message-box function
        return notepad.messageBox(msg, title if title else self.this_script_name, flags)

    def yes_no(self, question_text):  # returns True(Yes), False(No)
        answer = self.mb(question_text, MESSAGEBOXFLAGS.YESNO, self.this_script_name)
        return True if answer == MESSAGEBOXFLAGS.RESULTYES else False

    def prompt(self, prompt_text, default_text=''):
        if '\n' not in prompt_text: prompt_text = '\r\n' + prompt_text
        prompt_text += ':'
        return notepad.prompt(prompt_text, self.this_script_name, default_text)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        LINE_FILTER_VIA_HIDING1
    except NameError:
        LINE_FILTER_VIA_HIDING1 = LFVH1()
    LINE_FILTER_VIA_HIDING1.prompt_for_string_to_match()
