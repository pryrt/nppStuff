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

#### Visual Studio Single-Step

I went into all three projects, and in the **Properties > General > Platform Toolset**, changed from v143 to v142 (had to do it for Active/Active, then changed to Active/All and confirmed it was really changed for all).  (I also had to turn of warnings==errors in **Properties > C/C++ > Treat Warnings As Errors**; and I added `#pragma warning ( push ) // #pragma warning( disable: 26438 ) // ...scan_number()... // #pragma warning ( pop )` in json.hpp; `NppDarkMode.cpp` needed `#ifndef DWMWA_USE_IMMERSIVE_DARK_MODE // #define DWMWA_USE_IMMERSIVE_DARK_MODE 20 // #endif`

Single stepping through, I didn't notice any anomaly when doing keywords for ASCII vs UTF8 -- keywords use the "backwards search" logic, because it starts at the end of the word and compares backwards.  But when I switched to doing operators, `isInListForward()` iterates through the operators, and when it gets to `±` (codepoint=`0xB1`, UTF-8 bytes=`0xC2 0xB1`), it then calls Match(), and `*s` is `0xC2 0xB1` whereas `ch` (from the scintilla content) is just the codepoint `0xB1`... So i'm going to have to dig more into it with the backwards-search on keywords, to see how it interprets the keyword and document-text if ± was defined as a keyword, not an operator.

Okay, when I dig into `isInListBackward()` for `±`, `firstChar` is set to `0xC2`, which is what I would expect.  Oh, I wonder if the forward search on the operator is meaning that the active char has fast forwarded to the last of the UTF-8-encoded sequence, so it's not comparing correctly.  I wish I had picked a symbol whose final byte was _not_ the same as the codepoint.  

I think maybe next I'll try `⅀ U+2140` => `0xE2 0x85 0x80` , so that will be unambiguous.  It worked fine as a keyword.  Just before calling `Match()` in `isInListForward()`, sc.ch=`⅀`, sc.width=3 and iter2="`â…€`=``0xE2 0x85 0x80`"; moving into Match(), `*s` is the 3byte char-string from iter2; ch is the sc.ch from outside.  So the problem comes because `ch` is an `int` whereas `*s` is `char` -- so it's comparing apples and oranges.  If I force a `return true`, it properly skips forward the 3 -- wait, when I get back to the main loop, `sc.Forward(skipForward)` skips 3 characters instead of 3 bytes.  That's annoying.  And when it highlights, it highlights 3 characters instead of 3 bytes.  Ah, for the simplicity of coding when you didn't have to worry about multi-byte characters.  

I just don't understand how the logic and comparison worked correctly when doing it backward instead of forward.  Let's move it back to keyword, and see if I can figure out whether there's an equivalent to the Match() or if something else is called.  Okay, so it moves to the space _after_ the keyword, which then starts a backwards search; it sees the sc.LengthCurrent() is 3: I think they really get confused as to what is really a byte and what is a character; I am now curious about UDL for normal or high characters with the UTF16-LE, which I will try soon.  So it is comparing firstChar (probably better as firstByte) to the first element of char[] list.WordAt(i): WordAt works with bytes, so that's why it matches.  For operators (ie, `Match()`), I am wondering whether the `sc.GetRelative()` or the `styler.SafeGetCharAt()` that it calls might be a better choice, rather than accessing `sc.ch` directly; hmm, but `sc.Match()` is in the lexilla::`StyleContext.h`, so it's not something that I can change to make Notepad++ work correctly, so I might have to make my own alternate version of Match()
