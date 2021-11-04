# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/18297/"""
from Npp import *

#console.show()
#console.clear()

def forum_post18297_main():
    """

    assumes the map file in in the active editor, with
        "filename" xnum
    pairs on each, like
        "gcode100.g" 2718
        "gcode101.g" 314
        "gcode102.g" 16

    It will open the individual files in the other, do the
    search/replace, and save/close.

    """
    nLines = editor.getLineCount()
    mapBufID = notepad.getCurrentBufferID()
    mapView = notepad.getCurrentView()
    mapIndex = notepad.getCurrentDocIndex(mapView)

    for l in range(0,nLines):
        notepad.activateIndex(mapView, mapIndex)

        txt = editor1.getLine(l).rstrip()
        if len(txt)==0: continue
        fname, xid = txt.split('" ')
        fname = fname[1:]
        #console.write("fname = '{}', xid = '{}'\n".format(fname, xid))

        ret = notepad.open(fname)
        notepad.menuCommand(MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW)
        editor.rereplace(
            '^;LAYER:(\d+)$',
            lambda m: 'M117 Layer:' + str(m.group(1)) + '/' + xid
        )
        notepad.save()
        notepad.close()


if __name__ == '__main__': forum_post18297_main()

"""
To generate the files (gcode and map), used the following perl:

use Path::Tiny;
use strict;
use warnings;

# create the original files, and the map file
my $m = path( 'x.map' );
$m->remove();
for my $f ( 1 .. 10 ) {
    my $p = path( sprintf 'g%03d.gcode', $f );
    $p->append( ";LAYER:$_\n") for 1 .. rand 100;
    $m->append( sprintf qq("%s" %d\n), $p->absolute->canonpath, 10 + rand 9990 );
}
"""