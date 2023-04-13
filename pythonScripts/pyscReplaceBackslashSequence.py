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
* &#D+;? (where D+ is one or more decimal digit): convert HTML decimal entity (added 2023-Mar-08)
* &#xX+;? (where X+ is one or more hex digit): convert HTML hex entity (added 2023-Mar-08)
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

2023-Mar-08: add &# and &#x for up to &#xFFFF
2023-Apr-13: added surrogate pair, so now it can handle U+0000 to U+10FFFF in _any_ of the notations, which is the whole unicode range; add \\x{123456} notation as well

"""
from Npp import *
import re

def run_pyscReplaceBackslashSequence():
    """this is the function's doc string"""
    DEBUG=False
    if DEBUG:
        console.show()
        console.clear()
    currentCursorPosition = editor.getCurrentPos()

    foundAmpersand = False
    foundstartpos = -1
    searchpos = currentCursorPosition
    s_prev = None
    if DEBUG: console.write(__file__ + "::" + __name__ + "::{}..{}".format(searchpos, currentCursorPosition) + "\n")
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
                if DEBUG:
                    s = "searching"
                    console.write("\t{}: {}..{}\n".format(s, searchpos, q))

            if DEBUG:
                s = "found"
                console.write("\t{}: {}..{}\n".format(s, searchpos, q))
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

        if DEBUG:
            info = "#{0:5}# '{2}' = HEX:0x{1:04X} = DEC:{1} ".format(searchpos, c, s.encode('utf-8') if c not in [13, 10, 0] else 'LINE-ENDING' if c != 0 else 'END-OF-FILE')
            console.write(info + "\n")

        if c in [0, 10, 13, 8, 32]: # nul, newline, horizontal whitespace
            foundstartpos = -1
            break

        if s == '\\':
            foundstartpos = searchpos
            break

        # check for HTML &# and &#x encodings:
        if (s_prev is not None) and (s_prev == "#") and (s == "&"):
            foundstartpos = searchpos
            foundAmpersand = True
            break

        # store previous values
        s_prev = s

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
    # \x{2611}
    # &#9745;
    # &#x2611;
    # and some others to test surrogates
    # &#x1f644;
    # &#128570;
    # \x{1f644}
    # \U+1F923
    # \u1F4A6
    # \u10FFFD  -- last valid
    # \u10FFFE  -- shows four bytes
    # \u10FFFF  -- shows four bytes
    # \u110000  -- too high
    # \u123456  -- too high

    def _replc(CP, orig):
        if DEBUG: console.write( "#REPLC# '{:s}' => int:{:d}\n".format(orig, CP) )
        if CP < 0x10000:
            return unichr(CP).encode('utf-8')
        elif CP < 0x110000:
            # convert to surrogates
            L = 0xDC00 + (CP & 0x3FF)
            H = 0xD800 + (((CP-0x10000)>>10)&0x3FF)
            surrogate_pair = unichr(H) + unichr(L)
            if DEBUG: console.write( "#REPLC# '{:s}' => H=0x{:04X} L=0x{:04X} => '{:s}'\n".format(orig, H, L, surrogate_pair.encode('utf-8')) )
            return surrogate_pair.encode('utf-8')
        else:
            console.writeError("escape sequence '{:s}' is not known: codepoint=0x{:x} should be from 0 to 0x{:x}\n".format( orig, CP, 0x10FFFF ))
            return orig

    def b16(m):
        CP = int(m.group(1), 16)
        return _replc(CP, m.group(0))

    def b10(m):
        CP = int(m.group(1))
        return _replc(CP, m.group(0))

    if foundAmpersand:
        editor.rereplace( r'\&#([0-9]+);?', b10 , re.IGNORECASE, foundstartpos, currentCursorPosition)
        editor.rereplace( r'\&#x([0-9A-F]{1,6});?', b16 , re.IGNORECASE, foundstartpos, currentCursorPosition)
    else:
        editor.rereplace( r'\\x{([0-9A-F]{1,6})}', b16 , re.IGNORECASE, foundstartpos, currentCursorPosition)
        editor.rereplace( r'\\(?:u\+?|0x)([0-9A-F]{1,6})', b16 , re.IGNORECASE, foundstartpos, currentCursorPosition)


if __name__ == '__main__': run_pyscReplaceBackslashSequence()
