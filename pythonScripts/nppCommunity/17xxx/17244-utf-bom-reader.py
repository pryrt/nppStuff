# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/16870/

other notes go here
"""
from Npp import *

def forum_post17244_FunctionName():
    console.show()
    console.clear()
    console.write(__file__ + "::" + __name__ + "\n")
    firstBufferID = notepad.getCurrentBufferID()
    for (filename, bufferID, index, view) in notepad.getFiles():
        inf = open(filename, 'rb')
        data_at_start_of_file = inf.read(3)
        inf.close()
        if len(data_at_start_of_file) >= 3 and ord(data_at_start_of_file[0]) == 0xEF and ord(data_at_start_of_file[1]) == 0xBB and ord(data_at_start_of_file[2]) == 0xBF:
            console.write(filename+': found utf-8 bom'+'\n')
        elif len(data_at_start_of_file) >= 2 and ord(data_at_start_of_file[0]) == 0xFE and ord(data_at_start_of_file[1]) == 0xFF:
            console.write(filename+': found ucs-2 big endian bom'+'\n')
        elif len(data_at_start_of_file) >= 2 and ord(data_at_start_of_file[0]) == 0xFF and ord(data_at_start_of_file[1]) == 0xFE:
            console.write(filename+': found ucs-2 little endian bom'+'\n')

        # addendum:
        notepad.activateBufferID( bufferID )
        str = editor.getText()
        console.write('buffer: length = {}\n'.format(len(str)))
        for i in range(3):
            console.write('\t#{}: {} => {}\n'.format(i, str[i], ord(str[i])))

    notepad.activateBufferID( firstBufferID )


if __name__ == '__main__': forum_post17244_FunctionName()