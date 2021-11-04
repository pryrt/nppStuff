# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21653/

Add up all the numerical tokens in a file, separated by whitespace.
It will append the total to the end of file, like

    =====TOTAL=###=====

If you don't want just unsigned integers, you'll have to change the search
regular expression and change the code in the function to not force
integer arithmetic.

----

this uses the "add_1" style search in Notepad++

INSTRUCTIONS:
1. Install PythonScript
   * Plugins > Plugins Admin
   * Click ☑ PythonScript checkbox until checked
   * click INSTALL
   * restart Notepad++ as necessary
2. Create new PythonScript script
   * Plugins > PythonScript > New Script
   * Give it a reasonable name, like AddAllInts.py
   * Paste in the code from this black box
   * Save
3. Switch to the document where you want to search/replace
4. Plugins > PythonScript > Scripts > AddAllInts

To assign a keyboard shortcut:
1. Plugins > PythonScript > Configuration
2. In the User Scripts, click on AddAllInts.py
3. Click the left ADD button (above Menu Items)
    * This adds "AddAllInts" to the main Plugins > PythonScript menu, rather
      than requiring you to dig down into the Scripts submenu
4. Exit Notepad++ and restart
    * This is required for ShortcutMapper to be able to see the new entry
      in the PythonScript menu
5. Settings > ShortcutMapper > Plugin Commands
6. Filter by AddAllInts
7. Click on AddAllInts, then click the MODIFY button and
    set the keyboard shortcut in the dialog

PythonScript has documentation in its Context-Sensitive Help
"""
from Npp import *

grand_total = 0

def add_int_to_total(m):
    global grand_total
    i = int(m.group())
    grand_total += i

editor.beginUndoAction()
editor.documentStart()
editor.research(r'\b\d+\b', add_int_to_total)
editor.documentEnd()
editor.addText("\n====TOTAL={}====\n".format(grand_total))
editor.endUndoAction()
