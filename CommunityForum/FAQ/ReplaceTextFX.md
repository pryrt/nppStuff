# FAQ Desk: How do I Replicate the Features of TextFX?

Hello, and welcome to the FAQ Desk.  You have likely been directed here because you were a user of TextFX and need an alternative.

## TextFX is Abandonware

The last official version of TextFX (0.2.6) was from 2009.  That pre-dates Notepad++'s 64-bit version (v7.0), so TextFX has never been (officially) usable on 64-bit Notepad++.  And as of Notepad++ v8.4, the TextFX plugin causes problems for even the 32-bit version of Notepad++. (Starting in Notepad++ v8.4.3, Notepad++ will actively disable old copies of TextFX, because the plugin actions crashing Notepad++ is dangerous for data integrity.) So now, you need an alternative for some of the features.  (Or you need to revert to a version of Notepad++ 32bit before v8.4, and understand that you cannot upgrade Notepad++ if you continue to want to use TextFX.)

Fortunately for you, Notepad++ has improved a lot since 2009, and many of the features are actually built into Notepad++.  Other features are implemented in other plugins already.  Some can be replaced by Macros (especially recording macros of search-and-replace operations).  And some can be implemented with a script in one of the scripting plugins like PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS).

## Possible alternative plugins

### NPPTextFX2

