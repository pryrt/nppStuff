# encoding=utf-8
# zero width in name
editor.setRepresentation(u'\u200B', "ZWS")
editor.setRepresentation(u'\u200C', "ZWNJ")
editor.setRepresentation(u'\u200D', "ZWJ")
editor.setRepresentation(u'\uFEFF', "ZWNBSP")
# also zero width
editor.setRepresentation(u'\u2060', "WJ")       # word joiner (separate from ZWJ, but still claims zero width)
# directional controls and other toggles
editor.setRepresentation(u'\u200E', "LTR")  # left-to-right mark
editor.setRepresentation(u'\u200F', "RTL")  # right-to-left mark
editor.setRepresentation(u'\u202A', "EMBL")  # left-to-right embedding
editor.setRepresentation(u'\u202B', "EMBR")  # right-to-left embedding
editor.setRepresentation(u'\u202C', "EMBP")  # pop directional formatting
editor.setRepresentation(u'\u202D', "OVRL")  # left-to-right override
editor.setRepresentation(u'\u202E', "OVRR")  # right-to-left override
editor.setRepresentation(u'\u2061', "FA")      # function application
editor.setRepresentation(u'\u2062', "IT")      # invisible times
editor.setRepresentation(u'\u2063', "IS")      # invisible separator
editor.setRepresentation(u'\u2064', "IP")      # invisible plus
editor.setRepresentation(u'\u2066', "ISOL")  # left-to-right isolate
editor.setRepresentation(u'\u2067', "ISOR")  # right-to-left isolate
editor.setRepresentation(u'\u2068', "ISO1")  # first strong isolate
editor.setRepresentation(u'\u2069', "ISOP")  # pop directional isolate
editor.setRepresentation(u'\u206A', "SYMI")  # inhibit symmetric swapping
editor.setRepresentation(u'\u206B', "SYMA")  # activate symmetric swapping
editor.setRepresentation(u'\u206C', "ARAI")  # inhibit arabic form shaping
editor.setRepresentation(u'\u206D', "ARAA")  # activate arabic form shaping
editor.setRepresentation(u'\u206E', "SHNA")  # national digit shapes
editor.setRepresentation(u'\u206F', "SHNO")  # nominal digit shapes
p = editor.getCurrentPos()
editor.addText(u'Z\uFEFFZ')
editor.deleteRange(p, editor.getCurrentPos() - p)
