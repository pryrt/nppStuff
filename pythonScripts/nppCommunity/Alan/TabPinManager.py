# -*- coding: utf-8 -*-
from __future__ import print_function

#########################################
#
#  TabPinManager (TPM)
#
#########################################

# references:
#  https://community.notepad-plus-plus.org/topic/25731  <-- this script is posted here
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/5786
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15162 "[BUG] "Close All" and "Close All BUT This" can close file tabs the user can't see (in another view)"
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15115 "Allow plugins to get/set the existing color choice for a tab"
#   https://github.com/notepad-plus-plus/notepad-plus-plus/pull/15142 "Add plugin command NPPM_GETTABCOLORID"
#    https://github.com/notepad-plus-plus/notepad-plus-plus/commit/9244cd09430c82ecff805ea862c9133d5cb56ded
#  for newbie info on PythonScripts, see https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript

#-------------------------------------------------------------------------------

from Npp import *
import inspect
import os
from datetime import datetime as dt
import sys
import platform
from ctypes import (WinDLL, WINFUNCTYPE, Structure, POINTER, cast, create_unicode_buffer, addressof)
from ctypes.wintypes import (HWND, INT, UINT, WPARAM, LPARAM, LPCSTR, LPWSTR, DWORD, BOOL)

#-------------------------------------------------------------------------------

user32 = WinDLL('user32')

LRESULT = LPARAM

WndProcType = WINFUNCTYPE(
    LRESULT,  # return type
    HWND, UINT, WPARAM, LPARAM  # arguments
    )

SetWindowLong = user32.SetWindowLongW if platform.architecture()[0] == '32bit' else user32.SetWindowLongPtrW
SetWindowLong.restype = WndProcType
SetWindowLong.argtypes = [ HWND, INT, WndProcType ]

GWL_WNDPROC = -4

WM_COMMAND = 0x111
WM_NOTIFY = 0x4E

def LOWORD(value): return value & 0xFFFF

# see https://github.com/notepad-plus-plus/notepad-plus-plus/blob/e2a1234384cbbe0665baee77b1abfee985c1c5d8/PowerEditor/src/menuCmdID.h#L370
# note: these commands have yet to be added in to PythonScript's MENUCOMAND.xxx values list
IDM_VIEW_TAB_COLOUR_NONE = 44110
IDM_VIEW_TAB_COLOUR_1__yellow = 44111
IDM_VIEW_TAB_COLOUR_2__green  = 44112
IDM_VIEW_TAB_COLOUR_3__blue   = 44113
IDM_VIEW_TAB_COLOUR_4__orange = 44114
IDM_VIEW_TAB_COLOUR_5__pink   = 44115
IDM_VIEW_GOTO_START = 10005
IDM_VIEW_GOTO_END   = 10006

SendMessageW = user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [ HWND, UINT, WPARAM, LPARAM ]

WM_USER = 0x400
NPPMSG = (WM_USER + 1000)

TCN_FIRST = 4294966746
TCN_TABDELETE = (TCN_FIRST - 12)

class NMHDR(Structure):
    _fields_ = [
        ('hwndFrom', HWND),
        ('idFrom', WPARAM),
        ('code', UINT)
    ]
#LPNMHDR = POINTER(NMHDR)

class TABNOTIFICATION(Structure):
    _fields_ = [
        ('nmhdr', NMHDR),
        ('tabOrigin', INT),
    ]
LPTABNOTIFICATION = POINTER(TABNOTIFICATION)

#-------------------------------------------------------------------------------

try:
    notepad.hwnd  # available in PS3
except AttributeError:
    notepad.hwnd = user32.FindWindowW(u'Notepad++', None)  # have to find it ourselves for PS2

#-------------------------------------------------------------------------------

# someday notepad.getTabColorID() will be a real function in PythonScript, but not yet so use notepad_getTabColorID() we define here
#  see https://github.com/bruderstein/PythonScript/issues/337
def notepad_getTabColorID(view=-1, tab_index=-1):
    NPPM_GETTABCOLORID = (NPPMSG + 114)
    retval = SendMessageW(notepad.hwnd, NPPM_GETTABCOLORID, view, tab_index)
    return retval

#-------------------------------------------------------------------------------

