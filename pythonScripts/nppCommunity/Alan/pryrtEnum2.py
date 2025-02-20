# encoding=utf-8
"""followon to pryrtPyScEnumVals"""

import Npp

console.clear()
for inst in dir(Npp):
  if str(inst).isupper():
    #console.write(str(inst) + "\t" + repr(inst) + "\r\n")
    for val in eval(inst).values.values():
      console.write("{}.{}\n".format(inst,val))
