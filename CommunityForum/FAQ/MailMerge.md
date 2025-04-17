# FAQ: Bulk Substitution

Oftentimes, users want to have a template in one file, and a "database" or "list" in another document, and use the data from the "database" to fill in one or more "fields" from the template into one or more files.  This is traditionally called "mailmerge", because in word processing, it's used for generating form letters and/or envelopes (ie, "mail").

At other times, there is a list of many mappings that need to be done for one or more files.  An example of this would be translating specific strings in a document, or expanding abbreviations, or the like.

There have been multiple types of solutions for these problems offered over the years, and this FAQ was created to bring them into one easy-to-find place.

## MailMerge

Having source data with a name and title, want to insert those into a template

**database file**:
```
Peter Jones,Forum Regular
Pac-Man,Video-Game Character
Victor von Frankenstein,Monster-Creating Villain
```
**template file**:
```
Dear <NAME>,
As a <DESCRIPTION>, I thought you would be interested in this special offer: if you respond right now, you can get the awesome software known as Notepad++, absolutely free!
```
And have it result in
**output(s)**:
```
Dear Peter Jones,
As a Forum Regular, I thought you would be interested in this special offer: if you respond right now, you can get the awesome software known as Notepad++, absolutely free!

Dear Pac-Man,
As a Video-Game Character, I thought you would be interested in this special offer: if you respond right now, you can get the awesome software known as Notepad++, absolutely free!

Dear Victor von Frankenstein,
As a Monster-Creating Villain, I thought you would be interested in this special offer: if you respond right now, you can get the awesome software known as Notepad++, absolutely free!
```
(Sometimes, it is desired to put it all in one file, sometimes each output should go in a separate file)

### Natively, Not Always Possible -- but sometimes

With Notepad++ alone, it's not always possible to do that.  But if the "template" is small enough to fit in the **Replace with** box of Notepad++'s **Search > Replace**, and if the output can all be in the same file, then @PeterJones's suggestion [here](https://community.notepad-plus-plus.org/topic/22666/how-to-replace-multiple-variables-vs-a-template/2) might work.  Essentially, it boils down to running a Replacement on the database file (or better, on a copy of the file).

Using native Notepad++ **Search > Replace**, and using `\r\n` for a standard Windows CRLF newline:
- **Find What**: `(?-s)^(.*?),(.*)$`
- **Replace with**: `Dear $1,\r\nAs a $2, I thought you would be interested in this special offer: if you respond right now, you can get the awesome software known as Notepad++, absolutely free!`
- **Search mode**: `Regular Expression`

If you use a plugin that has a multi-line **Replace** field, like the ToolBucket plugin mentioned in that post, it can be even easier, because the replacement could be spread across multiple lines, without having to manually insert the newlines with `\r\n` in the **Replace with** string.

### PythonScript Plugin with `MailMerge.py`

!! TODO: build up my example into Alan's script !!
https://community.notepad-plus-plus.org/post/83683

## MultiReplace Plugin's "Lookup File"

For some variants of the "mailmerge" need, the MultiReplace plugin has a "Lookup File" feature that could help.  But rather 
If there only needs to be _one_ field in the output (for example, just the name)
!! TODO: I need to research how to turn my example into something that works there !!
https://community.notepad-plus-plus.org/topic/26682/multireplace-now-supports-lookup-files

