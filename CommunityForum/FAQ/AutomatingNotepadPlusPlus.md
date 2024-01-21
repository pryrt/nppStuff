# FAQ: Automating Noteapd++

Users often question whether Notepad++ has scripting or other automation capabilities available.

_Natively_, Notepad++ has [**Macros** functionality](https://npp-user-manual.org/docs/macros/), which allows you to record various Notepad++ menu commands, including search-and-replace commands.

If you need more power than macros provide, and have some skill with programming, then there are many Notepad++ Plugins that provide the power of a full programming language with an interface to the Notepad++ menus and the file buffers that are open inside Notepad++.  And if that wasn't enough, you can also do external remote-control of Notepad++.

## Macros

The Notepad++ built-in macro facility allows recording Notepad++ actions (both menu commands and file-editing actions), and playing them back once or repeatedly; macros can be just for a single session, or saved so that they are available every time you run Notepad++.  The [Online User Manual](https://npp-user-manual.org/) includes instructions on how to use the [**Macros** system](https://npp-user-manual.org/docs/macros/), along with a technical discussion of [format for saved macros in the config files](https://npp-user-manual.org/docs/config-files/#macros) so that you can manually edit an existing macro or create one from scratch, so that information will not be repeated here.  Any saved macro can be easily given a keyboard shortcut when it is save or by using Notepad++'s [Shortcut Mapper](https://npp-user-manual.org/docs/preferences/#shortcut-mapper) for an already-existing macro.

For many, Macros are sufficient for their automation needs, especially because it can automate multi-step search-and-replace sequences and the like.  However, there are some limitations on Macros that might help you decide to move on to something more powerful than the built-in Macros system:

- Some Notepad++ menu commands are not available to macros:
  - Some cannot be saved in a macro because they require user input, which the Macros feature doesn't support (so actions like **Save As** are not available).
  - Some used to be available, but after an [EU-FOSSA](https://joinup.ec.europa.eu/collection/eu-fossa-2/about) review some years ago, they were removed from the macro-recording capability due to their potential for abuse by malicious macros.
  - Some can be used by macros, but due to technical difficulties are just not recorded when you try to record a macro.  On those, if you manually edit or create a macro by editing the `shortcuts.xml` config file, you can still use them.
  - If you run across a command that doesn't get recorded when you are making a macro, you can try to manually edit the macro to include that command.  If it works, great.  If not, then unfortunately, you needs may be outside of a macro's capabilities.
  - The FAQ author has not come across a reference list that enumerates every Notepad++ command and whether it can be recorded in a macro or just played back in a manually-created macro or cannot be used at all in a macro.  If you know of such a list, or are willing to create it, feel free to contact the FAQ author, or put in a pull request to update the [GitHub copy of this FAQ](https://github.com/pryrt/nppStuff/new/main/CommunityForum/FAQ/AutomatingNotepadPlusPlus.md).
- The Macro language is not a full programming language:
  - It has no variables.
  - It has no looping capability (other than [playing the full macro N times](https://npp-user-manual.org/docs/macros/#play-a-recorded-macro-multiple-times)).
  - No conditional execution ("if/then/else" or similar constructs).
  - It has no method of user input when the macro is running, so you cannot prompt for a file name or for text to be used for a complicated interaction.

## Plugins

There are a variety of plugins which embed a full programming language in the Noteapd++ environment, which gives scripts in that plugin the ability to access Noteapd++ command and perform actions on the files open in Notepad++, with the full power of a programming language (with variables, looping, conditionals, user input, and libraries that are avaialable for that language).

The plugins linked below can all be installed through the Plugins Admin interface.  The first two get more mentions in the Community, because they are the ones that many of the regulars use, but all are reasonable choices for Notepad++ automation through scripting.

- [NppExec](https://github.com/d0vgan/nppexec) - This was one of the earliest "scripting" languages, which provides capabilities similar to a Windows batch file, but more powerful.  This is great if you are wanting to automate saving, file-system operations, and the like; it is also frequently used for gluing together a process using linters, code-cleaners, compilers, and even running the code in a console in Notepad++.
- [PythonScript](https://github.com/bruderstein/PythonScript) - Provides Python-based scripting (for now, Python 2.7 for the default PythonScript 2 installed via Plugins admin, though a Python 3.x interpreter is available by using one of the 3.0.X "alpha" pre-release versions that you can [download at GitHub](https://github.com/bruderstein/PythonScript/releases)).
  - PythonScript solutions are so common in the Commuity that we have an entire FAQ entry devoted to [installing and using scripts in PythonScript](/topic/23039).
- [ActiveX Plugin](https://sourceforge.net/projects/nppactivexplugin/)
- [Automation Scripts](https://github.com/oleg-shilo/scripts.npp) - This provides C#-based scripting.
- [jN Notepad++ Plugin](https://github.com/sieukrem/jn-npp-plugin/wiki) - This provides JavaScript-based scripting.
- [LuaScript](https://github.com/dail8859/LuaScript) - This provides Lua-based scripting.

There may be other scripting plugins that aren't available in the Plugins Admin (and possibly even ones that are listed there, but they haven't come up in the Community or aren't described in the Plugins Admin in a way that makes it obvious that they include Notepad++ automation capabilities).

Some users may argue that "if it requires a plugin, then Notepad++ doesn't _really_ support scripting".  The FAQ author and many Community members disagree: the Notepad++ Developer seems to have chosen to "support" scripting by encouraging the creation of and use of scripting plugins that interally use the plugin API that Notepad++ provides.  The Developer seems content to not "compete" with plugins by adding functionality that one or more plugins already successfully implement (this also frees up his time to focus on the core of Notepad++, rather than spending his time on maintaing and supporting one or more scripting languages, which is not where his interests apparently lie).

## External Automation

Any external application that can send keystrokes to a chosen application or use the Win32 API's `SendMessage` interface can control.

Some external tools known to be able to control Notepad++:

- [AutoHotKey](https://www.autohotkey.com/) - This is a popular automation tool used on Windows, and Community members sometimes share AHK scripts to perform Notepad++ automation tasks.
- [Win32::Mechanize::NotepadPlusPlus](https://metacpan.org/pod/Win32::Mechanize::NotepadPlusPlus) - This module for the Perl programming language supplies an interface similar to the scripting plugins, using a copy of Perl installed externally to Notepad++.
  - Though some Community members kindly refer to it as "PerlScript" due to it's similarity to the "PythonScript" plugin, it is _not_ a plugin.  The biggest drawback is that not include the menu interface provided by the  scripting plugins, so you cannot easily choose or create or edit a script from the Notepad++ menus.
