from Npp import *

count = 0

def add_1(m):
    global count
    count += 1
    kamal = m.group().rstrip()
    return kamal + "\r\n" + 'printf("' + kamal + ' log ' + str(count) + ' x=%d\\n", x);'

editor.rereplace(r'(?-s)^.+$', add_1);

