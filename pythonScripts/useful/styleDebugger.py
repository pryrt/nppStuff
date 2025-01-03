# encoding=utf-8
#
# tracks changes in style in the active file,
# and creates a new plaintext document containing the original file, but indicating style changes with {##}
#   so `{0}ABC{1}D{0}` means `ABC` are in styleID=0, and the `D` is in styleID=1

from Npp import editor,notepad,console

class pyscStyleDebugger(object):
    def onmatch(self,m):
        #console.write("style {} at {}\n".format(m.group(0), m.span(0)))
        editor.startStyling(m.start(0), 0)
        editor.setStyling(m.end(0)-m.start(0), 127)

    def go(self):
        original_pos = editor.getCurrentPos()
        ps = None
        sout = ""
        s_found = []
        skipTo = -1
        for i in range(editor.getTextLength()):
            if i<skipTo: 
                continue
            else:
                skipTo = -1
            s = editor.getStyleIndexAt(i)
            if s not in s_found:
                s_found.append(s)
            if s != ps:
                sout += "{{{}}}".format(s)
                ps = s
            c = editor.getCharAt(i)
            if c<0 or c>255:
                editor.gotoPos(i)
                p = editor.getCurrentPos()
                q = editor.positionAfter(p)
                skipTo = q
                #console.write("X[c:{:06x},i:{},p:{},q:{},skipTo={}]\n".format(c, i, p, q, skipTo))
                try:
                    ch = editor.getTextRange(p,q).decode('utf-8')
                except AttributeError:
                    ch = editor.getTextRange(p,q)
                    alreadyUTF8 = True
                except UnicodeDecodeError:
                    ch = editor.getTextRange(p,q)
                    alreadyUTF8 = True
                    
                if len(ch) != 2:
                    new_c = ord(ch)
                else:
                    new_c = 0x10000 + (ord(ch[0]) - 0xD800) * 0x400 + (ord(ch[1]) - 0xDC00)

                #console.write("Y[c:{:06x},i:{},p:{},q:{},skipTo={}, new_c:{:06x}]\n".format(c, i, p, q, skipTo, new_c))
                try:
                    sout += unichr(new_c)
                except NameError:
                    sout += chr(new_c) # already UTF8
            else:
                sout += chr(c)

        skey = "\n==========\n\nKEY:\n"
        for s in sorted(s_found):
            skey += "{{{:3}}}: {:<40} | {:<40} | {}\n".format(s, editor.nameOfStyle(s), editor.tagsOfStyle(s), editor.descriptionOfStyle(s))

        editor.gotoPos(original_pos)

        notepad.new()
        editor.setText(sout)
        fg0 = editor.styleGetFore(0)
        bg0 = editor.styleGetBack(0)
        fg127 = tuple([int(fg0[x] + (bg0[x]-fg0[x]) * 0.75) for x in range(3)])
        editor.styleSetFore(127, fg127)
        editor.styleSetBack(127, bg0)
        editor.research(r'{\d+}', self.onmatch)
        editor.startStyling(editor.getTextLength(),0)
        editor.appendText(skey)
        editor.setStyling(len(skey), 127)
        editor.setSavePoint()


pyscStyleDebugger().go()
# ±