# see https://notepad-plus-plus.org/community/topic/16597/how-to-open-a-path-in-windows-explorer
#   Author: Scott Sumner (received in 2019-Jan-25 email)

# ideas for future extension:
#  if a group of lines is selected, open the file on each line

import re
import os
import subprocess

def OFOFAC__main():

    explorer_format_str = 'explorer.exe "{}"'

    if editor.getSelections() == 1 and not editor.getSelectionEmpty():

        # selection is active; try to open only exactly what the selecton says

        path_to_try = os.path.expandvars(editor.getTextRange(editor.getSelectionStart(), editor.getSelectionEnd()).strip('"'))
        # note expandvars will resolve things like %USERPROFILE%, %TEMP% etc.

        if os.path.isfile(path_to_try):
            notepad.open(path_to_try)
        elif os.path.isdir(path_to_try):
            subprocess.Popen(explorer_format_str.format(path_to_try))

        return

    open_folder_at_or_left_of_caret = False
    if 1:  # change 1 to 0 if this script is bound to a keycombo for running instead of running from menu, toolbar button, or right-click context menu
        import ctypes
        GetKeyState = ctypes.windll.user32.GetKeyState
        VK_LSHIFT = 0xA0
        open_folder_at_or_left_of_caret = True if ((GetKeyState(VK_LSHIFT) & 0x8000) == 0x8000) else False

    cp = editor.getCurrentPos()
    lfp = editor.lineFromPosition(cp)
    pfl = editor.positionFromLine(lfp)

    current_line_contents = editor.getLine(lfp).rstrip()  # rstrip removes line-ending and any trailing spaces
    curr_line_left_of_caret = current_line_contents[: cp - pfl]
    curr_line_right_of_caret = current_line_contents[cp - pfl :]

    # first try left and right from caret to first space as the path to open
    # next try left and right from caret to first double quote as the path to open:
    for delim in (' ', '"'):  # a space or a double-quote could be a delimiter for either end of a pathname; look for space first as it is more(?) likely

        path_boundary_regex = r'[^ "]*' if delim == ' ' else r'[^"]*'
        left_part = os.path.expandvars(curr_line_left_of_caret[ -len((re.match(path_boundary_regex, curr_line_left_of_caret[::-1])).group(0)) : ].replace('/', '\\'))
        right_part = os.path.expandvars(curr_line_right_of_caret[ : len((re.match(path_boundary_regex, curr_line_right_of_caret)).group(0)) ].replace('/', '\\'))
        path_to_try = os.path.expandvars(left_part + right_part)  # calling expandvars here again because user could conceivably had caret in the middle of an e-var when invoking (is this likely?)

        if open_folder_at_or_left_of_caret:

            folder_path_to_try = None
            if os.sep in right_part: folder_path_to_try = left_part + right_part[ : right_part.find(os.sep)]
            elif os.sep in left_part: folder_path_to_try = left_part[ : left_part.rfind(os.sep)]
            if folder_path_to_try != None and os.path.isdir(folder_path_to_try):
                subprocess.Popen(explorer_format_str.format(folder_path_to_try))
                return

        else:

            if os.path.isfile(path_to_try):
                notepad.open(path_to_try)
                return
            elif os.path.isdir(path_to_try):
                subprocess.Popen(explorer_format_str.format(path_to_try))
                return

    # as a last resort (if we haven't returned yet) try entire line (without any leading/trailing whitespace) as the path to open:
    if not open_folder_at_or_left_of_caret:

        path_to_try = os.path.expandvars(current_line_contents.lstrip().strip('"'))

        if os.path.isfile(path_to_try):
            notepad.open(path_to_try)
            return
        elif os.path.isdir(path_to_try):
            subprocess.Popen(explorer_format_str.format(path_to_try))
            return

OFOFAC__main()
