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
from Npp import editor,notepad,console, MESSAGEBOXFLAGS

class RMIOWDMFT(object):
    def __init__(self):
        self.srcPos = 0 # will start the search in the source document at location 0

        # 1. prompt for correct file orientation (destination is active, source is other view)
        msg = """
        The destination file (file to be edited) should be in the active view.
        The source file (read only) should be in the other view

        Hit OK if this is correct.

        Hit CANCEL if you need to move the source file to the other view
            - View > Move/Clone Current Document > Move to Other View
              (or equivalent from Tab Right Click context menu)
            - Re-run this script
        """
        if MESSAGEBOXFLAGS.RESULTCANCEL == notepad.messageBox(msg, "Prepare Source and Destination Files", MESSAGEBOXFLAGS.OKCANCEL):
            return

        self.editor_dst = editor1 if notepad.getCurrentView()==0 else editor2
        self.editor_src = editor2 if notepad.getCurrentView()==0 else editor1

        # 3. prompt for regex for the source file re_src: default to r'^.*?$'
        msg = "Please enter a valid regex for the source file (CANCEL will exit script):"
        self.re_src = notepad.prompt(msg, "Regex for Source file", r'(?-s)^Replacement \d+$') # r'(?-s)^.*?$')
        if None is self.re_src:
            return
        #console.write("src regex: r'{}'\n".format(self.re_src))

        # 4. prompt for regex for the destination file re_dst
        msg = "Please enter a valid regex for the destination file (CANCEL will exit script):"
        self.re_dst = notepad.prompt(msg, "Regex for Searching Destination file", r'^\h*txt: \K.*?$')
        if None is self.re_dst:
            return
        #console.write("dst regex: r'{}'\n".format(self.re_dst))

        # 5. Confirm before running
        msg = """
        Please confirm that you want to replace text that matches
            {}
        from the destination file with text that matches
            {}
        from the source file
        """.format(self.re_dst, self.re_src)
        if MESSAGEBOXFLAGS.RESULTYES == notepad.messageBox(msg, "Confirm Running Search/Replace", MESSAGEBOXFLAGS.YESNO):
            self.editor_dst.rereplace(self.re_dst, lambda m: self.replace_each_match_in_destination(m))

        pass

    def match_in_source(self, m):
        #console.write("src[{:4d}..{:<4d}]\t{}\n".format(m.start(0), m.end(0), m.group(0)))

        if m.start(0) >= (self.editor_src.getLength()-1):
            self.src_match = None
            return

        self.src_match = m.group(0)
        self.srcPos = m.end(0)

        t = self.editor_src.getTextRange(self.srcPos, self.srcPos+2)
        o = self.editor_src.getTextRange(self.srcPos, self.srcPos+1)
        if t == "\r\n":
            self.srcPos += 2
        elif o in ("\r", "\n"):
            self.srcPos += 1

    def replace_each_match_in_destination(self, m):
        #console.write("dst[{:4d}..{:<4d}]\t'{}'\n".format(m.start(0), m.end(0), m.group(0)))
        self.src_match = None
        self.editor_src.research(self.re_src, lambda m: self.match_in_source(m), 0, self.srcPos, -1, 1)
        #console.write("-> src_match = '{}'\n".format(self.src_match))
        return m.group(0) if self.src_match is None else self.src_match

RMIOWDMFT()

"""
Dummy SRC:
Replacement 1
In Between
Replacement 2
In Between
Replacement 3
"""

"""
Dummy Destination:
txt: one
other: keep
txt: two
other: keep
txt: 3
txt: 4
txt: 5
txt: 6
txt: 7
txt: 8
txt: 9
"""
