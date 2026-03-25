# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/27472/
(fixed URL to Topic)

process -pluginMessage="PythonScriptCommandlineSearch=term"

`term` must be a normal search term, not a regular expression; it currently cannot include semicolons `;` or double-quotes `"`
"""
#####   -------
#####   Instructions:
#####
#####   {these assume a normal installation of Notepad++, using %AppData%\Notepad++ for user configuration}
#####
#####   See [PythonScript FAQ](https://community.notepad-plus-plus.org/topic/23039/faq-how-to-install-and-run-a-script-in-pythonscript)
#####
#####   - Create `%AppData%\Notepad++\plugins\PythonScript\scripts\commandlineSearch27482.py`, from the contents below
#####   - Check for menu entry **Plugins > Python Script > Scripts > startup (User)**
#####       - if it is listed, `Ctrl+click` on it to edit, and add the following to the end:
#####       - if it isn't listed, create `%AppData%\Notepad++\plugins\PythonScript\scripts\user.py` from the contents below
#####       - set **Plugins > Python Script > Configuration...** to **Initialisation: `ATSTARTUP`**
#####       - exit and restart Notepad++
#####
#####   After doing that, the script should look for
#####   `notepad++ -pluginMessage="PythonScriptCommandlineSearch=term"`, and run a search for `term`
#####
#####   For now, it won't work with semicolon `;` or double-quote `"` in the search term;
#####       if that is needed, I would need to add an escape sequence processing, which would make it more complicated.
#####   -------


from Npp import notepad, console, NOTIFICATION, MENUCOMMAND
import ctypes
import sys
import re

import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID

def usePluginMessageString27482(s):
    m = re.search(r'PythonScriptCommandlineSearch=([^;"]+)', s)
    t = m.group(1)

    # Define the functions and constants needed
    FindWindow = ctypes.windll.user32.FindWindowW
    FindWindow.argtypes = [LPCWSTR, LPCWSTR]
    FindWindow.restype  = HWND

    FindWindowEx = ctypes.windll.user32.FindWindowExW
    FindWindowEx.argtypes = [HWND, HWND, LPCWSTR, LPCWSTR]
    FindWindowEx.restype  = HWND

    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]
    SendMessage.restype  = LPARAM

    SendMessageStr = ctypes.windll.user32.SendMessageW
    SendMessageStr.argtypes = [HWND, UINT, WPARAM, LPCWSTR]
    SendMessageStr.restype  = LPARAM

    SendDlgItemMessage = ctypes.windll.user32.SendDlgItemMessageW
    SendDlgItemMessage.argtypes = [HWND, UINT, UINT, WPARAM, LPARAM]
    SendDlgItemMessage.restype = LPARAM

    WM_SETTEXT = 0x000C
    BM_CLICK = 0x00F5

    # see https://community.notepad-plus-plus.org/post/59785 for VB.net inspiration
    notepad.menuCommand(MENUCOMMAND.SEARCH_FIND)
    hFindWnd = FindWindow("#32770", "Find")
    hComboBx = FindWindowEx(hFindWnd, 0, "ComboBox", None) if hFindWnd else 0
    hFindStr = FindWindowEx(hComboBx, 0, "Edit", None) if hComboBx else 0
    SendMessageStr(hFindStr, WM_SETTEXT, 0, t)

    # set search mode:
    hNormBtn = FindWindowEx(hFindWnd, 0, "Button", "&Normal")
    if hNormBtn:
        SendMessageStr(hNormBtn, BM_CLICK, 0, None)

    # start search
    hFindBtn = FindWindowEx(hFindWnd, 0, "Button", "Find Next")
    #console.write(f"FindWindows: FIND={hFindWnd:08X} ComboBox={hComboBx:08X} FindNext:{hFindBtn:08X}\n")
    if hFindBtn:
        SendMessageStr(hFindBtn, BM_CLICK, 0, None)

    # TODO: I'd like to try SendDlgItemMessageW(hFindWnd, ctrlID, BM_CLICK, 0, 0), to avoid having to search for the "Find Next" button
    #   but using the 1625 from search macros, I couldn't get it to change Search Mode, so just manually click the buttons for now

def getStringFromNotification27482(args):
    code = args['code'] if 'code' in args else None
    idFrom = args['idFrom'] if 'idFrom' in args else None
    hwndFrom = args['hwndFrom'] if 'hwndFrom' in args else None
    #console.write(f"notification(code:{code}, idFrom:{idFrom}, hwndFrom:{hwndFrom}) received\n")
    if idFrom is None: return
    s = ctypes.wstring_at(idFrom)
    #console.write(f"\tAdditional Info: str=\"{s}\"\n")
    usePluginMessageString27482(s)

def getStringFromCommandLine27482():
    for token in sys.argv:
        if len(token)>15 and token[0:15]=="-pluginMessage=":
            s = token[15:]
            #console.write(f"TODO: process {token} => \"{s}\"\n")
            usePluginMessageString27482(s)

notepad.callback(getStringFromNotification27482, [NOTIFICATION.CMDLINEPLUGINMSG])
console.write("Registered getStringFromNotification27482 callback for CMDLINEPLUGINMSG\n")
getStringFromCommandLine27482()
