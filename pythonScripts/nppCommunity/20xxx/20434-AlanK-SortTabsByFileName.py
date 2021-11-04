# -*- coding: utf-8 -*-
""" https://community.notepad-plus-plus.org/topic/20434/

Peter's mods:
* add NOTIFICATION.FILESAVED
* add debug statements and showing the console

Alan's later mods:
* change the notification to BUFFERACTIVATED
* use another private property (self.in_callback) to prevent re-triggering the callback as it is sorting

Known issues:
* in PS 1.5.x, cannot clearCallback properly

"""

from Npp import editor, notepad, NOTIFICATION
import os

class SFTBF(object):

    def __init__(self):
        self.installed = False
        self.in_callback = False

    def install(self):
        if not self.installed:
            #notepad.callback(self.file_opened_callback, [NOTIFICATION.FILEOPENED,NOTIFICATION.FILESAVED])
            notepad.callback(self.file_opened_callback, [NOTIFICATION.BUFFERACTIVATED])
            console.write('SortFileTabsByFilename {} INSTALLED!\n'.format(self.file_opened_callback))
            self.installed = True

    def uninstall(self):
        if self.installed:
            notepad.clearCallbacks(self.file_opened_callback)
            console.write('SortFileTabsByFilename {} UNINSTALLED!\n'.format(self.file_opened_callback))
            self.installed = False

    def is_installed(self):
        return self.installed

    def file_opened_callback(self, args):
        console.write('file_opened_callback running...\n')
        if self.in_callback: return # the script moving tabs around will cause more callbacks to trigger; prevent this
        console.write('file_opened_callback {} in callback...\n'.format(self.file_opened_callback))
        self.in_callback = True
        current_view = notepad.getCurrentView()
        other_view = 1 if current_view == 0 else 0
        if notepad.getCurrentDocIndex(other_view) == 4294967295L: other_view = None
        curr_view_paths_list = []; curr_view_sorted_paths_list = []
        other_view_paths_list = []; other_view_sorted_paths_list = []
        for (filename, _, index_in_view, view) in notepad.getFiles():
            if view == current_view:
                curr_view_paths_list.append(filename)
                curr_view_sorted_paths_list.append(filename)
            else:
                other_view_paths_list.append(filename)
                other_view_sorted_paths_list.append(filename)
        curr_view_sorted_paths_list.sort(key=lambda x: x.rsplit(os.sep, 1)[-1].upper())
        curr_view_already_sorted = True if curr_view_paths_list == curr_view_sorted_paths_list else False
        other_view_sorted_paths_list.sort(key=lambda x: x.rsplit(os.sep, 1)[-1].upper())
        other_view_already_sorted = True if other_view_paths_list == other_view_sorted_paths_list else False
        if curr_view_already_sorted and other_view_already_sorted:
            self.in_callback = False
            console.write('file_opened_callback {} leaving callback without sorting...\n'.format(self.file_opened_callback))
            return  # nothing to do
        processed_other_view = False
        if other_view != None and not other_view_already_sorted:
            self.rearrange_tabs_in_view(other_view, other_view_sorted_paths_list)
            processed_other_view = True
        processed_current_view = False
        if not curr_view_already_sorted:
            self.rearrange_tabs_in_view(current_view, curr_view_sorted_paths_list)
            processed_current_view = True
        if processed_other_view and not processed_current_view:
            # leave the view we started in as the active one:
            notepad.activateIndex(current_view, notepad.getCurrentDocIndex(current_view))
        self.in_callback = False
        console.write('file_opened_callback {} leaving callback...\n'.format(self.file_opened_callback))

    def rearrange_tabs_in_view(self, view, sorted_name_list):
        notepad.activateIndex(view, notepad.getCurrentDocIndex(view))  # get switched into the correct view
        remembered_active_filename = notepad.getCurrentFilename()
        destination_index = 0
        num_of_tabs = len(sorted_name_list)
        while destination_index < num_of_tabs:
            current_order_list = []
            for (filename, _, index_in_view, v) in notepad.getFiles():
                if v == view: current_order_list.append(filename)
            curr_location_index = current_order_list.index(sorted_name_list[destination_index])
            move_left_count = curr_location_index - destination_index
            if move_left_count > 0:
                notepad.activateFile(current_order_list[curr_location_index])
                for _ in range(move_left_count): notepad.menuCommand(MENUCOMMAND.VIEW_TAB_MOVEBACKWARD)
            destination_index += 1
        notepad.activateFile(remembered_active_filename)

if __name__ == '__main__':

    if 'sftbf' not in globals(): sftbf = SFTBF()

    # each running of the script toggles install/uninstall:
    console.show()
    sftbf.uninstall() if sftbf.is_installed() else sftbf.install()
    notepad.messageBox('SortFileTabsByFilename {}INSTALLED!'.format('' if sftbf.is_installed() else 'UN'), '')
