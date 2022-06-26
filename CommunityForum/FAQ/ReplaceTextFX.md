# FAQ Desk: How do I Replace the Features of TextFX?

Hello, and welcome to the FAQ Desk.  You have likely been directed here because you were a user of TextFX and need an alternative.

## TextFX is Abandonware

The last official version of TextFX (0.2.6) was from 2009.  That pre-dates Notepad++'s 64-bit version (v7.0), so TextFX has never been (officially) usable on 64-bit Notepad++.  And as of Notepad++ v8.4, the TextFX plugin causes problems for even the 32-bit version of Notepad++.  So now, you need an alternative for some of the features.

Fortunately for you, Notepad++ has improved a lot since 2009, and many of the features are actually built into Notepad++.  Other features are implemented in other plugins already.  Some can be replaced by Macros (especially recording macros of search-and-replace operations).  And some can be implemented with a script in one of the scripting plugins like PythonScript.

## A menu-by-menu list of possible alternatives

### TextFX Characters

- Quote operations: easy to do with macros of "in selection" searches (this will be called _s/r macro_ from here on out)
- Case Toggles == **Edit > Convert Case To**
- Zap: _s/r macro_

### TextFX Quick

- Mark Word or ... == **Search > Select and Find ...**
- Find Matching ... == **Search > Goto/Select Matching Brace**
- Find/Replace == **Find** or **Replace**
- Duplicate == **Edit > Line Operations > Duplicate...**

### TextFX Edit

- Fill Down... == Copy what you want to fill, and either column-select or multi-select and paste
- Insert Through Lines == that's just a normal column-select paste
- Reindent == There are plugins that do that for particular languages, or you can use NppExec or PythonScript to define a "pretty" command which will call an external "pretty-print": see [this post](https://community.notepad-plus-plus.org/post/45549)
- Most of the useful space-related are now in **Edit > Blank Operations**
- Indent and surround with: _macro_
- Strip/Split: _macro_
- LineUp == Plugin:**Elastic Tabstops**
- Unwrap == similar to join followed by a replace, or just a replace
- Rewrap == <implement in pythonscript>
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
  
- There are lots of HTML and XML plugins (XML Tools especially); or you can use NppExec or PythonScript to define a "pretty" command which will call an external "pretty-print": see [this post](https://community.notepad-plus-plus.org/post/45549)
  
### TextFX Tools
  
- Sort: **Edit > Line Operations**
- ASCII Chart: **Edit > Character Panel** gives similar info
- Insert Ruler: Plugin=Column Tools
- Insert Line Numbers: easy enough with **Edit > Column Editor**
- Delete Line Numbers: column select and `DEL`, or _s/r macro_
- Clean Email Quoting: _s/r macro_
- \*decode: Plugins:MIME Tools
- Word Count: **View > Summary**
- Add Up Numbers: @alan-kilborn posted a PythonScript solution [here](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/11461#issuecomment-1086028467); you can find instructions for how to install PythonScript and bring in this script in [this FAQ](https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript/1)

### TextFX Viz
  
- It looks like that would require a new plugin, or significant coding in PythonScript

## Contributing
  
If you have more suggestions for this FAQ, let @peterjones know
