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
  - The FAQ author has not come across a reference list that enumerates every Notepad++ command and whether it can be recorded in a macro or just played back in a manually-created macro or cannot be used at all in a macro.  If you know of such a list, or are willing to create it, feel free to contact the FAQ author, or put in a pull request to update the [github copy of this FAQ](https://github.com/pryrt/nppStuff/new/main/CommunityForum/FAQ/AutomatingNotepadPlusPlus.md).
- The Macro language is not a full programming language:
  - It has no variables.
  - It has no looping capability (other than [playing the full macro N times](https://npp-user-manual.org/docs/macros/#play-a-recorded-macro-multiple-times)).
  - It has no method of user input when the macro is running, so you cannot prompt for a file name or for text to be used for a complicated interaction.

## Plugins



## External Automation

