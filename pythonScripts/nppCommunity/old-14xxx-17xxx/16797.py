# https://notepad-plus-plus.org/community/topic/16797/how-to-use-runmenucommand-in-python-script
console.show()
console.write("\nHello World\n")

# run the script called "PerlMonksQuestion.py":
if 'PerlMonksQuestion' in globals():
    console.write("PerlMonksQuestion already exists\n")
    reload(PerlMonksQuestion)
else:
    console.write("PerlMonksQuestion will be loaded\n")
    import PerlMonksQuestion

console.write("\nThe End\n")

"""
my goal: test if PerlMonksQuestion has already been loaded;
    if so, use `reload(PerlMonksQuestion)`,
    else `import PerlMonksQuestion`

* re-import = 2.7:reload() https://stackoverflow.com/questions/32234156/how-to-unimport-a-python-module-which-is-already-imported
        + https://docs.python.org/2/library/functions.html#reload
* https://realpython.com/python-modules-packages/
* https://stackoverflow.com/questions/4858100/how-to-list-imported-modules

I need to figure out a way to quickly test if "PerlMonksQuestion" is already in globals().items() without iterating through them all
* https://stackoverflow.com/questions/8214932/how-to-check-if-a-value-exists-in-a-dictionary-python
    print(globals())
        {...
        'PerlMonksQuestion': <module 'PerlMonksQuestion' from 'C:\Users\peter.jones\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\PerlMonksQuestion.pyc'>,
        ...}
    "PerlMonksQuestion" in globals().values()
        False
    "PerlMonksQuestion" in globals()
        True

Okay, that worked.
"""