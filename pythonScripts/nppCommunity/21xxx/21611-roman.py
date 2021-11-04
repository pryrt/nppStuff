# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21611/

matches any "roman numeral", which I define as
* any "word" that's a combination of I, V, X, L, C, D, M (only upper case)
* except if it's a lone I at the beginning of a line,
  or a lone I after a . or ? or ! or ; or , or " and one or two spaces
"""
from Npp import *

def roman_to_int(s):
    """stolen from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-2.php"""
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

def deromanize_match(m):
    return str(roman_to_int(m.group().rstrip()))

console.show()

#console.clear()
#console.write(str(roman_to_int('MMMCMLXXXVI')) + "\n")
#console.write(str(roman_to_int('MDCLXVI')) + "\n")

editor.beginUndoAction()
editor.rereplace(r'(?-is)(?!^\x20*I\x20)(?!(?<=[.?!,;"]\x20)I\x20)(?!(?<=[.?!,;"]\x20\x20)I\x20)\b[IVXLCDM]+\b', deromanize_match)
editor.endUndoAction()
