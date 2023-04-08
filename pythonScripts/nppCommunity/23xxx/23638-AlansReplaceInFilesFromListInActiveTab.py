# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://community.notepad-plus-plus.org/topic/23638/massive-list-and-massive-search-and-replace
#  also possibly https://community.notepad-plus-plus.org/topic/22601
#  also possibly https://community.notepad-plus-plus.org/topic/22721
#  also possibly https://community.notepad-plus-plus.org/topic/23495

from Npp import *
import inspect
import os
import re
import glob

#-------------------------------------------------------------------------------

class RIFFLIAT(object):

    def __init__(self):

        self.debug = True if 0 else False
        if self.debug:
            console.show()
            console.clear()

        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]

        substitutions_list_file_path = notepad.getCurrentFilename()
        if not os.path.isfile(substitutions_list_file_path):
            self.mb('Substitution list file must be a hard-named file in the file system, i.e.,  not e.g. "new 2"')
            return
        self.print('substitutions_list_file_path:', substitutions_list_file_path)

        # the active tab has the list of the substitution pairs
        find_and_repl_match_list = []
        delimiter = '->'
        editor.research(r'(?-s)^(.+?)' + delimiter + r'(.+)', lambda m: find_and_repl_match_list.append((m.group(1), m.group(2))))
        if len(find_and_repl_match_list) == 0:
            self.mb('\r\n'.join([
                'The substitution list in the active file has no findwhat/replacewith pairs\r\n',
                'Format of file is, 1 pair per line, using  {d}  as a delimiter, no extra spaces:\r\n'.format(d=delimiter),
                'find1{d}replace1'.format(d=delimiter),
                'find2{d}replace2'.format(d=delimiter),
                '...{d}...'.format(d=delimiter),
                ]))
            return

        sample_repl_summary_list = []
        three_or_less = min(3, len(find_and_repl_match_list))
        num_repl_above_3 = len(find_and_repl_match_list) - three_or_less
        max_chars_show = 20
        for (find_what, replace_with) in find_and_repl_match_list[ 0 : three_or_less ]:
            if len(find_what) > max_chars_show: find_what = find_what[ 0 : max_chars_show] + '...'
            if len(replace_with) > max_chars_show: replace_with = replace_with[ 0 : max_chars_show] + '...'
            sample_repl_summary_list.append('"{fw}" with "{rw}"'.format(fw=find_what, rw=replace_with))
        if num_repl_above_3 > 0: sample_repl_summary_list.append('(and {} more)'.format(num_repl_above_3))

        search_folder_top_level_path = substitutions_list_file_path.rsplit(os.sep, 1)[0] + os.sep
        self.print('search_folder_top_level_path:', search_folder_top_level_path)

        if not self.yes_no('\r\n\r\n'.join([
                'Q1 of 4:\r\n',
                'Perform these replacements (specified in the active file content):',
                '\r\n'.join(sample_repl_summary_list) + '\r\n',
                'in the files in this folder?',
                search_folder_top_level_path,
                '-' * 60,
                'IT IS STRONGLY SUGGESTED TO MAKE A BACKUP',
                'OF ALL SOURCE FILES BEFORE RUNNING THIS!',
                ])):
            return

        process_subfolders = self.yes_no_cancel('\r\n\r\n'.join([
            'Q2 of 4:\r\n',
            'Do replacements in files in SUBFOLDERS of this folder also?',
            search_folder_top_level_path,
            ]))
        if process_subfolders == None: return  # user cancel
        self.print('process_subfolders:', process_subfolders)

        default_filespec = '*.txt'
        filter_input = self.prompt(
            'Q3 of 4:\r\nSupply filespec filter list         (example:    *.html *.txt *.log    )', default_filespec)
        if filter_input == None: return  # user cancel
        filters_list = filter_input.split(' ')
        filters_list = [ f for f in filters_list if len(f) > 0 ]  # remove any empty entries in filters_list
        self.print('filters_list:', filters_list)

        pathnames_of_files_to_replace_in_list = []
        for (root, dirs, files) in os.walk(search_folder_top_level_path):
            for filt in filters_list:
                for p in glob.glob(os.path.join(root, filt)):
                    if p != substitutions_list_file_path:
                        pathnames_of_files_to_replace_in_list.append(p)
            if not process_subfolders: break
        if len(pathnames_of_files_to_replace_in_list) == 0:
            self.mb('No files matched specified filter(s)')
            return

        num_files_to_examine = len(pathnames_of_files_to_replace_in_list)

        if not self.yes_no('\r\n\r\n'.join([
                'Q4 of 4:\r\n',
                '---- FINAL CONFIRM ----\r\n',
                'Make replacements in {nfe} candidate files in this folder{b} ?'.format(
                    nfe=num_files_to_examine,
                    b=' AND below' if process_subfolders else '\r\n(but not its subfolders)'),
                search_folder_top_level_path,
                ])):
            return

        pathname_currently_open_in_a_tab_list = []
        for (pathname, buffer_id, index, view) in notepad.getFiles():
            if pathname not in pathname_currently_open_in_a_tab_list:
                pathname_currently_open_in_a_tab_list.append(pathname)

        num_repl_made_in_all_files = 0
        pathnames_with_content_changed_by_repl_list = []

        for pathname in pathnames_of_files_to_replace_in_list:

            if pathname in pathname_currently_open_in_a_tab_list:
                self.print('switching active tab to', pathname)
                notepad.activateFile(pathname)
                editor.beginUndoAction()
            else:
                self.print('opening', pathname)
                notepad.open(pathname)
            if notepad.getCurrentFilename() != pathname: continue  # shouldn't happen

            for (find_what, replace_with) in find_and_repl_match_list:

                self.num_repl_made_in_this_file = 0
                def match_found(m): self.num_repl_made_in_this_file += 1
                editor.search(find_what, match_found)

                if self.num_repl_made_in_this_file > 0:

                    self.print('replacing "{fw}" with "{rw}" {n} times'.format(
                        fw=find_what, rw=replace_with, n=self.num_repl_made_in_this_file))

                    num_repl_made_in_all_files += self.num_repl_made_in_this_file

                    if pathname not in pathnames_with_content_changed_by_repl_list:
                        pathnames_with_content_changed_by_repl_list.append(pathname)

                    editor.replace(find_what, replace_with)  # the actual replacement!

            if pathname in pathname_currently_open_in_a_tab_list:
                editor.endUndoAction()
            else:
                if editor.getModify():
                    self.print('saving', pathname)
                    notepad.save()
                self.print('closing', pathname)
                notepad.close()

        notepad.activateFile(substitutions_list_file_path)  # restore active state to tab we were in before we started

        self.mb('\r\n\r\n'.join([
            '---- DONE! ----',
            '{nr} total replacements made in {nrf} files'.format(nr=num_repl_made_in_all_files,
                nrf=len(pathnames_with_content_changed_by_repl_list)),
            '(of {nfe} files matching filters provided)'.format(nfe=num_files_to_examine),
            ]))

    def print(self, *args):
        if self.debug:
            print('RIFFLIAT:', *args)

    def mb(self, msg, flags=0, title=''):  # a message-box function
        return notepad.messageBox(msg, title if title else self.this_script_name, flags)

    def yes_no(self, question_text):
        retval = False
        answer = self.mb(question_text, MESSAGEBOXFLAGS.YESNO, self.this_script_name)
        return True if answer == MESSAGEBOXFLAGS.RESULTYES else False

    def yes_no_cancel(self, question_text):
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

if __name__ == '__main__': RIFFLIAT()
