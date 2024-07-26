# UDL names/extensions in OPEN and SAVE AS

Per [Community: File extension List](https://community.notepad-plus-plus.org/topic/25967/file-extension-list), reminded of [GH ISSUE#11096](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/11096).
I want UDLs to be able to add their extensions into the SaveAs and Open dialogs' "File Type" filter list.

I did a little research:
- File>Open implemented in [NppIO.cpp::Notepad_plus::fileOpen()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/NppIO.cpp#L2112)
- uses a [CustomFileDialog](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/WinControls/OpenSaveFileDialog/CustomFileDialog.cpp#L914)
- the filters appear to be set using [Notepad_plus::setFileOpenSaveDlgFilters()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/NppIO.cpp#L928)
  - in theory, if i can find a similar structure for where Notepad++ stores the UDL names and extensions, I could add a similar loop to add in the UDL to the list
- UDL parse a given file with [NppParameters::feedUserLang()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.cpp#L3105), which puts them into the [`UserLangContainer* _userLangArray[NB_MAX_USER_LANG]`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.h#L1872)
  - [class UserLangContainer](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.h#L1112)
    - [`.getName()` and `.getExtension()`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.h#L1155-L1157) are the getters for the important elements of the class
      - thus, I believe, `_userLangArray[i].getName()` and `_userLangArray[i].getExtension()` are what I would need to get the strings I'm interested in.
    - [`NppParameters::getNbUserLang()`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/bfe27cc8602d510abc9dc12545dadae432614bd6/PowerEditor/src/Parameters.h#L1561) will tell me how many there are,
    - and [`NppParameters::getULCFromIndex(i)`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/bfe27cc8602d510abc9dc12545dadae432614bd6/PowerEditor/src/Parameters.h#L1562) will allow me to return the `UserLangContainer &` for that specific instance (rather than using `_userLangArray[i]`)

- for my loop, do I need ltFound/langType checking?
  - v8.6.9 behavior:
    - SaveAs on .md selects filter "All types (*.*)",
    - SaveAs on .txt uses filter "Normal text file (*.txt)"
    - SaveAs on .cpp uses filter "C++ source file (*.cpp;...)"
  - from what I can piece together, saveAs will send langType value, from the L_ constants, like L_CPP.  For all UDL languages, it should send L_USER (15).
  - the `getLangDesc(L_USER, false).c_str()` (similar to what's in the existing loop) will use [`getLangDesc()`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/bfe27cc8602d510abc9dc12545dadae432614bd6/PowerEditor/src/Notepad_plus.cpp#L2782), which adds `currentBuf->getUserDefineLangName();` after `L("udf - ")` for the language name.  
  - so in my loop, I'd want to do a string comparison with `getLangDesc()` vs `"udf - " + lName` to determine if it's the _same_ UDL; if so, mark ltFound

⇒ Thus, I think I want to loop on index:
```cpp
  for(size_t u=0; u<nppParam.getNbUserLang(); u++) 
  {
    UserLangContainer& ulc = nppParam.getULCFromIndex(u);
    const wchar_t *extList = ulc.getExtension();
    const wchar_t *lName = ulc.getName();

    wstring list(L"");
    if(extList)
      list += extList;

    wstring stringFilters = exts2Filters(list, showAllExt ? -1 : 40);
    const wchar_t *filters = stringFilters.c_str();
    if (filters[0])
    {
      fDlg.setExtFilter(lName, filters);

      // When it's UDL, then 
      //  if type isn't yet found,
      //    if strings match, the loop UDL is the same as the fileUDL, mark the type as found
      //  if it's still not found, keep looking higher
      if (langType == L_USER)
      {
        if (!ltFound)
        {
          wstring fileUdlString(getLangDesc(langType, true));
          wstring loopUdlString(L"udf - ");
          thisUdlString += lName;
          ltFound = loopUdlString.compare(fileUdlString) == 0;
        }
        if (!ltFound)
        {
          ++ltIndex;
        }
      }
    }
  }
```

TASKS:
- ☑ dig into the UDL parsing to figure out what structure the UDL name/ext pairs are put into: making progress (see above)
- ☑ see if i can add similar parsing
- ☐ possibly: see if I can rename the fake `langs.xml` extension from `normal text` to the fake name, when it's not found (that might be easier than adding UDL)
