# FAQ Desk: Can I Do a Mathematical Replacement?

Hello, and welcome to the FAQ Desk.  You have likely been directed here because you have asked whether or not you can do a mathematical replacement in Notepad++.

There are many forms that this question can take, including but not limited to:

- "Can I find all numbers that match some pattern and add X to them?"
- "Can I find all numbers that match some pattern and increment the replacement for each?"
- "Can I find all numbers that match some pattern and round them to the nearest 1 (or 1000, or 0.001, or 0.000001, or ...)?"

## Native Notepad++

In native Notepad++, with no extra plugins, the short answer is "no".  The replacement engine, even with "regular expression" mode turned on, does not have a counter it can use while doing replacements, and it does not do math on the matches that it can output in the replacement.

## Allowing Plugins

If you allow us to recommend a plugin, then the answer is "yes".  With a scripting plugin like PythonScript, Lua Script, and others, you can bring the full power of the underlying scripting langauge that those plugins provide to bear on the math you want to do. 

The remainder of this FAQ will be showing examples using the PythonScript plugin, but the concepts will work in any of the scripting plugins.  For instructions on how to install the PythonScript plugin and to install and use the specific scripts, see our [FAQ: How to install and run a script in PythonScript](https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript).

## Add a value to each match

This example actually comes directly from the PythonScript documentation (**Plugins > Python Script > Context-Help**, then choose **Editor Object**, and go to the `editor.rereplace()` section:
```
# encoding=utf-8
from Npp import editor

def add_1(m):
    return 'Y' + str(int(m.group(1)) + 1)

# replace X followed by numbers by an incremented number
# e.g.   X56 X39 X999
#          becomes
#        Y57 Y40 Y1000

editor.rereplace('X([0-9]+)', add_1);
```

To customize this:

1. **Search**: to change what's matched, you will need to change the first expression in the `editor.rereplace(...)` line, which is a regular expression with similar syntax to Notepad++'s built-in [regular expression syntax](https://npp-user-manual.org/docs/searching/#regular-expressions).  
    - As a note, if you need backslashes `\` in the search expression, use `r'...'` quoting instead of the `'...'` quoting shown above.
    - You can place portions of the matched string in different "[capture groups](https://npp-user-manual.org/docs/searching/#capture-groups-and-backreferences)" in parentheses `()`.
2. **Replace**: the replacement is the return value from the `add_1` function 
    - Give the function a different name if you aren't adding one!
    - To access the text of the whole match, use `m.group(0)`.
    - To access the text of one of the parenthetical "capture groups", use `m.group(1)` for the first group, and so on.
    - To convert the text of a group to a number in python, use `int(m.group(1))` to make it an integer, or `float(m.group(1))` to make it a floating point number.
    - You can use as many lines of code as are needed in the `add_1` function, and use any variables and other function calls you want
    - To convert your mathy number back to a string, wrap it in the `str()` function.
    - The return value of the `add_1()` function _must_ be the string to use in the replacement
