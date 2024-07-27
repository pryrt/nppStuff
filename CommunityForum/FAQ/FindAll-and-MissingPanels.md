# FAQ: I Cannot Find My Panel!

Hello, and welcome to the FAQ Desk.  

You have likely been directed here because you have run one of the **Find All** searches, but you don't see your **Search Results** window -- or because one of your other Panels (Project Panels, Folder as Workspace Panel, Document List Panel, Function List Panel, or even a Panel belonging to a Plugin...) _should_ be visible, but is not.

## Find All results specifics

When you run one of the following **Find All** searches, the results are put into a **Search Results** window, which may be docked (by default, at the lower edge of the Notepad++ window) or may be floating (as a separate window).
- **Search > Find > Find All In Current Document** - looks just in the active document
- **Search > Find > Find All in All Opened Documents** - looks in all the files you have open in Notepad++ right now
- **Search > Find in Files > Find All** (the **Find in Files** tab of the Search/Replace/... dialog) - looks in files matching the filter
- **Project Panel > Right Click > Find in Projects... > Find All** (the **Find in Projects** tab of the Search/Replace/... dialog) - looks in files that are in the selected **Project Panel**(s)

If it finds something, it will list the results in the **Search Results** window, with a heading per search, and pointers to the matches in the file or in each matching file.  If there are no matches, the **Search Results** window still displays a result, saying `0 hits in 0 files of N searched`.

But some users have accidentally "lost" that window, so it appears that nothing happens when the search is performed, and **Search > Search Results Window** (or the `F7` default shortcut) does not _appear_ to bring up the window as expected.

If you _have_ done one of the **Find All**, then it _is_ open... somewhere.  You just might not be able to see it.

## Finding a Missing Panel

* By default, a Panel is docked to one of the edges of your Notepad++ window (**Search Results** is docked at the bottom by default, but other Panels are usually docked to the right or left sides).  But any Panel may have been re-docked to another edge, or even "floated" as a separate window.
* On older versions of Notepad++ (v8.6.8 or older) it may be docked, but shrunk down until you cannot see it -- **this was fixed in v8.6.9, so it _cannot_ get too small to see when docked**.  If you see a small gap between the editor and the status bar or another edge of the editor, hover over it and see if you get the up-down arrow ↕ (for the top and bottom edges) or left-right arrow ↔ (for the left and right edges) that you can click+drag to resize the panel.
    - screenshot: 
![9cef56b8-8298-4b82-b929-140b2d71f951-image.png](/assets/uploads/files/1659629486898-9cef56b8-8298-4b82-b929-140b2d71f951-image.png)
    - zoomed 4x: 
![zoomed](/assets/uploads/files/1693436693775-ed6cf59a-978d-45af-a1fb-dbdb560caa08-image.png) 
* if it was undocked, it may have been dragged off screen (either to another monitor, or in rare occasions, off-monitor, or nearly so).  In this case
    1. Click in your editor panel
    2. Hit `F7`, which will activate the **Search Results Window** (even if it is off screen).  (For non-**Search Results Windows** panels, use the menu action that is supposed to activate that Panel.)
    3. Hit `Alt+Spacebar`, which will activate the Windows special menu (with Move/Size/Minimize/Maximize) for that window.
    4. Hit `M` (or whatever character in your language is underlined in the normal Move entry for that menu on any window)
    5. If you move your mouse around at this point, the outline of the window should snap near your cursor, and you can now click to place the window in a visible location
    6. If you shrunk that window way too far, you might only see ![6ce17525-0d5d-420e-8cad-6890f56dbfa9-image.png](/assets/uploads/files/1659629971648-6ce17525-0d5d-420e-8cad-6890f56dbfa9-image.png)  ... in that case, put the cursor in the lower-right edge of that tiny box, see the ⤡ diagonal-drag arrow, and click/drag to resize until it's visible

For those who are not able to position their mouse pointer along the appropriate border, or cannot move the floating window back into view, it is possible to reset the **Search Results** location by editing `config.xml` (paying attention to the [Configuration File Location](https://npp-user-manual.org/docs/config-files/#configuration-files-location) and [Editing Configuration Files](https://npp-user-manual.org/docs/config-files/#editing-configuration-files) links in the References below):

1. Save all open files.
2. Exit Notepad++ completely (**File > Exit**).
3. Run Microsoft's `notepad.exe` (as per [the online User Manual](https://npp-user-manual.org/docs/config-files/#editing-configuration-files), you cannot use Notepad++ to edit `config.xml`, or it will be overwritten as you exit Notepad++, thus losing the changes you thought you made).
4. Edit `%AppData%\Notepad++\config.xml` or the equivalent file if you have a non-standard installation (such as portable edition, or Cloud Settings enabled, or using `--settingsDir` command line argument).
5. Search for `GUIConfig name="DockingManager"` in `config.xml`.
6. Replace the section that look similar to this:
    ```
    <GUIConfig name="DockingManager" leftWidth="200" rightWidth="200" topHeight="200" bottomHeight="200">
            <PluginDlg pluginName="Notepad++::InternalFunction" id="42052" curr="0" prev="-1" isVisible="yes" />
            <PluginDlg pluginName="Notepad++::InternalFunction" id="44084" curr="1" prev="-1" isVisible="yes" />
            <PluginDlg pluginName="Notepad++::InternalFunction" id="44080" curr="3" prev="-1" isVisible="yes" />
            <ActiveTabs cont="0" activeTab="0" />
            <ActiveTabs cont="1" activeTab="0" />
            <ActiveTabs cont="2" activeTab="-1" />
            <ActiveTabs cont="3" activeTab="0" />
    </GUIConfig>
    ```
    (The exact contents may be different.  It is the whole section from `<GUIConfig name="DockingManager"` through `</GUIConfig>`
    Replace that section with the following
    ```
    <GUIConfig name="DockingManager" leftWidth="200" rightWidth="200" topHeight="200" bottomHeight="200">
    </GUIConfig>
    ```
7. Save `config.xml`.
8. Exit `notepad.exe`.
9. When you run Notepad++ again and do a new **Find All**, the **Search Results** window will be back to its default size and location, docked to the bottom of the Notepad++ window.

If this doesn't work for you, you can reply in your original discussion (or create a new [Help Wanted](/category/4/help-wanted) post) and explain that you read this FAQ, and followed all the advice (including checking for tiny docked windows, tried to use the keyboard to move it in case it was off-screen, and tried to manually edit `config.xml`, all to no avail); when you make this reply or new post, please include a copy of the `<GUIConfig name="DockingManager"` through `</GUIConfig>` from your `config.xml`, along with the **?**-menu's **Debug Info**, and a screenshot of your **Find** dialog.  Without this information, you will just be asked to read this FAQ.

Reference:
- Notepad++ Online User Manual: [Search Results Window](https://npp-user-manual.org/docs/searching/#search-results-window)
- User Manual: [Configuration File Location](https://npp-user-manual.org/docs/config-files/#configuration-files-location)
- User Manual: [Editing Configuration Files](https://npp-user-manual.org/docs/config-files/#editing-configuration-files)
- [historic discussion](/topic/23344/not-able-to-see-the-search-results-windows-in-notepad)
- **CLOSED AS FIXED** [feature request](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/13084) - v8.6.9 has fixed the zero-width docked-panels issue by not allowing panels to be that narrow, so they will always be visible.
