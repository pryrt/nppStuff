# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/22410/

This will apply simple (non-nested) folding to the active file.

It will apply a start_regex and end_regex, which define the start and
end of your "block" of LOGFILE that is meant to be folded.
The first time you run, it will set up all the folding based on those
regex; you can then use Notepad++'s fold/unfold mechanism to fold/unfold
those blocks.  The next time you run, it will clear the folding.  Repeat
as necessary.

Right now, this is _on demand_, not _on edit_, so if you edit your logfile,
the

Please note that if your file type already has an associated Lexer (programming Language)
or UDL (user defined language), these folds will conflict with the Lexer/UDL folding,
with unpredictable results.  Mix with caution.

___INSTRUCTIONS____

INSTALL:
0. If PythonScript is not yet installed,
    * Plugins > Plugins Admin
    * Check the ☑ PythonScript checkbox
    * Click INSTALL
1. Create an empty script:
    * Plugins > Python Script > New Script
    * Make sure the folder selected is
        `...notepad++\plugins\Config\PythonScript\scripts`
    * give it a name like LogFolding.py
2. Paste this whole script (including these instructions)
    into the file, and save
3. Edit the start_regex and end_regex right here:
"""
start_regex = r'^\d+:\d+:\d+,\d+ ERROR'
end_regex = r'more\R{2,}'
"""
    These need to be boost-compatible regular expressions

RUN:
1. Plugins > PythonScript > Scripts > LogFolding.py
or use the keyboard shortcut defined below

KEYBOARD SHORTCUT:
1. Plugins > PythonScript > Configuration
2. In the User Scripts, click on LogFolding.py
3. Click the left ADD button (above Menu Items)
    * This adds "LogFolding" to the main Plugins > PythonScript menu, rather
      than requiring you to dig down into the Scripts submenu
4. Exit Notepad++ and restart
    * This is required for ShortcutMapper to be able to see the new entry
      in the PythonScript menu
5. Settings > ShortcutMapper > Plugin Commands
6. Filter by LogFolding
7. Click on LogFolding, then click the MODIFY button and
    set the keyboard shortcut in the dialog
"""
from Npp import *
from time import sleep

class topic22410_LogFolder(object):
    OUTSIDE = "OUTSIDE"
    INSIDE = "INSIDE"
    HEADER = "HEADER"
    _DEBUG_ = False

    def __init__(self, my_file):
        self.matching = topic22410_LogFolder.OUTSIDE
        self.folding_defined = False
        self.file = my_file
        self.editor = editor    # store the active editor
        if notepad.getLangType() == LANGTYPE.TXT:
            notepad.setLangType(LANGTYPE.USER)
            sleep(0.1)
        if topic22410_LogFolder._DEBUG_: console.write("Create folder[{}]\n".format(self.file))
        self.toggle_folds()

    def toggle_folds(self):
        self.folding_defined = not self.folding_defined
        if topic22410_LogFolder._DEBUG_: console.write(".toggle_folds() to {}\n".format(self.folding_defined))
        self.clear_folds()
        if self.folding_defined: self.make_folds()
        if topic22410_LogFolder._DEBUG_: console.write(".toggle_folds() done\n")

    def clear_folds(self):
        if topic22410_LogFolder._DEBUG_: console.write(".clear_folds() running\n")
        self.editor.forEachLine(lambda c,l,t: self.editor.setFoldLevel(l,0x400))
        if topic22410_LogFolder._DEBUG_: console.write(".clear_folds() done\n")

    def make_folds(self):
        #self.editor.setFoldLevel(0, 0x2400)
        #self.editor.setFoldLevel(1, 0x0401)
        if topic22410_LogFolder._DEBUG_: console.write(".make_folds() running\n")
        self.editor.forEachLine(self._per_line)
        if topic22410_LogFolder._DEBUG_: console.write(".make_folds() done\n")

    def _per_line(self, content, line_index, total_lines):
        p1 = self.editor.positionFromLine(line_index)
        p2 = self.editor.getLineEndPosition(line_index)
        pe = self.editor.getLength()
        #console.write("checking __{}__: ({}..{}) =~ {}\n".format(1+line_index, p1, p2, start_regex))
        self.editor.research(
            start_regex,
            lambda m: self._line_matches(m, line_index, topic22410_LogFolder.HEADER),
            0,      # flags
            p1,p2,  # start/end position
            1       # match just one instance
        )
        if self.matching == topic22410_LogFolder.HEADER:
            # since this line is header,
            # set the folding to header-state (0x2400)
            self.editor.setFoldLevel(line_index, 0x2400)
            #console.write("\tHEADER @ {}\n".format(line_index))

            # but as soon as we're done with the header,
            # the state is now INSIDE
            self.matching = topic22410_LogFolder.INSIDE
        elif self.matching == topic22410_LogFolder.INSIDE:
            # since this line is INSIDE, need to set folding to 0x0401
            self.editor.setFoldLevel(line_index, 0x0401)
            #console.write("\tINSIDE @ {}\n".format(line_index))
        elif self.matching == topic22410_LogFolder.OUTSIDE:
            # once we are outside, we don't need to change the
            # state of the active line, because it was already reset
            #console.write("\tOUTSIDE @ {}\n".format(line_index))
            pass

        self.editor.research(
            end_regex,
            lambda m: self._line_matches(m, line_index, topic22410_LogFolder.OUTSIDE),
            0,      # flags
            p1,pe,  # start/end position: for end_regex, match to end-of-file rather than just the single line
            1       # match just one instance
        )

        #console.write("\t{:<7s}\tlevel={:#06x}\n".format('__{}__'.format(line_index),self.editor.getFoldLevel(line_index)))


    def _line_matches(self, m, line_index, match_state):
        pos_eol = self.editor.getLineEndPosition(line_index)
        #console.write("MATCH {}:\t__{}__:({}..{}): {}[EOL={} {}]\n".format(match_state,line_index,m.start(0),m.end(0),m.group(0).strip(),pos_eol,m.start(0)<=pos_eol))
        if m.start(0) <= pos_eol: # end of match must be before EOL to change state
            self.matching = match_state


if __name__ == "__main__":
    my_file = notepad.getCurrentFilename()
    try:                                # see if dictionary and key exist, and try to toggle
        folderObjects[my_file].toggle_folds()
    except NameError:                   # if dictionary not yet initialized
        #console.clear()
        folderObjects = {}              #   create the dictionary
                                        #   and populate key
        folderObjects[my_file] = topic22410_LogFolder(my_file)
    except KeyError:                    # if dictionary key does not yet exist
                                        #   then populate key
        folderObjects[my_file] = topic22410_LogFolder(my_file)
