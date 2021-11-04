# encoding=utf-8
""" pyscReplaceBackslashSequence

When run, this script will search backwards from the current cursor position,
looking for a backslash \ .  If it finds intervening whitespace (tab, space,
newline, NUL), it will abort the search.  If it finds a sequence of \ to the
current cursor without whitespace interruption, it will try to interpret that
as a "shortcut sequence", and try to interpret that.  It will ignore any text
after the current position, so careful placement of the cursor when running
this script will allow inserting a character in between other text

For now, it recognizes shortcuts of the form
* \uXXXX or \u+XXXX or \0xXXXX, all three of which will be replaced by the
    unicode character at the hexadecimal codepoint XXXX.
    * EXAMPLE: \u+2611 => ☑
    * EXAMPLE: |\U+2611other| => |☑other| if the cursor is between 1 and o
* FUTURE: I might do other snippets or shorcuts; however, after learning of the
    nppQuickText plugin, which VinsWorldcom/VincentMichael converted to 64-bit
    and did fixes for at https://github.com/vinsworldcom/nppQuickText, I am not
    sure anything more is needed

Assumes UTF8 encoding of the file (or, rather, that getText/getTextRange returns a series
of UTF-8 octets).

Work inspired by to https://notepad-plus-plus.org/community/topic/18873/ .

I know it had been asked previously, similar to https://community.notepad-plus-plus.org/post/37979 (keyboard map chords, like ^X^C, or eko's ^K^L)
    -- but that one seems to watch every keystroke, which is more than I want.

I actually wanted it to be more like MS Word's Alt+X functionality, where if you type the 4-digit hex for a unicode, then press Alt+X, it will replace those four digits with the unicode character.


"""
from Npp import *
import re

def run_pyscReplaceBackslashSequence():
    """this is the function's doc string"""
    #console.show()
    #console.clear()
    currentCursorPosition = editor.getCurrentPos()

    foundstartpos = -1
    searchpos = currentCursorPosition
    #console.write(__file__ + "::" + __name__ + "::{}..{}".format(searchpos, currentCursorPosition) + "\n")
    while searchpos > 0:
        searchpos -= 1
        c = editor.getCharAt(searchpos)
        if c<0:
            # utf8: first byte&0xC0 is 0xC0; subsequent bytes in the char are 0x80
            # thus, step backword a byte while those aren't start-byte
            while searchpos>0 and c & 0xc0 != 0xc0:
                searchpos -= 1
                c = editor.getCharAt(searchpos)
                q = editor.positionAfter(searchpos)
                #s = "searching"
                #console.write("\t{}: {}..{}\n".format(s, searchpos, q))

            #s = "found"
            #console.write("\t{}: {}..{}\n".format(s, searchpos, q))
            s = editor.getTextRange(searchpos,q).decode('utf-8')
            if len(s)==1:
                c = ord(s)
            elif len(s)==2:
                c = 0x10000 + (ord(s[0]) - 0xD800) * 0x400 + (ord(s[1]) - 0xDC00)
            else:
                c = ord(s)  # will probably give an exception

        elif c>255:
            console.writeError("unknown character {} while searching for \\".format(c))
            s = unichr(c)   # should probably create an exception

        else:
            s = unichr(c)

        #info = "#{0:5}# '{2}' = HEX:0x{1:04X} = DEC:{1} ".format(searchpos, c, s.encode('utf-8') if c not in [13, 10, 0] else 'LINE-ENDING' if c != 0 else 'END-OF-FILE')
        #console.write(info + "\n")

        if c in [0, 10, 13, 8, 32]: # nul, newline, horizontal whitespace
            foundstartpos = -1
            break

        if s == '\\':
            foundstartpos = searchpos
            break

    #console.write(__file__ + "::" + __name__ + "::{}..{}..{}".format(foundstartpos, searchpos, currentCursorPosition) + "\n")

    if foundstartpos<0:
        return

    editor.setSel(foundstartpos, currentCursorPosition)
    s = editor.getTextRange(foundstartpos, currentCursorPosition)
    #console.write("\n\n" + "FOUND: '{}'\n".format(s) + "\n\n")

    # OK: look for unicode escapes: ☑
    # \u2611
    # \U+2611
    # \0x2611
    editor.beginUndoAction();
    editor.rereplace( r'\\(?:u\+?|0x)([0-9A-F]{4})', lambda m : unichr( int(m.group(1), 16) ).encode('utf-8') , re.IGNORECASE, foundstartpos, currentCursorPosition)
    editor.endUndoAction();

    # TODO: lookup the found text in the shortcuts ini file, or wherever it is


if __name__ == '__main__': run_pyscReplaceBackslashSequence()