# UDL names/extensions in OPEN and SAVE AS

Per [Community: File extension List](https://community.notepad-plus-plus.org/topic/25967/file-extension-list), reminded of [GH ISSUE#11096](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/11096).
I want UDLs to be able to add their extensions into the SaveAs and Open dialogs' "File Type" filter list.

I did a little research:
- File>Open implemented in [NppIO.cpp::Notepad_plus::fileOpen()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/src/NppIO.cpp#L2112)
- uses a [CustomFileDialog](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/WinControls/OpenSaveFileDialog/CustomFileDialog.cpp#L914)
- the filters appear to be set using [Notepad_plus::setFileOpenSaveDlgFilters()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/src/NppIO.cpp#L928)
  - in theory, if i can find a similar structure for where Notepad++ stores the UDL names and extensions, I could add a similar loop to add in the UDL to the list
- UDL parse a given file with [NppParameters::feedUserLang()](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/PowerEditor/src/Parameters.cpp#L3105), which puts them into the [`UserLangContainer* _userLangArray[NB_MAX_USER_LANG]`](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.h#L1872)
  - [class UserLangContainer](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/d8c6350918b76b040e55010feb0c16b7b03ac2da/PowerEditor/src/Parameters.h#L1112)

TODO:
- dig into the UDL parsing to figure out what structure the UDL name/ext pairs are put into: making progress (see above)
- see if i can add similar parsing
- possibly: see if I can rename the fake `langs.xml` extension from `normal text` to the fake name, when it's not found (that might be easier than adding UDL)
