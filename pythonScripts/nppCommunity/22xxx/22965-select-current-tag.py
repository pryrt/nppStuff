# encoding=utf-8
""" selectCurrentTag: in response to https://community.notepad-plus-plus.org/topic/22965/copy-entire-code-group

Starts at the current position; looks to see if it's `<open`, `</close`, or neither.  If not neither, then search for the balanced pair and

"""

from Npp import editor, notepad, console
console.show()

class SelectCurrentTag(object):
    class TAGTYPE(object):
        OPEN = 'OPEN'
        CLOSE = 'CLOSE'
        OTHER = None

    #def __init__(self):
    #    self.oldPos = editor.getCurrentPos()
    #    console.write("SelectCurrentTag: initialized\n")

    def getTagWord(self):
        self.oldPos = editor.getCurrentPos()
        self.tagword = editor.getCurrentWord()

        self.tagtype = self.TAGTYPE.OTHER

        self.wordtagpos = [None,None]
        direction = 0
        searchpos = self.oldPos
        #console.write(__file__ + "::" + __name__ + "::{}..{}".format(searchpos, self.oldPos) + "\n")
        while searchpos > 0 and searchpos < editor.getLength():
            c = editor.getCharAt(searchpos)
            if c<0:
                # utf8: first byte&0xC0 is 0xC0; subsequent bytes in the char are 0x80
                # thus, step backword a byte while those aren't start-byte
                while searchpos>0 and c & 0xc0 != 0xc0:
                    searchpos -= 1
                    c = editor.getCharAt(searchpos)
                    q = editor.positionAfter(searchpos)
                    #console.write("\t{}: {}..{}\n".format("searching", searchpos, q))

                #console.write("\t{}: {}..{}\n".format("found", searchpos, q))
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

            if c in [0, 10, 13, 8, 32] and direction==0: # nul, newline, horizontal whitespace not allowed when searching for start of the current open/close tag
                self.wordtagpos[direction] = None
                self.tagtype = self.TAGTYPE.OTHER
                break

            if s == '<' and direction==0:
                self.wordtagpos[direction] = searchpos
                if editor.getTextRange(searchpos+1,searchpos+2) == '/':
                    self.tagtype = self.TAGTYPE.CLOSE
                else:
                    self.tagtype = self.TAGTYPE.OPEN

                # since I found it, start from original and change direction
                searchpos = self.oldPos - 1
                direction = 1 # was: break

            if s == '>' and direction==1:
                self.wordtagpos[direction] = searchpos+1  # include the '>'
                if self.tagword == '':

                    def assn(m):
                        self.tagword = m.group(1)
                        #console.write("assn called: 0:'{}' 1:'{}'\n".format(m.group(0), m.group(1)))

                    editor.research(r'</?(\w+).*?>', lambda m: assn(m), 0, self.wordtagpos[0], self.wordtagpos[1], 1)
                    pass
                break

            # if not found yet, go back a character and loop
            searchpos += (2*direction-1)    # so direction==0 will subtract 1, direction==1 will add 1

        #console.write("SelectCurrentTag: {:d}..{:d}..\n".format(foundstartpos, self.oldPos))

        return self.tagword, self.tagtype

    def selectFromOpen(self):
        editor.setSelection( self.wordtagpos[0], editor.getLength() )
        # TODO: actually find the next close tag (or eventually, matching close tag)

    def selectToClose(self):
        editor.setSelection( 0, self.wordtagpos[1] )
        # TODO: actually find the previous open tag (or eventually, matching open tag)

    def go(self):
        self.getTagWord()
        console.write("SelectCurrentTag: tagword='{:s}' tagtype={:s} oldPos={:d} wordtagpos={}\n".format(self.tagword, self.tagtype, self.oldPos, self.wordtagpos))
        if self.tagtype == self.TAGTYPE.OPEN:
            self.selectFromOpen()
            pass
        elif self.tagtype == self.TAGTYPE.CLOSE:
            self.selectToClose()
            pass
        else:   # no matching tag found, so don't select anything new
            editor.setSelection( self.oldPos, self.oldPos )
            pass

SelectCurrentTag().go()

"""
<div class="1">
    <p>...</p>
    <div class="2">
        <p>...</p>
        <div class="3">
        ...
        </div>
    </div>
</div>
"""