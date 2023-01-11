# https://notepad-plus-plus.org/community/topic/15485/increase-decrease-all-highlighted-x-or-y-coordinates
# Will prompt for which column (allows x, y, w, h) and how much to add or subtract (requires a number)
# Will then do the search/replace over the whole file
DEBUG = False

def delt_1(m):
    global addend
    this = m.group(1)

    if DEBUG:
        console.write("matched '")
        console.write(this)
        console.write("'\t")

    r = str(addend + int(this))

    if DEBUG:
        console.write("return: '" + r + "'")
        console.write("\n")

    return r

####################################################

if DEBUG: console.show()
if DEBUG: console.clear()
column = None
while column != "x" and column != "y" and column != "w" and column != "h":
    column = notepad.prompt("Which column [x y w h]?", "Choose column", "y")

addend = None
while addend == None:
    direction = notepad.prompt("Number to add (negative for subtraction)", "Choose delta", "1")
    try:
        addend = int( direction )
    except:
        addend = None

if DEBUG:
    console.write("column: " + column + "\n")
    console.write("addend: " + str(addend) + "\n")

pattern = "((?<=\s{0})\\d+)".format( column )
if DEBUG: console.writeError(pattern + "\n")
editor.beginUndoAction()
editor.rereplace(pattern , delt_1)
editor.endUndoAction()

# used the PythonScript > Context-Help > Editor Object > Helper Methods > .rereplace() docs
# as well as:
#   https://docs.python.org/2/library/re.html
#   https://docs.python.org/2/tutorial/errors.html