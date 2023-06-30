Hello, and welcome to the FAQ Desk.  You have been directed here to help you understand the usage and purpose of Notepad++'s built-in "Enable session snapshot and periodic backup" feature, and comparing that to the additional features of the AutoSave plugin, to help you get the most data safety that you can out of your Notepad++.

The "Enable Session Snapshot and Periodic Backup" feature is described in the online Notepad++ User Manual at https://npp-user-manual.org/docs/preferences/#backup .  The description below gives practical examples.

The AutoSave plugin can be installed using Notepad++'s **Plugins > Plugins Admin** tool.  After it is installed, it needs to be configured, as described below.

### Caveat

"_Save early, save often._"

You are responsible for your own data.  This FAQ entry will explain to you how the built-in feature and plugin both work, but it is up to you to configure these in such a way that it will work for your personal workflow.  Any data you care about should be part of your personal file hierarchy and backup plan; external backup software, and/or revision control software, will do more to protect your data than either the built-in feature or the plugin.

### Built-in "Enable Session Snapshot and Periodic Backup" Feature

With Notepad++'s built-in "save/open last session" + "enable session snapshot and periodic backup", Notepad++ automatically saves a backup of all edited-but-not-saved files into the defined backup directory, every _N_ seconds (as defined by preference setting -- defaults to 7sec).  Please note that if you only had the "save/open last session" checked on without the "enable session snapshot and periodic backup" also checked on, then Notepad++ would not be keeping periodic backups of unsaved files at all -- so it _must_ be turned on in order for you to have the `new NNN@yyyy-mm-dd_hhmmss` files in that backup folder.

#### Named files

