# Themes in v8.8.9

With the release of v8.8.9, there is a [new feature](https://community.notepad-plus-plus.org/topic/27298/notepad-v8-8-9-vulnerability-fix) which automatically updates the active Theme if it is missing Style Configurator settings for any GUI elements, or missing any Languages or any Style entries in existing Languages.  This is a long-needed feature, so that as Notepad++ adds new styles for the Style Configurator, you'll be able to set them, even if your theme hasn't been updated since before those styles were added.  (Before now, if you switched to a theme years ago and set any custom color or user keyword or custom file extensions for a built-in language, it would never update the theme, no matter how many times you update Notepad++ in the meanwhile.  This v8.8.9 feature is able to correct that issue, and you will be able to use the Style Configurator to set the colors of any new styles going forward, as soon as you upgrade to a Notepad++ executable that supports the new style.)

Unfortunately, the v8.8.9 implementation included some annoying growing pains: the procedure always uses the same colors that those styles have in the `stylers.model.xml` file (ie, the default "light mode" colors), even if you are using a dark theme, which can make for glaring color issues: on Languages that get new styles added, the text that should be that new style can end up as black-on-white text, even if the rest of the text has a dark background; and if the theme was old enough, some GUI elements (like the Bookmark margin and Change History margin, between the line numbers and the text being edited) may clash with the surrounding GUI elements.

In the future v8.9 this issue will be fixed, so people who had an older theme and use v8.9 will see new styles show up using the default foreground and background colors of that theme, so they won't clash: it might not highlight the new keywords, for example, but at least it won't look worse than it used to.  

But unfortunately, once you run it in v8.8.9, your theme will no longer have those entries "missing", and the glaring white background will be saved.  The instructions below will help you with that:

## Instructions

**These instructions are _only_ needed if you ran Notepad++ v8.8.9. If you upgraded from something earlier to v8.9-or-later, you do _not_ need these instructions.**

1. Download the updated theme file(s) from the Source (see **Download Source** below)
2. Depending on circumstances, decide whether you need to update the installation-directory theme, the user-config-directory theme, or both
    - If you have a portable version of Notepad++, without using the Cloud directory or `-settingsDir`, then you need to just follow the instructions to **Update Theme(s) in User Config Directory**
    - If you are not using a portable version of Notepad++, then it is recommended to follow **Update Theme(s) in Installation Directory** first, and then decide based on the next item whether to continue or not
    - If you have any theme file(s) in the user-configuration directory (whether it's `%AppData%\Notepad++\themes\` or the Cloud directory's `.\themes` subdirectory or the `-settingsDir`'s `.\themes` subdirectory, then you should follow the **Update Theme(s) in User Config Directory** for those.

Please note: when correctly following step 2, you may need to follow multiple sets of instructions.  Please read and understand each point under step 2 to make the right changes.

### Download Source

The [installer themes in the source code](https://github.com/notepad-plus-plus/notepad-plus-plus/tree/master/PowerEditor/installer/themes) have been updated to have all the styles needed (to be able to fix the problems from v8.8.9).  You can go here to grab the theme file(s) you want: <https://github.com/notepad-plus-plus/notepad-plus-plus/tree/master/PowerEditor/installer/themes>.

### Update Theme(s) in Installation Directory

Except when you have a portable version of Notepad++, you will generally need to follow this set of instructions for the themes that come in the installation directory.  In a [normal installation](https://npp-user-manual.org/docs/config-files/#configuration-files-location) of Notepad++, the installation will be in `c:\program files\Notepad++` directory or equivalent, and the installation-directory themes will thus be in `c:\program files\Notepad++\themes`.  (See the **Instructions** section above for the decision process to know for sure whether to use this section.)

1. Exit Notepad++
2. Go to the URL mentioned in the **Download Source** section (above), and download the raw version of your Theme file(s)
3. Use Explorer to go to `c:\program files\Notepad++\themes\` directory
4. Copy the downloaded Theme(s) into that directory, overwriting what's there
5. When you run Notepad++ next time, it will use the updated theme, and the glaring color issues should be gone.

If you have customized your theme with user-keywords or user-extensions, then this won't be sufficient, because Notepad++ gives priority to the copy from the user-settings directory. (See the **Instructions** section above for the decision process to know for sure whether this section is sufficient for your needs.)

### Update Theme(s) in User Config Directory

If you have your Theme file in the user-settings directory (AppData hierarchy or Cloud directory or `-settingsDir` directory) for any reason -- whether you customized it by changing the font or color or added user-defined keywords or user-defined extensions using the Style Configurator, or whether you intentionally copied or downloaded a Theme into the user-settings directory, or whether it's there and you don't know how or why it got there: under any of those circumstances, then just replacing the theme in the installation directory won't be sufficient.   (See the **Instructions** section above for the decision process to know for sure whether to use this section.)

1. Exit Notepad++
2. If you haven't already, go to the URL mentioned in the **Download Source** section (above), and download the raw version of your Theme file(s)
3. Use Explorer to go to `%AppData%\Notepad++\` ([🛈](https://community.notepad-plus-plus.org/topic/15740/faq-desk-what-is-appdata "FAQ: What is %AppData%?")) or to wherever your Cloud Directory or `-settingsDir` option point to
4. There should be a `themes` subdiretory in that directory, if you have customized your Theme.
5. _Rename_ your old custom theme to `<themeName>_OLD.xml` (like `khaki.xml` becomes `khaki_OLD.xml`)
6. Copy the downloaded version of the Theme into that directory (for example, `khaki.xml`)
7. Start Notepad++.  It will use the updated version of the theme, but your customizations will be temporarily missing.
8. Open `%AppData%\Notepad++\themes\<themeName>.xml` _and_ `%AppData%\Notepad++\themes\<themeName>_OLD.xml`
9. In the _OLD copy, search for `ext="(?!")` in Regular Expression mode.  The value between the quotes will be the user-extensions for that language.  Copy any that you find in the OLD file to the language's equivalent entry in `<themeName>.xml`
10. In the _OLD copy, search for `(?<!>)</WordsStyle>` in Regular Expression mode.  Any values between the `>` and the `</WordsStyle>` should be copied to the equivalent location in the `<themeName>.xml` file. If `<themeName>.xml` just has `<WordsStyle name="..." ... />` without having a `</WordsStyle>` closer, you can replace the `/>` with a `>` and the list of keywords, then the closing `</WordsStyle>`
11. Save `<themeName>.xml`
12. Exit Notepad++
13. When you run Notepad++ again, it should now include your customizations again.

## Native Feature compared to ConfigUpdater plugin

The [ConfigUpdater plugin](https://github.com/pryrt/NppPlugin-ConfigUpdater) was introduced as a testbed for some of the ideas that made it into the v8.8.9 native implementation.  As such, if you are in v8.8.9 or newer, you no longer need the ConfigUpdater plugin.  But if you are before v8.8.9, and waiting for the v8.9 fix to the Notepad++ feature before upgrading, then using ConfigUpdater while in v8.8.8-or-older will help you get to a point where if you did change your mind and upgrade to v8.8.9, it wouldn't make the glaring UI clash and black-on-white text in dark themes.

# JavaScript in v8.9 Themes

In v8.8.8 and earlier, Notepad++ would magically use the embedded javascript (JS-in-HTML) styler settings if the javascript.js (*.js) language didn't have defined styles in a given theme, making it _appear_ to JavaScript users that their theme had the standalone JavaScript colors defined.  The v8.9 fix, which filled in default FG/BG colors for all javascript.js styles for themes that were missing javascript.js made it _appear_ to the JavaScript users that v8.9 broke their theme, when it really meant that their already-broken theme was just being "fixed" in a different way.  Updated themes are being submitted to the Notepad++ codebase, so that javascript.js will use similar colors to embedded javascript, so they won't get the surprise color change if they upgrade from v8.8.8-or-plder to v8.9.1-or-newer.  

If you already updaded to v8.9, and JavaScript *.js files look like they have stopped syntax highlighting then you will need to follow instructions similar to the **Update Theme(s) in Installation Directory** and/or **Update Theme(s) in User Config Directory**
- Until the PR has been merged, you can use https://github.com/pryrt/notepad-plus-plus/tree/javascriptTheme/PowerEditor/installer/themes as the source for the updated themes (once the PR is accepted, this link will be deleted from the FAQ, and you can use the files from the **Download Source** link, above).
- You can just copy the entire `<LexerType name="javascript.js" desc="JavaScript" ext="">...</LexerType>` section from the downloaded theme(s) and paste it overtop that same section in your **Config Directory** and/or **Installation Directory** theme file(s), then save and restart to get it to take effect.