@rainman74 is working on an [NPPTextFX2](https://github.com/rainman74/NPPTextFX2) replacement plugin.  As of the 1.0 release, it works with v8.4-and-newer, though there are a couple of menu entries that were disabled for now.  @rainman74 says that most of the functions also work under 64bit, except for the **TextFX Edit** submenu.  But since that user seems willing to actively maintain the plugin, there is a chance that eventually all of TextFX's features will be fixed in NPPTextFX2, and maybe even get full 64bit compatibility.

### NppTextViz

KubaDee has a [NppTextViz](https://github.com/KubaDee/NppTextViz) plugin, which has a 64bit version, which claims:
> This plugin is meant to hide or show lines to help you analysing larger files - logs for example. You can hide all lines that contain text pattern. Or simply select several lines and hide them.
> 
> Plugin is based on TextFX plugin v0.25 by Chris Severance.

It does not document, beyond "hiding lines", what other features it supplies based on the original TextFX.

Unfortunately, it has not been updated in two years, and suffers with similar incompatibilities with Notepad++ v8.4-and-newer.

## A menu-by-menu list of possible alternatives

Please note that all search/replace actions below assume Search Mode is set to Regular Expression.  If you want to take the action only on the selected text, you must checkmarl the **☑ In Selection** search-and-replace option.

### TextFX Characters

- Quote operations:
    - Convert SIMPLE quotes to DOUBLE quotes :
        - N++ SEARCH  :  `(')|(‘)|(’)`
          N++ REPLACE :  `(?1")(?2“)(?3”)`
        OR
        - N++ SEARCH  :  `'`
          N++ REPLACE :  `"`
    - Convert DOUBLE quotes to SIMPLE quotes :
        - N++ SEARCH  :  `(")|(“)|(”)`
          N++ REPLACE :  `(?1')(?2‘)(?3’)`
        OR
        - N++ SEARCH  :  `"`
          N++ REPLACE :  `'`
    - Swap DOUBLE and SIMPLE quotes :
        - N++ SEARCH  :  `(')|(")|(‘)|(’)|(“)|(”)`
          N++ REPLACE :  `(?1")(?2')(?3“)(?4”)(?5‘)(?6’)`
        OR
        - N++ SEARCH  :  `(')|(")`
          N++ REPLACE :  `(?1")(?2')`
    - Drop DOUBLE and SIMPLE quotes :
        - N++ SEARCH  :  `'|"|‘|’|“|”`
          N++ REPLACE :  Leave EMPTY
        OR
        - N++ SEARCH  :  `'|"`
          N++ REPLACE :  Leave EMPTY
    - ESCAPE `"` to `\"` :
        - N++ SEARCH  :  `"`
          N++ REPLACE :  `\\"`
    - ESCAPE `'` to `\'` :
        - N++ SEARCH  :  `'`
          N++ REPLACE :  `\\'`
    - ESCAPE `'` to `\"` :
        - N++ SEARCH  :  `'`
          N++ REPLACE :  `\\"`
    - ESCAPE both `"` to `\"` and `'` to `\'` :
        - N++ SEARCH  :  `'|"`
          N++ REPLACE :  `\\$0`
    - UNESCAPE `\"` to `"` :
        - N++ SEARCH  :  `\\"`
          N++ REPLACE :  `"`
    - UNESCAPE `\'` to `'` :
        - N++ SEARCH  :  `\\'`
          N++ REPLACE :  `'`
    - UNESCAPE `\"` to `'` :
        - N++ SEARCH  :  `\\"`
          N++ REPLACE :  `'`
    - UNESCAPE both `\"` to `"` and `\'` to `'` :
        - N++ SEARCH  :  `\\('|")`
          N++ REPLACE :  `\1`
    - ESCAPE `"` to `""` :
        - N++ SEARCH  :  `"`
          N++ REPLACE :  `""`
    - ESCAPE `'` to `""` :
        - N++ SEARCH  :  `'`
          N++ REPLACE :  `""`
    - UNESCAPE `""` to `"` :
        - N++ SEARCH  :  `""`
          N++ REPLACE :  `"`
    - UNESCAPE `""` to `'` :
        - N++ SEARCH  :  `""`
          N++ REPLACE :  `'`
- Case Toggles
    - UPPER CASE
    - lower case
    - Proper Case
    - Sentence case
    - iNVERT cASE
        - N++ option :  **Edit > Convert Case to > ...**
- Zap:
    - Zap all characters to space
        - N++ SEARCH  :  `.`
          N++ REPLACE :  `\x20`
    - Zap all non-printable characters to `#`
        - N++ SEARCH  :  `(?s)(?![\x{0020}-\x{007E}\t\r\n]).`
          N++ REPLACE :  `#`

### TextFX Quick

- Mark Word or Find Reverse :
    - **Search > Select and Find Previous** ( `Ctrl + Shift + F3` )
- Mark Word or Find Forward :
    - **Search > Select and Find Next** ( `Ctrl + F3` )
- Find Matching {([ <Brace> ])} :
    - **Search > Goto Matching Brace**
- Mark to Matching {([ <Brace> ])} :
    - **Search > Select Matching Brace**
- Delete Marked {([ <Brace> ])} Pair :
    - **Search > Select Matching Brace** , then DEL
- Mark lines to matching {([ <Brace> ])} :
    - No exact duplicate, but **Search > Select Matching Brace** gets you close
- Find/Replace :
    - See the N++ **Search / Replace / Find in Files / Mark** dialog ( `Ctrl + F`, `Ctrl + H`, `Ctrl + Shift + F`, `Ctrl + M` )
- Duplicate Line or Block :
    - **Edit > Line Operations > Duplicate Current Line** ( `Ctrl + D` )

### TextFX Edit

- Fill Down... == Copy what you want to fill, and either column-select or multi-select and paste
- Insert Through Lines == that's just a normal column-select paste
- Reindent == There are plugins that do that for particular languages, or you can use NppExec or PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS) to define a "pretty" command which will call an external "pretty-print": see [this "Python Indent..." discussion](https://community.notepad-plus-plus.org/post/45549)
- Most of the useful space-related are now in **Edit > Blank Operations**
- Indent and surround with: _macro_
- Strip/Split: _macro_
- LineUp == Plugin:**Elastic Tabstops**
- Unwrap == similar to join followed by a replace, or just a replace
- Rewrap == this can be implemented in PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS): [this "rewrap script"](https://community.notepad-plus-plus.org/post/78262)
- Pad Rectangular == modern notepad++ already allows column-select beyond end of line, to keep it a rectangle

### TextFX Convert

- Most of the first section is handled by default plugins MIME Tools and Converter
- Rot13 is a gimmick
- EBCDIC: if you still need this, you probably have a command-line tool that already converts EBCDIC to UTF-8, like [iconv](http://gnuwin32.sourceforge.net/packages/libiconv.htm) `iconv -f EBCDIC  -t UTF-8  file-to-translate.txt`
- KOI8R: also handled by `iconv`

### TextFX Insert
  
- File Info: Right click on the tab title, and select **Full File Path to clipboard** (and similar)
- Date/Time: **Edit > Insert**

### TextFX HTML Tidy
  
- There are lots of HTML and XML plugins (XML Tools especially); or you can use NppExec or PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS) to define a "pretty" command which will call an external "pretty-print": see [this "Python Indent..." discussion](https://community.notepad-plus-plus.org/post/45549)
  
### TextFX Tools
  
- Sort: **Edit > Line Operations**
- ASCII Chart: **Edit > Character Panel** gives similar info
- Insert Ruler: Plugin=Column Tools
- Insert Line Numbers: easy enough with **Edit > Column Editor**; [this script](https://community.notepad-plus-plus.org/post/78328) for PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS)  will do it for the current selection without needing column-selection mode
- Delete Line Numbers: column select and `DEL`, or _s/r macro_
- Clean Email Quoting: _s/r macro_
- \*decode: Plugins:MIME Tools
- Word Count: **View > Summary** for the whole document; [this script](https://community.notepad-plus-plus.org/post/78320) for a PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS) solution that works on the active selection
- Add Up Numbers: [here](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/11461#issuecomment-1086028467) is a script implementation in PythonScript[¹](#:~:text=NOTE%20ON%20PYTHONSCRIPT%20SOLUTIONS)

### TextFX Viz
  
- It looks like that would require a new plugin, or significant coding in PythonScript

### ¹Note on PythonScript Solutions

You can find instructions for how to install PythonScript and bring in a linked script in [this FAQ](https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript/1)

If it can be done in PythonScript, it can be done in others of the scripting plugins as well (like LuaScript or jN Notepad++ Plugin); most of the suggestions here are in PythonScript because that's the solution style that gets the most examples in the Forum.  (If you want to Contribute equivalent solutions in your scripting plugin of choice, such suggestions are welcome!)

## Contributing
  
If you have more suggestions for this FAQ, let @peterjones know by \@-mentioning him in a new or already-existing-and-related [Help Wanted](https://community.notepad-plus-plus.org/category/4/help-wanted) or [General Discussion](https://community.notepad-plus-plus.org/category/2/general-discussion) thread

If there is an existing implementation of one of these scripts or regex/macro solutions, please give me a link to which post implements it, and I will add a link from this FAQ to that implementation post.
