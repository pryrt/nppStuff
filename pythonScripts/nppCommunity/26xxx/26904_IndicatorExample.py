# This line contains | Trace
# This line contains | Error
# This line contains | Debug

from Npp import *
positions = ( (0,28), (30,58), (60,88) )

try:
    traceIndicator
except NameError:
    traceIndicator = notepad.allocateIndicator(3)
    errorIndicator = traceIndicator + 1
    debugIndicator = traceIndicator + 2

console.write("traceIndicator={}, errorIndicator={}, debugIndicator={}\n".format(traceIndicator,errorIndicator,debugIndicator))
editor.setIndicatorCurrent(traceIndicator)
editor.indicSetFore(traceIndicator, (0,255,255)) # cyan
editor.indicSetStyle(traceIndicator, INDICATORSTYLE.FULLBOX)
editor.indicatorFillRange(positions[0][0], positions[0][1]-positions[0][0])

editor.setIndicatorCurrent(errorIndicator)
editor.indicSetFore(errorIndicator, (255,255,0)) # yellow
editor.indicSetStyle(errorIndicator, INDICATORSTYLE.FULLBOX)
editor.indicatorFillRange(positions[1][0], positions[1][1]-positions[1][0])

editor.setIndicatorCurrent(debugIndicator)
editor.indicSetFore(debugIndicator, (255,128,128)) # orange-ish
editor.indicSetStyle(debugIndicator, INDICATORSTYLE.FULLBOX)
editor.indicatorFillRange(positions[2][0], positions[2][1]-positions[2][0])

console.write("{} => {} .. {}\n".format(traceIndicator, editor.indicatorStart(traceIndicator, positions[0][0]), editor.indicatorEnd(traceIndicator, positions[0][0])))
console.write("{} => {} .. {}\n".format(errorIndicator, editor.indicatorStart(errorIndicator, positions[1][0]), editor.indicatorEnd(errorIndicator, positions[1][0])))
console.write("{} => {} .. {}\n".format(debugIndicator, editor.indicatorStart(debugIndicator, positions[2][0]), editor.indicatorEnd(debugIndicator, positions[2][0])))

#editor.setIndicatorCurrent(traceIndicator)
#editor.indicatorClearRange(positions[0][0], positions[0][1]-positions[0][0])
#editor.indicatorClearRange(0, 2212)
#editor.setIndicatorCurrent(errorIndicator)
#editor.indicatorClearRange(positions[1][0], positions[1][1]-positions[1][0])
#editor.indicatorClearRange(0, 2212)
#editor.setIndicatorCurrent(debugIndicator)
#editor.indicatorClearRange(positions[2][0], positions[2][1]-positions[2][0])
#editor.indicatorClearRange(0, 2212)
