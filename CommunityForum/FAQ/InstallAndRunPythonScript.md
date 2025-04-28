# FAQ: How to install and run a script in PythonScript

Hello, and welcome to the FAQ Desk.  You have likely been directed here because someone provided you with a script for PythonScript, and you need instructions on how to install and run the script.

Please read at least the **Simple Version** of the FAQ in its entirety before trying to follow the instructions.  If the person recommending you use a script in PythonScript says there are extra instructions, you should read the _entire_ FAQ.  You may miss some important concepts by trying to skip reading this whole FAQ.  If you have problems at any stage in this process, go back and re-read this entire FAQ and make sure you haven't missed anything.

To be clear, the PythonScript plugin comes bundled with a Python interpreter -- the version numbers will be different between the PythonScript plugin and the version of the Python interpreter that comes bundled with the plugin (PythonScript 2.1 comes with Python interpreter 2.7.17; PythonScript 3.0.22 comes with Python interpreter 3.12.9).  YOU DO NOT NEED TO SEPARATELY INSTALL A PYTHON INTERPRETER; IT COMES WITH THE PLUGIN.

This FAQ is in two main sections, with the full details having three main points:

- **Simple Version** ⇒ This assumes you have a normal Notepad++ installation, and that the script is compatible with PythonScript 2.  (The script author will tell you if it is not compatible with PythonScript 2)
- **Full Details** ⇒ This provides extra details, for how to work with edge cases, and gives you a fuller understanding of what's going on.
   - **Installation** ⇒ Describes how to install and configure the PythonScript plugin, and how to create a new script to paste the contents of a script that you are copying from somewhere else
   - **Usage -- How to Run the Script** ⇒ Describes how to run the script, once you've installed the plugin and created the script with its contents.
   - **Footnotes** ⇒ Gives additional details.  The FAQ will link to the appropriate footnote with a link like [Footnote N](#footnotes "Footnote N"), or you can just scroll down to that section to see the footnote referenced.

## Simple Version

This assumes you have a normal installation of Notepad++, and are willing to use the easiest-to-install PythonScript (even though it uses the Python 2 interpreter rather than Python 3 interpreter)

1. If you don't have PythonScript installed, this needs to be done once:
    - **Plugins > Plugins Admin**, checkmark **Python Script** 2.1, and click **Install**.
    - After Notepad++ restarts, **Plugins > Python Script** will exist.
2. **Plugins > Python Script > New script**
    - Save it, usually in `%AppData%\Notepad++\Plugins\Config\PythonScript\scripts\`_`<SomeName>`_`.py`
        - For those who didn't know, `%AppData%\` automatically expands to something like `c:\users\`_`<username>`_`\AppData\Roaming\`
    - Paste in the contents of the script from the posting.  Save.
3. To run the script: **Plugins > Python Script > Scripts > _`<nameOfScript>`_**

It's really that simple.

Everything in the details below just help work around edge cases.  The script author should tell you things like "you need PythonScript v3" or "if you want it to run every time you start notepad++, then follow the instructions in the FAQ".  If they give extra instructions like that, then the details are found below.  It might look complicated as you try to read the remaining for the first time, but if you just follow the instructions, it **will** work.

## Full Details

### Installation

These are the installation instructions.  If you want to know how to _run_ the script, that is described in the **Usage** section, farther down in this FAQ.

1. Install PythonScript plugin, if you don't have it already
    - There are two versions of the PythonScript plugin -- you can install either of them (though some scripts might take some tweaking to work in one or the other).
        - In general, if you want "easy to install", and the script author hasn't told you otherwise, you can just install PythonScript 2.1.
        - If you are an experienced Python programmer, and want the full features of the modern Python3 interpreter, you can choose to instead manually install PythonScript 3.0.x.
            - PythonScript 3.0.x will work great if you are only dealing with Unicode files (UTF-8, usually).  If you are using the old ANSI character sets, some of the text manipulation might not behave as you expect.
    - PythonScript 2.1.0: This version of the plugin uses the outdated Python 2.7 at its core, but most of the scripts found in the forum were written for and tested with this version of the plugin.  To install it:
        - **Plugins > Plugins Admin**
        - checkmark `PythonScript`
        - click **Install**
        - _Recommended_: After Notepad++ restarts
            - go to **Plugins > Python Script > Configuration...**
            - checkmark **☑ Automatically open console on error** -- this will make sure that if there's a syntax error or runtime error in the script you run later, the console will be shown so that you can see the error
            - set **Initialisation:** to `ATSTARTUP` so that your startup script will be properly run right when Notepad++ is loaded.  (this is also recommended in the [startup script section (below)](#:~:text=putting%20some%20commands%20in%20your%20%E2%80%9Cstartup%20script%E2%80%9D "startup script")
    - PythonScript 3.0.x: This version of the plugin uses a recent Python 3.y version (for example, plugin 3.0.18 uses Python 3.12), which matches modern Python, but some scripts will need to be modified slightly to work with the newer syntax.  To install it:
        - Close all instances of Notepad++
        - Go to https://github.com/bruderstein/PythonScript/releases
        - Go to the newest v3.0.y "pre-release" in the list
        - Under the "Assets" for that version, pick the "PythonScript_Full" for PluginsAdmin (or whichever variant suits your fancy, really) -- making sure to get the x64 version if you have 64-bit Notepad++
        - Unzip the contents into the `<npp_install_directory>\Plugins\PythonScript` directory, so the two DLLs are at `<npp_install_directory>\Plugins\PythonScript\*.dll`, and the subdirectories from the zipfile are in subdirectories of that directory
        - Run Notepad++
2. Create a new script 
    - **Plugins > Python Script > New script**
    - Give it the name that was suggested in the original post, or something that makes sense to you.  I will call it `ProvidedScript.py` for purposes of this FAQ entry.
    - It should be placed in your "user scripts" directory (_see [Footnote 1](#footnotes:~:text=PythonScript%20directory%20structure%20is%20described%20below. "Footnote #1")_) ... If it doesn't default to that location, then change to the correct location.
    - **Save**
3. Populate the script
    - Copy the text from the script that was provided to you, verbatim (including spacing/indentation... that is critical): copy/paste is your friend.
        - **_Caveat_**: many scripts posted in the forum end up in a grey or black box; if there is a scroll bar on the right side of that box, please make sure you scroll through and grab the _whole_ script, not just the first "page" worth.
    - Paste in the `ProvidedScript.py` file
    - **Save**
4. If you want to give it a keyboard shortcut or add it to the editor's right-click context menu:
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

### Usage -- How to Run the Script

You need to start by doing any preparatory work suggested in the original post, including but not limited to:

- opening the right file(s)
- maybe editing the script to customize some regular expression

Run the script using one of the three methods below:
- If you followed step #4 from **Installation**, you can just use the keyboard shortcut you defined in the Shortcut Mapper
- If you followed step #4 from **Installation**, you can access the script through **Plugins > Python Script > ProvidedScript**
- Whether or not you followed step #4 from **Installation**, you can access the script through  **Plugins > Python Script > Scripts > ProvidedScript**

### Footnotes

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
