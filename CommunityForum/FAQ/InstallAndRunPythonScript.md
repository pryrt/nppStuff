# FAQ: How to install and run a script in PythonScript

Hello, and welcome to the FAQ Desk.  You have likely been directed here because someone provided you with a script for PythonScript, and you need instructions on how to install and run the script.

## Installation

0. Install PythonScript plugin, if you don't have it already
    - **Plugins > Plugins Admin**
    - checkmark `PythonScript`
    - click **Install**
1. Create a new script 
    - **Plugins > Python Script > New script**
    - Give it the name that was suggested in the original post, or something that makes sense to you.  I will call it `ProvidedScript.py` for purposes of this FAQ entry.
    - It should be placed in your "user scripts" directory (_see [Footnote 1](#footnotes:~:text=PythonScript%20directory%20structure%20is%20described%20below. "Footnote #1")_) ... If it doesn't default to that location, then change to the correct location.
    - **Save**
2. Populate the script
    - Copy the text from the script that was provided to you, verbatim (including spacing/indentation... that is critical): copy/paste is your friend.
        - **_Caveat_**: many scripts posted in the forum end up in a grey or black box; if there is a scroll bar on the right side of that box, please make sure you scroll through and grab the _whole_ script, not just the first "page" worth.
    - Paste in the `ProvidedScript.py` file
    - **Save**
3. If you want to give it a keyboard shortcut or add it to the editor's right-click context menu:
    - **Plugins > Python Script > Configuration...**
    - Select **User Scripts**
    - Select `ProvidedScript.py`
    - Click the left **Add** to add the script to the **Menu items** table
        - Note: it needs to be added to this list to be able to be accessed via Notepad++'s Shortcut Mapper
    - **OK**
    - Exit Notepad++ completely and restart the application
    - **Plugins > Python Script** will now list `ProvidedScript`
    - To give it a keyboard shortcut:
        - **Settings > Shortcut Mapper**
            - select the **Plugin commands** tab
            - Filter = `ProvidedScript`
            - Click on `ProvidedScript` in the list, **Modify**, and set the shortcut as desired, **OK**
            - Click **Close**
        - Now that shortcut will be assigned to the `ProvidedScript` script
    - To add it to the editor’s right-click context menu
        - Choose **Edit Popup contextMenu** from the **Settings** menu (noting the info about having to restart Notepad++ for changes to be realized)
        - A file named `contextMenu.xml` will open into a new tab
        - Insert this line between existing lines of the XML, as desired for your menu:
           ~~~
           <Item PluginEntryName = "Python Script" PluginCommandItemName = "ProvidedScript" ItemNameAs = "Select to run ProvidedScript" />
            ~~~
        - save `contextMenu.xml`
        - Exit Notepad++ completely and restart for that entry to show up in the context menu.

If the script's author mentioned putting some commands in your "startup script" or `startup.py`, then between steps #2 and #3, you will need to do the following:
- **Plugins > Python Script > Scripts**
- `Ctrl+click` (_see [Footnote 2](#footnotes:~:text=General%20PythonScript%20hint%3A "Footnote #2")_) on `startup (User)`, which will edit that file
    - **NOTE:** _not_ `startup` by itself, which is the "Machine scripts" version (_see [Footnote 1](#footnotes:~:text=PythonScript%20directory%20structure%20is%20described%20below. "Footnote #1")_): you should never need to edit the "machine scripts" `startup.py`
    - If `startup (User)` does not exist, create a **New Script** as before, but call this one `startup.py`, and save it in the same directory as `ProvidedScript.py`
- Put in any code that they recommended for your `startup.py` script
- **Save**
- **Plugins > Python Script > Configuration...**
- Make sure the **Initialisation** pulldown is set to `ATSTARTUP`
- **OK**
- See [Footnote 3](#footnotes:~:text=If%20you%20are%20using%20the%20user%20setup.py "Footnote #3: import search paths") for info on Import search paths

It is also highly recommended that you go to **Plugins > Python Script > Configuration...** and checkmark **☑ Automatically open console on error** -- this way, if something goes wrong, the error message will be visible (so you can ask the original author of the script for help _with the error message and details of what went wrong_)

## Usage -- How to Run the Script

You need to start by doing any preparatory work suggested in the original post, including but not limited to:

- opening the right file(s)
- maybe editing the script to customize some regular expression

Run the script using one of the three methods below:
- If you followed step #3 from **Installation**, you can just use the keyboard shortcut you defined in the Shortcut Mapper
- If you followed step #3 from **Installation**, you can access the script through **Plugins > Python Script > ProvidedScript**
- Whether or not you followed step #3 from **Installation**, you can access the script through  **Plugins > Python Script > Scripts > ProvidedScript**

## Footnotes

1. PythonScript directory structure is described below.  You will want the "User Scripts" when following these instructions:
    - "Machine Scripts" go in the `...\Plugins\PythonScript\scripts\` directory:
        - These scripts will be accessible by all users on the same machine
        - For a normal installation, it will be relative to your installation folder (often `C:\Program Files\Notepad++\` or similar)
        - For a portable installation, it will be relative to your portable folder (whichever folder contains `notepad++.exe`)
        - Unless you are on a multi-user computer and know what you are doing, there is no reason to create "machine scripts"
    - "User Scripts" go in the `...\Plugins\Config\PythonScript\scripts\` directory:
        - These scripts are individual to the given user
        - For a normal installation, it will be relative to your AppData folder, and you can paste `%AppData\Notepad++\Plugins\Config\PythonScript\scripts\` into your **Save** dialog to get it to change to the right directory
        - If you have your settings in the Cloud or redirected to another folder based on a command-line-option, as described in the [Online User Manual's "Configuration Files Location" section](https://npp-user-manual.org/docs/config-files/#configuration-files-location), you will need to go to the `...\Plugins\Config\PythonScript\scripts\` folder relative to the settings folder
        - If you have a portable, it will be in `...\Plugins\Config\PythonScript\scripts\` relative to your portable folder (whichever folder contains `notepad++.exe`)
            - Note the difference in this path compared to the machine scripts: it has `Config\` as an extra level of directory
2. General PythonScript hint: `Ctrl+Click` on any script name in the **Scripts** menu to edit that script.
3. If you are using the user `setup.py` to load a script with an `import` statement, if you are getting errors about not finding the module to import, try something like the following near the top of the user `setup.py`, which will make sure the Python interpreter can see all of your user scripts so that it can import them.
    ~~~
    import os
    for (root, dirs, files) in os.walk(notepad.getPluginConfigDir() + r'\PythonScript\scripts', topdown=False):
        if root not in sys.path:
            sys.path.append(root)
    ~~~
