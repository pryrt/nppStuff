# FAQ Desk: Can I Do a Mathematical Replacement?

Hello, and welcome to the FAQ Desk.  You have likely been directed here because you have asked whether or not you can do a mathematical replacement in Notepad++.

There are many forms that this question can take, including but not limited to:

- "Can I find all numbers that match some pattern and add X to them?"
- "Can I find all numbers that match some pattern and increment the replacement for each?"
- "Can I find all numbers that match some pattern and round them to the nearest 1 (or 1000, or 0.001, or 0.000001, or ...)?"

# In Short: No

Notepad++ itself doesn't do math on the text during search-and-replace.  That is not what text editors are designed to do.

The replacement engine, even with "regular expression" mode turned on, does not have a counter it can use while doing replacements, and it does not do math on the matches that it can output in the replacement.

So Notepad++ cannot do this.

# Actually: No, but Plugins might work for you

However, if you allow us to recommend a plugin, then the answer is, "yes, with certain plugins, you might be able to get the math replacement you want".  See below for examples of how plugins might help you do specific math searches or replacements.

# Plugin: Columns++

It might not sound like a math-related plugin, but the [Columns++](https://github.com/Coises/ColumnsPlusPlus) is able to do calculations in its search-and-replace.  You can download the plugin from the [Columns++ repo](https://github.com/Coises/ColumnsPlusPlus) and manually install it.  (Eventually, @Coises might get it submitted to the Notepad++ Plugins Admin list, but it's not there yet.)

The following example (derived from [this post](/post/89472)) will search for text that looks like `num_1=1, num_2=100` and replace so that num_1 will count from 1 and up with each match, and num_2 will count by twos, starting at 100.
- **Plugins > Columns++ > Search...**
- **Find What**: `num_1=\d+, num_2=\d+`
  **Replace With**: `num_1=(?=match), num_2=(?=98+2*match)`
  **Search Mode**: `☑ Regular Expression`

## Columns++: Formula Replacement Quick Start

All Formula Replacements go inside of a `(?=...)` wrapper: the math / formula goes in place of the  `...` .  Any of the expressions below can go inside a Formula Replacement wrapper, as well as any standard math using `+ - * /` for the addition, subtraction, multiplication, and division operators.

- `match` ⇒ This variable is the number of times the regular expression has matched (essentially, a counter for matches).  So a replacement of `(?=match)` will replace with `1` on the first match, `2` on the second match, `3` on the third, etc.
- `reg(ℕ)` ⇒ This grabs the numerical value of the ℕth capture group (similar to `$ℕ` or `${ℕ}` in a normal regex).  
- `this` ⇒ This variable is the numeric value of the entire match — only useful if the entire match is, in fact, a number.

For all the details, see the [Columns++ Documentation > Formulas](https://coises.github.io/ColumnsPlusPlus/help.htm#formulas) -- it includes other functions and operators for getting and manipulating data from your file, as well as other math functions and operators

# Scripting Plugins

If you are willing to use a scripting plugin, you can perform math to do replaceplacements; however, there is a big **Caveat** below, which you must understand in order to make use of a scripting plugin solution.

With a scripting plugin like PythonScript, Lua Script, and others, you can bring the full power of the underlying scripting language that those plugins provide to bear on the math you want to do. 

The remainder of this FAQ will be showing examples using the PythonScript plugin, but the concepts will work in any of the scripting plugins.  For instructions on how to install the PythonScript plugin and to install and use the specific scripts, see our [FAQ: How to install and run a script in PythonScript](https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript).

## Caveat

The following contains regular expressions and programming (in Python).  If you are not familiar with both, then the solutions described below might be too difficult for you to customize: feel free to give it a try, but understand that, for you, the full answer might be "Notepad++ (or any text editor) is the wrong task for the job if you want a replacement to do math, and you do not have the skills necessary to make use of scripting-based solutions".  

The Community Forum members are not obliged to custom-write a solution for your exact transformation, nor will they handhold you through the entire process of you customizing these examples to your actual specifications.  

If you have direct questions that are related to the Notepad++\-specific aspects of these solutions, we can answer questions, but if your questions stray into the realm of generic regex advice and generic Python programming questions, we will direct you to the regex and python documentation, as those aspects of your problem have nothing to do with Notepad++, and are off topic for this Community Forum.

If you understand and agree to those terms, feel free to continue.

## Apply Math to the match for the replacement

### Add a value to each match (or subtract, or multiply, or divide, or other f(x))

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
    - You can use as many lines of code as are needed in the `add_1` function, and use any variables and other function calls you want, and include any algebraic operators like add `+` or subtract `-` or multiply `*` or divide `/` or exponentiate `**` or modulus `%`, or combinations of those with any Python mathematical operators.
    - To convert your mathy number back to a string, wrap it in the `str()` function.
    - The return value of the `add_1()` function _must_ be the string to use in the replacement

### Round off values to the nearest XXX

This is acually solved in the same way as adding the value to each match.  You would just use a search expression that matches a floating point number, and use Python's [`round()`](https://docs.python.org/2/library/functions.html?highlight=round#round) function to round it off.  An example of that might be:

```
from Npp import editor

def round_to_penny(m):
    return str(round(float(m.group(1)), 2))

editor.rereplace(r'(\d*\.?\d+)', round_to_penny)
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

### Counters and Cycles

#### ADD HARD LINE NUMBERS TO THE CURRENT FILE
Let's say you have some text in a file:
```txt
The rose is red, the violet's blue,
The honey's sweet, and so are you.
Thou are my love and I am thine;
I drew thee to my Valentine:
The lot was cast and then I drew,
And Fortune said it should be you.
```
And you want it to be replaced with this:
```txt
1  The rose is red, the violet's blue,
2  The honey's sweet, and so are you.
3  Thou are my love and I am thine;
4  I drew thee to my Valentine:
5  The lot was cast and then I drew,
6  And Fortune said it should be you.
```
Well, with only 6 lines it is easy enough manually or with the Column-Editor feature of Notepad++; but if you had 20,000 lines, you could use a script like:
```py
# encoding=utf-8
from Npp import *

def custom_replace_func(m):
    new_text = "{C:{P}{D}}{S}".format(
        C=custom_replace_func.counter,
        D=custom_replace_func.digits,
        P='0' if custom_replace_func.zero_pad else ' ',
        S=' ' * custom_replace_func.spaces_after)
    custom_replace_func.counter += custom_replace_func.increment
    return new_text

custom_replace_func.counter = 1  # starting value
custom_replace_func.increment = 1
custom_replace_func.digits = len(str(editor.getLineCount()))  # don't change this
custom_replace_func.zero_pad = False  # zero- or space- padding of line number
custom_replace_func.spaces_after = 2  # spaces between line number and line content
editor.rereplace('^', custom_replace_func)
```
You can do some tweaking to the output format, by changing the `zero_pad` and `spaces_after` values.

#### REPLACE WITH A SIMPLE COUNTER (i.e., RENUMBERING)
If you have text that has many "`zone_`digit(s)" instances, and you want want to have each replacement count up from 1 (so `zone_1` then `zone_2` and so on), you could do something like:
```py
# encoding=utf-8
from Npp import *

def custom_replace_func(m):
    new_text = "zone_{}".format(custom_replace_func.counter)
    custom_replace_func.counter += custom_replace_func.increment
    return new_text

custom_replace_func.counter = 1  # starting value
custom_replace_func.increment = 1
editor.rereplace(r'zone_(\d+)', custom_replace_func)
```
This would take this input text:
```txt
zone_235 zone_249 zone_193 zone_151
zone_207 zone_172 zone_5 zone_221
zone_2 zone_270 zone_186 zone_228
```
And produce this output text:
```txt
zone_1 zone_2 zone_3 zone_4
zone_5 zone_6 zone_7 zone_8
zone_9 zone_10 zone_11 zone_12
```
-------------------------------------------------------------------------------
We could change our starting-value and increment-value to begin renumbering at 60, and go in steps of 5, by changing the relevant line in the code to:
```py
custom_replace_func.counter = 60  # starting value
custom_replace_func.increment = 5
```
And produce this output text:
```txt
zone_60 zone_65 zone_70 zone_75
zone_80 zone_85 zone_90 zone_95
zone_100 zone_105 zone_110 zone_115
```

#### REPLACE FROM A SMALL LIST OF VALUES
If you have a small list of replacements that you want to cycle through, it is similar. This example will look for an `&` in your text, and replace it with the next value in the sequence `c`, `a`, `b`, `z`, `y`, `x`, wrapping around and starting with `c` again if there are more than 6 `&`:
```py
# encoding=utf-8
from Npp import *

def custom_replace_func(m):
    replace_with = custom_replace_func.repl_list[custom_replace_func.index]
    custom_replace_func.index = (custom_replace_func.index + 1) % len(custom_replace_func.repl_list)
    return replace_with

custom_replace_func.index = 0
custom_replace_func.repl_list = ['c', 'a', 'b', 'z', 'y', 'x']
editor.rereplace(r'&', custom_replace_func)
```
This would take this input text:
```txt
this & that & more & less & who &
what & where & when & why & how
```
And produce this output text:
```txt
this c that a more b less z who y
what x where c when a why b how
```

#### INCREMENT THE COUNTER (RENUMBER) PER-SECTION INSTEAD OF PER-MATCH
Let's say you have some text in `{`...`}` -delimited sections, like this:
```txt
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
And you want it to be replaced with this:
```txt
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
You could use a script like:
```py
# encoding=utf-8
from Npp import *
import re  # to be able to use Python's regular expression library

def custom_replace_func(m):
    replace_with = re.sub(r'(?<=zone[ _])\d+', str(custom_replace_func.counter), m.group(0))
    custom_replace_func.counter += 1
    return replace_with

custom_replace_func.counter = 1  # starting value
editor.rereplace(r'(?s)^{.+?^},?\h*$', custom_replace_func)
```
The `rereplace` function call is working on the whole section from `{` to `},`. Inside that, you use the `re` engine of Python (not Notepad++) to do a replacement of the `zone_1` or `zone 1` with the next value of the running counter.

## Search

The examples above were all focused on replacements using math. Instead, if you want to do math that limits a search, you can use the `editor.search()` and `editor.research()`, which call a function on any matched text, and allow you to do any manipulation (including converting to numbers and doing comparisons).  So you could do set a regex that looks for something number-like, and then have the callback function convert the text to a number, and do the mathematical comparison or other manipulation, and only perform some other follow-on action (updating the editor view's active selection, or such as setting a bookmark, or anything else you can code) on text that matches both the textual regex _and_ the conditions defined in your callback's code.

### Examples of Mathematical Searches

#### Search for integers greater than or equal to 25

The regex in the search needs to be for a generic integer (`\b\d+\b`): `editor.research()` invokes the callback on any string that looks like an integer, without regard for the mathematical requirement.  Then the callback does the math to determine whether or not the text represents an integer that meets the mathematical restriction, and will then "do something" if the text _and_ math meet the requirements.

In this version, the callback will toggle the bookmark on each matched line.  After running this script, you can use the **Search > Bookmark > ...** sub-menu to navigate between the various bookmarks:

```py
# encoding=utf-8
from Npp import editor, notepad, MENUCOMMAND
import re  # to be able to use Python's regular expression library

def custom_match_func(m):
    i = int(m.group(0))
    if i >= 25:
        editor.setSel( m.start(0), m.end(0) )
        notepad.menuCommand(MENUCOMMAND.SEARCH_TOGGLE_BOOKMARK)

editor.research(r'^\b\d+\b', custom_match_func)
```

Alternatively, if you want a "find next" with the same restriction, so that it will just move the selection forward, without doing any bookmarking:

```py
# encoding=utf-8
from Npp import *

def custom_match_func(m):
    if custom_match_func.stop: return
    i = int(m.group(0))
    if i >= 25:
        editor.setSel( m.start(0), m.end(0) )
        custom_match_func.stop = True

custom_match_func.stop = False
editor.research(r'^\b\d+\b', custom_match_func, 0, editor.getCurrentPos())
```

The `stop` flag was used, instead of just using `editor.research()`'s `maxCount`, because `maxCount` refers to the number of times that the `editor.research()` finds the matching text (ie, any integer), but the custom match function callback only updates the selection when it _also_ matches the mathematical condition, so those two counts aren't always the same.

## Conclusion

The possibilities of this mechanism are limited only by your imagination, and your knowledge of Python (or some other scripting language) and regular expressions.

You may be able to convince a Community member to customize one of these for your exact circumstances... but the chances will be much higher if you try it on your own first, and show us what you tried, before asking us to write it for you.
