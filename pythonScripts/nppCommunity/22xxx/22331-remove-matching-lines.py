# encoding=utf-8
""" in response to https://community.notepad-plus-plus.org/topic/22331/multiple-search-and-remove

You can run this script, and it will delete all the lines in the active file that contain
that text (even if it's as a substring).  You can comment/uncomment lines in the script
to make it match only whole lines (so the string "blah" would only match "blah", not "something blah something")

You could modify it to read editor2 contents and then delete matching lines in editor1, but
I will leave that as an exercise for the reader.

Populate the list_of_strings array below, then run this script.  The text in each line will be
treated as a literal string, so regex characters will not be treated as regex (ie, dot will
match a dot, not any single character).
"""

class forum_post22331:
    list_of_strings = [
        'MTkxMTMxOTkyMzcxNzg5ODcy.B3G_W0.pOFRk4TGe_SPNUhKrb58IVJvty6',
        'ODY5NjU0MDYwNzkyOTM5NTEw.XqCHPX.bNW7X8fayguYEnVBmRkMvejlG4s',
        'MjY4MzU4MjQwMTMyMTE3ODky.HlytHz.JOehsSFExPn1T_7RkoQq8LrZwjK',
        'NDY4MTMxOTg5NjE2NjI1NjUz.ZvEGgz.3tHiZ80sc64WyQV5fr-Fklhax_O',
        'NjUwNzM1Mzc3MzA0MDk1OTgd.Pr75Ph.JtTLUwxZWHaqc5jmvoueS0h6KGY',
        'MTgzNTY4ODkyODAxMDMwOTE5.FKIb9Z.41SZmRhuPVXYAtienEsH2pG6075'
    ]

    def runme(self):
        editor.beginUndoAction()

        for search_string in self.list_of_strings:
            # uncomment the regex_string below that matches your desired behavior:
            regex_string = r'(?-is)^.*\Q' + search_string + '\E.*$(\R|\Z)'      # match the string anywhere on the line in the active file
            #regex_string = r'(?-is)^\Q' + search_string + '\E$(\R|\Z)'          # match the string only if it matches the whole line in the active file
            editor.rereplace(regex_string, "")

        editor.endUndoAction()

if __name__ == '__main__': forum_post22331().runme()
