# encoding=utf-8

def get_wide_ordinal(char):
    '''https://stackoverflow.com/a/7291240/5508606'''
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)

def callback_sci_UPDATEUI(args):
    c = editor.getCharAt(editor.getCurrentPos())
    #console.write("c=0x{0:04X}={0}dec\n".format(c));
    if c < 0 or c > 255:
        p = editor.getCurrentPos()
        q = editor.positionAfter(p)
        try:
            s = editor.getTextRange(p,q).decode('utf-8')
        except AttributeError:
            s = editor.getTextRange(p,q)
        c = get_wide_ordinal(s)
    else:
        try:
            s = unichr(c)
        except NameError:
            s = chr(c)

    try:
        is_eof = (editor.getCurrentPos()==editor.getLength())
        if c < 0x10000:
            info = "'{1}' = HEX:0x{0:04X} = DEC:{0} ".format(c, s.encode('utf-8') if c not in [13, 10, 0] else 'LINE-ENDING' if c != 0 else 'END-OF_FILE' if is_eof else 'NUL')
        elif c < 0x110000:
            # added the surrogate-pair listing for non-BMP Unicode
            #   inspired by https://community.notepad-plus-plus.org/topic/25784/
            L = 0xDC00 + (c & 0x3FF)
            H = 0xD800 + (((c-0x10000)>>10)&0x3FF)
            try:
                se_utf8 = s.encode('utf-8')
            except AttributeError:
                se_utf8 = s
            info = "'{1}' = HEX:0x{0:04X} = DEC:{0} ⇒ SURROGATE(0x{2:04X} 0x{3:04X})".format(c, se_utf8, H, L)
        else:
            raise ValueError("Invalid Unicode character")
    except ValueError:
        info = "HEX:?? DEC:?"
    notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, info)

callback_sci_UPDATEUI(None)     # per https://notepad-plus-plus.org/community/topic/17799/, want on-demand
# editor.callback(callback_sci_UPDATEUI, [SCINTILLANOTIFICATION.UPDATEUI]) # per https://notepad-plus-plus.org/community/topic/14767/, want live

'''
unicode: ☐ ☑ ☒ ✓ ✗ ◯ ○ ⊙ ⦾ ⦿
wide unicode: 🔘  (U+1F518)
wide: 😞 (U+1F61E)

inspired by https://notepad-plus-plus.org/community/topic/14767/ascii-hex-of-current-character
but make a unicode version...
'''
