def add_1(m):
    return (m.group(1)) + str(int(m.group(2)) + 1) + (m.group(3))

editor.rereplace('(lootmax=")([0-9]+)(")', add_1);

"""
lootmax="2"
lootmax="4"
lootmax="6"
lootmax="1"
lootmax="5"
lootmax="9"
lootmax="99"
lootmax="999"
lootmax="9999"
"""