# Change History

Hello, and welcome to the FAQ Desk.

You have likely been directed here because you have asked about the Change History feature, which is new to [v8.4.6](https://github.com/notepad-plus-plus/notepad-plus-plus/wiki/Changes#846): you probably asked something like "how do I get rid of the new orange/red line?" or "when I print, I get a strange orange background", or something similar.

## What is Change History

The new Change History feature tracks the changes made since you last loaded the file: it tracks it with a colorful bar on the edge of the editor window.  Changes will be indicated by the orange bar.  A green bar indicates that the change has been saved since it was last changed.  A pale green (some call it "olive") indicates that you have done enough **undo** to get back to a previous save state (as the [author calls it](https://notepad-plus-plus.org/news/v846-released/), "revert to modified").  A light blue indicates that you have done enough **undo** actions to get back to the _original_ state of the file from when you loaded that file from disk.

It's quite useful feature.  Similar techniques have been found in other text editors for years, and it's great that Notepad++ has finally implemented it.

## How do I turn it off?

Please give it a chance before you try to turn it off.  It really is useful.

But if you insist on abandoning one of the most useful new features of Notepad++, there is a **Display Change History** checkbox in the **Settings > Preferences > Margins/Border/Edge**.  

![](https://community.notepad-plus-plus.org/assets/uploads/files/1664445587834-93039d56-a88b-4351-9bb6-7a03ca5dbd67-capture-d-%C3%A9cran-2022-09-29-115124.png)

You can uncheck the checkbox in the settings and have the change take effect immediately.  But if you checkmark the setting again to turn it back on, you will have to restart Notepad++ to take effect... So it's not a good idea to turn it off and back on frequently.  If what you're really trying to do is just clear the margin for the short term (get it back to a nice clean margin, with no orange or green, equivalent to how it was when you first loaded your file), all you have to do is clear the history, as described in the next section.

## How do I clear the history? I want to make it have no orange or green bars!

Since saving the file just turns the bar green, that is insufficient to get it back to a "blank slate".  And **File > Reload From Disk** will actually turn it _all_ green, not just lines that had been recently changed then saved.  

Instead, you can save the file, close it , and then use the **File > Recent Files > Restore Recently Closed File** or equivlant, which will cause Notepad++ to close reload it from scratch, with no change markings.  With default keyboard shortcuts, that sequence would be `Ctrl+S` then `Ctrl+W` then `Ctrl+Shift+T`, so only three keystrokes.  If that three-shortcut pattern is too difficult, you can insert the following macro in `shortcuts.xml`:

```
        <Macro name="ResetHistory" Ctrl="yes" Alt="no" Shift="yes" Key="72">
            <Action type="2" message="0" wParam="41006" lParam="0" sParam="" />
            <Action type="2" message="0" wParam="41003" lParam="0" sParam="" />
            <Action type="2" message="0" wParam="41021" lParam="0" sParam="" />
        </Macro>
```

To insert the macro: **File > Open** `%AppData%\Notepad++\shortcuts.xml`, go to the `<Macros>` section, and add that macro before the `</Macros>`.  Save. Exit Notepad++.  Re-run Notepad++.  Now **Macro > ResetHistory**, or the `Ctrl+Shift+H` shortcut (mnemonic: "**control** the **H**istory") will clear the active file's history.

## How do I change the size?

If you find the Change History markers in the margin visually “distracting”, perhaps try leaving them on but minimizing their visual impact. You can do this by using the PythonScript or NppExec plugins; here’s how:

PythonScript: Execute the console window command `editor.setMarginWidthN(2, 1)`

NppExec: Execute a temporary script consisting of one line `sci_sendmsg 2242 2 1`

If you want to go the OPPOSITE way, and have maximal visual impact, try changing the `1` in either of the above to `0`!

## How do I change the color?

The background color is set with **Settings > Style Configurator > Language: `Global Styles` > Style: `Change History margin`**.  

Unfortunately, you cannot (yet) change the four foreground colors (though that feature [has been requested](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/12321)).

## Consequences for Plugins

In order to support the Change History feature, Notepad++ had to reassign some resources it was using for other purposes, because Scintilla used these same resources for Change History. Summary: The marker id number for bookmarks changed from 24 to 20, and three marker id numbers used for the hidden-lines feature changed from 21-23 to 17-19.

Further, Change History uses Margin number 2, so that is no longer available to plugins.

Plugins that made use of affected marker-numbers or margin 2 will have to be updated in order to not conflict with Notepad++'s use.  If they are not updated, there will be unexpected interactions, and users will be confused.

## Known Issues

This is a new feature, so it will likely take a few versions of Notepad++ before it is stable.  Known issues will be described below, with links to the official bugtracker issue number, and with any known workarounds.  You can check the issue links to see if the status for an issue has changed since this FAQ was last updated.

### Printing

[Issue #12281](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/12281): Due to a bug in an underlying library, if the Change Margin history is visible, then any lines that were changed (or even saved-since-last-change) will get an unexpected background color when printed.  

**Workaround**: Until this bug is fixed in the underlying library and the fix is propagated to Notepad++ and released, you can workaround this problem by clearing the history (see the **Clear the History** section, above).

The new version [v8.4.7](https://community.notepad-plus-plus.org/topic/23696/notepad-v8-4-7-release-candidate/10) fixes this problem, so install that newer version to avoid the printing issue.