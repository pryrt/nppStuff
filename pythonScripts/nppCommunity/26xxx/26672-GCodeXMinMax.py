from Npp import editor

rememberMin = 999999999
rememberMax = -rememberMin

def checkMatchForSize(m):
    """
    For a given match, check the integer value after the X,
    and compare it to the remembered Min/Max values
    """
    matchInt = int(m.group(1))
    global rememberMin
    global rememberMax
    if matchInt < rememberMin: rememberMin = matchInt
    if matchInt > rememberMax: rememberMax = matchInt

# look for all instances of capital X followed by 1 or more digits, and call the checkMatchForSize function with that match
editor.research(r'X(\d+)', checkMatchForSize)

# add a line at position 0
editor.insertText(0, "# The min to max X values are: {} ... {}\r\n".format(rememberMin, rememberMax))
