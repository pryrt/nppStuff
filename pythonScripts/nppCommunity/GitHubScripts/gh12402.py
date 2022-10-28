# -*- coding: utf-8 -*-
from __future__ import print_function

# references:
#  https://github.com/notepad-plus-plus/notepad-plus-plus/issues/12402 "[Feature Request] Option in Search>Find for ignoring whitespace characters in search string."

from Npp import *
import inspect
import os
import ctypes
from ctypes.wintypes import (HWND, UINT, WPARAM, LPARAM)

#-------------------------------------------------------------------------------

user32 = ctypes.WinDLL('user32')
BM_CLICK = 0x00F5
SendMessage = user32.SendMessageW
LRESULT = LPARAM
SendMessage.restype = LRESULT
SendMessage.argtypes = [ HWND, UINT, WPARAM, LPARAM ]

#-------------------------------------------------------------------------------

class PFFIW(object):

    def __init__(self):

        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]
        text = editor.getSelText()
        input = self.prompt('Enter search string, possibly containing arbitrary whitespace:', text)
        if input == None or len(input) == 0: return  # user cancel
        token_list = []
        for char in input.strip():
            if char in ' \t':
                continue  # drop space or tab
            elif char in r'([][\.^$*+?(){}\\|-])':
                token_list.append('\\' + char)  # escape regex metachar
            else:
                token_list.append(char)
        findwhat_regex = r'\h*'.join(token_list)
        notepad.menuCommand(MENUCOMMAND.SEARCH_FIND)
        find_window_hwnd = user32.FindWindowExW(None, None, u'#32770', u'Find')
        regex_radio_hwnd = user32.GetDlgItem(find_window_hwnd, 1605)
        SendMessage(regex_radio_hwnd, BM_CLICK, 0, 0)
        find_what_edit_hwnd = user32.GetDlgItem(find_window_hwnd, 1601)
        user32.SetWindowTextW(find_what_edit_hwnd, unicode(findwhat_regex, 'utf-8'))

    def prompt(self, prompt_text, default_text=''):
        if '\n' not in prompt_text: prompt_text = '\r\n' + prompt_text
        prompt_text += ':'
        return notepad.prompt(prompt_text, self.this_script_name, default_text)

#-------------------------------------------------------------------------------

if __name__ == '__main__': PFFIW()
