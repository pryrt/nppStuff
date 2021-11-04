from Npp import *

global myGlobal
try:
    myGlobal
except NameError:
    myGlobal = "initial value"

console.write(myGlobal+"\n")

myGlobal += "1"
