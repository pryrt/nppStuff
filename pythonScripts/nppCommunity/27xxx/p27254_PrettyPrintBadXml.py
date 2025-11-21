# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27254/

This will take malformed XML (many/most tags with no closing tag) and
pretty-print it so that each layer of closed tags indents its contents
"""
from Npp import editor
import re

editor.beginUndoAction()

sEOL = ('\r\n', '\r', '\n')[editor.getEOLMode()]

# First, one tag per line, no indentation
editor.rereplace(r'\s*<', sEOL + r'<', re.MULTILINE)

# get rid of extra newlines at beginning and end (but final line will end with EOL, so N++ shows empty last line)
editor.rereplace(r'\A\s+', '', re.MULTILINE)
editor.rereplace(r'\v+\z', sEOL, re.MULTILINE)

# figure out all the closing tags `</CLOSING>`
closers = {}
def trackClosingTags(m):
    global closers
    closers[m.group(1)] = True
editor.research(r'</(\w+)\s*>', trackClosingTags)

for tag in closers.keys():
    f = r'(?-si:<{0}\b|(?!\A)\G)(?s-i:(?!</{0}\b).)*?\K(?-si:^(?!\h*</{0}))'.format(tag)
    editor.rereplace(f, '\t', re.MULTILINE)

editor.endUndoAction()

"""
<OFX> <SIGNONMSGSRQV1> <SONRQ> <DTCLIENT>20250520104016.123[-7:MST] <USERID>anonymous00000000000000000000000 <USERPASS>X <GENUSERKEY>N <LANGUAGE>ENG <APPID>QWIN <APPVER>2700 </SONRQ> </SIGNONMSGSRQV1> <INTU.BRANDMSGSRQV1> <INTU.BRANDTRNRQ> <TRNUID>19FFC8F0-7EF9-1000-BC8D-909811990026 <INTU.BRANDRQ> <FAKE> <OTHER> <TAG> <FAKE> <OTHER> <EMBEDDED> <FAKE> <DEEPER> <OTHER> </DEEPER> <OTHER> </EMBEDDED> </TAG>
"""