The name of the periodic backup file is `filename.ext@yyyy-mm-dd_hhmmss`, and is placed in the `%AppData%\Notepad++\backup\` directory (or equivalent based on [config file location](https://npp-user-manual.org/docs/config-files/#configuration-files-location) and [backup preferences](https://npp-user-manual.org/docs/preferences/#backup)).  As soon as you manually save the file (so it's written to disk in the real location), this periodic backup goes away, because the purpose of the periodic backup is to save a copy of a file that you've edited but not saved.  The timestamp part of the periodic-backup-name is based on the first automatic save after the last manual save.  Example: if you saved a file at 8:10:00am, the backup would go away; then, at 8:12:30am, you type something but don't save, so sometime within _N_ seconds of that (8:12:30+N) it will periodic-backup-save and make a file with a timestamp about then -- something like `filename.ext@2021-06-23_081234`.  If you left for a while (or exited Notepad++ and reloaded) and came back at 12:34:56pm and typed another character, it would do it's periodic-backup-save on that file again so the last-modified time of the backup would be updated), but the name of the periodic-backup file will remain the same.

_SUMMARY: Named files that haven't recently been manually saved will exist in two locations -- a copy that is at most N seconds old in the backup folder, and a copy that matches the last manual save in the normal filesystem location where the named file was last saved.  As soon as you save the file, the filesystem location is the only copy._

#### Unnamed files

For _unnamed_ files: the name of the periodic backup file is `new NNN@yyyy-mm-dd_hhmmss`.  Since `new NNN` files are by definition not manually saved, the timestamp in the periodic-backup filename is based on when it did the first periodic-backup-save for that unnamed file.

#### Scenario: My (unsaved) files are missing!

The [configuration file](https://npp-user-manual.org/docs/config-files/) called [`session.xml`](https://npp-user-manual.org/docs/config-files/#other-configuration-files) stores, among other information, the list of unnamed/unsaved files that are currently open and points to the file in the backup directory that is storing the periodic backup for that unsaved file.

If something happens to your `session.xml` file -- for example, a Windows crash prevents the session file from being saved properly before Notepad++ exits; or, rarely, a Notepad++ upgrade erases your session file or otherwise prevents it from writing correctly; or if you have multiple instances of Notepad++ open, whichever one is closed last will save its session overtop the session for all the others -- then the next time you run Notepad++, your files may no longer be open in Notepad++.  At this point, don't panic.  If you look in `%AppData%\Notepad++\backup\`, you should see files for all of your previously-open-but-unsaved files.  You can just open those files in Notepad++ the same as you would any other file.  At this point, it is recommended that you save the files to a normal location (in your "My Documents" folder, or wherever else you keep your documents, notes, source code files, or whatever else) with meaningful names.  Or, you can create new unnamed files, and copy the contents of those old periodic-backup files into those new tabs, and continue without saving or naming the files.  Or you can keep them with the `new NNN@yyyy-mm-dd_hhmmss` naming scheme, and when Notepad++ does a periodic backup for an unsaved one of those, it will make an even longer name.  However you handle it, as long as Notepad++ is still set to keep periodic backups, the unedited versions of the files will be saved per Notepad++'s rules (as long as Windows problems or crashes don't get in the way).

Sometimes, users find that the files they find in the backup folder don't match their most recent edits.  This might be because the files were saved somewhere else (in which case, the most recent version is in their saved location, wherever that was).  Unfortunately, if the session file hasn't stored the information, or the session has been deleted or overwritten, then we cannot tell you where the files, so we cannot tell you where they are.  Windows has search functions in the Windows Explorer that can search by name or by date or possibly even by contents.

But rarely, it's because something got corrupted by Windows during the periodic-backup write sequence or during a crash, so the periodic backup file is actually wrong.  If that is the case, you may have to resort to file recovery software like Recuva (not affiliated with Notepad++ or this Forum; many users in the Community Forum have just recommended that software over the years) -- just point it at your `%AppData%\Notepad++\backup\` folder, and see if it can find older copies of the files.

Even worse, if you accidentally closed an unsaved file and said "No" when Notepad++ prompted to save it, Notepad++ _intentionally_ deletes that periodic backup, because that's what you told Notepad++ to do ("No" to that dialog meant "no, don't save this file that I'm closing with unsaved edits").  At this point, the file has been deleted from your `%AppData%\Notepad++\backup\` folder, and the only option is file recovery software like Recuva.

### Built-in Backup On Save

The **Settings > Preferences > Backup** also has a `Backup on Save` setting described in the "[Backup](https://npp-user-manual.org/docs/preferences/#backup)" section of the preferences documentation.  This sets where an extra copy of a file will be placed everytime you save a file (whether through a manual save, or through a plugin like the AutoSave plugin).

This setting section does not affect the behavior with regards to unsaved file changes; this is something that purely happens when the file is saved.

The details of `None` vs `Simple` vs `Verbose` are in the [documentation](https://npp-user-manual.org/docs/preferences/#backup).  Setting this option to anything but `None` is the way to keep a backup file even when you have saved the file (unlike periodic backups, which are deleted when the file is saved).

This backup will go either in the same folder or hierarchy as the original, or in a fixed location.  _Note_: that means it is usually on the same filesystem as the original, which, as many backup experts will tell you, is no better than having no backups at all.  Even if you use this option to make a local backup, industry best practice is to have external backup and/or version control software running, with one or more external off-site storage location(s) for critical data.

Notepad++ v8.1.9.1 - v8.3 installed standard with `Simple` backup-on-save enabled for new installations.  This annoyed some users, so v8.3.1 and newer went back to defaulting without any backup-on-save active.

### AutoSave Plugin

When you first installed the AutoSave Plugin, using Notepad++'s **Plugins > Plugins Admin** tool, the default configuration is to not have AutoSave providing any automatic saving, so it is doing nothing and you are still relying on Notepad++'s periodic backup (if enabled).

You will have to configure this plugin if it is going to do any automatic saving for you.  You do this by going to the **Plugins** menu, selecting **Auto Save**, and picking **Options**.  The following screenshot shows Auto Save v1.61's default Options dialog:

![e7286d9d-88ed-49d2-82b5-c275180b3440-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1624455467432-e7286d9d-88ed-49d2-82b5-c275180b3440-image.png)


#### AutoSave When

These options control when AutoSave is triggered.

_WARNING_: If both options remain unchecked, there is no AutoSave occurring and the plugin is doing nothing.

`☐ Notepad++ loses focus`: If this option is checkmarked on ☑, then every time you move from Notepad++ to another window (a Windows explorer, or your browser window, or any other application, or even change focus to the Desktop or clicking on the Windows Start Menu), AutoSave plugin will trigger a save event.

`☐ At timed intervals every _N_ minutes`: If this option is checkmarked on ☑, then every N minutes, AutoSave plugin will trigger save event, even if you have never clicked outside of Notepad++.

If both of the options are checkmarked on ☑, then AutoSave will trigger a save event every N minutes _and_ everytime Notepad++ loses focus.  This saves the most often.

#### AutoSave What

`○ Current file only`: If this option is active ⦿, only the "current" file in Notepad++ (the active tab) will have AutoSave events.  If you have multiple files open, the other tabs will _not_ be AutoSaved.

`○ All Open Files`: If this option is active ⦿, all files currently opened in Notepad++ will be protected by AutoSave.

Only one of those two options can be active ⦿.

`Ignore files larger than N KB`: If this is set to `0 KB`, all files will be AutoSaved.  If this is set to a non-zero numbewr, files that are larger than that threshold will _not_ be AutoSaved.

#### Named Files

`○ Ignore/do nothing`: If this option is active ⦿, _nothing_ will happen for _named_ files when AutoSave is triggered.  This means that _named_ files will not be protected by the AutoSave plugin in this configuration.

`○ Overwrite existing file`: If this option is active ⦿, when AutoSave is triggered, the plugin will send a "Save" command to the Notepad++ application, and the file will be written in the same location where you last manually saved the file (the same place it was when it was first named).  _Note_: This has the side effect of telling Notepad++ that the file is properly saved, so Notepad++ will remove its periodic-backup file for this named file.  This feature is basically equivalent to the Plugin hitting the SAVE button for you every time the AutoSave is triggered.

`○ Save autorecover in the same directory`: If this option is active ⦿, when AutoSave is triggered for the named file `namedfile.txt`, the plugin will create a file with `~` after the extension (`namedfile.txt~`) in the same directory as the original `namedfile.txt`.  _Note_: This time, since the state of the main file in Notepad++ is still "unsaved changes", the Notepad++ periodic-backup for `namedfile.txt` still exists; Notepad++ and AutoSave plugin will both treat this file as "unsaved".

#### Unnamed/new Files

`○ Ignore/do nothing`: If this option is active ⦿, _nothing_ will happen for _unnamed/new_ files when AutoSave is triggered.  This means that _unnamed/new_ files will not be protected by the AutoSave plugin in this configuration.

`○ Ask for filename`: If this option is active ⦿, when AutoSave is triggered, the Plugin will prompt you for a name for the file.  Once you enter the filename, AutoSave will tell Notepad++ to do a SaveAs to that location, and the file will now be a _named_ file, and treated according to the Notepad++ and AutoSave rules for _named_ files.

`○ Save (overwrite) silently here`: If this option is active ⦿, you need to choose a directory when you enable this option; the default `$CDIR$\autorecover` doesn't seem to carry any meaning; choose a real directory.  When AutoSave is triggered, the plugin will create a file called `new #` (matching Notepad++'s naming scheme) in that folder; from then on, Notepad++ and the AutoSave plugin will treat that file as a _named_ file. _Warning_: This has the side effect of resetting Notepad++ `new #` numbering... so be careful, because creating another new file at this point might be given a number that's already been used but saved by AutoSave, so AutoSave will try to put two files with the same name in the directory you specify.

