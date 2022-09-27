# FAQ Desk: Request for Help without sufficient information to help you #

Hello, and welcome to the FAQ Desk.  

You have likely been directed here because you asked for help in another thread, but told us very little about the actual problem, so there’s not much we can do at this point except make wild guesses.

If you are willing to help us help you, and give us more details, and do some back and forth, the following may be helpful: this is my generic list of questions, which I've found over my time here that are helpful to start out with (and it's the steps I go through before even thinking of asking someone else for help, just to make sure that it's not PEBCAK)

Critical to any "I cannot get Notepad++ to work" problem is relevant information about your installation and usage of Notepad++.  The easiest way to get us much of that is to use the `?` menu, `Debug Info`, `copy debug info to clipboard`.  This can be pasted into your reply in one of three manners.

1. The  easiest way is to paste the text into the forum's post-editor, highlight the new text, then click the `</>` button on the top of the post-editing toolbar.

1. Indented: use the [Markdown syntax for a code block](https://daringfireball.net/projects/markdown/syntax#precode), by indenting by 4 spaces. (Since I have Notepad++ set up to replace TAB with 4 spaces, I just paste the Debug Info into an empty Notepad++ window, select all, TAB, and select all, copy, then paste in my post)
and that will render as:


    Notepad++ v7.5.6   (32-bit)
    Build time : Mar 19 2018 - 00:26:59
    Path : C:\Program Files (x86)\Notepad++\notepad++.exe
    Admin mode : OFF
    Local Conf mode : OFF
    OS : Windows 10 (64-bit)
    Plugins : ComparePlugin.dll dbgpPlugin.dll DSpellCheck.dll MarkdownViewerPlusPlus.dll mimeTools.dll NppConverter.dll NppExec.dll NppExport.dll NppFTP.dll PluginManager.dll PreviewHTML.dll PythonScript.dll XMLTools.dll

2. Using a trick that @Scott-Sumner recommends, wrap what you want to appear in \`\`\`z (opening delimiter) and \`\`\` (closing delimiter) on lines by themselves, example:

\`\`\`z
Notepad++ v7.5.6   (32-bit)
Build time : Mar 19 2018 - 00:26:59
Path : C:\Program Files (x86)\Notepad++\notepad++.exe
Admin mode : OFF
Local Conf mode : OFF
OS : Windows 10 (64-bit)
Plugins : ComparePlugin.dll dbgpPlugin.dll DSpellCheck.dll MarkdownViewerPlusPlus.dll mimeTools.dll NppConverter.dll NppExec.dll NppExport.dll NppFTP.dll PluginManager.dll PreviewHTML.dll PythonScript.dll XMLTools.dll
\`\`\`

which will render as:

```z
Notepad++ v7.5.6   (32-bit)
Build time : Mar 19 2018 - 00:26:59
Path : C:\Program Files (x86)\Notepad++\notepad++.exe
Admin mode : OFF
Local Conf mode : OFF
OS : Windows 10 (64-bit)
Plugins : ComparePlugin.dll dbgpPlugin.dll DSpellCheck.dll MarkdownViewerPlusPlus.dll mimeTools.dll NppConverter.dll NppExec.dll NppExport.dll NppFTP.dll PluginManager.dll PreviewHTML.dll PythonScript.dll XMLTools.dll
```
---

You may, also, use this alternate syntax :
\~~~z
Bloc
~ ~ ~

---

This will give us lots of relevant information about your installation of Notepad++, including
* version
* whether it’s 32b or 64b,
* whether you're in Administrator mode, or opened as normal user
* whether it’s a standard install or a “local configuration” / “portable install” (i.e., doesn’t use the %AppData% for storing settings)
* specifics of your OS
* It will also tell us which plugins are installed (there are some plugins with stability issues).

Other things that might be relevant:

* location of the problem file(s): local hard drive, network drive, ftp/remote server accessed through NppFTP, etc
* Do you have huge amounts of your memory already used by some memory-hog application, or lots of free memory?
* does it happen for any file(s), or just specific ones.  What's unique about that file / those files?
* If there are any error messages, please quote the full, exact message.
*  You can provide screenshots in two ways:
    1. Use `Alt-PrintScreen` on the Notepad++ to get the screenshot into your copy buffer, then `Ctrl+V` to paste it into your reply; the forum will embed the image automatically (which you can see in the preview window).

    2. If you like doing things manually, you can still save the screenshot file to [imgur.com](http://imgur.com/) or similar service, and then embed the image so it’s visible in your post using the syntax `![](https://i.imgur.com/_______.png)`, where you need to replace the `____` with imgur’s random name for your picture (or replace the whole URL, if it’s not imgur)
