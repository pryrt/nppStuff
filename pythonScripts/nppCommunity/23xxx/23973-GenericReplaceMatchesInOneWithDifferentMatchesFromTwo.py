# encoding=utf-8
"""inspired by https://community.notepad-plus-plus.org/topic/23973/

The basic goal of the 23973 post is to take matches from file2 using re_src,
and use that value as the next replacement for matches a file1 replacement re_dst.

Not knowing whether the OP has two formatted files, or whether file2
is just a long list, I decided to make it as generic as possible,
but to default the expression for re_src to r'^.*?$' (that is,
to grab each line from file2, without newlines, to be inserted into matches
of re_dst in file1).

    The algorithm can then be:
    - for each match in file1
        - find the next match in file2
        - replace the file1 match with file2 match

I think this will make it as generic as possible.
"""
from Npp import editor,notepad,console

class RMIOWDMFT(object):
    def __init__(self):
        console.write("pass")
        pass

RMIOWDMFT()
