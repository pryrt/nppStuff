# encoding=utf-8
""" in response to https://community.notepad-plus-plus.org/topic/22331/multiple-search-and-remove

You can run this script, and it will delete all the lines in the active file that contain
that text (even if it's as a substring).  You can comment/uncomment lines in the script
to make it match only whole lines (so the string "blah" would only match "blah", not "something blah something")

Modified to read other view's contents and then delete matching lines in active view

Populate the list_of_strings array below, then run this script.  The text in each line will be
treated as a literal string, so regex characters will not be treated as regex (ie, dot will
match a dot, not any single character).
"""

class forum_post22331:
    list_of_strings = []
    active_editor = None
    file2_editor = None

    def __init__(self):
        self.active_editor = editor1 if notepad.getCurrentView()==0 else editor2
        self.file2_editor  = editor2 if notepad.getCurrentView()==0 else editor1

    def runme(self):
        editor.beginUndoAction()

        for file2_line_num in range(self.file2_editor.getLineCount()):
            file2_line_str = self.file2_editor.getLine(file2_line_num).rstrip()
            if len(file2_line_str)>0:
                self.list_of_strings.append(file2_line_str)

        for search_string in self.list_of_strings:
            # uncomment the regex_string below that matches your desired behavior:
            regex_string = r'(?-is)^.*\Q' + search_string + '\E.*$(\R|\Z)'      # match the string anywhere on the line in the active file
            #regex_string = r'(?-is)^\Q' + search_string + '\E$(\R|\Z)'          # match the string only if it matches the whole line in the active file
            editor.rereplace(regex_string, "")

        editor.endUndoAction()

if __name__ == '__main__': forum_post22331().runme()
