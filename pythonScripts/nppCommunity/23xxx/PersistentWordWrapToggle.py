# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://community.notepad-plus-plus.org/topic/23855/file-tab-specific-word-wrap-vs-global-enable-thread-reboot
#  https://community.notepad-plus-plus.org/topic/10985/file-specific-word-wrap-vs-global-enable
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/5232
# Author: AlanKilborn @ community.notepad-plus-plus.org

from Npp import *
import os
import inspect
import json

#-------------------------------------------------------------------------------

class WWTFATWP(object):

    def __init__(self):
        self.debug = True if 0 else False
        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]
        self.wrap_by_buffer_id_dict = {}
        self.pathname_by_buffer_id_dict = {}
        self.this_script_path_without_ext = inspect.getframeinfo(inspect.currentframe()).filename.rsplit('.', 1)[0]
        self.settings_json_file_path = self.this_script_path_without_ext + '.json'
        # read settings written the last time Notepad++ was shut down:
        pathnames_with_wrap_on_list = []
        if os.path.isfile(self.settings_json_file_path):
            self.dprint('json file found')
            try:
                with open(self.settings_json_file_path) as f:
                    pathnames_with_wrap_on_list = json.load(f)['wrap_on_list']
            except:
                self.dprint('problem opening/reading json file')
        self.dprint('pathnames_with_wrap_on_list:', pathnames_with_wrap_on_list)
        for (pathname, buffer_id, index, view) in notepad.getFiles():
            self.wrap_by_buffer_id_dict[buffer_id] = 1 if pathname in pathnames_with_wrap_on_list else 0
            self.pathname_by_buffer_id_dict[buffer_id] = pathname
        self.dprint('wrap_by_buffer_id_dict:', self.wrap_by_buffer_id_dict)
        self.dprint('pathname_by_buffer_id_dict:', self.pathname_by_buffer_id_dict)
        notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])
        notepad.callback(self.shutdown_notify, [NOTIFICATION.SHUTDOWN])
        editor.callback(self.updateui_callback, [SCINTILLANOTIFICATION.UPDATEUI])
        self.bufferactivated_callback(None)  # artificial call to get the wrap mode set for the current file

    def updateui_callback(self, args):
        # this is mainly useful for when a tab is renamed; so that it gets "noticed" by our logic asap
        self.bufferactivated_callback(None)

    def bufferactivated_callback(self, args):
        curr_bid = args['bufferID'] if args else notepad.getCurrentBufferID()
        curr_pathname = notepad.getCurrentFilename()
        editor.setWrapMode(self.wrap_by_buffer_id_dict[curr_bid] if curr_bid in self.wrap_by_buffer_id_dict else 0)
        self.pathname_by_buffer_id_dict[curr_bid] = curr_pathname  # maintain link between constant bid and possibly changing pathname

    def shutdown_notify(self, args):
        # write settings so they persist between runs of N++
        pathnames_with_wrap_on_list = []
        for bid in self.pathname_by_buffer_id_dict:
            pathname_for_buffer_id = self.pathname_by_buffer_id_dict[bid]
            if bid in self.wrap_by_buffer_id_dict:
                wrap_for_buffer_id = self.wrap_by_buffer_id_dict[bid]
                if wrap_for_buffer_id == 1:
                    # only save state for paths that have wrap turned on
                    if pathname_for_buffer_id not in pathnames_with_wrap_on_list:
                        pathnames_with_wrap_on_list.append(pathname_for_buffer_id)
            else:
                pass  # this part of the code will be reached for the renegade "new x" document that isn't visible!
        try:
            with open(self.settings_json_file_path, 'w') as f:
                f.write(json.dumps({ 'wrap_on_list' : pathnames_with_wrap_on_list }, sort_keys=True, indent=1, default=str))
        except:
            pass

    def toggle_wrap_mode(self):
        curr_bid = notepad.getCurrentBufferID()
        curr_pathname = notepad.getCurrentFilename()
        if curr_bid in self.wrap_by_buffer_id_dict:
            self.wrap_by_buffer_id_dict[curr_bid] = 1 if self.wrap_by_buffer_id_dict[curr_bid] == 0 else 0  # toggle
        else:
            self.wrap_by_buffer_id_dict[curr_bid] = 1  # turn wrap on for current file
        editor.setWrapMode(self.wrap_by_buffer_id_dict[curr_bid])
        self.sb_output('Wrapping is {} for active tab'.format('ON' if self.wrap_by_buffer_id_dict[curr_bid] else 'OFF'))
        self.pathname_by_buffer_id_dict[curr_bid] = curr_pathname  # maintain link between constant bid and possibly changing pathname

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

    def sb_output(self, *args):  # output to N++'s status bar (will be overwritten by N++ e.g. when active tab is changed)
        notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, ' '.join(map(str, args)))

#-------------------------------------------------------------------------------

# to run via another file, e.g., startup.py, put these lines (uncommented and unindented) in that file:
#  import WordWrapToggleForActiveTabWithPersistence
#  wwtfatwp = WordWrapToggleForActiveTabWithPersistence.WWTFATWP()

if __name__ == '__main__':

    try:
        wwtfatwp
    except NameError:
        wwtfatwp = WWTFATWP()

    # when this script is run interactively, it will toggle the wrap setting on the currently active tab
    wwtfatwp.toggle_wrap_mode()
