# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://community.notepad-plus-plus.org/topic/24053

from Npp import *
import inspect
import os
from datetime import datetime as dt
import re

#-------------------------------------------------------------------------------

class MM(object):

    demo_template_str = '''
Dear <CUSTOMER_TITLE> <CUSTOMER_LAST_NAME>,
We would like to invite you or a representative of <CUSTOMER_COMPANY> to join us at the Text Editor Users' Trade Show in Berlin.
If possible, we would like to meet you on <MEETING_TIME> in order to review our distribution agreement.
I'm looking forward for your reply, <CUSTOMER_FIRST_NAME>.
<WRITERS_NAME>,
<WRITERS_COMPANY>
---------------------------------------------------
'''.lstrip()

    demo_datatable_str = '''
<CUSTOMER_FIRST_NAME>|<CUSTOMER_LAST_NAME>|<CUSTOMER_TITLE>|<CUSTOMER_COMPANY>|<MEETING_TIME>|<WRITERS_NAME>|<WRITERS_COMPANY>
Michael|Smith|Mr.|XYZ, Inc.|21st of August at 3PM|Alan Kilborn|NPP Support Specialists, Inc.
Paula|Poundstone|Ms.|ABC, Inc.|22nd of August at 10AM|Peter Jones|NPP Support Specialists, Inc.
Shankar|Vedantam|M.|QED, LLC|23rd of August, 4PM|Terry Bradshaw|Broadcasters Unlimited
'''.lstrip()

    def __init__(self):

        self.debug = True if 1 else False
        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]
        self.this_script_path_without_ext = inspect.getframeinfo(inspect.currentframe()).filename.rsplit('.', 1)[0]

        run_demo = self.yes_no_cancel('Run demo mail-merge?\r\n\r\nNo = Let me get to my real data, NOW!')
        if run_demo is None: return

        if run_demo:

            notepad.new()
            eol = [ '\r\n', '\n', '\r' ][editor.getEOLMode()]
            editor.setText(self.demo_template_str.replace('\n', eol))
            editor.setSavePoint()
            template_tab_path = notepad.getCurrentFilename()
            notepad.new()
            datatable_tab_path = notepad.getCurrentFilename()
            editor.setText(self.demo_datatable_str.replace('\n', eol))
            editor.setSavePoint()

            self.expand_template_and_datatable_into_new_tab(template_tab_path, datatable_tab_path)

            return  # end after running the 'demo'

        for which in [ 'TEMPLATE', 'DATATABLE' ]:
            while True:
                tab_path = self.get_user_filetab_choice('Choose {w} filetab by putting an X in the brackets to its left'.format(w=which))
                if tab_path is None:
                    if self.yes_no('Could not detect your file choice or maybe you want to abort?\r\n\r\n'
                            'Select Yes to abort, No to try selecting a file again.'):
                        return  # abort
                    continue
                if which == 'TEMPLATE':
                    template_tab_path = tab_path
                else:
                    datatable_tab_path = tab_path
                    if template_tab_path == datatable_tab_path:
                        self.mb('You picked the same file for the data as the template; pick again')
                        continue
                break

        self.expand_template_and_datatable_into_new_tab(template_tab_path, datatable_tab_path)

    def expand_template_and_datatable_into_new_tab(self, template_tab_pathname, datatable_tab_pathname):

            notepad.activateFile(template_tab_pathname)
            template_str = editor.getText()

            notepad.activateFile(datatable_tab_pathname)
            sub_line_list = editor.getText().splitlines()

            accumulated_expanded_template_str = ''
            for (sub_row_num, sub_row_contents) in enumerate(sub_line_list):
                substitution_list = sub_row_contents.split('|')
                num_data_items = len(substitution_list)
                if sub_row_num == 0:
                    sub_tag_list = substitution_list[::]  # copy list
                elif num_data_items == len(sub_tag_list):
                    one_expanded_template_str = template_str
                    for j in range(len(sub_tag_list)):
                        one_expanded_template_str = re.sub(sub_tag_list[j], substitution_list[j], one_expanded_template_str)
                    accumulated_expanded_template_str += one_expanded_template_str

            notepad.new()
            eol = [ '\r\n', '\n', '\r' ][editor.getEOLMode()]
            accumulated_expanded_template_str = self.unify_line_endings(accumulated_expanded_template_str, eol)
            editor.setText(accumulated_expanded_template_str)

    def get_user_filetab_choice(self, prompt_str):
        retval = None
        file_list = []
        view1_file_list = []
        pathname_to_avoid_clones_dict = {}
        for (j, (pathname, buffer_id, index, view)) in enumerate(notepad.getFiles()):
            if pathname in pathname_to_avoid_clones_dict: continue
            pathname_to_avoid_clones_dict[pathname] = True
            view_addendum = '' if notepad.isSingleView() else ' (view {})'.format(view)
            entry = '[   ] {f}{v}'.format(v=view_addendum, f=self.filename_from_pathname(pathname))
            file_list.append(entry) if view == 0 else view1_file_list.append(entry)
        file_list = file_list[::-1]  # reverse the list
        file_list.extend(view1_file_list)
        user_input = self.prompt(prompt_str, '\r\n'.join(file_list))
        if user_input is not None:
            m = re.search(r'\[\s*\S+\s*\]\s+([^\r\n]+)', user_input)
            if m:
                filename = m.group(1)
                index = filename.find(' (view ')
                if index != -1: filename = filename[:index]
                retval = self.pathname_from_filename_on_tab(filename)
        return retval

    def filename_from_pathname(self, p):
        f = p.rsplit(os.sep, 1)[-1]
        return f

    def pathname_from_filename_on_tab(self, f):
        retval = None
        for (pathname, buffer_id, index, view) in notepad.getFiles():
            tab_f = pathname.rsplit(os.sep, 1)[-1]
            if f == tab_f:
                retval = pathname
                break
        return retval

    def unify_line_endings(self, text, desired_line_ending='\r\n'):
        any_line_ending_regex = r'\r(?!\n)|((?<!\r)\n)|\r\n'
        retval = re.sub(any_line_ending_regex, desired_line_ending, text)
        return retval

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
        d_tag = ''
        if 'debug' in kwargs:
            now = dt.now()
            hr = now.strftime('%I')
            if hr[0] == '0': hr = hr[1:]
            ap = 'p' if now.strftime('%p')[0] == 'P' else 'a'
            ms = now.strftime('%f')[:3]
            d_tag = now.strftime('<%a{hr}:%M:%S{ap}.{ms}>'.format(hr=hr, ap=ap, ms=ms))
            del kwargs['debug']
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

    def yes_no_cancel(self, question_text):  # returns True(Yes), False(No), or None(Cancel)
        retval = None
        answer = self.mb(question_text, MESSAGEBOXFLAGS.YESNOCANCEL, self.this_script_name)
        if answer == MESSAGEBOXFLAGS.RESULTYES: retval = True
        elif answer == MESSAGEBOXFLAGS.RESULTNO: retval = False
        return retval

    def prompt(self, prompt_text, default_text=''):
        if '\n' not in prompt_text: prompt_text = '\r\n' + prompt_text
        prompt_text += ':'
        return notepad.prompt(prompt_text, self.this_script_name, default_text)

#-------------------------------------------------------------------------------

if __name__ == '__main__': MM()
