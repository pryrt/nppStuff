# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/19099/

This does not solve the problem.  This just gives the Notepad++ and PythonScript specific parts of the answer

The actual implementation of the sorting algorithm is a general Python programming exercise,
and whether or not Notepad++ exists has no bearing on that part of the coding (thus not a question for this forum)
"""

# step 0: assume data is active file in editor1 (main/left view)
# debug: console.clear()

# step 1: grab all the data from the editor1; keep the newline sequence, since I'll be printing it out later
contentsArray = []
def grabContentsArray(contents, lineNumber, totalLines):
    contentsArray.append(contents)

editor1.forEachLine( grabContentsArray )

# step 2: define a function that implements _your_ sort algorithm;
#   it's a generic programming exercise, nothing Notepad++ or PythonScript-plugin specific,
#   so left for you to implement
def sortTheContents( inputArray ):
    # these next two lines should be replaced by the real algorithm
    returnArray = list(inputArray)  # this will have to be replaced by your actual algorithm
    returnArray.sort() # in-place alphabetical sort
    # once the algorithm is done, return the result here
    return returnArray

sortedContents = sortTheContents( contentsArray )

# step 3: replace the entire file's contents with the sorted data
editor1.beginUndoAction()
editor1.clearAll()
# debug: console.show()
for s in sortedContents:
    # debug: console.write(s)
    editor1.addText(s)

editor1.endUndoAction()