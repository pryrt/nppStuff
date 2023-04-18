''' Basic functionality which one would expect from a full-fledged IDE

By: Notepad++ Community Forum member: @Michael-Vincent (aka vinsworldcom@perlmonks)

https://community.notepad-plus-plus.org/topic/20340/perl-subroutine-calltips-with-pythonscript


'''

import re
from Npp import (
    editor, notepad, console,
    SCINTILLANOTIFICATION, NOTIFICATION, LANGTYPE
    )

class PerlIDE(object):

    def __init__(self):
        self.is_perl = False
        self.excluded_styles = [1, 3, 4, 6, 7, 12, 16, 17, 18, 19]


    def initialize(self):
        #console.write("PerlIDE: initializing\n")
        editor.callbackSync(self.on_charadded, [SCINTILLANOTIFICATION.CHARADDED])
        notepad.callback(self.on_buffer_activated, [NOTIFICATION.BUFFERACTIVATED])
        self.is_perl = notepad.getCurrentLang() == LANGTYPE.PERL


    def on_buffer_activated(self, args):
        self.is_perl = notepad.getCurrentLang() == LANGTYPE.PERL
        self.path = notepad.getCurrentFilename()
        #console.write("PerlIDE: buffer activated: {} {}\n".format(self.is_perl, self.path))


    def on_charadded(self, args):
        if self.is_perl:
            #console.write("PerlIDE: CHAR ADDED TO PERL\n");
            c = chr(args['ch'])
            if c in '\r\n:-+*/#=)':
                return

            pos = editor.getCurrentPos()
            if editor.getStyleAt(pos) in self.excluded_styles:
                return

            if c == '(':
                # subName will contain the subroutine's name from the current typing line
                # by finding the last open paren `(` and then capturing the word (\w+)
                # before.  For example:
                #     if ( not defined( $session = getCMSession(
                # should capture `getCMSession`
                subName = '\0'
                callTip = ""
                line = editor.getCurLine()
                # sub = re.search(r'^.*[\s\t\=](\w+)\s*\(', line)
                # sub = re.search(r'^.*[\s\t\=]\s*(?:\w+(?:\:\:|\'|->))*(\w+)\s*\(', line) # 2021-Oct-26: allow method calls, package functions, etc
                sub = re.search(r'^.*\b(\w+)\s*\(', line) # 2021-Oct-26: limit it less: just require boundary-word-optionalSpace-paren, so will allow the function call to be the first characters on a line, too
                if sub:
                    subName = sub.group(1)
                else:
                    return

                # get the entire file into an array, 1 file line per array index
                lines = editor.getText().split("\n")

                # find the start of the sub, form example above, we're looking for
                # something like:
                #   sub getCMSession {
                myMatchString = r"^\s*sub\s+{}\s*".format(subName)
                start = 0
                for line, text in enumerate(lines):
                    match = re.search(myMatchString, text)
                    if match:
                        start = line
                        break
                search = lines[start+1:]

                # new array `search` now starts at the line after the subroutine start
                # we need to find the start of the next sub so we know where to stop
                # searching.  The next sub starts at a line like:
                #     "sub "
                # without the double-quotes, but the 'sub' must be followed by
                # some whitespace
                myMatchString = r'^\s*sub\s+'
                end = None
                for line, text in enumerate(search):
                    match = re.search(myMatchString, text)
                    if match:
                        end = line
                        break
                if end is None:
                    # use the whole search array if the end of the sub wasn't found
                    sub = search
                else:
                    sub = search[0:end]

                # the new array `sub` now contains each line of the full subName
                # subroutine's code, let's search for a function signature looking thing
                for line, text in enumerate(sub):
                    match = re.search(r'^\s*my\s+.*\s*\=\s*\@\_\;', text)
                    if match:
                        callTip = match.group(0)
                        editor.callTipShow(pos, callTip)
                        break
