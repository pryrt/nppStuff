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
        ps = None
        sout = ""
        s_found = []
        for i in range(editor.getTextLength()):
            s = editor.getStyleIndexAt(i)
            if s not in s_found:
                s_found.append(s)
            if s != ps:
                sout += "{{{}}}".format(s)
                ps = s
            c = editor.getCharAt(i)
            sout += chr(c)

        skey = ""
        for s in sorted(s_found):
            skey += "{{{:3}}}: {:<40} | {:<40} | {}\n".format(s, editor.nameOfStyle(s), editor.tagsOfStyle(s), editor.descriptionOfStyle(s))

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
