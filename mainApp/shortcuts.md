in looking at https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15966 :

I was able to go to [`getKeyStrFromVal()`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/7544df534804319720540e0b1848bdc999b5e91e/PowerEditor/src/WinControls/shortcut/shortcut.cpp#L284-L301) and change 
```
	if (found)
		str = namedKeyArray[i].name;
```
to
```
	if (found) {
		str = namedKeyArray[i].name;
        str = "<<" + str + ">>";
        string _pryrt = "PRYRT: getKeyStrFromVal() => " + str;
        OutputDebugStringA(_pryrt.c_str());
        UINT out = MapVirtualKeyA((UINT)namedKeyArray[i].id, MAPVK_VK_TO_CHAR);
        char _pryrt_c[512];
        sprintf_s(_pryrt_c, "PRYRT: getKeyStrFromVal() => MapVirtualKeyA(id=%u, MAPVK_VK_TO_CHAR) => %u", namedKeyArray[i].id, out);
        OutputDebugStringA(_pryrt_c);
    }
```
... and this made all the menus and ShortcutMapper's table show `Modifier+<<X>>` instead of `Modifier+X` , so that means it's the right place.  And the dbgview64 shows `~` (192==VK_OEM_3==0xC0) maps to `out==96`, which is the `` ` ``/`~` key ... And I confirmed it does that mapping at some point during the first run when building those menus, along with every time the ShortcutMapper is loaded.

So, if I knew exactly where it was calling things to get the initial shortcuts for the menus during startup, I could edit the `namedKeyArray[]` table's `.name` field during that same time, which should allow it to just do the change once when the program is loaded.

But that doesn't tell me how to modify the combobox values; I would have to figure out how to do that (or where the populating is already done, since it's not in the .rc file), and then apply the same keyboard logic to the populator :

- `Shortcut::run_dlgProc` => `case WM_INITDIALOG`: uses `CB_ADDSTRING` to populate `IDC_KEY_COMBO` when the dialog is initialized (I don't know if that's just at startup, or every time it's run)
- Similarly in `ScintillaKeyMap::run_dlgProc`

So when I load program, that doesn't get run.  But when I launch MODIFY to get the shortcut dialog, then `Shortcut::run_dlgProc()` gets called.

So, in theory, I should be able to add it there... But it's not immediately working.
