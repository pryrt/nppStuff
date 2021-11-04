# encoding=utf-8
"""Run ctags -R for the current file

It will check the current directory and a few levels up
to see if it can find a tags file (or a .ctags or ctags.cnf)
"""
import os.path
import os

#console.show()
#console.clear()

file = notepad.getCurrentFilename()
# console.write(file+"\n") # debug: print the original filename
d = os.path.dirname(file)
found = ''
runFrom = d

while os.path.exists(d):
    # console.write(d+"\n") # debug: print level

    # check for tags, .ctags, ctags.cnf; also check for .editorconfig, which is another way of indicating the top of a project
    for fname in ['tags', 'ctags', 'ctags.cnf', '.editorconfig']:
        f = os.path.join(d, fname)
        e = os.path.exists(f)
        # console.write(f+"\t"+str(e)+"\n") # debug: print the file being tried
        if e:
            found = f
            break

    # found it! so we can be done
    if os.path.exists(found):
        break       # found it!

    # go up another level and try again
    pd = os.path.dirname(d)
    if pd == d:
        break       # prevent infinite loop
    d = pd

if os.path.exists(found):
    # console.write("tag search: '"+found+"'\n")
    runFrom = os.path.dirname(found)
#else:
#    console.write("tag search: no tags found\n")

# console.write("run from '"+runFrom+"'\n")
os.chdir(runFrom)
# console.write("cwd: "+os.getcwd()+"\n")
os.system("echo running ctags -R in %CD% & ctags -R || pause ") # should pause on error