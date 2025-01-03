Started playing around with `lexilla\lexers\LexUser.cxx` and `PowerEditor\src\ScintillaComponent\UserDefineDialog.rc` and similar, seeing how the UDL interface really works.

### Dialog Layout

Per https://github.com/notepad-plus-plus/notepad-plus-plus/issues/12143 , experiment with dialog layout.  The following gives a horizontal layout inspired by that issue:
```
IDD_SYMBOL_STYLE_DLG DIALOGEX 36, 44, 466, 415
STYLE DS_SETFONT | DS_FIXEDSYS | WS_CHILD
FONT 8, "MS Shell Dlg", 0, 0, 0x0
BEGIN
    EDITTEXT        IDC_OPERATOR1_EDIT,15,31,205,19,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_OPERATOR2_EDIT,247,31,206,19,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler",IDC_OPERATOR_STYLER,14,12,54,14
    GROUPBOX        "Operators style",IDC_OPERATOR_DESCGROUP_STATIC,8,3,451,55,BS_CENTER
    RTEXT           "Operators 1",IDC_OPERATOR1_STATIC,142,20,75,8
    RTEXT           "Operators 2 (separators required)",IDC_OPERATOR2_STATIC,328,20,124,8
    EDITTEXT        IDC_DELIMITER1_BOUNDARYOPEN_EDIT,72,72,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER1_ESCAPE_EDIT,202,72,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER1_BOUNDARYCLOSE_EDIT,332,72,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler1",IDC_DELIMITER1_STYLER,14,71,54,14
    GROUPBOX        "Delimiter 1 style",IDC_DELIMITER1_DESCGROUP_STATIC,8,63,451,25,BS_LEFT
    LTEXT           " Open:",IDC_DELIMITER1_BOUNDARYOPEN_STATIC,72,58,56,8
    LTEXT           " Escape:",IDC_DELIMITER1_ESCAPE_STATIC,202,58,56,8
    LTEXT           " Close:",IDC_DELIMITER1_BOUNDARYCLOSE_STATIC,332,58,56,8
    EDITTEXT        IDC_DELIMITER2_BOUNDARYOPEN_EDIT,72,97,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER2_ESCAPE_EDIT,202,97,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER2_BOUNDARYCLOSE_EDIT,332,97,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler2",IDC_DELIMITER2_STYLER,14,96,54,14
    //RTEXT           "Open:",IDC_DELIMITER2_BOUNDARYOPEN_STATIC,251,90,56,8
    //RTEXT           "Escape:",IDC_DELIMITER2_ESCAPE_STATIC,251,109,56,8
    //RTEXT           "Close:",IDC_DELIMITER2_BOUNDARYCLOSE_STATIC,251,127,56,8
    GROUPBOX        "Delimiter 2 style",IDC_DELIMITER2_DESCGROUP_STATIC,8,88,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER3_BOUNDARYOPEN_EDIT,72,122,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER3_ESCAPE_EDIT,202,122,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER3_BOUNDARYCLOSE_EDIT,332,122,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler3",IDC_DELIMITER3_STYLER,14,121,54,14
    //RTEXT           "Open:",IDC_DELIMITER3_BOUNDARYOPEN_STATIC,12,176,56,8
    //RTEXT           "Escape:",IDC_DELIMITER3_ESCAPE_STATIC,12,195,56,8
    //RTEXT           "Close:",IDC_DELIMITER3_BOUNDARYCLOSE_STATIC,12,214,56,8
    GROUPBOX        "Delimiter 3 style",IDC_DELIMITER3_DESCGROUP_STATIC,8,113,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER4_BOUNDARYOPEN_EDIT,72,147,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER4_ESCAPE_EDIT,202,147,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER4_BOUNDARYCLOSE_EDIT,332,147,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler4",IDC_DELIMITER4_STYLER,14,146,54,14
    //RTEXT           "Open:",IDC_DELIMITER4_BOUNDARYOPEN_STATIC,251,176,56,8
    //RTEXT           "Escape:",IDC_DELIMITER4_ESCAPE_STATIC,251,195,56,8
    //RTEXT           "Close:",IDC_DELIMITER4_BOUNDARYCLOSE_STATIC,251,214,56,8
    GROUPBOX        "Delimiter 4 style",IDC_DELIMITER4_DESCGROUP_STATIC,8,138,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER5_BOUNDARYOPEN_EDIT,72,172,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER5_ESCAPE_EDIT,202,172,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER5_BOUNDARYCLOSE_EDIT,332,172,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler",IDC_DELIMITER5_STYLER,14,171,54,14
    //RTEXT           "Open:",IDC_DELIMITER5_BOUNDARYOPEN_STATIC,12,260,56,8
    //RTEXT           "Escape:",IDC_DELIMITER5_ESCAPE_STATIC,12,279,56,8
    //RTEXT           "Close:",IDC_DELIMITER5_BOUNDARYCLOSE_STATIC,12,299,56,8
    GROUPBOX        "Delimiter 5 style",IDC_DELIMITER5_DESCGROUP_STATIC,8,163,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER6_BOUNDARYOPEN_EDIT,72,197,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER6_ESCAPE_EDIT,202,197,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER6_BOUNDARYCLOSE_EDIT,332,197,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler",IDC_DELIMITER6_STYLER,14,196,54,14
    //RTEXT           "Open:",IDC_DELIMITER6_BOUNDARYOPEN_STATIC,251,261,56,8
    //RTEXT           "Escape:",IDC_DELIMITER6_ESCAPE_STATIC,251,280,56,8
    //RTEXT           "Close:",IDC_DELIMITER6_BOUNDARYCLOSE_STATIC,251,299,56,8
    GROUPBOX        "Delimiter 6 style",IDC_DELIMITER6_DESCGROUP_STATIC,8,188,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER7_BOUNDARYOPEN_EDIT,72,222,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER7_ESCAPE_EDIT,202,222,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER7_BOUNDARYCLOSE_EDIT,332,222,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler",IDC_DELIMITER7_STYLER,14,221,54,14
    //RTEXT           "Open:",IDC_DELIMITER7_BOUNDARYOPEN_STATIC,251,347,56,8
    //RTEXT           "Escape:",IDC_DELIMITER7_ESCAPE_STATIC,251,365,56,8
    //RTEXT           "Close:",IDC_DELIMITER7_BOUNDARYCLOSE_STATIC,251,384,56,8
    GROUPBOX        "Delimiter 7 style",IDC_DELIMITER7_DESCGROUP_STATIC,8,213,451,25,BS_LEFT
    EDITTEXT        IDC_DELIMITER8_BOUNDARYOPEN_EDIT,72,247,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER8_ESCAPE_EDIT,202,247,120,12,ES_MULTILINE | WS_VSCROLL
    EDITTEXT        IDC_DELIMITER8_BOUNDARYCLOSE_EDIT,332,247,120,12,ES_MULTILINE | WS_VSCROLL
    PUSHBUTTON      "Styler",IDC_DELIMITER8_STYLER,14,246,54,14
    //RTEXT           "Open:",IDC_DELIMITER8_BOUNDARYOPEN_STATIC,12,346,56,8
    //RTEXT           "Escape:",IDC_DELIMITER8_ESCAPE_STATIC,12,365,56,8
    //RTEXT           "Close:",IDC_DELIMITER8_BOUNDARYCLOSE_STATIC,12,385,56,8
    GROUPBOX        "Delimiter 8 style",IDC_DELIMITER8_DESCGROUP_STATIC,8,238,451,25,BS_LEFT
    GROUPBOX        "Delimiter 9 style",IDC_DELIMITER8_DESCGROUP_STATIC,8,263,449,25,BS_LEFT
    GROUPBOX        "Delimiter 10 style",IDC_DELIMITER8_DESCGROUP_STATIC,8,288,449,25,BS_LEFT
    GROUPBOX        "Delimiter 11 style",IDC_DELIMITER8_DESCGROUP_STATIC,8,313,449,25,BS_LEFT
    GROUPBOX        "Delimiter 12 style",IDC_DELIMITER8_DESCGROUP_STATIC,8,338,449,25,BS_LEFT
END
```

