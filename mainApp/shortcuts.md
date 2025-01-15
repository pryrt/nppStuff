in looking at https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15966 :

heavily reference [MSLearn: Virtual-Key Codes](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes) and [Shortcut FAQ](https://community.notepad-plus-plus.org/topic/19734/faq-list-of-notepad-key-combinations-available-for-shortcuts)

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

Ah, I was in the ScintillaKeyMap, not the Shortcut.  When I went there, I started making it work.

After some debug, set up a separate map which can hold the updated key characters... what I get:
```c++
bool mapped_vk_oem = false;
map<UCHAR, char*> map_of_vk_oem;
void _map_vk_oem()
{
    const size_t MAX_MAPSTR_CHARS=16;
    const LANGID EN_US = 0x0409;
    
    // this function should only be called once, so update the flag
    mapped_vk_oem = true;
    
    // determine the active keyboard "language"
    LANGID current_lang_id = LOWORD(GetKeyboardLayout(0));
    
    // Debug only:
    wchar_t _tmp_str[512];
    swprintf_s(_tmp_str, L"PRYRT: _map_vk_oem(): current_lang_id=0x%04X", current_lang_id);
    OutputDebugStringW(_tmp_str);
    
    // for each of the namedKeyArray, check if it's VK_OEM_*, and update the map of VK_OEM names as needed
    for (size_t i = 0 ; i < nbKeys ; ++i)
    {
        // only need to map the VK_OEM_* keys, which are all at or above 0xA0
        if(namedKeyArray[i].id >= 0xA0) {
            // first make sure there's a slot in the map for the current id=>STR mapping
            if (map_of_vk_oem.find(namedKeyArray[i].id) == map_of_vk_oem.end())
            {
                char* pstr = new char[MAX_MAPSTR_CHARS+1];
                map_of_vk_oem[namedKeyArray[i].id] = pstr;
            }

            // now update the STR in the mapping
            sprintf_s(map_of_vk_oem[namedKeyArray[i].id], MAX_MAPSTR_CHARS, "%c", MapVirtualKeyA((UINT)namedKeyArray[i].id, MAPVK_VK_TO_CHAR));

            // en-US only: change from ` to ~, because that's what's historically been shown
            if(current_lang_id==EN_US && map_of_vk_oem[namedKeyArray[i].id][0]=='`')
            {
                map_of_vk_oem[namedKeyArray[i].id][0] = '~';
            }

            // Debug Only
            swprintf_s(_tmp_str, L"PRYRT: map i=%d id=%d => '%hs'", i, namedKeyArray[i].id, map_of_vk_oem[namedKeyArray[i].id]);
            OutputDebugStringW(_tmp_str);
        }
    }
    return;
}

... IN getKeyStrFromVal()
	if(!mapped_vk_oem) { _map_vk_oem(); }
	...
	if (found)
	{
		if(namedKeyArray[i].id >= 0xA0) 
		{
			str = map_of_vk_oem[namedKeyArray[i].id];
		}
		else
		{
			str = namedKeyArray[i].name;
		}
	}

... IN both Shortcut::run_dlgProc() and ScintillaKeyMap::run_dlgProc():
			if(!mapped_vk_oem) { _map_vk_oem(); }
	...
				if(namedKeyArray[i].id >= 0xA0) {
					::SendDlgItemMessage(_hSelf, IDC_KEY_COMBO, CB_ADDSTRING, 0, reinterpret_cast<LPARAM>(string2wstring(map_of_vk_oem[namedKeyArray[i].id], CP_UTF8).c_str()));
				} else {
					::SendDlgItemMessage(_hSelf, IDC_KEY_COMBO, CB_ADDSTRING, 0, reinterpret_cast<LPARAM>(string2wstring(namedKeyArray[i].name, CP_UTF8).c_str()));
				}


```

But, as far as I can tell with a single keyboard option, that should work.

I need to copy that off to a temporary location, and create a new branch (FROM main, not the existing branch).  New (clean) branch exists, and working as before.

**Win > Settings > Time & Language > Language**: add a language, **Portuguese (Brazil)**.  Switch to POR and launch N++: it properly gives a different set of characters -- but not all of them display properly.  I will need to add back in some debugging prints, to see if I can figure out what characters it wants.

Okay, so what it does is it does 0x80000000|C, where C is the 1-byte char in the ActiveCodePage.  So I need to trap for the 0x80000000.
But the MultiByteToWideChar(CP_UTF8) (which is used elsewhere) is expecting its input to be a multibyte character string with proper UTF8-encoding... so if C>0x7F, I need to have properly encoded the codepoint to multiple bytes.

So I came up with something that worked -- creating a psueod-widechar from the v2c value -- but I think it's a hack that's likely to go wrong someplace.  I want a safety commit, but then I want to start exploring MapVirtualKeyW instead, because that will keep it wide to begin with, without ambiguity (I hope).

Okay, the experimental version of MapVirtualKeyW() implementation seems to get the same results for POR(BRAZIL), so I am hoping that it will work for other languages as well.  Quickly verified it still works with en-US keyboard as well.
**TODO**: I need to merge it above for the >127; then I need to see if it makes sense to just use the W to begin with (but not enough time today)

--

Today, I was able to collapse those down, and also tried with German QWERTZ keyboard.  I think things are working, to the best of my ability to test.  Make a [comment on the issue](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15966#issuecomment-2578036556) giving the OP the steps to test my experimental build.

----

That all worked, and I cleaned it up and (after Don's confirmation) put in a PR with just fixing the names.

I had also been working on adding the unique-to-keyboard keys: I got it working for French by Jan 14, and I think I have it basically working for ABNT2 keyboard Jan 15.  I will want \@gusgo to verify, but my request indicates a technical failure in the fix-the-names commit (since it needs the extra calls that I've got there), and I don't want to advertise this to Don at this point.  Once the original has been accepted, I will want to send the following comment:
```
https://github.com/notepad-plus-plus/notepad-plus-plus/issues/16071

\@gusgo,

I am not an expert on the ABNT2 keyboard (never touched one); I've been using Microsoft's `osk.exe` onscreen keyboard tool to test most of the keyboard shortcuts I've been experimenting with; but even when I change the **Options** to show keypad**, I cannot test the extra `.` key on the keypad, because `osk.exe` doesn't include that extra key.

Could you use [this experimental build](https://github.com/pryrt/notepad-plus-plus/actions/runs/12793637914#artifacts) to verify that you can correctly set keyboard shortcuts on either the normal commands or the Scintilla commands using the `/` key, the `Num .` , and the `Num ,` and that the right physical key activates those shortcuts for each?

Thank you.
```
