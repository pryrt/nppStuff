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

## Apply Math to the match

### Add a value to each match

This example actually comes directly from the PythonScript documentation (**Plugins > Python Script > Context-Help**, then choose **Editor Object**, and go to the `editor.rereplace()` section):
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

### Round off values to the nearest XXX

This is acually solved in the same way as adding the value to each match.  You would just use a search expression that matches a floating point number, and use Python's [`round()`](https://docs.python.org/2/library/functions.html?highlight=round#round) function to round it off.  An example of that might be:

```
from Npp import editor

def round_to_penny(m):
    return str(round(float(m.group(1)), 2))

editor.rereplace(r'(\d*\.*\d+)', round_to_penny)
```

This would take
```
pi=3.14159
e=2.71828
three=3
1.618x
```
and connvert it to
```
pi=3.14
e=2.72
three=3.0
1.62x
```

Why isn't `3.0` shown as `3.00`?  Because the `round()` function rounded the value to 3.0 exactly, and the `str(3.00)` is just `3.0`.  If you want to guarantee it's printed with that same number of digits always, you can just use the [Python 2.7 format mini-language](https://docs.python.org/2/library/string.html#formatspec) instead of the `str()` and `round()` calls.  Change the `return...` line above to the following to use the format string instead:
```
    return "{:0.2f}".format(float(m.group(1)))
```
When run on the same input, this will result in
```
pi=3.14
e=2.72
three=3.00
1.62x
```

## Counters and Cycles

### Replace with a simple counter

If you have text that has a bunch of `zone_1` instances, and you want want to have each replacement count up from 1 (so `zone_1` then `zone_2` and so on), you could do something like,
```
from Npp import *

counter = 0

def repl_with_counter(m):
    global counter
    counter += 1
    return "zone_{}".format(counter)

editor.rereplace(r'zone_(\d+)', repl_with_counter)
```

### Replace from a small list of values

If you have a small list of replacements that you want to cycle through, it is similar.  This example will look for an `&` in your text, and replace it with the next `a`, `b`, `c`, `x`, `y`, `z`, wrapping around if there are more than 6 `&`:
```
from Npp import *

counter = 0
replacements = ('a','b','c','x','y','z')

def replace_with_cycle(m):
    global counter
    repl = replacements[counter]
    counter = (counter + 1) % len(replacements)
    return repl

editor.rereplace(r'&', replace_with_cycle) 
```

### Increment the counter per-group instead of per-match

Let's say you have some groups between `{...}`, like:
```
{
    'zone_1': "Name Goes Here",
    'other': "This is zone 1",
},
{
    'zone_1': "Something Else",
    'other': "And zone 1",
},
{
    'zone_1': "The Third",
    'other': "Now zone 1",
},
```
and you want it to come out like
```
{
    'zone_1': "Name Goes Here",
    'other': "This is zone 1",
},
{
    'zone_2': "Something Else",
    'other': "And zone 2",
},
{
    'zone_3': "The Third",
    'other': "Now zone 3",
},
```

You could use a script like,
```
from Npp import editor
import re  # required for the in-group replacement

counter = 1

def replace_group(m):
    global counter
    out = re.sub(r'(?<=zone[ _])\d+', str(counter), m.group(0))
    counter = counter + 1
    return out

editor.beginUndoAction()
editor.rereplace(r'(?s)^{\h*$.*?^},?\h*$', replace_group)
editor.endUndoAction()
```

The `rereplace` call is working on the whole group from `^{` to `^},`.  Inside that, you use the `re` engine of Python to do a replacement of the `zone_1` with the next value of the counter.

## Conclusion

The possibilities of this mechanism are limited only by your imagination, and your knowledge of Python (or some other scripting language) and regular expressions.

You may be able to convince a Community member to customize one of these for your exact circumstances... but the chances will be much higher if you try it on your own first, and show us what you tried, before asking us to write it for you.
