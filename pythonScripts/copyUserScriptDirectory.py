# encoding=utf-8
"""Puts the AppData-or-equivalent Plugins\Config\PythonScript\Scripts directory into the clipboard
Run this right before calling Plugins > Python Script > New Script, then paste that directory to make sure you create the script in the right location
"""
from Npp import editor,notepad
editor.copyText(os.path.join(notepad.getPluginConfigDir(), "PythonScript", "Scripts"))