### Unicode keywords / etc

I was able to make a language with Unicode keywords, like `π αßΓ σαµ` and `σµτ ΦΘΩδ ταß` -- it will highlight those properly for UTF8 or UTF16, but if I use the same keywords in a Win1252 file, it won't match.

However, if I create a separate language, where the UDL XML is declared with `<?xml version="1.0" encoding="Windows-1252" ?>` prolog, and make sure the file itself is **ANSI**, then it matches up right, and keywords or operators or delimiters can use any character from the 1252 charset.  If I force N++ to interpret that same file as 1252 instead of ANSI, it stops matching.

Going back to the UTF8-BOM file and UTF-8-based XML/prolog, I was able to double-confirm: keywords work with unicode, but operators and delimiters do not.  Comment do not.  

| Category | Unicode | ANSI/1252 |
|----------|---------|-----------|
| Keyword  | Yes     | Yes       |
| Operator | No      | Yes       |
| Delimiter| No      | Yes       |
| Comment  | No      | Yes       |
| Number   | No      | Yes       |
| Fold     | No      | Yes       |

So in unicode mode, only keywords work.  If the file is 1252-encoded and N++ is "ANSI", then any character representable in 1252 is allowed.

Next, I could dig into how it's doing the pattern matching, and what exactly is being compared, to see what is different between the keyword search and operator search in Unicode, and between the operator search in unicode vs ANSI.

### LexUser.cxx

Looking at LexPython, I was able to add the `LexicalClass lexicalClasses[]` instance, which defines tags and descriptions for each of the SCE_USER_STYLE_... styles; I was able to make that compile -- I don't have PS on this N++, but in theory, that should mean that the stylerDebugger output should show information in the key.  Actually, let's add in PS2 and do that.  Had to do some debug to get styleDebugger.py working with UTF8 codepoint>127, but eventually able to get it working as with normal code: and with that, I have names for my KEY section.  Interestingly, despite the name of `_IDENTIFIER`, style#24 is really only ever used before whitespace (space, newline, etc)

While trying to loop over the vvstring (`vector<vector<string>>`) for operators1, it seems to stop at the first level: I cannot seem to get a string for the second index... at least not with my current printing scheme.  And I have VS2019, so it cannot build using N++'s VS2022 environment, so I cannot use debugger.
