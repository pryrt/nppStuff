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
   * Give it a reasonable name, like round_r.py
   * Paste in the code from this black box
   * Save
3. Switch to the document where you want to search/replace
4. Plugins > PythonScript > Scripts > round_r

To assign a keyboard shortcut:
1. Plugins > PythonScript > Configuration
2. In the User Scripts, click on round_r.py
3. Click the left ADD button (above Menu Items)
    * This adds "round_r" to the main Plugins > PythonScript menu, rather
      than requiring you to dig down into the Scripts submenu
4. Exit Notepad++ and restart
    * This is required for ShortcutMapper to be able to see the new entry
      in the PythonScript menu
5. Settings > ShortcutMapper > Plugin Commands
6. Filter by round_r
7. Click on round_r, then click the MODIFY button and
    set the keyboard shortcut in the dialog

You can change the replacement values, or the number of replacements,
then save, and it will still run.

PythonScript has documentation in its Context-Sensitive Help
"""
from Npp import *

def round_1(m):
    rounded = round(float(m.group(0)), 1)  # round to 1 decimal place
    return str(rounded)

editor.rereplace(r'(?<=r=")\d+\.?\d*(?=")', round_1)