class TPM(object):

    class ContextMgr(object):  # a context manager to be used with "with"
        def __init__(self): self.ref_count = 0
        def __enter__(self): self.ref_count += 1
        def __exit__(self, exc_type, exc_value, exc_traceback): self.ref_count -= 1
        def is_entered(self): return self.ref_count > 0

    def __init__(self):

        self.debug_on = True if 0 else False  # don't use this variable elsewhere, use "self.dprint()" or "if self.debugging_on():"
        this_script_file_or_path = inspect.getframeinfo(inspect.currentframe()).filename  # PS2 always returns path; PS3 can return file without path
        scripts_top_level_dir_path = os.path.join(notepad.getPluginConfigDir(), 'PythonScript', 'scripts')
        if scripts_top_level_dir_path in this_script_file_or_path:
            self.this_script_path = this_script_file_or_path
            self.this_script_filename = this_script_file_or_path.rsplit(os.sep, 1)[1]
        else:
            self.this_script_filename = this_script_file_or_path
            def find_file(file_name_to_search_for, top_level_path_to_search):
                for (root, dirs, files) in os.walk(top_level_path_to_search):
                    if file_name_to_search_for in files: return os.path.join(root, file_name_to_search_for)
                assert 0  # not found
            self.this_script_path = find_file(self.this_script_filename, scripts_top_level_dir_path)
        self.this_script_name = self.this_script_filename.rsplit('.', 1)[0]
        self.this_script_path_without_ext = self.this_script_path.rsplit('.', 1)[0]
        self.turn_debug_on_file = self.this_script_path_without_ext + '__DebugON.cfg'
        self.turn_debug_off_file = self.this_script_path_without_ext + '__DebugOFF.cfg'
        #with open(self.turn_debug_on_file, 'w') as f: pass  # easy create file; don't leave this enabled!

        self.print('{} initializing...'.format(self.this_script_name))

        self.minimum_npp_version_required = 8.68
        if self.npp_version_as_float() < self.minimum_npp_version_required:
            self.initialized = False
            self.mb('Use of this script requires N++ version >= 8.6.8')
            return

        self.initialized = True

        self.get_editor_tab_ctrl_hwnd()

        self.closeall_cmd_id_list = [
            MENUCOMMAND.FILE_CLOSE,     # Ctrl+w
            MENUCOMMAND.FILE_CLOSEALL,  # Ctrl+Shift+w
            MENUCOMMAND.FILE_CLOSEALL_BUT_CURRENT,
            MENUCOMMAND.FILE_CLOSEALL_TOLEFT,
            MENUCOMMAND.FILE_CLOSEALL_TORIGHT,
            MENUCOMMAND.FILE_CLOSEALL_UNCHANGED,
            ]

        self.move_clone_cmd_id_list = [
            MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW,
            MENUCOMMAND.VIEW_CLONE_TO_ANOTHER_VIEW,
            ]

        self.move_tab_cmd_id_list = [
            MENUCOMMAND.VIEW_TAB_MOVEFORWARD,   # Ctrl+PageDown
            MENUCOMMAND.VIEW_TAB_MOVEBACKWARD,  # Ctrl+PageUp
            IDM_VIEW_GOTO_START,
            IDM_VIEW_GOTO_END,
            ]

        self.tab_no_color_cmd = first_tab_color_cmd = IDM_VIEW_TAB_COLOUR_NONE
        self.tab_color_cmd_range = range(first_tab_color_cmd, IDM_VIEW_TAB_COLOUR_5__pink + 1)

        yellow_color_id = 0
        green_color_id  = 1
        blue_color_id   = 2
        orange_color_id = 3
        pink_color_id   = 4

        set_color_of_tab_cmd_by_color_id_dict = {
            yellow_color_id : IDM_VIEW_TAB_COLOUR_1__yellow,
            green_color_id  : IDM_VIEW_TAB_COLOUR_2__green,
            blue_color_id   : IDM_VIEW_TAB_COLOUR_3__blue,
            orange_color_id : IDM_VIEW_TAB_COLOUR_4__orange,
            pink_color_id   : IDM_VIEW_TAB_COLOUR_5__pink,
        }

        self.color_id_representing_pinned_tab = pink_color_id  # pink works well in light and dark mode
        self.cmd_to_set_color_representing_pinned_tab = set_color_of_tab_cmd_by_color_id_dict[self.color_id_representing_pinned_tab]

        self.buff_activated_callback_suspended_cm = self.ContextMgr()
        self.buff_activated_running = False
        notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])

        self.npp_new_wnd_proc_for_SWL = WndProcType(self.npp_new_wnd_proc)  # this absolutely needs to be a "self." variable!
        self.orig_npp_wnd_proc = SetWindowLong(notepad.hwnd, GWL_WNDPROC, self.npp_new_wnd_proc_for_SWL)

    def toggle_tab_pin_state(self):

        if not self.initialized: return

        with self.buff_activated_callback_suspended_cm:

            active_view =  notepad.getCurrentView()
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            self.dprint('active_tab_index:|{T}|'.format(T=active_tab_index))
            rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]
            self.dprint('rightmost_pinned_tab_index:|{T}|'.format(T=rightmost_pinned_tab_index))

            if self.is_active_tab_pinned():

                # unpin it
                positions_to_move = rightmost_pinned_tab_index - active_tab_index
                self.dprint('positions_to_move forward:|{T}|'.format(T=positions_to_move))
                self.move_active_tab_right_n_times(positions_to_move)
                self.active_tab_color_set_to_pinned_color(False)

            else:

                # pin it
                positions_to_move = active_tab_index - rightmost_pinned_tab_index - 1
                self.dprint('positions_to_move backward:|{T}|'.format(T=positions_to_move))
                self.move_active_tab_left_n_times(positions_to_move)
                self.active_tab_color_set_to_pinned_color()

    def npp_new_wnd_proc(self, hwnd, msg, wParam, lParam):

        let_npp_see_the_msg = True  # assume we are going to let N++ see the msg

        if msg == WM_NOTIFY:  # this is for the on-tab close button, or double-clicking a tab to close it

            tab_notify = cast(lParam, LPTABNOTIFICATION).contents

            if tab_notify.nmhdr.code == TCN_TABDELETE:

                self.dprint('TCN_TABDELETE WM_NOTIFY w={0}/0x{0:X} l={0}/0x{0:X}'.format(wParam, lParam))
                if self.editor1_tab_ctrl_hwnd is not None:
                    view = 0 if tab_notify.nmhdr.hwndFrom == self.editor1_tab_ctrl_hwnd else 1
                else:
                    view = 1 if tab_notify.nmhdr.hwndFrom == self.editor2_tab_ctrl_hwnd else 0
                tab_index = tab_notify.tabOrigin
                # don't trigger buffer activated callbacks during execution of the following code section:
                with self.buff_activated_callback_suspended_cm:
                    notepad.activateIndex(view, tab_index)
                self.dprint('TCN_TABDELETE view: {v} index: {i} filename: "{f}"'.format(v=view, i=tab_index, f=notepad.getCurrentFilename()))

                # convert to WM_COMMAND message with FILE_CLOSE as wParam:
                msg = WM_COMMAND
                wParam = MENUCOMMAND.FILE_CLOSE
                # note: fall-thru into the next section

        if msg == WM_COMMAND:  # not elif, because the above could fall-thru into here!

            wParam = LOWORD(wParam)  # disregard whether we got this command via menu or accelerator

            self.dprint('WM_COMMAND w={0}/0x{0:X} l={0}/0x{0:X}'.format(wParam, lParam))

            if wParam in self.tab_color_cmd_range or \
                    wParam in self.closeall_cmd_id_list or \
                    wParam in self.move_clone_cmd_id_list or \
                    wParam in self.move_tab_cmd_id_list:

                active_view = notepad.getCurrentView()
                active_tab_index = notepad.getCurrentDocIndex(active_view)
                rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]

                if wParam in self.move_clone_cmd_id_list:

                    if self.is_active_tab_pinned():
                        self.mb('Cannot move/clone a pinned tab to the other view without unpinning first.')
                        let_npp_see_the_msg = False

                elif wParam in self.move_tab_cmd_id_list:

                    if self.is_no_tab_pinned_in_view() or self.is_all_tabs_pinned_in_view():
                        pass  # command ok for n++ to execute

                    else:

                        if wParam == MENUCOMMAND.VIEW_TAB_MOVEFORWARD:

                            if active_tab_index == rightmost_pinned_tab_index:
                                self.mb('Cannot move a pinned tab into the unpinned tab area without first unpinning it.')
                                let_npp_see_the_msg = False

                        elif wParam == MENUCOMMAND.VIEW_TAB_MOVEBACKWARD:

                            if active_tab_index == rightmost_pinned_tab_index + 1:
                                self.mb('Cannot move an unpinned tab into the pinned tab area; simply pin it instead.')
                                let_npp_see_the_msg = False

                        elif wParam == IDM_VIEW_GOTO_START:

                            if active_tab_index == 0 or active_tab_index == rightmost_pinned_tab_index + 1:
                                # tab is already where it was commanded to be; nothing to do
                                let_npp_see_the_msg = False
                            elif active_tab_index > rightmost_pinned_tab_index + 1:
                                # move tab to start of unpinned area:
                                self.move_active_tab_left_n_times(active_tab_index - rightmost_pinned_tab_index - 1)
                                let_npp_see_the_msg = False
                            else:
                                pass  # tab is in pinned area; ok for n++ to move it to the start

                        elif wParam == IDM_VIEW_GOTO_END:

                            if active_tab_index == rightmost_pinned_tab_index or \
                                    active_tab_index == self.get_tab_count_in_view() - 1:
                                # tab is already where it was commanded to be; nothing to do
                                let_npp_see_the_msg = False
                            elif active_tab_index < rightmost_pinned_tab_index:
                                # move tab to end of pinned area:
                                self.move_active_tab_right_n_times(rightmost_pinned_tab_index - active_tab_index)
                                let_npp_see_the_msg = False
                            else:
                                pass  # tab is in unpinned area; ok for n++ to move it to the end

                elif wParam in self.tab_color_cmd_range:

                    if wParam == self.cmd_to_set_color_representing_pinned_tab:

                        if not self.is_active_tab_pinned():
                            self.mb('Cannot set a tab to this color -- this color is reserved for the tab-pinning feature to represent a pinned tab.')
                        let_npp_see_the_msg = False

                    elif self.is_active_tab_pinned():

                        self.mb('Cannot set the color on a pinned tab.')
                        let_npp_see_the_msg = False

                elif wParam in self.closeall_cmd_id_list:

                    with self.buff_activated_callback_suspended_cm:

                        keep_going = True

                        if wParam == MENUCOMMAND.FILE_CLOSE:
                            pass  # single-tab closure of a pinned or unpinned tab is okay;
                                  #  for the pinned case user will get confirmation prompt
                        elif self.is_all_tabs_pinned_in_view():
                            keep_going = let_npp_see_the_msg = False
                            self.mb('All tabs are pinned -- cannot perform requested action.')
                        elif wParam in [ MENUCOMMAND.FILE_CLOSEALL, MENUCOMMAND.FILE_CLOSEALL_BUT_CURRENT]:  # note: important that this check comes before the check for 0 pinned tabs!
                            if notepad.isSingleView():
                                keep_going = self.get_pinned_tab_count_in_view() > 0
                            else:
                                keep_going = let_npp_see_the_msg = False
                                self.mb('The chosen command is disallowed as it affects too much (both views).\r\n\r\nSee issue # 15162.\r\n\r\n')
                        elif self.is_no_tab_pinned_in_view():
                            keep_going = False

                        if keep_going:

                            if wParam == MENUCOMMAND.FILE_CLOSE:

                                self.dprint('got MENUCOMMAND.FILE_CLOSE')
                                self.dprint('active_tab_index:|{T}|'.format(T=active_tab_index))
                                self.dprint('rightmost_pinned_tab_index:|{T}|'.format(T=rightmost_pinned_tab_index))
                                if self.is_active_tab_pinned():
                                    let_npp_see_the_msg = self.yes_no('"{n}" is a pinned tab -- really close it?'.format(n=self.get_name_from_active_tab()))
                                # note: leaves a N++ chosen tab as the active tab when done

                            elif wParam == MENUCOMMAND.FILE_CLOSEALL:

                                notepad.activateIndex(active_view, rightmost_pinned_tab_index)
                                # note: leaves the rightmost pinned tab active when done
                                wParam = MENUCOMMAND.FILE_CLOSEALL_TORIGHT

                            elif wParam == MENUCOMMAND.FILE_CLOSEALL_BUT_CURRENT:

                                if self.is_active_tab_pinned():
                                    # a pinned tab is active, so we should close all unpinned
                                    notepad.activateIndex(active_view, rightmost_pinned_tab_index)
                                    # note: leaves the rightmost pinned tab active when done
                                else:
                                    # an unpinned tab is active; close all unpinned except the active tab;
                                    #  move current tab to the position just to the right of all the pinned tabs
                                    self.move_active_tab_left_n_times(active_tab_index - rightmost_pinned_tab_index - 1)
                                    # note: leaves the original tab active when done
                                    #       UNLESS the user cancels a save, then tab order is changed and an undesired tab is left active!
                                wParam = MENUCOMMAND.FILE_CLOSEALL_TORIGHT

                            elif wParam == MENUCOMMAND.FILE_CLOSEALL_TOLEFT:

                                if active_tab_index == 0:
                                    self.mb('No tab(s) exist to the left of the "{n}" tab -- nothing to close.'.format(n=self.get_name_from_active_tab()))
                                elif active_tab_index <= rightmost_pinned_tab_index + 1:
                                    self.mb('All tabs to the left of "{n}" are pinned; tabs must be unpinned before closing.'.format(n=self.get_name_from_active_tab()))
                                else:
                                    remember_buff_id = notepad.getCurrentBufferID()
                                    buff_id_to_close_list = []
                                    for (__, buffer_id, index, view) in notepad.getFiles():
                                        if view != active_view: continue
                                        elif buffer_id == remember_buff_id: break
                                        elif index > rightmost_pinned_tab_index: buff_id_to_close_list.append(buffer_id)
                                    for bid in buff_id_to_close_list:
                                        notepad.activateBufferID(bid)
                                        notepad.close()
                                        if self.is_buff_id_open_in_view(bid, active_view):
                                            # user must have canceled the closure, so don't keep going with closing of additional tabs
                                            break
                                    notepad.activateBufferID(remember_buff_id)  # restore originally-active tab to the active state

                                let_npp_see_the_msg = False

                            elif wParam == MENUCOMMAND.FILE_CLOSEALL_TORIGHT:

                                if active_tab_index == self.get_tab_count_in_view() - 1:
                                    self.mb('No tab(s) exist to the right of the "{n}" tab -- nothing to close.'.format(n=self.get_name_from_active_tab()))
                                    let_npp_see_the_msg = False
                                elif active_tab_index < rightmost_pinned_tab_index:
                                    notepad.activateIndex(active_view, rightmost_pinned_tab_index)
                                    # note: this will leave the right-most pinned tab as the active tab when the action is finished
                                else:
                                    pass
                                    # note: the originally active non-pinned tab will be active when the action is finished

                            elif wParam == MENUCOMMAND.FILE_CLOSEALL_UNCHANGED:

                                # note: soft-named files have never been saved, thus they are by definition modified/changed, so they aren't closed by this command
                                remember_buff_id = notepad.getCurrentBufferID()
                                candidate_buff_id_to_close_list = []
                                for (__, buffer_id, index, view) in notepad.getFiles():
                                    if view != active_view: continue
                                    elif index > rightmost_pinned_tab_index: candidate_buff_id_to_close_list.append(buffer_id)
                                closed_count = 0
                                user_canceled_closure = False
                                for bid in candidate_buff_id_to_close_list:
                                    notepad.activateBufferID(bid)
                                    if os.path.isfile(notepad.getCurrentFilename()) and not editor.getModify():
                                        notepad.close()
                                        if self.is_buff_id_open_in_view(bid, active_view):
                                            # user must have canceled the closure, so don't keep going with closing of additional tabs
                                            user_canceled_closure = True
                                            break
                                        closed_count += 1
                                if self.is_buff_id_open_in_view(remember_buff_id, active_view):
                                    notepad.activateBufferID(remember_buff_id)  # if tab that was originally active is still open, make it active
                                if closed_count == 0 and not user_canceled_closure:
                                    self.mb('No unchanged files to close.\r\n\r\nNote that untitled tabs are always considered as changed.')
                                let_npp_see_the_msg = False

        if let_npp_see_the_msg:
            let_npp_see_the_msg = self.orig_npp_wnd_proc(hwnd, msg, wParam, lParam)

        return let_npp_see_the_msg

    def bufferactivated_callback(self, args):

        # this callback is used solely to correct any tab coloring that is considered "wrong" (by some user action)

        # don't bother checking that tab-coloring is correct when this script is activating different tabs (assume script is correct)
        if self.buff_activated_callback_suspended_cm.is_entered(): return

        # don't allow self-retriggering:
        if self.buff_activated_running: return
        self.buff_activated_running = True

        active_view = notepad.getCurrentView()
        active_tab_index = notepad.getCurrentDocIndex(active_view)
        inactive_view = 1 if active_view == 0 else 0
        inactive_view_active_tab_index = notepad.getCurrentDocIndex(inactive_view)
        rightmost_pinned_tab_indices_tup = self.get_rightmost_pinned_tab_index_in_both_views()

        any_coloring_changes_made = False

        for (__, __, index, view) in notepad.getFiles():
            rightmost_pinned_tab_index = rightmost_pinned_tab_indices_tup[view]
            if index > rightmost_pinned_tab_index: continue
            color_id = notepad_getTabColorID(view, index)
            if color_id != self.color_id_representing_pinned_tab:
                notepad.activateIndex(view, index)
                self.active_tab_color_set_to_pinned_color()
                any_coloring_changes_made = True

        if any_coloring_changes_made:
            # restore what user had active originally:
            notepad.activateIndex(inactive_view, inactive_view_active_tab_index)
            notepad.activateIndex(active_view, active_tab_index)

        self.buff_activated_running = False

    def get_editor_tab_ctrl_hwnd(self):

        self.editor1_tab_ctrl_hwnd = self.editor2_tab_ctrl_hwnd = None

        class TCITEM(Structure):
            _fields_ = [
                ('mask', UINT),
                ('dwState', DWORD),
                ('dwStateMask', DWORD),
                ('pszText', LPWSTR),
                ('cchTextMax', INT),
                ('iImage', INT),
                ('lParam', LPARAM)
            ]

        TCIF_TEXT = 1
        TCM_FIRST = 4864
        TCM_GETITEMCOUNT = (TCM_FIRST + 4)
        TCM_GETITEMW = (TCM_FIRST + 60)

        curr_class = create_unicode_buffer(256)
        pszText = create_unicode_buffer(256)

        tcitem = TCITEM()
        tcitem.mask = TCIF_TEXT
        tcitem.pszText = addressof(pszText)
        tcitem.cchTextMax = len(pszText)

        file_by_view_list = [ [], [] ]
        def tab_text_from_pathname(pathname): return pathname.rsplit(os.sep, 1)[-1]
        for (pathname, __, __, view) in notepad.getFiles():
            file_by_view_list[view].append(tab_text_from_pathname(pathname))

        def foreach_window_to_find_editor_tab_controls(hwnd, lParam):
            cc = curr_class[ : user32.GetClassNameW(hwnd, curr_class, 256) ]
            if cc == u'SysTabControl32':
                tab_count_in_prospective_tabctrl = SendMessageW(hwnd, TCM_GETITEMCOUNT, 0, 0)
                v0_tab_text_matches = v1_tab_text_matches = 0
                for tab_num in range(tab_count_in_prospective_tabctrl):
                    tab_count_in_prospective_tabctrl = SendMessageW(hwnd, TCM_GETITEMW, tab_num, addressof(tcitem))
                    tab_text = tcitem.pszText
                    if sys.version_info.major == 3:  # ps3
                        if tab_text in file_by_view_list[0]: v0_tab_text_matches += 1
                        if tab_text in file_by_view_list[1]: v1_tab_text_matches += 1
                    else:
                        if tab_text.encode('utf-8') in file_by_view_list[0]: v0_tab_text_matches += 1  # ps2hack!
                        if tab_text.encode('utf-8') in file_by_view_list[1]: v1_tab_text_matches += 1  # ps2hack!
                if v0_tab_text_matches == len(file_by_view_list[0]):
                    self.editor1_tab_ctrl_hwnd = hwnd
                    if notepad.isSingleView() or self.editor2_tab_ctrl_hwnd is not None: return False
                elif v1_tab_text_matches == len(file_by_view_list[1]):
                    self.editor2_tab_ctrl_hwnd = hwnd
                    if notepad.isSingleView() or self.editor1_tab_ctrl_hwnd is not None: return False
                    return False
            return True  # True to keep going, False to STOP enumerating!

        WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
        user32.EnumChildWindows(notepad.hwnd, WNDENUMPROC(foreach_window_to_find_editor_tab_controls), 0)

        assert self.editor1_tab_ctrl_hwnd or self.editor2_tab_ctrl_hwnd  # only need one!

    def move_active_tab_left_n_times(self, n):
        for __ in range(n): notepad.menuCommand(MENUCOMMAND.VIEW_TAB_MOVEBACKWARD)

    def move_active_tab_right_n_times(self, n):
        for __ in range(n): notepad.menuCommand(MENUCOMMAND.VIEW_TAB_MOVEFORWARD)

    def get_name_from_active_tab(self):
        pathname = notepad.getCurrentFilename()
        tab_text = pathname.rsplit(os.sep, 1)[-1]
        return tab_text

    def get_tab_count_in_view(self):
        retval = 0
        for (__, __, __, view) in notepad.getFiles():
            if view == notepad.getCurrentView(): retval += 1
        return retval

    def get_pinned_tab_count_in_view(self):
        rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[notepad.getCurrentView()]
        retval = rightmost_pinned_tab_index + 1
        return retval

    def is_active_tab_pinned(self):
        active_view = notepad.getCurrentView()
        active_tab_index = notepad.getCurrentDocIndex(active_view)
        rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]
        return active_tab_index <= rightmost_pinned_tab_index

    def is_no_tab_pinned_in_view(self):
        return self.get_pinned_tab_count_in_view() == 0

    def is_all_tabs_pinned_in_view(self):
        return self.get_pinned_tab_count_in_view() == self.get_tab_count_in_view()

    def get_rightmost_pinned_tab_index_in_both_views(self):
        rv_list = [ -1, -1 ]  # -1 signifies no tabs (in a given view) are pinned
        for (__, __, index, view) in notepad.getFiles()[::-1]:  # do view1 files first, process tabs right to left
            if notepad_getTabColorID(view, index) == self.color_id_representing_pinned_tab and rv_list[view] == -1:
                rv_list[view] = index
        return tuple(rv_list)

    def active_tab_color_set_to_pinned_color(self, color_it_not_clear_color=True):
        notepad.menuCommand(self.cmd_to_set_color_representing_pinned_tab if color_it_not_clear_color else self.tab_no_color_cmd)

    def npp_version_as_float(self):
        tup = notepad.getVersion()
        if 2 <= len(tup) <= 3:
            retval = tup[0] + tup[1] / 10.0
            if len(tup) == 3:
                retval += tup[2] / 100.0
        else:
            assert False
        return retval

    def is_buff_id_open_in_view(self, test_buf_id, test_view):
        for (__, buffer_id, __, view) in notepad.getFiles():
            if view == test_view and buffer_id == test_buf_id: return True
        return False

    def close_all_in_current_view(self):
        self.dprint('executing close_all_in_current_view()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]
            if self.is_no_tab_pinned_in_view():
                if notepad.isSingleView():
                    notepad.menuCommand(MENUCOMMAND.FILE_CLOSEALL)
                else:
                    notepad.activateIndex(active_view, 0)
                    notepad.menuCommand(MENUCOMMAND.FILE_CLOSEALL_TORIGHT)  # close all but one tab
                    notepad.menuCommand(MENUCOMMAND.FILE_CLOSE)  # close last remaining tab
            elif self.is_all_tabs_pinned_in_view():
                self.mb('All tabs are pinned in current view; some tabs must be unpinned to execute this command.')
            else:
                notepad.activateIndex(active_view, rightmost_pinned_tab_index)
                notepad.menuCommand(MENUCOMMAND.FILE_CLOSEALL_TORIGHT)
                if active_tab_index < rightmost_pinned_tab_index:
                    notepad.activateIndex(active_view, active_tab_index)  # leave original tab as the active tab

    def close_all_untitled_regardless_of_modified_state(self):
        self.dprint('executing close_all_untitled_regardless_of_modified_state()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]
            remember_buff_id = notepad.getCurrentBufferID()
            candidate_buff_id_to_close_list = []
            for (__, buffer_id, index, view) in notepad.getFiles():
                if view != active_view: continue
                elif index > rightmost_pinned_tab_index: candidate_buff_id_to_close_list.append(buffer_id)
            closed_count = 0
            for bid in candidate_buff_id_to_close_list:
                notepad.activateBufferID(bid)
                if not os.path.isfile(notepad.getCurrentFilename()):
                    notepad.close()
                    closed_count += 1
            if self.is_buff_id_open_in_view(remember_buff_id, active_view):
                notepad.activateBufferID(remember_buff_id)  # if tab that was originally active is still open, make it active
            if closed_count == 0:
                self.mb('No tabs met the criteria for closure.')

    def unpin_all_in_current_view(self):  # called from another script
        self.dprint('executing unpin_all_in_current_view()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            for (__, __, index, view) in notepad.getFiles():
                if view == active_view:
                    notepad.activateIndex(active_view, index)
                    self.active_tab_color_set_to_pinned_color(False)
            notepad.activateIndex(active_view, active_tab_index)

    def pin_current_and_left(self):  # called from another script
        self.dprint('executing pin_current_and_left()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            for (__, __, index, view) in notepad.getFiles():
                if view == active_view:
                    if index <= active_tab_index:
                        if notepad_getTabColorID(active_view, index) != self.color_id_representing_pinned_tab:
                            notepad.activateIndex(active_view, index)
                            self.active_tab_color_set_to_pinned_color()
                    else:
                        break
            notepad.activateIndex(active_view, active_tab_index)

    def pin_current_and_right(self):  # called from another script
        self.dprint('executing pin_current_and_right()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            rightmost_pinned_tab_index = self.get_rightmost_pinned_tab_index_in_both_views()[active_view]
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            active_tab_buffer_id = notepad.getCurrentBufferID()
            num_tabs_to_pin = self.get_tab_count_in_view() - active_tab_index
            self.dprint('num_tabs_to_pin:|{T}|'.format(T=num_tabs_to_pin))
            working_tab_index = active_tab_index
            for __ in range(num_tabs_to_pin):
                notepad.activateIndex(active_view, working_tab_index)
                positions_to_move = working_tab_index - rightmost_pinned_tab_index - 1
                self.dprint('positions_to_move:|{T}|'.format(T=positions_to_move))
                self.move_active_tab_left_n_times(positions_to_move)
                self.active_tab_color_set_to_pinned_color()
                rightmost_pinned_tab_index += 1
                working_tab_index += 1
            notepad.activateBufferID(active_tab_buffer_id)

    def unpin_current_and_right(self):  # called from another script
        self.dprint('executing unpin_current_and_right()')
        with self.buff_activated_callback_suspended_cm:
            active_view = notepad.getCurrentView()
            active_tab_index = notepad.getCurrentDocIndex(active_view)
            for (__, __, index, view) in notepad.getFiles():
                if view == active_view:
                    if index >= active_tab_index:
                        notepad.activateIndex(active_view, index)
                        self.active_tab_color_set_to_pinned_color(False)
            notepad.activateIndex(active_view, active_tab_index)

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

    def mb(self, msg, flags=0, title=''):  # a message-box function
        return notepad.messageBox(msg, title if title else self.this_script_name, flags)

    def yes_no(self, question_text):  # returns True(Yes), False(No)
        answer = self.mb(question_text, MESSAGEBOXFLAGS.YESNO, self.this_script_name)
        return True if answer == MESSAGEBOXFLAGS.RESULTYES else False

    def debugging_on(self): return (self.debug_on or os.path.isfile(self.turn_debug_on_file)) and not os.path.isfile(self.turn_debug_off_file)

    def dprint(self, *args, **kwargs):  # debug print function
        if self.debugging_on():
            kwargs['debug'] = True
            self.print(*args, **kwargs)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        tpm
    except NameError:
        tpm = TPM()
    else:
        tpm.toggle_tab_pin_state()
