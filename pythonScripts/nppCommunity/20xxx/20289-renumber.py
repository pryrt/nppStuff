""" https://community.notepad-plus-plus.org/topic/20289/find-replace-number-with-increment-value/6
"""

prev = None
def renumber(m):
    global prev
    if prev == None:
        prev = int(m.group(2))
    else:
        prev = prev + 1

    return m.group(1) + str(prev) + m.group(3)

editor.rereplace(r'^(\[#)(\d+)(\])', renumber);

"""
[#34]
T=2
F=INITIALKEY
None=E maj
None=12B
None=0|0

[#1]
T=2
F=INITIALKEY
None=Gm
None=1A
None=0|0

[#2]
T=2
F=INITIALKEY
None=A\u266dm
None=1A
None=0|0
"""
