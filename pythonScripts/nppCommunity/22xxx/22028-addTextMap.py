# encoding=utf-8
"""https://community.notepad-plus-plus.org/topic/22028/is-this-possible-suffix-text-based-on-a-list

Enter your list of suffixes here:
"""

suffixes = {
    # your search string and suffix go here, using the same format as these examples, including colons and commas
    'G90': "Absolute programming",
    'G21': "Programming in millimeters \(mm\)",
    'G40': "Tool radius compensation off",
    'G80': "Cancel canned cycle",

    # leave this one alone
    None: None
}

"""
INSTRUCTIONS:
1. Install PythonScript Plugin
   * Plugins > Plugins Admin
   * Click ☑ PythonScript checkbox until checked
   * click INSTALL
   * restart Notepad++ as necessary
2. Create new PythonScript script
   * Plugins > PythonScript > New Script
   * Give it a reasonable name, like addSuffixes.py
   * Paste in all the code from this black box
   * Save
3. Switch to the document where you want to search/replace
4. Plugins > PythonScript > Scripts > addSuffixes

To assign a keyboard shortcut:
1. Plugins > PythonScript > Configuration
2. In the User Scripts, click on addSuffixes.py
3. Click the left ADD button (above Menu Items)
    * This adds "addSuffixes" to the main Plugins > PythonScript menu, rather
      than requiring you to dig down into the Scripts submenu
4. Exit Notepad++ and restart
    * This is required for ShortcutMapper to be able to see the new entry
      in the PythonScript menu
5. Settings > ShortcutMapper > Plugin Commands
6. Filter by addSuffixes
7. Click on addSuffixes, then click the MODIFY button and
    set the keyboard shortcut in the dialog
"""


from Npp import *

editor.beginUndoAction()

for search,suffix in suffixes.items():
    if search is None: continue
    search_re = r'\b\Q' + str(search) + r'\E\b'
    editor.rereplace(search_re, '$0 \({}\)'.format(suffix))

editor.endUndoAction()
