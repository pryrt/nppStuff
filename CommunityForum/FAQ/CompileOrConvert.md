Hello, and welcome to the FAQ Desk. You have likely been directed to this page because you asked a question about compiling your source code from within Notepad++, or replace your text with the output of some external program (pretty-printer, formatter, encrypter, etc).

In general: almost exactly the same as if you were compiling or converting it from the command line.

### Compiling

Please note that Notepad++ is _not_ a compiler: if you do not have a separate executable that can compile your source code into an executable, Notepad++ cannot compile it for you.

* If all you need is a single command based on the filename, for example you normally type `"c:\path with spaces\to\compiler.exe" "FILENAMEHERE.cs"` at the command line, where `FILENAMEHERE.cs` is your desired file to compile, then you can just use the builtin **Run** menu's **Run** command, where you could type `"c:\path with spaces\to\compiler.exe" "$(FULL_CURRENT_PATH)"` (using the quotes around each term, because there can be spaces in those paths)

    * the official docs have a section on [User Defined Commands](https://npp-user-manual.org/docs/config-files/#userdefinedcommands), which includes a description of the "environment variables" like `$(FULL_CURRENT_PATH)` that the **Run** command recognizes.

    * you can click the **Save** button in the **Run** dialog to save that command for later, and even assign a keyboard shortcut for later use.  It will show up in the **Run** menu from now on.  You can even use the Shortcut Mapper to assign a keyboard shortcut to the compile command.

* If you have a more complicated build need, which needs to set other environment variables, or run multiple commands (compile and link as separate steps, for example; or compile then run the resulting executable) you can either create a windows batch file or use a Notepad++ plugin.

    * For a windows batch file (`.bat` or `.cmd` or `.ps1` file -- whatever you are most comfortable with), you can pass the filename as an argument to your batch file instead of directly to the compiler: `c:\path\to\batchfile.bat "$(FULL_CURRENT_PATH)"`

    * You can use a plugin like the NppExec plugin, which has its own batch scripting language.  For example, the following is an NppExec script which takes the the current `.c` file, saves any changes, compiles, and then runs the resulting `.exe` (with any output going into the NppExec console inside Notepad++):

            npp_save
            cd "$(CURRENT_DIRECTORY)"
            c:\path\to\gcc.exe "$(FILE_NAME)" -o "$(NAME_PART)"
            npp_run cmd.exe /k "$(NAME_PART)"

        * Note: I recommend using the full path to your compiler in your script

        * The NppExec script can be added to the Macro menu using **Plugins > NppExec > Advanced Settings**, and once in the Macro menu, you can use the **Macro > Modify Shortcut** command to add a keyboard shortcut for that script.

### Converting

This same procedure will work for tasks that are similar to compiling, like "how can I use Notepad++ to launch some external converter program?" -- examples might be encryption/decryption, or a program that converts Markdown to HTML, etc.  If you want to keep the source code, and have the output of the conversion in a new file, then the instructions above will work.  However, if you want to convert the text _in place_, so that the result of the conversion _replaces_ the text currently in the editor, here are a few options:

* There is a Plugin available in Plugins Admin called "[Pork to Sausage](https://github.com/npp-plugins/pork2sausage)", whose entire purpose in life is to convert text from one form to another, using an external program.

    - _Note_: Pork to Sausage works on the active selection; if there is no active selection, Pork to Sausage will not send your whole file to the converter, even though that might be the natural assumption
    - _Note_: Pork to Sausage takes the text characters from the active selection, encodes them as UTF-16 LE, and sends that UTF-16 LE bytestream to the converter.  This is true even if the underlying file is ANSI or UTF-8 encoded, so if the difference in byte representation matters to your converter, you will need to use a different option, like the NppExec script below.

* If you want to use NppExec, it is similar to the script above.  One technique is to save output of your converter to a temporary file, and then copy the contents of that temporary file overtop the file active in Notepad++.  (This example uses the gpg executable to encrypt your file, but the ideas are similar for other processes as well.  The comments after the `//` should tell you the purpose of each line, so you can use those to help you develop your own script to run your converter program.)

        cls
        npp_save
        cmd.exe /c exit %RANDOM%                                                        // cannot access $(SYS.RANDOM) directly through NppExec, but can tell cmd.exe to return it as a value
        set tempfile = $(SYS.TEMP)\NppGpgFile_$(EXITCODE).tmp                           // create random tempfile name
        set ascfile = $(SYS.TEMP)\NppGpgFile_$(EXITCODE).asc                            // create associated ascfile name
        sci_sendmsg SCI_SELECTALL                                                       // select all
        sel_saveto $(ascfile) :a                                                        // save selection to the ascfile    (use :a to save as ansi, to prevent unicode prefix ÿþ getting embedded)
        "c:\path\to\gpg.exe" --output "$(tempfile)" --decrypt "$(ascfile)"              // decrypt
        sel_loadfrom $(tempfile)                                                        // replace selection with results
        sci_sendmsg SCI_DOCUMENTSTART                                                   // deselect
        rm -rf "$(tempfile)" "$(ascfile)"                                               // cleanup temp files
        npp_save

* There might already exist a dedicated plugin for your specific conversion task.

----------

### Pork To Sausage

The `pork2Sausage.ini`, accessible through **Plugins > Pork to Sausage > Edit user commands**, has a number of parameters for use in the the INI definitions, plus two special variables.

**Parameters**:

- `progPath`: [Mandatory] The full path of the program to launch
   - This is the full path, including the name of the `.exe`
- `progCmd`: [Mandatory] The whole command to call the program
   - This is the whole command; because the program path is given in the first Parameter, this one can use just the name of the command rather than the full path
- `workDir`: [Mandatory] The path of working directory
   - This is needed for setting the "working directory" for the program -- for example, if it needs to be able to find specific libraries relative to some "current directory"
- `progInput`: [Optional] The full path name of the program input file. Pork to sausage plugin will write the selected text in a new created file with the given full path file name.
   - This is helpful if you don't want to try to input the "selected text" (see variables, below) on the command line (or example, if the selected text is too long, or the external program doesn't accept text input on the command line)
- `progOutput`: [Optional] The full path name of the program output file. Pork to sausage plugin will replace selected text by the content of indicated file, which is supposed to be the output file of the program. If this parameter is absent, then Pork to sausage plugin will use the stdout of program to replace the selected text.
   - This is useful if the external program writes its output to a file, instead of STDOUT.  
- `replaceSelection`: [Optional] If its value is false, then the selected text will be untouched.
   - Set this to `false` if you don't want the active selection in Notepad++ to be overwritten.

**Variables**

- `$(SELECTION)`: Your text selection.
   - The text will be encoded as UTF16-LE.  Your external command must be able to handle the text in that encoding.
- `$(TIMSTAMP)`: the Timestamp which will be generated by Pork to Sausage at the start of the call. This varible used for naming the file created by Pork to sausage plugin (progInput) to ensure the unicity (uniqueness) of the created file.

**Discussion**

There are two primary input methods to your application.
1. You can send the selected text as an argument on the command line:
   ```
   progCmd=external.exe -inText "$(SELECTION)" ...
   ```
2. You can have Pork to Sausage create a temporary file containing the selection:
   ```
   progInput=%TEMP%\Pork2Sausage.$(TIMESTAMP).input
   progCmd=external.exe -inputFile "%TEMP\Port2Sausage.$(TIMESTAMP).input"
   ```
   
