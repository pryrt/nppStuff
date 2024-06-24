# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25902/"""
from Npp import notepad,console,editor1
editor = None

def _doit():
    #console.clear()
    #console.show()
    linemap = {}
    for l in range(editor1.getLineCount()):
        p = editor1.positionFromLine(l)
        linemap[p] = l

    # console.write(str(linemap)+"\n\n")

    def match_found(m):
        s = m.start()
        p = s
        l = None

        # console.write("match start={} p={} line={} [before p search]\n".format(s,p,l))

        while p>0:
            # console.write("{} => {}\n".format(p, p in linemap))
            if p in linemap:
                l = linemap[p]
                break
            else:
                p = p - 1

        # console.write("match start={} p={} line={}\n".format(s,p,l))
        editor1.markerAdd(l,20)

    editor1.search("!HERE!", match_found)

_doit()
del(_doit)
