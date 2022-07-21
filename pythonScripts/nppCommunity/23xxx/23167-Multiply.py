# encoding=utf-8
from Npp import editor

def multiply_by_2(m):
    return 'DamageCapacity="' + str(int(m.group(1)) * 2) + '"'

editor.rereplace(r'DamageCapacity="(\d*\.?\d+)"', multiply_by_2)