`○ Save autorecover here`: If this option is active ⦿, you need to choose a directory when you enable this option; the default `$CDIR$\autorecover` doesn't seem to carry any meaning; choose a real directory.  When AutoSave is triggered, the plugin will create a file called `new #` (matching Notepad++'s naming scheme) in that folder; however, it still keeps the file that's shown in Notepad++ as a new/unsaved/unnamed file, so Notead++ and AutoSave Plugin both treat the file as "unsaved" and "unnamed".  This configuration doesn't reset Notepad++'s `new #` numbering, so new files created won't generally collide with the existing autorecover files.  When you close a `new #` tab without saving, the AutoSave plugin's autorecover file will still exist; however, the next time you create a new tab, if Notepad++ re-uses that number, then the new autorecover file will overwrite the old autorecover file of the same name.

#### AutoSave v2.00 (September 2022)

The v2.00 options were greatly simplified:

![dfd25063-1e19-4f2e-8bd0-28f7fef76f68-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1688130926697-dfd25063-1e19-4f2e-8bd0-28f7fef76f68-image.png)

It added options to the **Auto Save when** list:

- `☐ File tab changes`: If this option is checkmarked on ☑, it saves every time you activate a different tab in Notepad++.

- `☐ Notepad++ exits`: If this option is checkmarked on ☑, it saves when you exit Notepad++.

It removed options for the "autorecover" style of backup -- so now it will always overwrite the existing file, rather than creating a recovery file alongside the original.  And v2.00 removed the handling of the **Unnamed/new Files**, forcing you to rely on Notepad++'s native handling of unnamed files (and thus strengthening the argument behind the admonishment to always manually save your unnamed files to a known location as soon as you can, since AutoSave isn't helping you with that anymore).

Also, if you upgraded from v1.61 or earlier to v2.00, you will need to check your settings, to make sure it's still set up in a way that functions with your workflow.


### In Summary

Notepad++'s built-in periodic backup function will save a copy of files that you have edited but not saved, but things outside of Notepad++'s control will occasionally go wrong.   The AutoSave Plugin can provide additional safety in automatic file saving, but in order for it to do anything, you have to install it then set its options to something other than the default state.

It is highly recommend that you spend some time experimenting with how exactly Notepad++'s periodic backup works, and how the AutoSave plugin works, so that you can be sure that you know how they work, and that they're set up in a way that will actually _help_ you.  And please understand that no automatic-save-of-unnamed files is 100% effective, and that you are responsible for saving your files to a known location and making sure you have good working copies and good backups of any critical or mildly important data.

-----

### Links

* [Notepad++](https://notepad-plus-plus.org/) by Don Ho
* [Notepad++ Community Forum](https://community.notepad-plus-plus.org/) by the Notepad++ Community
* [Notepad++ Online User Manual](https://npp-user-manual.org/) => with a section on [backup preferences](https://npp-user-manual.org/docs/preferences/#backup)
* [AutoSave Plugin](https://github.com/francostellari/NppPlugins) by Franco Stellari => maintained separately from Notepad++
* [Recuva](https://www.google.com/search?q=recuva) => completely unaffiliated with Notepad++ or the Notepad++ Community Forum; listed as an example of [file recovery software for Windows](https://www.google.com/search?q=file+recovery+software+windows) with no guarantee or warranty, explicit or implied, by its listing in this FAQ
