# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26061/

Sets the representation for all Unicode characters (above U+0080)
"""
from Npp import editor,notepad,console

# pick the right chr() vs unichr()
def fn_chr2(code):
    if(code>0xFFFF):
        s = "u'\\U{:08X}'".format(code)
        return eval(s)
        #console.write("Debug: eval({}) => {}\n".format(s, repr(eval(s))))
        #raise Exception("Need to debug U+{:08X} => {}\n".format(code, s))
    return unichr(code)
def fn_chr3(code):
    return chr(code)
fn_chr = fn_chr3 if notepad.getPluginVersion()[0]=='3' else fn_chr2

# show progress
console.show()
console.write("Begining to remap Unicode characters.  This may take a few seconds.\n")

# loop through "Unicode characters" (anything not in ASCII 0x00-0x7F) and change to representation
for code in range(0x80, 0x110000):
    c = fn_chr(code)
    if 0xD800 <= code and code <= 0xDFFF:
        continue
    try:
        #if 0 == code % 0x8000:
        #    console.write(u"{} => \\U+{:X}\n".format(c, code))
        editor.setRepresentation(c, "U+{:X}".format(code))
    except Exception as e:
        console.writeError(u"code U+{:X} failed\n".format(code))
        raise e

# force screen redraw
p = editor.getCurrentPos()
editor.addText(u'Z\uFEFFZ')
editor.deleteRange(p, editor.getCurrentPos() - p)

# final progress:
console.write("Finished remapping Unicode characters.  Sorry for the delay.\n")
console.write("Go into another tab and back to reset to normal text.\n")

# 👍
# Checkboxes:
#   ☐ ☑ ☒ ✓ ✗ ◯ ○ 🔘 ⊙ ⦾ ⦿ -- where the last is my favorite (but doesn't always render in NPP)
#   Other circles: ● ○ ◌ ◍ ◙ ◯ ⚫ ⦾ ⦿
# Arrows ← ↑ → ↓ ↔ ↕ ⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ▲ ▶ ▼ ◀ 〈 〉 ﹀ ︿ 《 》 ︽ ︾
# Angles: ΘΦΨ (upper) θφψ (lower) ° (degrees) ∠ (angle) ∟ (right angle) ⟂ (perpendicular)
# Products: dot:∙ cross:×
# Footnotes/Links { ° , ⁰¹²³⁴⁵⁶⁷⁸⁹ⁿⁱ ₀₁₂₃₄₅₆₇₈₉, † , ‡, 🛈 , ↗ , ↱ , 🔗 , ⛓}
# “” ™ ± ≈
# ☺☹😐😉😀😭😧😥😦😢👍👎
