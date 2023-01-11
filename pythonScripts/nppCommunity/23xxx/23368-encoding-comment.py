# <?xml version="1.0" encoding="IBM850" ?>
# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23368/can-i-tell-np-the-encoding-via-pseudo-comment/

References:
- PEP 263: https://peps.python.org/pep-0263/#defining-the-encoding
- nppFileSettings plugin: https://github.com/ffes/nppfilesettings/issues/1
- "official" charset/encoding names: https://jkorpela.fi/chars/sorted.html
- less official: https://perldoc.perl.org/Encode::Supported

want to have a map with known encodings pointing to the right MENUCOMMAND constant.
    utf-8 => .FORMAT_AS_UTF_8
    .FORMAT_ANSI
    ...

needs to recognize:
    # (en)?coding[:=]...
    <?xml version="1.0" encoding="IBM850" ?>
    <meta http-equiv="Content-type" content="text/html; charset=ibm850">
    <meta charset="UTF-8">

"""
from Npp import editor,notepad,console,MENUCOMMAND

class EncodingModelineProcessor(object):
    def __init__(self):
        editor.research(r'(?-s)^[ \t\f]*(?:#|<?xml|<meta ).*?coding[:=][ \t]*"?([-_.a-zA-Z0-9]+)"?', lambda m: self.parseEncodingModeline(m), 0, 0, -1, 1)  # find the first modeline
        pass

    def parseEncodingModeline(self, m):
        console.write("match modeline = '{}' -> encoding: '{}'\n".format(m.group(0), m.group(1)))
        console.write("\t{}..{} => line {}\n".format(m.start(0), m.end(0), editor.lineFromPosition(m.start(0))))

EncodingModelineProcessor()
