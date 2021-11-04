# encoding=utf-8
"""this uses the "add_1" style search and replace in Notepad++

INSTRUCTIONS:
1. Install PythonScript
   * Plugins > Plugins Admin
   * Click ☑ PythonScript checkbox until checked
   * click INSTALL
   * restart Notepad++ as necessary
2. Create new PythonScript script
   * Plugins > PythonScript > New Script
   * Give it a reasonable name, like add_1.py
   * Paste in the code from this black box
   * Save
3. Switch to the document where you want to search/replace
4. Plugins > PythonScript > Scripts > add_1

To assign a keyboard shortcut:
1. Plugins > PythonScript > Configuration
2. In the User Scripts, click on add_1.py
3. Click the left ADD button (above Menu Items)
    * This adds "add_1" to the main Plugins > PythonScript menu, rather
      than requiring you to dig down into the Scripts submenu
4. Exit Notepad++ and restart
    * This is required for ShortcutMapper to be able to see the new entry
      in the PythonScript menu
5. Settings > ShortcutMapper > Plugin Commands
6. Filter by add_1
7. Click on add_1, then click the MODIFY button and
    set the keyboard shortcut in the dialog

You can change the replacement values, or the number of replacements,
then save, and it will still run.

PythonScript has documentation in its Context-Sensitive Help
"""
from Npp import *

counter = 1

def add_1(m):
    global counter
    repl = str(counter)
    counter = counter + 1
    return repl

def disp_1(m):
    console.write("found {}\n".format(m.group()))

editor.rereplace(r'(?<=int\[\] arr)\d+', add_1)
