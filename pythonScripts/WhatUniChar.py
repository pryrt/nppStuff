# encoding=utf-8

def get_wide_ordinal(char):
    '''https://stackoverflow.com/a/7291240/5508606'''
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)

def callback_sci_UPDATEUI(args):
    c = editor.getCharAt(editor.getCurrentPos())
    if c < 0 or c > 255:
        p = editor.getCurrentPos()
        q = editor.positionAfter(p)
        s = editor.getTextRange(p,q).decode('utf-8')
        c = get_wide_ordinal(s)
    else:
        s = unichr(c)

    try:
        info = "'{1}' = HEX:0x{0:04X} = DEC:{0} ".format(c, s.encode('utf-8') if c not in [13, 10, 0] else 'LINE-ENDING' if c != 0 else 'END-OF-FILE')
    except ValueError:
        info = "HEX:?? DEC:?"
    notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, info)

callback_sci_UPDATEUI(None)     # per https://notepad-plus-plus.org/community/topic/17799/, want on-demand
# editor.callback(callback_sci_UPDATEUI, [SCINTILLANOTIFICATION.UPDATEUI]) # per https://notepad-plus-plus.org/community/topic/14767/, want live

'''
unicode: ☐ ☑ ☒ ✓ ✗ ◯ ○ ⊙ ⦾ ⦿
wide unicode: 🔘  (U+1F518)

inspired by https://notepad-plus-plus.org/community/topic/14767/ascii-hex-of-current-character
but make a unicode version...
'''