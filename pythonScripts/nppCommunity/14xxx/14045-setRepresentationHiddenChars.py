# encoding=utf-8
# from https://community.notepad-plus-plus.org/post/56581 and following discussion
# updated to include Guy's full list at the end
editor.setRepresentation(u'\u00A0', "NBSP")    # no-break space
editor.setRepresentation(u'\u2000', "NQSP")    # EN quad
editor.setRepresentation(u'\u2001', "MQSP")    # EM quad
editor.setRepresentation(u'\u2002', "ENSP")    # EN space
editor.setRepresentation(u'\u2003', "EMSP")    # EN space
editor.setRepresentation(u'\u2004', "3/MSP")   # three-per-EM space
editor.setRepresentation(u'\u2005', "4/MSP")   # four-per-EM space
editor.setRepresentation(u'\u2006', "6/MSP")   # six-per-EM space
editor.setRepresentation(u'\u2007', "FSP")     # figure space
editor.setRepresentation(u'\u2008', "PSP")     # punctuation space
editor.setRepresentation(u'\u2009', "THSP")    # thin space
editor.setRepresentation(u'\u200A', "HSP")     # hair space
# FORMAT chars ( Cf )
editor.setRepresentation(u'\u200B', "ZWSP")    # zero width space
editor.setRepresentation(u'\u200C', "ZWNJ")    # zero width non-joiner
editor.setRepresentation(u'\u200D', "ZWJ")     # zero width joiner
editor.setRepresentation(u'\u200E', "LRM")     # left-to-right mark
editor.setRepresentation(u'\u200F', "RLM")     # right-to-left mark
editor.setRepresentation(u'\u202A', "LRE")     # left-to-right embedding
editor.setRepresentation(u'\u202B', "RLE")     # right-to-left embedding
editor.setRepresentation(u'\u202C', "PDF")     # pop directional formatting
editor.setRepresentation(u'\u202D', "LRO")     # left-to-right override
editor.setRepresentation(u'\u202E', "RLO")     # right-to-left override
# SPACE chars ( Zs )
editor.setRepresentation(u'\u202F', "NNBSP")   # narrow no-break space
editor.setRepresentation(u'\u205F', "NNBSP")   # medium mathematical space
# FORMAT chars ( Cf )
editor.setRepresentation(u'\u2060', "WJ")      # word joiner ( zero width no-break space )
editor.setRepresentation(u'\u2061', "FA")      # function application
editor.setRepresentation(u'\u2062', "IT")      # invisible times
editor.setRepresentation(u'\u2063', "IS")      # invisible separator
editor.setRepresentation(u'\u2064', "IP")      # invisible plus
editor.setRepresentation(u'\u2066', "LRI")     # left-to-right isolate
editor.setRepresentation(u'\u2067', "RLI")     # right-to-left isolate
editor.setRepresentation(u'\u2068', "FSI")     # first strong isolate
editor.setRepresentation(u'\u2069', "PDI")     # pop directional isolate
# FORMAT chars ( Cf ) DEPRECATED
editor.setRepresentation(u'\u206A', "ISS")     # inhibit symmetric swapping
editor.setRepresentation(u'\u206B', "ASS")     # activate symmetric swapping
editor.setRepresentation(u'\u206C', "IAFS")    # inhibit arabic form shaping
editor.setRepresentation(u'\u206D', "AAFS")    # activate arabic form shaping
editor.setRepresentation(u'\u206E', "NADS")    # national digit shapes
editor.setRepresentation(u'\u206F', "NODS")    # nominal digit shapes
# SPACE chars ( Zs )
editor.setRepresentation(u'\u3000', "IDSP")    # ideographic space
# FORMAT chars ( Cf ) SPECIALS
editor.setRepresentation(u'\uFEFF', "ZWNBSP")  # zero width no-break space : deprecated ( see U+2060 ) / byte order mark
editor.setRepresentation(u'\uFFF9', "IAA")     # interlinear annotation anchor
editor.setRepresentation(u'\uFFFA', "IAS")     # interlinear annotation separator
editor.setRepresentation(u'\uFFFB', "IAT")     # interlinear annotation terminator
# OTHER symbols ( So )
editor.setRepresentation(u'\uFFFC', "OBJ")     # object replacement character
editor.setRepresentation(u'\uFFFD', "<?>")     # replacement character
# FORMAT chars ( Cf )
# For characters OVER the BMP, with code > FFFF, we can use, EITHER, the syntaxes :
#    - editor.setRepresentation(u'\U0001BCA0', "SFLO")    TRUE "32-bits" representation
#    - editor.setRepresentation(u'\uD82F\uDCA0', "SFLO")  The   16-bits "SURROGATES PAIR"
editor.setRepresentation(u'\uD82F\uDCA0', "SFLO")   # shorthand format letter overlap
editor.setRepresentation(u'\uD82F\uDCA1', "SFCO")   # shorthand format continuing overlap
editor.setRepresentation(u'\uD82F\uDCA2', "SFDS")   # shorthand format down step
editor.setRepresentation(u'\uD82F\uDCA3', "SFUS")   # shorthand format up step
##############
# my addition: forces a screen refresh, so the representations become visible
p = editor.getCurrentPos()
editor.addText(u'Z\uFEFFZ')
editor.deleteRange(p, editor.getCurrentPos() - p)
