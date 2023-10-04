# Perl Syntax

Here are some of my notes regarding keeping Notepad++'s Perl hooks up to date, including

- autoCompletion\perl.xml
- langs.model.xml
- stylers.model.xml

Actually, I started some of this in the [perlapi section of howto/npp.html](https://pryrt.com/howto/npp.html)

A little about some of the contents:

- testNewScintillaProperties.pl ⇒ example for syntax highlighting verification
- stylers.snippet.xml ⇒ the "perl" section of stylers.model.xml
- langs.snippet.xml ⇒ the "perl" section of langs.model.xml

TBD:

- convertTheme.pl ⇒ TBD ⇒ converts theme(s) to include the new LexPerl attributes

## Issues

### Perl keywords need updating

The last major update of Perl keywords (`autoCompletion\perl.xml` and `langs.model.xml` keyword list) was for Perl v5.30.
Perl is now at v5.38, and there are a number of new keywords (both built-in functions and pragmas) that need to be added.

Also, the default list of extensions should include `t`, as the Perl-standard naming convention for a Perl-unit-test file (I confirmed that `langs.model.xml` doesn't have any other language whose extensions include `t`, so it won't conflict with anything.)

I will be submitting a PR momentarily to address this.

=> https://github.com/notepad-plus-plus/notepad-plus-plus/issues/14190
=> https://github.com/notepad-plus-plus/notepad-plus-plus/pull/14191

### Perl styles need updating

LexPerl has changed significantly since the `stylers.model.xml` list of styles for Perl was created/last-updated.

- `stylers.model.xml` defines three styles (PREPROCESSOR, PUNCTUATION, LONGQUOTE) that aren't used by LexPerl.
- `stylers.model.xml` is missing 24 styles that are used by LexPerl.
- Some of the names for the styles should be updated for clarity.

I will be submitting a PR that includes the updates to the style list for both `stylers.model.xml` and `themes\DarkModeDefault.xml`, with colors that are reasonable for those default themes.
For the other themes that ship with Notepad++, I was thinking of setting `colorStyle="0"` for the new styles, so that they will inherit the foreground and background from their theme, to avoid defining colors that clash with the theme (it will mean that users who use those themes will not notice any changes in syntax highlighting, but if they go to Style Configurator, they will see more Styles available to Perl).  But if someone disagrees and thinks I should leave the other themes alone, I won't bother.

=> https://github.com/notepad-plus-plus/notepad-plus-plus/issues/14192
=> https://github.com/notepad-plus-plus/notepad-plus-plus/pull/14193