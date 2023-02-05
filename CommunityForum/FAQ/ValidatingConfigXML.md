# FAQ Desk: Validating Config-File XML

If you are developing Notepad++ config-file XML for distribution (Function List definitions, autoCompletion files, and User Defined Languages), you may want to validate that the XML is reasonable before trying to use it (and distribute it).

If you have a DTD or XSD Schema File for each of the config XML types, you can use an interal tool (like the XMLTools plugin) or an external tool (like `xmllint.exe`, available in the [Git for Windows](https://gitforwindows.org/) or [Strawberry Perl](https://strawberryperl.com) distributions) for validation; those are by no means the only such tools, but are just the ones the author of this FAQ is familiar with, and you should be able to use any XML validation tool in a manner similar to the methods described for these two tools.

If you would like a pre-made XSD for any of those three config-file types, they can be found in the [UDL Collection's validation folder](https://github.com/notepad-plus-plus/userDefinedLanguages/tree/master/.validators), or possibly attached to this FAQ.

## Instructions For Validation

Most XML validators will accept the XSD schema files in two ways: either being referenced internally in the XML file itself, or tools usually have a way of specifying how to use a specific XSD file.

Using an externally-specified XSD file is good because you can then validate an XML file directly generated or installed by Notepad++ without editing the XML; not editing the XML files also keeps them clean, so that users who don't have your exact filesystem structure will not have problems on their end.  On the other hand, for a tool like the XMLTools plugin which can automatically validate while you are editing, it may save time and effort to have the XSD linked from inside the XML, so that it doesn't have to ask you for the XSD every time it validates.  How you do the validation on your end is completely up to you; however, it is recommended that you do not link to a local XSD file in the XML that you are going to distribute to the public (especially if you are submitting it to the UDL Repository or trying to get your Functino List definition for a builtin lexer added to the Notepad++ codebase for distribution), in case that causes problems for the repository or end user.

### XML Tools

The XML Tools plugin will read the XSD filename from the XML file if it's there, and if it's not, it will ask in a dialog box to "Please select an XML Schema (XSD)" where you can click on the **...** button and pick the `.xsd` file to use for validating the active XML.

### `xmllint.exe`

To run using the internally-linked XSD file:
```
xmllint --noout --schema path\to\external.xsd filename.xml
```
... where `filename.xml` is the name of the XML file you'd like to check.

To run using an externally-specified XSD file:
```
xmllint --noout --schema path\to\external.xsd filename.xml
```
... where `filename.xml` is the name of the XML file you'd like to check, and `path\to\external.xsd` is the file path (relative or absolute) for the XSD file.

If you would like to run a whole directory of XML files using the same XSD schema (for example, testing your whole UDL directory for validity):
```
REM cmd.exe Command Line Syntax:
FOR /F %F ('DIR /D UDLs/*.xml') DO @xmllint --noout --schema path\to\userDefineLangs.xsd UDLs\%F

REM *.bat Syntax:
FOR /F %%F ('DIR /D UDLs/*.xml') DO @xmllint --noout --schema path\to\userDefineLangs.xsd UDLs\%%F
```

## Instructions for Internally Linking the XSD

The `<NotepadPlus>` element normally has no attributes.  But if you add a couple of attributes (as shown below), you can link to the XSD from inside the XML:
```
<NotepadPlus
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="_______.xsd"
>
```

There are options for the `_______.xsd`:
- If the XSD file is in the same directory as the XML, you can just use a simple `filename.xsd` as the attribute value.
- If the XSD file is in a nearby directory compared to the XML, you can specify a relative file, like `subdirectory\filename.xsd` if the XSD is in a subdirectory compared to the XML, or `..\siblingDirectory\filename.xsd` if the XSD is in a sibling directory alongside the XML directory.
- If the XSD file is somewhere else in your filesystem, you might want to use an absolute path, like `c:\path\to\filename.xsd`.
- If the XSD is in a URL online, you can actually supply that URL (for example, `https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/.validators/userDefineLangs.xsd` will link to the UDL Repository's schema for UDL files), but that will mean that the tool may have to re-download the URL every time it validates (depending on how the tool is designed).
